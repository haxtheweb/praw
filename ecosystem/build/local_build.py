"""Finish hax.cloud's own build/ (run by site.sh after the compiled tree is in place).

    python3 -I local_build.py _site

The page's import map sends custom/ code's @haxtheweb/ imports to the CDN; with build/ shipped beside the
page they go to ./build/ instead, so the whole site loads from one origin. The page must also say
HAXCMSContext="published", HAXcms's context for a site that is only read: "php" makes HAXcms ask the
server for a backend (a request that can only fail here). The boilerplate's ghpages.html says "published"
itself now; an older one that still says "php" is rewritten. Fails, rather than publishing a site that
silently loads half from somewhere else, when the page has neither context or no CDN entry, or build/
lacks what the site needs: the HAXcms core, the autoloader, the theme and the network bar. The pages the
HAX CLI's site:build-static rendered (<slug>/index.html, marked data-haxcms-static-route) get the same
changes as index.html.
"""
import os
import sys

CDN = '"@haxtheweb/": "https://cdn.hax.cloud/cdn/build/es6/node_modules/@haxtheweb/"'
LOCAL = '"@haxtheweb/": "./build/es6/node_modules/@haxtheweb/"'
PHP = 'globalThis.HAXCMSContext="php";'
PUBLISHED = 'globalThis.HAXCMSContext="published";'
NEEDED = [
    "haxcms-elements/lib/core/HAXCMSThemeWiring.js",
    "haxcms-elements/lib/core/haxcms-site-builder.js",
    "haxcms-elements/lib/base.css",
    "wc-autoload/wc-autoload.js",
    "ecosystem-theme/ecosystem-theme.js",
    "ecosystem-web/ecosystem-web.js",
    "hax-network-bar/hax-network-bar.js",
]


def main(out):
    tree = os.path.join(out, "build", "es6", "node_modules", "@haxtheweb")
    missing = [f for f in NEEDED if not os.path.isfile(os.path.join(tree, f))]
    if missing:
        sys.exit("build/ is missing @haxtheweb/%s; not publishing" % ", @haxtheweb/".join(missing))
    for f in ("wc-registry.json", "build/THIRD_PARTY_LICENSES"):
        if not os.path.isfile(os.path.join(out, f)):
            sys.exit("%s is missing; not publishing" % f)
    page = os.path.join(out, "index.html")
    with open(page, encoding="utf-8") as f:
        html = f.read()
    if html.count(CDN) != 1:
        sys.exit("index.html changed: expected one custom/ import map entry for the CDN")
    # exactly one context statement, either already "published" or the older "php"
    if html.count(PHP) + html.count(PUBLISHED) != 1:
        sys.exit("index.html changed: expected one %s (or the older %s)" % (PUBLISHED, PHP))
    with open(page, "w", encoding="utf-8") as f:
        f.write(html.replace(CDN, LOCAL).replace(PHP, PUBLISHED))
    # the pages site:build-static rendered (one folder per page, each the same shell as index.html)
    rendered = 0
    for folder, dirs, files in os.walk(out):
        rel = os.path.relpath(folder, out)
        if rel.split(os.sep)[0] in ("build", "pages", "files", "assets", "custom", "theme"):
            dirs[:] = []
            continue
        if rel == "." or "index.html" not in files:
            continue
        path = os.path.join(folder, "index.html")
        with open(path, encoding="utf-8") as f:
            text = f.read()
        if "data-haxcms-static-route" not in text:
            continue
        if text.count(CDN) != 1 or text.count(PHP) + text.count(PUBLISHED) != 1:
            sys.exit("%s changed: expected the same import map and context as index.html" % path)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text.replace(CDN, LOCAL).replace(PHP, PUBLISHED))
        rendered += 1
    print("local build: build/ checked, custom/ imports point at ./build/, context is published"
          " (index.html and %d rendered pages)" % rendered)


if __name__ == "__main__":
    main(sys.argv[1])
