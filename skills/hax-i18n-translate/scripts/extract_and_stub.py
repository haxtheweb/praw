#!/usr/bin/env python3
"""Phase 1: extract English strings from a HAX element and scaffold locale files.

Supports two HAX i18n patterns (auto-detected; an element may use both):

1. this.t flat-object i18n:
   Parses the `this.t = { ... }` block in the constructor, writes
   `locales/<namespace>.en.json` (canonical English), then stubs
   `locales/<namespace>.<lang>.json` for every language in
   references/languages.json (English values as placeholders). Existing
   locale files are never clobbered.

2. haxProperties-based i18n:
   English strings live in `lib/<tag>.haxProperties.json`; the namespace is
   `<tag>.haxProperties` (declared via an `i18n-manager-register-element`
   event, or inferred). No `.en.json` is written -- the base schema IS the
   English reference. Each language gets a SPARSE nested
   `locales/<namespace>.<lang>.json` containing only the translatable leaves
   (English placeholders), structured to deep-merge over the base schema at
   runtime. Re-runs merge-fill: existing translated leaves are preserved and
   missing translatable leaves are added as placeholders.

Translatable leaves (haxProperties mode): gizmo.title, gizmo.description,
and for each settings group (configure, advanced, developer) each entry's
.title, .description, and (if present) the values of an .options map.

Usage:
  python3 extract_and_stub.py <element-dir> [--js <path>] [--namespace <tag>]

Example:
  python3 extract_and_stub.py elements/wikipedia-query
"""
import argparse
import glob
import json
import os
import re
import sys


# --- shared helpers ---------------------------------------------------------

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


def write_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def load_languages(languages_arg, script_dir):
    langs_path = languages_arg or os.path.join(
        script_dir, "..", "references", "languages.json"
    )
    with open(langs_path, encoding="utf-8") as f:
        return json.load(f)


# --- flat (this.t) mode -----------------------------------------------------

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
    """Extract key: "value" pairs from a this.t object literal."""
    if block is None:
        return {}
    # drop the ...this.t spread so it isn't mistaken for a pair
    block = re.sub(r"\.\.\.this\.t\s*,?", "", block)
    pairs = {}
    for m in re.finditer(r'(\w+)\s*:\s*"((?:[^"\\]|\\.)*)"', block):
        pairs[m.group(1)] = unescape(m.group(2))
    return pairs


def run_flat(element_dir, src, tag, languages, namespace_arg):
    """Stub the flat this.t locale files. Returns the namespace, or None."""
    pairs = parse_pairs(extract_t_block(src))
    if not pairs:
        return None
    namespace = namespace_arg or tag or os.path.basename(element_dir)
    locales_dir = os.path.join(element_dir, "locales")
    os.makedirs(locales_dir, exist_ok=True)

    en_path = os.path.join(locales_dir, f"{namespace}.en.json")
    write_json(en_path, pairs)
    print(f"[flat] wrote {en_path} ({len(pairs)} strings)")

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
    print(f"[flat] stubbed {created}, skipped {skipped} existing (namespace={namespace})")
    return namespace


# --- haxProperties mode -----------------------------------------------------

SETTINGS_GROUPS = ("configure", "advanced", "developer")
GIZMO_FIELDS = ("title", "description")
QUOTE_CLASS = r'[`"\x27]'


def detect_hax_namespace(src, tag, element_dir, has_flat):
    """Return (namespace, base_schema_path) for haxProperties i18n, or (None, None).

    Detection order:
      1. i18n-manager-register-element event with a *.haxProperties namespace.
      2. Existing locales/*haxProperties*.json filenames.
      3. Fallback (only when there is no this.t object): static get haxProperties
         pointing at a lib/*.haxProperties.json file -> namespace <tag>.haxProperties.
    """
    namespace = None

    # 1. register event
    m = re.search(
        r'i18n-manager-register-element[^}]*?namespace\s*:\s*'
        + QUOTE_CLASS + r'([^`"\x27]+\.haxProperties)' + QUOTE_CLASS,
        src, re.DOTALL,
    )
    if m:
        namespace = m.group(1)

    # 2. existing haxProperties locale files
    if not namespace:
        loc = os.path.join(element_dir, "locales")
        if os.path.isdir(loc):
            for f in sorted(os.listdir(loc)):
                if not f.endswith(".json"):
                    continue
                parts = f.split(".")
                if len(parts) >= 3 and "haxProperties" in parts:
                    namespace = ".".join(parts[:-2])
                    break

    # 3. fallback: haxProperties loaded from lib/ (only when no this.t)
    if not namespace and not has_flat:
        if tag and re.search(r'static get haxProperties\(\)', src) \
           and re.search(r'\.haxProperties\.json', src):
            namespace = f"{tag}.haxProperties"

    if not namespace:
        return None, None

    # resolve the base schema
    base_tag = (
        namespace[:-len(".haxProperties")]
        if namespace.endswith(".haxProperties") else tag
    )
    candidates = []
    if base_tag:
        candidates.append(os.path.join(element_dir, "lib", f"{base_tag}.haxProperties.json"))
    candidates += sorted(glob.glob(os.path.join(element_dir, "lib", "*haxProperties*.json")))
    for c in candidates:
        if os.path.isfile(c):
            return namespace, c
    return namespace, None


def build_skeleton(base):
    """Sparse nested object holding only translatable leaves (English values).

    Structure mirrors the base schema so it deep-merges at runtime; array
    entries are kept index-aligned (trailing empty entries trimmed).
    """
    result = {}

    gizmo = base.get("gizmo")
    if isinstance(gizmo, dict):
        g = {}
        for f in GIZMO_FIELDS:
            v = gizmo.get(f)
            if isinstance(v, str):
                g[f] = v
        if g:
            result["gizmo"] = g

    settings = base.get("settings")
    if isinstance(settings, dict):
        s = {}
        for group in SETTINGS_GROUPS:
            arr = settings.get(group)
            if isinstance(arr, list):
                out = []
                for entry in arr:
                    e = {}
                    if isinstance(entry, dict):
                        for f in GIZMO_FIELDS:
                            v = entry.get(f)
                            if isinstance(v, str):
                                e[f] = v
                        opts = entry.get("options")
                        if isinstance(opts, dict):
                            o = {}
                            for k, v in opts.items():
                                if isinstance(v, str):
                                    o[k] = v
                            if o:
                                e["options"] = o
                    out.append(e)
                while out and not out[-1]:
                    out.pop()
                if out:
                    s[group] = out
        if s:
            result["settings"] = s
    return result


def collect_paths(obj, prefix=""):
    """Yield (dotted_path, english_value) for each translatable leaf."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{prefix}.{k}" if prefix else k
            yield from collect_paths(v, p)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from collect_paths(v, f"{prefix}[{i}]")
    elif isinstance(obj, str):
        yield prefix, obj


def deep_merge_fill(fill, existing):
    """existing wins; fill provides defaults for paths missing from existing."""
    if isinstance(fill, dict) and isinstance(existing, dict):
        result = dict(existing)
        for k, fv in fill.items():
            if k in existing:
                result[k] = deep_merge_fill(fv, existing[k])
            else:
                result[k] = fv
        return result
    if isinstance(fill, list) and isinstance(existing, list):
        result = list(existing)
        for i, fv in enumerate(fill):
            if i < len(result):
                result[i] = deep_merge_fill(fv, result[i])
            else:
                result.append(fv)
        return result
    return existing


def run_hax(element_dir, namespace, base_path, languages):
    with open(base_path, encoding="utf-8") as f:
        base = json.load(f)
    skeleton = build_skeleton(base)
    paths = list(collect_paths(skeleton))
    locales_dir = os.path.join(element_dir, "locales")
    os.makedirs(locales_dir, exist_ok=True)

    print(f"[hax] namespace={namespace}  base={base_path}  leaves={len(paths)}")
    for p, v in paths:
        print(f"       {p} = {v!r}")

    created = 0
    filled = 0
    for code in sorted(languages):
        if code == "en":
            continue
        path = os.path.join(locales_dir, f"{namespace}.{code}.json")
        if os.path.isfile(path):
            try:
                with open(path, encoding="utf-8") as f:
                    existing = json.load(f)
            except Exception:
                existing = {}
            merged = deep_merge_fill(skeleton, existing)
            write_json(path, merged)
            filled += 1
        else:
            write_json(path, skeleton)
            created += 1
    print(f"[hax] created {created}, merge-filled {filled} (total {created + filled})")
    return namespace


# --- main -------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("element_dir", help="path to the element directory, e.g. elements/video-player")
    ap.add_argument("--js", help="path to the main JS file (auto-detected if omitted)")
    ap.add_argument("--namespace", help="namespace/tag (auto-detected if omitted)")
    ap.add_argument("--languages", help="path to languages.json")
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

    tag = extract_tag(src)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    languages = load_languages(args.languages, script_dir)

    has_flat = bool(parse_pairs(extract_t_block(src)))
    did_work = False

    # haxProperties mode
    hax_ns, base_path = detect_hax_namespace(src, tag, element_dir, has_flat)
    if hax_ns and base_path:
        run_hax(element_dir, args.namespace or hax_ns, base_path, languages)
        did_work = True
    elif hax_ns and not base_path:
        print(
            f"warn: detected haxProperties namespace '{hax_ns}' but no base schema in lib/",
            file=sys.stderr,
        )

    # flat (this.t) mode
    if run_flat(element_dir, src, tag, languages, args.namespace):
        did_work = True

    if not did_work:
        print(
            f"error: no this.t object or haxProperties i18n found in {js_path}",
            file=sys.stderr,
        )
        return 1

    print("next: node scripts/generate-translation-manifest.js  (from webcomponents root)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
