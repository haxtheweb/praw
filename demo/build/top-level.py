"""Turn the webcomponents HAXcms demo page into one that runs from the top of demo.hax.cloud.

    python3 -I top-level.py source.html index.html

The demo page pins <base href="/elements/haxcms-elements/demo/">, so the HAXcms router writes every page
under that folder. Here the base becomes "/" and the demo's own files (site.json, pages/, theme/, custom/,
dist/dev/ ...) are proxied from that folder by demo/vercel.json, so routes read demo.hax.cloud/<page>.
Paths the page already writes from the root (/elements/..., /node_modules/...) are proxied as they are.
The one path written relative to the demo folder, ../lib/themes.json for ?theme=, is made absolute.
Fails if the page no longer has what it changes, rather than publishing a demo that silently breaks.
"""
import sys

DEMO_BASE = '<base href="/elements/haxcms-elements/demo/" />'
TOP_BASE = '<base href="/" />'
THEMES_REL = "'../lib/themes.json'"
THEMES_ABS = "'/elements/haxcms-elements/lib/themes.json'"


def main(src, dest):
    with open(src, encoding="utf-8") as f:
        html = f.read()
    for needle in (DEMO_BASE, THEMES_REL):
        if html.count(needle) != 1:
            sys.exit("demo page changed: expected exactly one %s" % needle)
    html = html.replace(DEMO_BASE, TOP_BASE).replace(THEMES_REL, THEMES_ABS)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
