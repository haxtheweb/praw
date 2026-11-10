#!/usr/bin/env bash
# Fetch the sources the generators read into the working folder given as $1 (default: ecosystem/.work).
# Clones are reused and fast-forwarded on later runs. Nothing here is committed: .work is ignored.
set -euo pipefail
ECO="$(cd "$(dirname "$0")/.." && pwd)"
WORK="${1:-$ECO/.work}"
mkdir -p "$WORK" && cd "$WORK"

clone() { # clone <owner/repo> <folder>
  if [ -d "$2/.git" ]; then git -C "$2" pull -q --ff-only || true
  else git clone -q "https://github.com/$1" "$2"; fi
}
# folder names are the ones the generators expect
clone haxtheweb/haxcms-nodejs haxcms-nodejs
clone haxtheweb/haxcms-php haxcms-php
clone haxtheweb/create createrepo
clone haxtheweb/haxcms-mcp mcprepo
clone haxtheweb/hax-schema hs
clone haxtheweb/json-outline-schema josrepo
clone haxtheweb/learn learnrepo
# webcomponents is large: a blobless, sparse clone of just the files the registry and token generators read
if [ -d wcrepo/.git ]; then git -C wcrepo pull -q --ff-only || true
else
  git clone -q --filter=blob:none --no-checkout https://github.com/haxtheweb/webcomponents wcrepo
  git -C wcrepo sparse-checkout set --no-cone '/package.json' '/gulpfile.mjs' '/scripts/' '/wc-registry.json' '/wc-registry-graph.json' \
    '/elements-catalog.json' '/hax-elements-registry.json' '/elements/i18n-manager/lib/*.json' '/elements/*/package.json' '/elements/*/custom-elements.json' \
    '/elements/d-d-d/design-system/' '/elements/d-d-d/tokens/' '/elements/d-d-d/lib/' '/.github/workflows/'
  git -C wcrepo checkout -q
fi
# praw is this repo
[ -e prawrepo ] || ln -s "$(cd "$ECO/.." && pwd)" prawrepo

# history only (no file contents) for freshness and bus factor on repos the GitHub API may not reach
mkdir -p gitlog
for r in haxtheweb/hax11ty haxtheweb/haxiam haxtheweb/haxcms-plugin-examples elmsln/elmsln btopro/edtechjoker; do
  d="gitlog/${r/\//_}"
  if [ -d "$d" ]; then git -C "$d" fetch -q || true; else git clone -q --bare --filter=blob:none "https://github.com/$r" "$d" || true; fi
done

# published packages: the haxcms-nodejs build (themes) and the two icon sets (element icons)
mkdir -p pkgs ext/el
npm_unpack() { # npm_unpack <package> <dest>
  local tgz; tgz="$(npm pack -q "$1" --pack-destination pkgs | tail -1)"
  rm -rf "$2" && mkdir -p "$2" && tar -xzf "pkgs/$tgz" -C "$2"
}
npm_unpack @haxtheweb/haxcms-nodejs ext/el/hn
for p in simple-icon hax-iconset; do
  v="$(npm view "@haxtheweb/$p" version)"
  [ -d "pkgs/haxtheweb-$p-$v" ] || npm_unpack "@haxtheweb/$p" "pkgs/haxtheweb-$p-$v"
done
echo "sources ready in $WORK"
