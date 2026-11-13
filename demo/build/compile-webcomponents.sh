#!/usr/bin/env bash
# Compile HAX's front-end build from webcomponents into WORK/, the same build/es6 tree the CDN serves:
# fetch WC_REPO@WC_REF, install, polymer build, the xterm and latex2html5 vendor copies, CSS template
# minify, terser, then wc-autoloader (wc-registry.json from the compiled tree, so elements added on master
# load before the next ubiquity release) and the third-party license file. This is the build half of
# `ubiquity` in a throwaway checkout; it never publishes anything. Used by demo.hax.cloud
# (demo/build/build.sh) and hax.cloud (ecosystem/build/site.sh); it lives in demo/ because the demo is its
# own Vercel project rooted there. Needs git, node, yarn (v1), python3.
#
#   demo/build/compile-webcomponents.sh WORK
#
# Leaves: WORK/build/es6/node_modules (the compiled tree), WORK/build/THIRD_PARTY_LICENSES,
# WORK/wc-registry.json and WORK/wc-registry-graph.json (also written into the haxcms-elements demo folder),
# and WORK/node_modules (the source packages, whose package.json files name each package's entry point).
#
# WC_REPO (default haxtheweb/webcomponents) and WC_REF (default master: a branch, tag or commit) set
# beforehand point the build at another source, e.g. a pull request branch.
set -euo pipefail
WORK="${1:?usage: compile-webcomponents.sh WORK}"
REPO="${WC_REPO:-haxtheweb/webcomponents}"
REF="${WC_REF:-master}"
START=$SECONDS
step() { echo "webcomponents [$((SECONDS - START))s]: $*"; }

rm -rf "$WORK" && mkdir -p "$WORK"
step "fetching $REPO@$REF"
cd "$WORK"
git init -q && git remote add origin "https://github.com/$REPO.git"
git fetch -q --depth 1 origin "$REF" && git checkout -q FETCH_HEAD
step "installing $(git rev-parse --short HEAD)"
# engines pins node 24; the build runs on what the project has. HUSKY=0: no git hooks for a throwaway checkout.
HUSKY=0 yarn install --frozen-lockfile --ignore-engines --non-interactive --network-timeout 600000 --silent
BIN="$WORK/node_modules/.bin"
gulp_task() { "$BIN/gulp" "$1" --gulpfile=gulpfile.mjs; }

step "compiling (polymer build)"
"$BIN/polymer" build
gulp_task vendor-copy-xterm
gulp_task vendor-copy-latex2html5
node scripts/minify-css-templates.mjs build/es6/node_modules/@haxtheweb
step "minifying (terser)"
gulp_task terser
step "registry"
# reads the terser output (static get tag(){return"..."}), so it runs after terser, as in ubiquity
gulp_task wc-autoloader
node scripts/copy-dep-licenses.js

python3 -I - "$WORK/wc-registry.json" <<'EOF'
import json, sys
reg = json.load(open(sys.argv[1]))
if len(reg) < 400 or "haxcms-site-builder" not in reg:
    sys.exit("wc-registry.json looks incomplete (%d tags); not publishing" % len(reg))
print("webcomponents: wc-registry.json has %d tags" % len(reg))
EOF
step "compiled $(git rev-parse --short HEAD)"
