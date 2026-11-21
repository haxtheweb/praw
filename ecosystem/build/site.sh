#!/usr/bin/env bash
# Build hax.cloud into _site/ at the repo root: the HAXcms site boilerplate from haxcms-nodejs main, with
# site.json, pages/ and the interactive web written by build_site.py, and build/: HAX's front-end build
# compiled from webcomponents master (ecosystem/build/compile-webcomponents.sh), so every element, the theme included, loads from hax.cloud itself and runs the latest code.
# Run by the hax.cloud workflow and by Vercel (vercel.json); needs bash, python3 (3.9+), git, node and
# yarn (v1). WC_REPO / WC_REF build against another webcomponents source (see the compile script).
#
#   ecosystem/build/site.sh
#
# The theme is ecosystem-theme once it is on npm, clean-one until then. HAX_CLOUD_THEME set beforehand wins.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OUT="$ROOT/_site"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

"$ROOT/ecosystem/build/run.sh" --assemble

# haxcms-nodejs main: the HAXcms site boilerplate, and the backend code that renders its templates
# (static_site.cjs below), so the two always come from the same commit
if command -v git >/dev/null 2>&1; then
  git clone -q --depth 1 https://github.com/haxtheweb/haxcms-nodejs "$TMP/hn"
else
  mkdir -p "$TMP/hn"
  curl -fsSL https://codeload.github.com/haxtheweb/haxcms-nodejs/tar.gz/refs/heads/main |
    tar -xz -C "$TMP/hn" --strip-components=1
fi
(cd "$TMP/hn" && npm install --omit=dev --ignore-scripts --no-audit --no-fund --loglevel=error)

if [ -z "${HAX_CLOUD_THEME:-}" ] && npm view @haxtheweb/ecosystem-theme version >/dev/null 2>&1; then
  export HAX_CLOUD_THEME=ecosystem-theme
fi
echo "theme: ${HAX_CLOUD_THEME:-clean-one}"

rm -rf "$OUT" && mkdir "$OUT"
cp -r "$TMP/hn/src/boilerplate/site/." "$OUT/"
# server-only files and the boilerplate's own content go; the static entry point comes in
rm -rf "$OUT/pages" "$OUT/site.json" "$OUT/.github" "$OUT/docker" "$OUT/Dockerfile" "$OUT/index.php" \
  "$OUT/config.php" "$OUT/.htaccess" "$OUT/llms.txt" "$OUT/netlify.toml"
cp "$OUT/ghpages.html" "$OUT/index.html"
cd "$ROOT/ecosystem/.work" && python3 -I ../build/build_site.py "$OUT" hax-area-icons.html
# recent activity from the public GitHub API (https://github.com/haxtheweb/issues/issues/3387): recent.json, the
# Recent page and each repository's tile page. It keeps the last published snapshot when GitHub can't be read,
# and never stops the build.
python3 -I "$ROOT/ecosystem/build/build_recent.py" "$OUT" || echo "recent: skipped"

# the boilerplate's files are templates ({{ title }}, {% if socialImage %} ...): haxcms-nodejs main renders
# them from site.json, refreshes the generated files (robots.txt, llms.txt, sitemap, feeds, search index,
# agent skills) and, for search engines and AI agents (https://github.com/haxtheweb/issues/issues/3352),
# renders every page as its own HTML file (<slug>/index.html with its title, description, canonical link,
# JSON-LD and text). The same steps as the HAX CLI's site:build-static, run with the backend these templates
# came from: the published CLI's backend can lag the boilerplate on main, and shipped them unrendered.
# The build fails if a template is left unrendered. It runs before the compiled build/ and its loader
# scripts go in, so those stay the ones shipped here.
cd "$ROOT"
node "$ROOT/ecosystem/build/static_site.cjs" "$TMP/hn" "$OUT"
# the rebuild brings back the boilerplate's server-only files; a static host doesn't run them
rm -rf "$OUT/docker" "$OUT/Dockerfile" "$OUT/index.php" "$OUT/config.php" "$OUT/.htaccess" "$OUT/files/.htaccess" \
  "$OUT/netlify.toml" "$OUT/.hax-static-build"

# build/: the compiled front end, shipped with the site. The magic script finds ./build/ and loads from it,
# so nothing comes from cdn.hax.cloud; the registry files sit at the top of the site where HAXcms looks.
bash "$ROOT/ecosystem/build/compile-webcomponents.sh" "$TMP/wc"
mkdir -p "$OUT/build/es6"
mv "$TMP/wc/build/es6/node_modules" "$OUT/build/es6/node_modules"
cp "$TMP/wc/build/THIRD_PARTY_LICENSES" "$OUT/build/THIRD_PARTY_LICENSES"
cp "$TMP/wc/wc-registry.json" "$TMP/wc/wc-registry-graph.json" "$OUT/"
# and the loader scripts that go with this build (the boilerplate's copies wait for the next ubiquity release)
cp "$TMP/wc/build.js" "$TMP/wc/build-haxcms.js" "$OUT/"
# custom/ code resolves @haxtheweb/ through the page's import map: point it at this build, not the CDN
python3 -I "$ROOT/ecosystem/build/local_build.py" "$OUT"
echo "site: $OUT ($(find "$OUT" -type f | wc -l) files, $(du -sh "$OUT" | cut -f1))"
