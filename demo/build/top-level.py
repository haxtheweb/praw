"""Turn the webcomponents HAXcms demo page into one that runs from the top of demo.hax.cloud on the
assets compiled beside it.

    python3 -I top-level.py source.html index.html <built node_modules> <source node_modules>

The demo page pins <base href="/elements/haxcms-elements/demo/">, so the HAXcms router writes every page
under that folder. Here the base becomes "/", and the demo folder's own files (theme/, custom/, dist/dev/,
wc-registry.json ...) sit at the top of the site beside it.

The page already loads elements through /node_modules/ (WCAutoloadBasePath, __appCDN), which is where the
compiled tree lives, and the compiled modules import each other by relative path. Only the page's own
module script and custom/src/ use bare specifiers (import "@haxtheweb/..."; import "lit"), so an import map
built from the compiled tree resolves those to /node_modules/. Package entry points come from the source
package.json files, which the compiled tree does not ship.

The one path written relative to the demo folder, ../lib/themes.json for ?theme=, is made absolute.
Fails if the page no longer has what it changes, rather than publishing a demo that silently breaks.
"""
import json
import os
import sys

DEMO_BASE = '<base href="/elements/haxcms-elements/demo/" />'
TOP_BASE = '<base href="/" />'
THEMES_REL = "'../lib/themes.json'"
THEMES_ABS = "'/node_modules/@haxtheweb/haxcms-elements/lib/themes.json'"
PREFIX = "/node_modules/"


def packages(built):
    """Every package folder in the compiled tree: lit, @lit/reactive-element, @haxtheweb/hax-body ..."""
    found = []
    for name in sorted(os.listdir(built)):
        path = os.path.join(built, name)
        if not os.path.isdir(path):
            continue
        if name.startswith("@"):
            found.extend(name + "/" + sub for sub in sorted(os.listdir(path))
                         if os.path.isdir(os.path.join(path, sub)))
        else:
            found.append(name)
    return found


def entry(source, pkg):
    """The file a bare `import "pkg"` loads, from the package's source package.json."""
    try:
        with open(os.path.join(source, pkg, "package.json"), encoding="utf-8") as f:
            meta = json.load(f)
    except (OSError, ValueError):
        return None
    exp = meta.get("exports")
    dot = exp.get(".", exp) if isinstance(exp, dict) else exp
    while isinstance(dot, dict):
        dot = dot.get("browser") or dot.get("import") or dot.get("module") or dot.get("default")
    target = dot if isinstance(dot, str) else (meta.get("module") or meta.get("main") or "index.js")
    return target[2:] if target.startswith("./") else target


def import_map(built, source):
    # whole scopes first (@haxtheweb/ ...), so a deep import of any package in them resolves
    imports = {name + "/": PREFIX + name + "/" for name in sorted(os.listdir(built))
               if name.startswith("@") and os.path.isdir(os.path.join(built, name))}
    for pkg in packages(built):
        if pkg.startswith("@haxtheweb/"):
            continue  # covered by the scope entry; HAX code imports files by explicit path
        imports[pkg + "/"] = PREFIX + pkg + "/"
        target = entry(source, pkg)
        if target and os.path.isfile(os.path.join(built, pkg, target)):
            imports[pkg] = PREFIX + pkg + "/" + target
    return {"imports": imports}


def main(src, dest, built, source):
    with open(src, encoding="utf-8") as f:
        html = f.read()
    for needle in (DEMO_BASE, THEMES_REL):
        if html.count(needle) != 1:
            sys.exit("demo page changed: expected exactly one %s" % needle)
    if 'type="importmap"' in html:
        sys.exit("demo page changed: it has its own import map now")
    mapping = import_map(built, source)
    if "lit" not in mapping["imports"] or "@haxtheweb/" not in mapping["imports"]:
        sys.exit("compiled tree is missing lit or @haxtheweb; not publishing")
    # the import map has to come before any module script or modulepreload, so right after <base>
    tag = '<script type="importmap">%s</script>' % json.dumps(mapping, separators=(",", ":"))
    html = html.replace(DEMO_BASE, TOP_BASE + "\n  " + tag).replace(THEMES_REL, THEMES_ABS)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(html)
    print("demo: index.html with %d import map entries" % len(mapping["imports"]))


if __name__ == "__main__":
    main(*sys.argv[1:5])
