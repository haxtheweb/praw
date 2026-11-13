#!/usr/bin/env bash
# Build hax.cloud into _site/ at the repo root: the HAXcms site boilerplate from haxcms-nodejs main, with
# site.json, pages/ and the interactive web written by build_site.py. Run by the hax.cloud workflow and by
# Vercel (vercel.json); needs bash, python3 (3.9+), and git or curl.
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

# the HAXcms site boilerplate, from haxcms-nodejs main
if command -v git >/dev/null 2>&1; then
  git clone -q --depth 1 --filter=blob:none --sparse https://github.com/haxtheweb/haxcms-nodejs "$TMP/hn"
  git -C "$TMP/hn" sparse-checkout set src/boilerplate/site
else
  mkdir -p "$TMP/hn"
  curl -fsSL https://codeload.github.com/haxtheweb/haxcms-nodejs/tar.gz/refs/heads/main |
    tar -xz -C "$TMP/hn" --strip-components=1 haxcms-nodejs-main/src/boilerplate/site
fi

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
echo "site: $OUT"
