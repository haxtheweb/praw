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
