#!/usr/bin/env bash
# Build demo.hax.cloud into demo/_site/: the HAXcms demo compiled from webcomponents main on every deploy,
# served from the top of its own domain and running this folder's own site (demo/site: site.json and
# pages/). Nothing is fetched from cdn.hax.cloud or webcomponents.hax.cloud at run time: every module,
# style and registry file is built here and served from this domain. Run by Vercel (demo/vercel.json);
# needs bash, git, node, yarn (v1) and python3.
#
#   demo/build/build.sh
#
# Steps: fetch webcomponents at WC_REF, install it, compile the same build/es6 tree the CDN serves
# (polymer build, vendor copies, CSS template minify, terser), regenerate wc-registry.json from that tree
# so new elements on main load, then lay the demo folder, the compiled node_modules/ and site/ into _site.
# This runs the build half of `ubiquity` in a throwaway checkout; it never publishes anything.
#
# WC_REPO (default haxtheweb/webcomponents) and WC_REF (default master: a branch, tag or commit) set
# beforehand point the build at another source, e.g. a pull request branch.
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$HERE/_site"
WORK="$HERE/.webcomponents"
REPO="${WC_REPO:-haxtheweb/webcomponents}"
REF="${WC_REF:-master}"
START=$SECONDS
step() { echo "demo [$((SECONDS - START))s]: $*"; }

rm -rf "$OUT" && mkdir -p "$OUT"
# the compiled tree, the same one hax.cloud ships (build/compile-webcomponents.sh reads WC_REPO / WC_REF)
bash "$HERE/build/compile-webcomponents.sh" "$WORK"

DEMO="$WORK/elements/haxcms-elements/demo"
python3 -I - "$DEMO/wc-registry.json" <<'EOF'
import json, sys
reg = json.load(open(sys.argv[1]))
if len(reg) < 400 or "haxcms-site-builder" not in reg:
    sys.exit("wc-registry.json looks incomplete (%d tags); not publishing" % len(reg))
print("demo: wc-registry.json has %d tags" % len(reg))
EOF

step "assembling _site"
cp -R "$DEMO/." "$OUT/"
# the demo's node_modules is a link into the checkout, its pages/ and site.json are replaced by site/
rm -rf "$OUT/node_modules" "$OUT/pages" "$OUT/index.php" "$OUT/CNAME"
mv "$WORK/build/es6/node_modules" "$OUT/node_modules"
cp "$WORK/build/THIRD_PARTY_LICENSES" "$OUT/THIRD_PARTY_LICENSES"
python3 -I "$HERE/build/top-level.py" "$DEMO/index.html" "$OUT/index.html" "$OUT/node_modules" "$WORK/node_modules"
# this domain's own site (site.json, pages/)
cp -R "$HERE/site/." "$OUT/"
echo "$REPO@$REF" > "$OUT/build-source.txt"

cd "$HERE" && rm -rf "$WORK"
step "done: $(find "$OUT" -type f | wc -l) files, $(du -sh "$OUT" | cut -f1) from $REPO@$REF"
