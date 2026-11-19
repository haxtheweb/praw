#!/usr/bin/env bash
# Compile HAX's front-end build from webcomponents into WORK/, the same build/es6 tree the CDN serves:
# fetch WC_REPO@WC_REF, install, polymer build, then webcomponents' own package scripts in the order its
# `ubiquity` script runs them (locales, vendor copies, CSS template minify, terser, wc-autoloader, so
# wc-registry.json comes from the compiled tree and elements added on master load before the next ubiquity
# release) and the third-party license file. Running webcomponents' scripts by name, not its gulp tasks,
# keeps this in step when a step moves between gulp and a script there. This is the build half of
# `ubiquity` in a throwaway checkout; it never publishes anything. Used by hax.cloud
# (ecosystem/build/site.sh). Needs git, node, yarn (v1), python3.
#
#   ecosystem/build/compile-webcomponents.sh WORK
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
# engines pins node 24; the build runs on what the project has (Vercel's Node can be newer). yarn v1 checks
# engines again on every `yarn run`, which --ignore-engines on install doesn't cover, so it is off for every
# yarn command here. HUSKY=0: no git hooks for a throwaway checkout.
export YARN_IGNORE_ENGINES=true
HUSKY=0 yarn install --frozen-lockfile --ignore-engines --non-interactive --network-timeout 600000 --silent
BIN="$WORK/node_modules/.bin"
# a webcomponents package script by name; one this ref does not define is skipped (an older WC_REF may
# not have every step yet). --ignore-engines as at install: yarn v1 checks engines on `run` too, so on any
# node but 24 (Vercel's project node, say) every script refuses to start.
run_script() {
  if node -e 'process.exit(require("./package.json").scripts[process.argv[1]] ? 0 : 1)' "$1"; then
    yarn --ignore-engines run --silent "$1"
  else
    echo "webcomponents: no '$1' script at this ref, skipped"
  fi
}

step "compiling (polymer build)"
"$BIN/polymer" build
run_script copy-locales
run_script vendor-copy-xterm
run_script vendor-copy-latex2html5
run_script vendor-copy-mermaid
run_script vendor-copy-monaco
run_script vendor-copy-h5p
run_script minify-css-templates
step "minifying (terser)"
run_script terser
step "registry"
# reads the terser output (static get tag(){return"..."}), so it runs after terser, as in ubiquity
run_script wc-autoloader
node scripts/copy-dep-licenses.js
# webcomponents writes build/THIRD_PARTY_LICENSES.md now (THIRD_PARTY_LICENSES before); the sites keep
# serving it at build/THIRD_PARTY_LICENSES, so either name leaves that file
if [ ! -f build/THIRD_PARTY_LICENSES ] && [ -f build/THIRD_PARTY_LICENSES.md ]; then
  cp build/THIRD_PARTY_LICENSES.md build/THIRD_PARTY_LICENSES
fi
test -f build/THIRD_PARTY_LICENSES || { echo "webcomponents: no third-party license file in build/; not publishing" >&2; exit 1; }

python3 -I - "$WORK/wc-registry.json" <<'EOF'
import json, sys
reg = json.load(open(sys.argv[1]))
if len(reg) < 400 or "haxcms-site-builder" not in reg:
    sys.exit("wc-registry.json looks incomplete (%d tags); not publishing" % len(reg))
print("webcomponents: wc-registry.json has %d tags" % len(reg))
EOF
step "compiled $(git rev-parse --short HEAD)"
