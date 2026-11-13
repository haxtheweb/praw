#!/usr/bin/env bash
# Build demo.hax.cloud into demo/_site/: the live HAXcms demo page from webcomponents.hax.cloud
# (elements/haxcms-elements/demo/index.html) served from the top of its own domain, running this
# folder's own site (demo/site: site.json and pages/) instead of the demo's. Run by Vercel
# (demo/vercel.json); needs bash, curl and python3.
#
#   demo/build/build.sh
#
# Everything else the page asks for is proxied back to webcomponents.hax.cloud by demo/vercel.json, so the
# demo at its direct path keeps working as it is and this domain always runs the latest webcomponents build.
# DEMO_SOURCE set beforehand wins (e.g. a Vercel preview of webcomponents).
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$HERE/_site"
SOURCE="${DEMO_SOURCE:-https://webcomponents.hax.cloud/elements/haxcms-elements/demo/index.html}"

rm -rf "$OUT" && mkdir -p "$OUT"
curl -fsSL "$SOURCE" -o "$OUT/source.html"
python3 -I "$HERE/build/top-level.py" "$OUT/source.html" "$OUT/index.html"
rm "$OUT/source.html"
# this domain's own site (site.json, pages/): served as files, so they win over the proxy to the demo folder
cp -R "$HERE/site/." "$OUT/"
echo "demo: $OUT/index.html from $SOURCE"
