#!/usr/bin/env python3
"""Phase 2 (inline path): apply a translations map to locale files.

Supports two i18n patterns (auto-detected by namespace):

- flat (this.t): map is { "<lang>": { "<key>": "<translation>" } }. Keys are
  the flat this.t keys; output preserves <namespace>.en.json key order and
  merges with existing files (already-translated es.json is preserved).

- haxProperties: namespace ends with ".haxProperties". Map is
  { "<lang>": { "<dotted.path>": "<translation>" } } using dotted notation
  with array indices, e.g. "gizmo.title", "settings.configure[0].title",
  "settings.configure[2].options.en". The applier materializes each code's
  flat paths into a sparse nested object, then deep-merges over the existing
  locale file and the English skeleton (from lib/<tag>.haxProperties.json):
  map values win, then existing translated values, then English placeholder.

This lets the orchestrator produce all ~100 translations in a single response
and apply them with one script run -- no child agents.

Usage:
  python3 apply_translations.py --map <translations.json> <element-dir> [--namespace <tag>]

Exit 0 if all map codes written, else 1.
"""
import argparse
import glob
import json
import os
import sys


# --- path helpers (dotted notation with array indices) ---------------------

def parse_path(path):
    """'settings.configure[2].options.en' -> ['settings','configure',2,'options','en']."""
    parts = []
    cur = ""
    i = 0
    while i < len(path):
        c = path[i]
        if c == ".":
            if cur:
                parts.append(cur)
                cur = ""
        elif c == "[":
            if cur:
                parts.append(cur)
                cur = ""
            j = path.index("]", i)
            parts.append(int(path[i + 1:j]))
            i = j
        else:
            cur += c
        i += 1
    if cur:
        parts.append(cur)
    return parts


def set_path(root, parts, val):
    d = root
    for idx in range(len(parts) - 1):
        p = parts[idx]
        nxt = parts[idx + 1]
        container = {} if isinstance(nxt, str) else []
        if isinstance(p, str):
            if not isinstance(d.get(p), (dict, list)):
                d[p] = container
            d = d[p]
        else:
            while len(d) <= p:
                d.append(None)
            if not isinstance(d[p], (dict, list)):
                d[p] = container
            d = d[p]
    last = parts[-1]
    if isinstance(last, str):
        d[last] = val
    else:
        while len(d) <= last:
            d.append(None)
        d[last] = val


def materialize(path_map):
    """{dotted_path: value} -> nested sparse object."""
    root = {}
    for path, val in path_map.items():
        if not isinstance(val, str):
            continue
        set_path(root, parse_path(path), val)
    return root


def deep_merge_override(target, source):
    """source wins at leaves; merge source into target (returns new structure)."""
    if isinstance(target, dict) and isinstance(source, dict):
        result = dict(target)
        for k, sv in source.items():
            if k in result:
                result[k] = deep_merge_override(result[k], sv)
            else:
                result[k] = sv
        return result
    if isinstance(target, list) and isinstance(source, list):
        result = list(target)
        for i, sv in enumerate(source):
            if i < len(result):
                result[i] = deep_merge_override(result[i], sv)
            else:
                result.append(sv)
        return result
    return source


# --- haxProperties skeleton -------------------------------------------------

SETTINGS_GROUPS = ("configure", "advanced", "developer")
GIZMO_FIELDS = ("title", "description")


def build_skeleton(base):
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
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{prefix}.{k}" if prefix else k
            yield from collect_paths(v, p)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from collect_paths(v, f"{prefix}[{i}]")
    elif isinstance(obj, str):
        yield prefix, obj


def find_base_schema(element_dir, namespace):
    tag = namespace[:-len(".haxProperties")] if namespace.endswith(".haxProperties") else None
    cand = []
    if tag:
        cand.append(os.path.join(element_dir, "lib", f"{tag}.haxProperties.json"))
    cand += sorted(glob.glob(os.path.join(element_dir, "lib", "*haxProperties*.json")))
    for c in cand:
        if os.path.isfile(c):
            return c
    return None


# --- writers ----------------------------------------------------------------

def write_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def apply_flat(locales_dir, namespace, translations):
    en_path = os.path.join(locales_dir, f"{namespace}.en.json")
    if not os.path.isfile(en_path):
        print(f"error: no {namespace}.en.json found in {locales_dir}", file=sys.stderr)
        return 1
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
        write_json(path, out)
        written += 1

    print(f"[flat] namespace={namespace}  en keys={len(en_keys)}  written={written}  skipped={skipped}")
    if missing_keys:
        print("codes with missing keys (kept existing/en fallback):")
        for c, gaps in missing_keys:
            print(f"  {c}: {gaps}")
    return 1 if skipped else 0


def apply_hax(element_dir, locales_dir, namespace, translations):
    base_path = find_base_schema(element_dir, namespace)
    if not base_path:
        print(f"error: no base schema in lib/ for namespace {namespace}", file=sys.stderr)
        return 1
    with open(base_path, encoding="utf-8") as f:
        base = json.load(f)
    skeleton = build_skeleton(base)
    paths = list(collect_paths(skeleton))

    written = 0
    skipped = 0
    missing_paths = []
    path_set = {p for p, _ in paths}
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
        # priority: map > existing > skeleton(English)
        merged = deep_merge_override(deep_merge_override(skeleton, existing), materialize(vals))
        write_json(path, merged)
        written += 1
        gaps = [p for p, _ in paths if p not in vals and p not in _existing_paths(existing)]
        if gaps:
            missing_paths.append((code, gaps))

    print(f"[hax] namespace={namespace}  base={base_path}  leaves={len(paths)}  written={written}  skipped={skipped}")
    if missing_paths:
        print("codes with missing paths (kept existing/english fallback):")
        for c, gaps in missing_paths:
            print(f"  {c}: {gaps}")
    return 1 if skipped else 0


def _existing_paths(existing):
    out = set()
    for p, _ in collect_paths(existing):
        out.add(p)
    return out


# --- main -------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--map", required=True, help="path to translations JSON")
    ap.add_argument("element_dir", help="path to the element directory, e.g. elements/stop-note")
    ap.add_argument("--namespace", help="namespace/tag (auto-detected if omitted)")
    args = ap.parse_args()

    element_dir = os.path.normpath(args.element_dir)
    locales_dir = os.path.join(element_dir, "locales")
    if not os.path.isdir(locales_dir):
        print(f"error: no locales/ directory in {element_dir}", file=sys.stderr)
        return 1

    with open(args.map, encoding="utf-8") as f:
        translations = json.load(f)

    # resolve namespace + mode
    namespace = args.namespace
    if not namespace:
        hax = sorted(glob.glob(os.path.join(locales_dir, "*haxProperties.*.json")))
        if hax:
            f = os.path.basename(hax[0])
            namespace = ".".join(f.split(".")[:-2])
        else:
            en = sorted(glob.glob(os.path.join(locales_dir, "*.en.json")))
            if not en:
                print(f"error: no locale files found in {locales_dir}", file=sys.stderr)
                return 1
            namespace = os.path.basename(en[0])[: -len(".en.json")]

    if namespace.endswith(".haxProperties"):
        return apply_hax(element_dir, locales_dir, namespace, translations)
    return apply_flat(locales_dir, namespace, translations)


if __name__ == "__main__":
    sys.exit(main())
