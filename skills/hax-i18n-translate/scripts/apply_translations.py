#!/usr/bin/env python3
"""Phase 2 (inline path): apply a translations map to locale files.

Takes a JSON map of { "<lang code>": { "<key>": "<translation>", ... }, ... }
and writes each language's values into locales/<namespace>.<code>.json,
preserving the canonical key order from <namespace>.en.json and keeping any
existing translated values for keys not present in the map.

This lets the orchestrator produce all ~100 translations in a single response
and apply them with one script run — no child agents — for elements with few
strings. Existing files (e.g. an already-translated es.json) are merged, not
clobbered: map values win for keys they specify, existing values are kept
otherwise, and only English-fallback is used if a key is missing everywhere.

Usage:
  python3 apply_translations.py --map <translations.json> <element-dir> [--namespace <tag>]

Exit 0 if all map codes written, else 1.
"""
import argparse
import glob
import json
import os
import sys


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--map", required=True, help="path to translations JSON: {code: {key: value}}")
    ap.add_argument("element_dir", help="path to the element directory, e.g. elements/stop-note")
    ap.add_argument("--namespace", help="namespace/tag (inferred from en.json filename if omitted)")
    args = ap.parse_args()

    element_dir = os.path.normpath(args.element_dir)
    locales_dir = os.path.join(element_dir, "locales")
    if not os.path.isdir(locales_dir):
        print(f"error: no locales/ directory in {element_dir}", file=sys.stderr)
        return 1

    with open(args.map, encoding="utf-8") as f:
        translations = json.load(f)

    en_files = sorted(glob.glob(os.path.join(locales_dir, "*.en.json")))
    if not en_files:
        print(f"error: no <namespace>.en.json found in {locales_dir}", file=sys.stderr)
        return 1
    en_path = en_files[0]
    namespace = args.namespace or os.path.basename(en_path)[: -len(".en.json")]
    with open(en_path, encoding="utf-8") as f:
        en = json.load(f)
    en_keys = list(en.keys())

    written = 0
    skipped = 0
    missing_keys = []
    for code, vals in sorted(translations.items()):
        if code == "en":
            continue
        if not isinstance(vals, dict):
            print(f"warn: {code} value is not an object, skipping", file=sys.stderr)
            skipped += 1
            continue
        path = os.path.join(locales_dir, f"{namespace}.{code}.json")
        existing = {}
        if os.path.isfile(path):
            try:
                with open(path, encoding="utf-8") as f:
                    existing = json.load(f)
            except Exception:
                existing = {}
        # build ordered output following en.json key order
        out = {}
        for k in en_keys:
            if k in vals:
                out[k] = vals[k]
            elif k in existing:
                out[k] = existing[k]
            else:
                out[k] = en[k]
        gaps = [k for k in en_keys if k not in vals]
        if gaps:
            missing_keys.append((code, gaps))
        with open(path, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
            f.write("\n")
        written += 1

    print(f"namespace: {namespace}  |  en keys: {len(en_keys)}  |  files written: {written}  |  skipped: {skipped}")
    if missing_keys:
        print("codes with missing keys (kept existing/en fallback):")
        for c, gaps in missing_keys:
            print(f"  {c}: {gaps}")
    return 1 if skipped else 0


if __name__ == "__main__":
    sys.exit(main())
