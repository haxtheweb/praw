#!/usr/bin/env bash
# Build the ecosystem web from the files in ecosystem/.
#
#   ecosystem/build/run.sh                  fetch sources, check for drift, assemble the page
#   ecosystem/build/run.sh build_json.py    run one generator (or several), then assemble
#   ecosystem/build/run.sh --assemble       assemble only, from ecosystem/web as it stands
#
# Generators run in ecosystem/.work (ignored), where web/*, player/* and build/data (as ext/)
# are linked in, so whatever a generator writes lands back in ecosystem/. The page is written
# to ecosystem/.work/hax-area-icons.html.
set -euo pipefail
ECO="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$ECO/.work"
mkdir -p "$WORK"
cd "$WORK"
ln -sfn "$ECO/build/data" ext
for f in "$ECO"/web/* "$ECO"/player/*; do ln -sfn "$f" .; done

adopt_new() { # a generator that makes a new web writes a plain file here: move it into web/ and link it back
  for f in hax-*.mmd hax-*.json; do
    [ "$f" = "hax-area-icons.html" ] && continue
    if [ -f "$f" ] && [ ! -L "$f" ]; then mv "$f" "$ECO/web/$f" && ln -s "$ECO/web/$f" "$f"; fi
  done
}

if [ "${1:-}" != "--assemble" ]; then
  if [ "$#" -gt 0 ]; then
    for g in "$@"; do python3 -I "$ECO/build/$g"; adopt_new; done
  else
    "$ECO/build/sources.sh" "$WORK"
    python3 -I "$ECO/build/drift.py" --no-pull
    adopt_new
  fi
fi
python3 -I "$ECO/build/assemble.py" template.html hax-area-icons.html
echo "page: $WORK/hax-area-icons.html"
