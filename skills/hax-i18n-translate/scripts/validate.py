#!/usr/bin/env python3
"""Validate HAX element locale files against the English reference.

Checks every locales/<namespace>.*.json:
  - parses as valid JSON
  - reports keys whose value still equals the English source (untranslated
    leftovers), excluding englishLabel and known loanword keys where keeping the
    English value is correct (crossoriginTitle, gizmoTitle, tagMedia,
    tagAudioVideo, sourceTitle).

Exit code 0 if no parse errors and no genuine leftovers, else 1.

Usage:
  python3 validate.py <element-dir> [--namespace <tag>]
"""
import argparse
import glob
import json
import os
import sys

# Keys where the English value is an HTML keyword or a legitimate loanword that
# many languages keep untranslated. These are NOT counted as untranslated.
LOANWORD_KEYS = {
    "crossoriginTitle",  # HTML attribute keyword
    "gizmoTitle",        # "Video"
    "tagMedia",          # "Media"
    "tagAudioVideo",     # "Media"
    "sourceTitle",       # "Source"
    "englishLabel",      # name of English in the target language; handled per-lang
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("element_dir", help="path to the element directory, e.g. elements/video-player")
    ap.add_argument("--namespace", help="namespace/tag (inferred from en.json filename if omitted)")
    args = ap.parse_args()

    element_dir = os.path.normpath(args.element_dir)
    locales_dir = os.path.join(element_dir, "locales")
    if not os.path.isdir(locales_dir):
        print(f"error: no locales/ directory in {element_dir}", file=sys.stderr)
        return 1

    en_files = sorted(glob.glob(os.path.join(locales_dir, "*.en.json")))
    if not en_files:
        print(f"error: no <namespace>.en.json found in {locales_dir}", file=sys.stderr)
        return 1
    en_path = en_files[0]
    # derive namespace from filename: <namespace>.en.json
    base = os.path.basename(en_path)
    namespace = base[: -len(".en.json")]

    with open(en_path, encoding="utf-8") as f:
        en = json.load(f)

    parse_errors = []
    genuine = []
    total = 0
    for path in sorted(glob.glob(os.path.join(locales_dir, f"{namespace}.*.json"))):
        code = os.path.basename(path)[len(namespace) + 1: -len(".json")]
        if code == "en":
            continue
        total += 1
        try:
            with open(path, encoding="utf-8") as f:
                d = json.load(f)
        except Exception as e:
            parse_errors.append((code, str(e)))
            continue
        leftover = []
        for k, v in en.items():
            if k in LOANWORD_KEYS:
                continue
            if k in d and d[k] == v:
                leftover.append(k)
        if leftover:
            genuine.append((code, leftover))

    print(f"namespace: {namespace}")
    print(f"english strings: {len(en)}")
    print(f"locale files checked: {total}")
    print()
    if parse_errors:
        print("PARSE ERRORS:")
        for c, e in parse_errors:
            print(f"  {c}: {e}")
        print()
    if genuine:
        print("UNTRANSLATED LEFTOVERS (excluding loanwords + englishLabel):")
        for c, keys in genuine:
            print(f"  {c}: {keys}")
        print()
    else:
        print("no genuine untranslated leftovers")
    print(f"parse errors: {len(parse_errors)}  |  files with leftovers: {len(genuine)}  |  ok: {total - len(parse_errors) - len(genuine)}/{total}")
    return 1 if (parse_errors or genuine) else 0


if __name__ == "__main__":
    sys.exit(main())
