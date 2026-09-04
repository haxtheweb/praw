#!/usr/bin/env python3
"""Phase 1: extract the this.t object from a HAX element and scaffold locale files.

Reads the element's main JS file, parses the `this.t = { ... }` block in the
constructor, writes `locales/<namespace>.en.json` (canonical English strings),
then stubs `locales/<namespace>.<lang>.json` for every language in
../references/languages.json by copying the English values as placeholders.
Existing locale files are never clobbered.

Usage:
  python3 extract_and_stub.py <element-dir> [--js <path>] [--namespace <tag>]

Example:
  python3 extract_and_stub.py elements/video-player
"""
import argparse
import json
import os
import re
import sys


def find_main_js(element_dir):
    """Pick the JS file named after the directory, else the first .js at root."""
    name = os.path.basename(os.path.normpath(element_dir))
    candidate = os.path.join(element_dir, name + ".js")
    if os.path.isfile(candidate):
        return candidate
    js_files = sorted(
        f for f in os.listdir(element_dir)
        if f.endswith(".js") and os.path.isfile(os.path.join(element_dir, f))
    )
    if not js_files:
        return None
    return os.path.join(element_dir, js_files[0])


def extract_tag(src):
    """Read static get tag() { return "tag-name"; }."""
    m = re.search(r'static get tag\(\)\s*\{\s*return\s*"([^"]+)"', src)
    return m.group(1) if m else None


def extract_t_block(src):
    """Return the text of the largest this.t = { ... } object literal, or None."""
    candidates = []
    for m in re.finditer(r'this\.t\s*=\s*\{', src):
        start = m.end() - 1  # index of '{'
        depth = 0
        i = start
        in_str = False
        esc = False
        while i < len(src):
            ch = src[i]
            if in_str:
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == '"':
                    in_str = False
            else:
                if ch == '"':
                    in_str = True
                elif ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        candidates.append(src[start:i + 1])
                        break
            i += 1
    if not candidates:
        return None
    return max(candidates, key=lambda c: len(re.findall(r'(\w+)\s*:\s*"', c)))


def unescape(s):
    return (
        s.replace("\\\\", "\x00")
         .replace('\\"', '"')
         .replace("\\n", "\n")
         .replace("\\t", "\t")
         .replace("\x00", "\\")
    )


def parse_pairs(block):
    """Extract key: \"value\" pairs from a this.t object literal."""
    if block is None:
        return {}
    # drop the ...this.t spread so it isn't mistaken for a pair
    block = re.sub(r"\.\.\.this\.t\s*,?", "", block)
    pairs = {}
    for m in re.finditer(r'(\w+)\s*:\s*"((?:[^"\\]|\\.)*)"', block):
        pairs[m.group(1)] = unescape(m.group(2))
    return pairs


def write_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("element_dir", help="path to the element directory, e.g. elements/video-player")
    ap.add_argument("--js", help="path to the main JS file (auto-detected if omitted)")
    ap.add_argument("--namespace", help="tag name / namespace (auto-detected if omitted)")
    ap.add_argument("--languages", help="path to languages.json (default: ../references/languages.json next to this script)")
    args = ap.parse_args()

    element_dir = os.path.normpath(args.element_dir)
    if not os.path.isdir(element_dir):
        print(f"error: {element_dir} is not a directory", file=sys.stderr)
        return 1

    js_path = args.js or find_main_js(element_dir)
    if not js_path or not os.path.isfile(js_path):
        print(f"error: could not find a JS file in {element_dir}", file=sys.stderr)
        return 1

    with open(js_path, encoding="utf-8") as f:
        src = f.read()

    namespace = args.namespace or extract_tag(src) or os.path.basename(element_dir)

    pairs = parse_pairs(extract_t_block(src))
    if not pairs:
        print(f"error: no this.t = {{ ... }} object with key:value pairs found in {js_path}", file=sys.stderr)
        return 1

    langs_path = args.languages or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "references", "languages.json"
    )
    with open(langs_path, encoding="utf-8") as f:
        languages = json.load(f)

    locales_dir = os.path.join(element_dir, "locales")
    os.makedirs(locales_dir, exist_ok=True)

    # 1. canonical English file
    en_path = os.path.join(locales_dir, f"{namespace}.en.json")
    write_json(en_path, pairs)
    print(f"wrote {en_path} ({len(pairs)} strings)")

    # 2. stubs for every language (never overwrite existing)
    created = 0
    skipped = 0
    for code in sorted(languages):
        if code == "en":
            continue
        path = os.path.join(locales_dir, f"{namespace}.{code}.json")
        if os.path.exists(path):
            skipped += 1
            continue
        write_json(path, pairs)
        created += 1
    print(f"stubbed {created} locale files, skipped {skipped} existing")
    print(f"namespace: {namespace}  |  languages: {len(languages) - 1}")
    print("next: node scripts/generate-translation-manifest.js  (from webcomponents root)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
