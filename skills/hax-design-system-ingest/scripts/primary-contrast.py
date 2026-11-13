"""Contrast of the text color DDD puts on each data-primary background, per bridge.

DDD gives every data-primary palette a fixed text color (--lowContrast-override:
black or white) that assumes DDD's own colors. A bridge that remaps a color to a
darker or lighter shade can break that pairing, and the bridge generator's
contrast report does not check it (haxtheweb/issues#3338). Run this before
choosing which data-primary palettes a demo shows.

usage, from the webcomponents monorepo root:
  python3 primary-contrast.py elements/<system>-theme/lib/<System>DDDMap.js
Prints one line per palette: number, DDD color, text color, ratio(s), FAIL below 4.5.
light-dark() values report both ratios; oklch values are reported as unresolved.
"""
import glob
import os
import re
import sys

LOW = re.compile(
    r'\[data-primary="(\d+)"\] \{\s*--ddd-theme-primary: var\(--ddd-primary-\d+\);'
    r"\s*--lowContrast-override: (\w+);"
)
PRIM = re.compile(r"--ddd-primary-(\d+): var\(\s*--ddd-theme-default-(\w+)")


def lum(r, g, b):
    def c(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4

    return 0.2126 * c(r) + 0.7152 * c(g) + 0.0722 * c(b)


def main(map_file):
    ddd = open("elements/d-d-d/lib/DDDStyles.js").read()
    override = {m.group(1): m.group(2) for m in LOW.finditer(ddd)}
    primary = {m.group(1): m.group(2) for m in PRIM.finditer(ddd)}
    bridge = open(map_file).read()
    tokens = "".join(
        open(f).read()
        for f in glob.glob(os.path.join(os.path.dirname(map_file), "*Tokens.js"))
    )

    def resolve(value, depth=0):
        ref = re.match(r"var\((--[\w-]+)", value)
        if not ref or depth > 5:
            return value
        found = re.search(re.escape(ref.group(1)) + r": ([^;]+);", tokens)
        return resolve(found.group(1).strip(), depth + 1) if found else value

    failed = 0
    for n in sorted(primary, key=int):
        name, text = primary[n], override.get(n, "white")
        m = re.search(r"--ddd-theme-default-%s: ([^;]+);" % name, bridge)
        if not m:
            continue
        value = resolve(m.group(1).strip())
        if value.startswith("#"):
            h = value[1:7]
            nums = [int(h[i : i + 2], 16) for i in (0, 2, 4)]
        elif value.startswith(("rgb", "light-dark")):
            nums = [int(x) for x in re.findall(r"\d+", value)]
        else:
            nums = []
        if len(nums) < 3:
            print(n, name, text, value, "(unresolved)")
            continue
        ratios = []
        for i in range(0, len(nums) - 2, 3):
            L = lum(*nums[i : i + 3])
            ratios.append(round(1.05 / (L + 0.05) if text == "white" else (L + 0.05) / 0.05, 2))
        flag = " <-- FAIL" if min(ratios) < 4.5 else ""
        failed += bool(flag)
        print(n, name, text, ratios, flag)
    return 1 if failed else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
