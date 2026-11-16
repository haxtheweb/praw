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

The HAX network bar goes above the demo in its demo mode (<hax-network-bar demo>): a thin strip saying the
demo has no backend, so nothing is saved, with links to HAXcms in the browser and Install HAX. The editor
bar sits under it through --haxcms-top-offset, which the strip sets. A compiled bar without demo mode (a
webcomponents source from before it) is left out, rather than stacking a full second bar and Merlin on
the editor.

Fails if the page no longer has what it changes, rather than publishing a demo that silently breaks.

For search engines and AI agents (https://github.com/haxtheweb/issues/issues/3352) the page's placeholder
head ("HAXCMS", "My HAXCMS site description", books-app) says what this site is, from ../site/site.json:
title, description, canonical link, Open Graph tags, WebApplication JSON-LD and rel="llms"; a <noscript>
block gives a reader without JavaScript a heading, the description and the tour's pages; and robots.txt,
sitemap.xml and llms.txt are written beside the page. The address is DEMO_SITE_URL, else
https://demo.hax.cloud/. These are best-effort: a placeholder the page no longer has is left alone.
"""
import html as htmllib
import json
import os
import sys

DEMO_BASE = '<base href="/elements/haxcms-elements/demo/" />'
TOP_BASE = '<base href="/" />'
THEMES_REL = "'../lib/themes.json'"
THEMES_ABS = "'/node_modules/@haxtheweb/haxcms-elements/lib/themes.json'"
BUILDER = '<haxcms-site-builder id="site"'
NETWORK_BAR = "@haxtheweb/hax-network-bar/hax-network-bar.js"
DEMO_STRIP = (
    '<hax-network-bar demo></hax-network-bar>\n  '
    '<script type="module" src="/node_modules/' + NETWORK_BAR + '"></script>\n  '
)
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


SITE_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site", "site.json")


def attr(value):
    return htmllib.escape(str(value), quote=True)


def discovery(html, dest_dir, address):
    """The head, a <noscript> block and robots.txt / sitemap.xml / llms.txt, from this domain's site.json."""
    with open(SITE_JSON, encoding="utf-8") as f:
        site = json.load(f)
    title = site.get("title") or "Try HAX"
    desc = site.get("description") or ""
    items = [i for i in site.get("items", []) if i.get("slug")
             and (i.get("metadata") or {}).get("published", True) is not False]
    swaps = [
        ("<title>HAXCMS</title>", "<title>%s</title>" % attr(title)),
        ('<meta name="description" content="My HAXCMS site description">',
         '<meta name="description" content="%s">' % attr(desc)),
        ('<meta name="application-name" content="My site">', '<meta name="application-name" content="%s">' % attr(title)),
        ('<meta name="apple-mobile-web-app-title" content="My App">',
         '<meta name="apple-mobile-web-app-title" content="%s">' % attr(title)),
        ('<meta property="og:site_name" content="books-app">', '<meta property="og:site_name" content="HAX">'),
        ('<meta property="og:image" content="assets/icon-144x144.png" />',
         '<meta property="og:image" content="%sassets/icon-144x144.png" />' % attr(address)),
    ]
    for old, new in swaps:
        if html.count(old) == 1:
            html = html.replace(old, new)
    app = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": title,
        "description": desc,
        "url": address,
        "applicationCategory": "DeveloperApplication",
        "operatingSystem": "Any (web browser)",
        "isAccessibleForFree": True,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "publisher": {"@type": "Organization", "name": "HAXTheWeb", "url": "https://haxtheweb.org/",
                      "sameAs": ["https://github.com/haxtheweb"]},
    }
    head = "\n  ".join([
        '<link rel="canonical" href="%s" />' % attr(address),
        '<meta property="og:url" content="%s" />' % attr(address),
        '<meta property="og:title" content="%s" />' % attr(title),
        '<meta property="og:description" content="%s" />' % attr(desc),
        '<link rel="llms" href="/llms.txt" title="LLM Content Map" />',
        '<link rel="alternate" type="text/markdown" href="/llms.txt" title="Markdown Summary" />',
        '<script type="application/ld+json">%s</script>' % json.dumps(app).replace("<", "\\u003c"),
    ])
    if "</head>" in html:
        html = html.replace("</head>", "  " + head + "\n</head>", 1)
    links = "".join('<li><a href="/%s">%s</a></li>' % (attr(i["slug"]), attr(i.get("title") or i["slug"]))
                    for i in items)
    noscript = ("<noscript><h1>%s</h1><p>%s</p><p>This demo runs the HAX editor in your browser, so it needs "
                "JavaScript. Its pages:</p><ul>%s</ul><p>Make your own HAX site with nothing installed at "
                '<a href="https://browser.hax.cloud/">HAXcms in your browser</a>, or learn about HAX at '
                '<a href="https://hax.cloud/">hax.cloud</a>.</p></noscript>') % (attr(title), attr(desc), links)
    body = html.find("<body")
    end = html.find(">", body) if body != -1 else -1
    if end != -1:
        html = html[:end + 1] + "\n  " + noscript + html[end + 1:]
    with open(os.path.join(dest_dir, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n" % address)
    with open(os.path.join(dest_dir, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        f.write("  <url><loc>%s</loc></url>\n" % attr(address))
        for i in items:
            f.write("  <url><loc>%s%s</loc></url>\n" % (attr(address), attr(i["slug"])))
        f.write("</urlset>\n")
    with open(os.path.join(dest_dir, "llms.txt"), "w", encoding="utf-8") as f:
        f.write("# %s\n\n> %s\n\n" % (title, desc))
        f.write("A live HAXcms demo: the real HAX editor running in the browser on a short tour site anyone can edit"
                " for five minutes. Nothing is saved. To make a site of your own with nothing installed, use"
                " [HAXcms in your browser](https://browser.hax.cloud/); for scripted or agent work on sites, the"
                " HAX CLI (`npm install --global @haxtheweb/create`, then `hax site`).\n\n## Tour\n\n")
        for i in items:
            line = "- [%s](%s%s)" % (i.get("title") or i["slug"], address, i["slug"])
            if i.get("description"):
                line += ": " + " ".join(str(i["description"]).split())
            f.write(line + "\n")
        f.write("\n## HAX\n\n- [hax.cloud](https://hax.cloud/): the HAX ecosystem and how it connects\n"
                "- [HAX CLI](https://github.com/haxtheweb/create): create, edit and publish HAX sites\n"
                "- [Issues](https://github.com/haxtheweb/issues/issues): report a problem or ask for a feature\n")
    print("demo: head, <noscript>, robots.txt, sitemap.xml and llms.txt say what %s is (%d pages)" % (address, len(items)))
    return html


def main(src, dest, built, source):
    with open(src, encoding="utf-8") as f:
        html = f.read()
    for needle in (DEMO_BASE, THEMES_REL, BUILDER):
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
    bar = os.path.join(built, NETWORK_BAR)
    if os.path.isfile(bar) and "--haxcms-top-offset" in open(bar, encoding="utf-8").read():
        html = html.replace(BUILDER, DEMO_STRIP + BUILDER)
        print("demo: the network bar's demo strip is above the demo")
    else:
        print("demo: the compiled network bar has no demo strip yet; left out")
    address = os.environ.get("DEMO_SITE_URL") or "https://demo.hax.cloud/"
    if not address.endswith("/"):
        address += "/"
    html = discovery(html, os.path.dirname(os.path.abspath(dest)), address)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(html)
    print("demo: index.html with %d import map entries" % len(mapping["imports"]))


if __name__ == "__main__":
    main(*sys.argv[1:5])
