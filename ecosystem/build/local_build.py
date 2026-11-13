"""Finish hax.cloud's own build/ (run by site.sh after the compiled tree is in place).

    python3 -I local_build.py _site

The page's import map sends custom/ code's @haxtheweb/ imports to the CDN; with build/ shipped beside the
page they go to ./build/ instead, so the whole site loads from one origin. The boilerplate page also says
HAXCMSContext="php", which makes HAXcms ask the server for a backend (a request that can only fail here);
hax.cloud is a static site, so it says "published", HAXcms's context for a site that is only read. Fails, rather than publishing a
site that silently loads half from somewhere else, when the page no longer has that entry or build/ lacks
what the site needs: the HAXcms core, the autoloader, the theme and the network bar.
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
    if html.count(PHP) != 1:
        sys.exit("index.html changed: expected one %s" % PHP)
    with open(page, "w", encoding="utf-8") as f:
        f.write(html.replace(CDN, LOCAL).replace(PHP, PUBLISHED))
    print("local build: build/ checked, custom/ imports point at ./build/, context is published")


if __name__ == "__main__":
    main(sys.argv[1])
