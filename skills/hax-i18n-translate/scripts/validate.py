#!/usr/bin/env python3
"""Validate HAX element locale files against the English reference.

Auto-detects i18n pattern per namespace:

- flat (this.t): reference is <namespace>.en.json. Reports keys whose value
  still equals the English source, excluding englishLabel and known loanword
  keys (crossoriginTitle, gizmoTitle, tagMedia, tagAudioVideo, sourceTitle).

- haxProperties: namespace ends with ".haxProperties"; reference is the
  translatable leaves walked from lib/<tag>.haxProperties.json. Reports paths
  whose value still equals English. gizmo.title leftovers are routed to a
  "review (may be brand)" bucket (a bare proper-noun title can legitimately
  stay); all other leftovers are genuine.

Exit 0 if no parse errors and no genuine leftovers, else 1.

Usage:
  python3 validate.py <element-dir> [--namespace <tag>]
"""
import argparse
import glob
import json
import os
import sys


# --- loanword keys for flat mode -------------------------------------------

LOANWORD_KEYS = {
    "crossoriginTitle",
    "gizmoTitle",
    "tagMedia",
    "tagAudioVideo",
    "sourceTitle",
    "englishLabel",
}


# --- path helpers ----------------------------------------------------------

def parse_path(path):
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


def get_path(obj, parts):
    d = obj
    for p in parts:
        if isinstance(p, str):
            if isinstance(d, dict) and p in d:
                d = d[p]
            else:
                return None
        else:
            if isinstance(d, list) and p < len(d):
                d = d[p]
            else:
                return None
    return d


# --- haxProperties skeleton ------------------------------------------------

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


# --- validators ------------------------------------------------------------

def validate_flat(namespace, files):
    en_path = files.get("en")
    if not en_path:
        print(f"[{namespace}] skip: no .en.json reference")
        return 0, 0
    with open(en_path, encoding="utf-8") as f:
        en = json.load(f)

    parse_errors = []
    genuine = []
    total = 0
    for code, path in sorted(files.items()):
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

    print(f"[{namespace}] flat mode  english strings={len(en)}  locales={total}")
    if parse_errors:
        print("  PARSE ERRORS:")
        for c, e in parse_errors:
            print(f"    {c}: {e}")
    if genuine:
        print("  UNTRANSLATED LEFTOVERS (excluding loanwords + englishLabel):")
        for c, keys in genuine:
            print(f"    {c}: {keys}")
    else:
        print("  no genuine untranslated leftovers")
    print(f"  parse errors={len(parse_errors)}  files with leftovers={len(genuine)}  ok={total - len(parse_errors) - len(genuine)}/{total}")
    return len(parse_errors), len(genuine)


def validate_hax(element_dir, namespace, files):
    base_path = find_base_schema(element_dir, namespace)
    if not base_path:
        print(f"[{namespace}] error: no base schema in lib/", file=sys.stderr)
        return 1, 0
    with open(base_path, encoding="utf-8") as f:
        base = json.load(f)
    skeleton = build_skeleton(base)
    paths = list(collect_paths(skeleton))

    parse_errors = []
    genuine = []
    brand = []
    total = 0
    for code, path in sorted(files.items()):
        if code == "en":
            continue
        total += 1
        try:
            with open(path, encoding="utf-8") as f:
                d = json.load(f)
        except Exception as e:
            parse_errors.append((code, str(e)))
            continue
        g_left = []
        b_left = []
        for dotted, en_val in paths:
            val = get_path(d, parse_path(dotted))
            if val == en_val:
                if dotted == "gizmo.title":
                    b_left.append(dotted)
                else:
                    g_left.append(dotted)
        if g_left:
            genuine.append((code, g_left))
        if b_left:
            brand.append((code, b_left))

    print(f"[{namespace}] haxProperties mode  base={base_path}  leaves={len(paths)}  locales={total}")
    if parse_errors:
        print("  PARSE ERRORS:")
        for c, e in parse_errors:
            print(f"    {c}: {e}")
    if genuine:
        print("  UNTRANSLATED LEFTOVERS (genuine):")
        for c, keys in genuine:
            print(f"    {c}: {keys}")
    else:
        print("  no genuine untranslated leftovers")
    if brand:
        print("  REVIEW (may be brand -- gizmo.title kept as proper noun):")
        for c, keys in brand:
            print(f"    {c}: {keys}")
    print(f"  parse errors={len(parse_errors)}  genuine leftovers={len(genuine)}  brand-review={len(brand)}  ok={total - len(parse_errors) - len(genuine)}/{total}")
    return len(parse_errors), len(genuine)


# --- main ------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("element_dir", help="path to the element directory, e.g. elements/video-player")
    ap.add_argument("--namespace", help="validate only this namespace (auto: all in locales/)")
    args = ap.parse_args()

    element_dir = os.path.normpath(args.element_dir)
    locales_dir = os.path.join(element_dir, "locales")
    if not os.path.isdir(locales_dir):
        print(f"error: no locales/ directory in {element_dir}", file=sys.stderr)
        return 1

    # group locale files by namespace: <namespace>.<lang>.json
    groups = {}
    for f in sorted(os.listdir(locales_dir)):
        if not f.endswith(".json"):
            continue
        parts = f.split(".")
        if len(parts) < 3:
            continue
        lang = parts[-2]
        ns = ".".join(parts[:-2])
        groups.setdefault(ns, {})[lang] = os.path.join(locales_dir, f)

    if args.namespace:
        groups = {k: v for k, v in groups.items() if k == args.namespace}
    if not groups:
        print("error: no locale files found", file=sys.stderr)
        return 1

    total_errors = 0
    total_leftovers = 0
    for ns, files in sorted(groups.items()):
        if ns.endswith(".haxProperties"):
            e, g = validate_hax(element_dir, ns, files)
        else:
            e, g = validate_flat(ns, files)
        total_errors += e
        total_leftovers += g

    return 1 if (total_errors or total_leftovers) else 0


if __name__ == "__main__":
    sys.exit(main())
