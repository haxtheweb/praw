"""Site anatomy sub-web: what is on disk when you export a HAX site, authored versus generated, and what writes each file.
Portals: ids from hax-ecosystem.mmd, hax-haxcms.mmd and hax-contracts.mmd. Details in hax-anatomy.json."""
import json
GH = "https://github.com/haxtheweb"
def L(a, b): return {"label": a, "url": b}

# id, label, group (authored|generated), desc
FILES = [
 ("f_sitejson", "site.json", "authored", "The manifest and navigation tree in JSON Outline Schema. Edit it through the CLI or the outline designer, not by hand."),
 ("f_pages", "pages/<id>/index.html", "authored", "One folder per page holding the authored HTML, written with HAX web components; a markdown alternate may sit beside it."),
 ("f_files", "files/", "authored", "Uploads: images, PDFs and media the site uses."),
 ("f_theme", "theme/", "authored", "theme.css and theme assets for a custom theme layer on top of the chosen theme element."),
 ("f_custom", "custom/", "authored", "custom.es6.js, the site's own custom build when it has one."),
 ("f_registry", "wc-registry.json", "generated", "Maps every valid tag name to its module path. Built by Ubiquity; never hand-edited."),
 ("f_autoload", "build.js and the autoloader", "generated", "Finds undefined tags in the DOM, looks them up in wc-registry.json and imports the module, so a page full of custom elements needs no explicit imports."),
 ("f_magic", "the magic script", "generated", "One script tag that loads the autoloader and registry, so any page, HAX site or not, can use HAX elements."),
 ("f_llms", "llms.txt", "generated", "A site guide for language models, with links to the machine-readable resources."),
 ("f_maps", "sitemap.xml, robots.txt, rss.xml", "generated", "Crawler and feed maps with absolute URLs rooted at the site's domain and base path."),
 ("f_search", "lunrSearchIndex.json", "generated", "The full-text search corpus the site's search and the x/search route use."),
 ("f_pwa", "manifest.json and service-worker.js", "generated", "Progressive web app files, so a site installs and works offline."),
 ("f_wellknown", ".well-known/", "generated", "security.txt, api-catalog and agent-skills/index.json: how security researchers and agents discover the site."),
 ("f_static", "index.html, 404.html", "generated", "Static fallbacks that boot the theme and the autoloader."),
]
# writer portals: id -> (web, verb, [files])
WRITERS = {
 "outline": ("haxcms", "writes", ["f_sitejson"]),
 "editor": (None, "writes", ["f_pages"]),
 "files": ("haxcms", "fills", ["f_files"]),
 "themes": (None, "layer under", ["f_theme"]),
 "ubiquity": (None, "builds", ["f_registry"]),
 "haxcms": (None, "generates", ["f_llms", "f_maps", "f_search", "f_pwa", "f_wellknown", "f_static"]),
 "cli": (None, "creates and builds", ["f_sitejson", "f_pages"]),
 "components": (None, "are loaded by", ["f_autoload"]),
 "deploy": (None, "publishes", ["f_static"]),
 "hax11ty": (None, "renders from", ["f_sitejson", "f_pages"]),
 "skeletons": (None, "ship as", ["f_sitejson", "f_pages", "f_files"]),
 "agents": (None, "discover through", ["f_wellknown", "f_llms"]),
}
lines = ["%% Site anatomy sub-web: what is on disk when you export a HAX site, authored versus generated, and what writes each file.",
         "%% Portals: ids from hax-ecosystem.mmd and hax-haxcms.mmd. Details in hax-anatomy.json.",
         "flowchart TB", "  %%@ layout rings=0,240,470,720 sizes=92,64,58,52",
         '  subgraph hub ["A HAX site on disk"]', '    site["A HAX site on disk"]', "  end", '  subgraph authored ["Authored: yours to edit"]']
for id, label, g, d in FILES:
    if g == "authored": lines.append(f'    {id}["{label}"]')
lines += ["  end", '  subgraph generated ["Generated: rebuilt, never hand-edited"]']
for id, label, g, d in FILES:
    if g == "generated": lines.append(f'    {id}["{label}"]')
lines += ["  end", '  subgraph writers ["What writes them"]']
for p in WRITERS: lines.append(f'    {p}["{p}"]')
lines += ["  end", ""]
for id, label, g, d in FILES: lines.append(f"  site -->|{'holds' if g == 'authored' else 'is served with'}| {id}")
lines.append("  f_autoload -.->|reads| f_registry")
lines.append("  f_magic -->|loads| f_autoload")
lines.append("  f_magic -->|loads| f_registry")
lines.append("  f_sitejson -.->|locates| f_pages")
for p, (web, verb, fs) in WRITERS.items():
    for f in fs: lines.append(f"  {p} -->|{verb}| {f}")
lines += ["", "  %%@ group hub tier=0", "  %%@ group authored tier=1", "  %%@ group generated tier=2", "  %%@ group writers tier=3",
          "  %%@ node site icon=hax:site-map color=discoveryCoral motion=pop"]
for id, label, g, d in FILES: lines.append(f"  %%@ node {id} icon={'hax:page-edit' if g == 'authored' else 'icons:build'} color={'opportunityGreen' if g == 'authored' else 'slateGray'} motion=nudge")
for p, (web, verb, fs) in WRITERS.items(): lines.append(f"  %%@ node {p} portal" + (f"={web}" if web else ""))
open("hax-anatomy.mmd", "w").write("\n".join(lines) + "\n")

nodes = {"site": {"always": True, "desc": "A HAXcms site is a folder you can zip and hand to someone. Five things in it are yours; the rest is generated by HAXcms and rebuilt on demand.", "links": {"docs": "https://haxtheweb.org/documentation"}}}
for id, label, g, d in FILES: nodes[id] = {"desc": d, "kind": g}
nodes["f_sitejson"]["links"] = {"spec": GH + "/json-outline-schema"}
nodes["f_magic"]["links"] = {"issue": GH + "/issues/issues/2944"}
def S(c, *i): return {"caption": c, "nodes": list(i)}
tours = [{"id": "anatomy", "label": "Open a site folder", "message": "What is on disk when you export a HAX site, which files are yours and which are generated, and what writes each.", "scenes": [
    S("A HAX site is a folder.", "site"),
    S("Five things in it are yours: site.json, pages, files, theme and custom.", *[id for id, _, g, _ in FILES if g == "authored"]),
    S("site.json locates every page; the outline designer and the CLI write it.", "f_sitejson", "f_pages", "outline", "cli", "editor"),
    S("Everything else is generated and rebuilt, never hand-edited.", *[id for id, _, g, _ in FILES if g == "generated"], "haxcms"),
    S("The registry, the autoloader and the magic script are how a page full of custom elements just works.", "f_registry", "f_autoload", "f_magic", "ubiquity", "components"),
    S("Skeletons ship as these files; HAX11ty and publishing read them; agents discover the site through .well-known.", "skeletons", "hax11ty", "deploy", "agents", "f_wellknown", "f_llms"),
    S("The whole folder."),
]}]
meta = {"name": "Site anatomy", "parent": "main", "noTimeline": True,
        "about": "What is on disk when you export a HAX site: the five authored parts, the generated files HAXcms rebuilds, and the tools that write each.",
        "kindLabels": {"rel": "holds, writes or reads", "schema": "file to file"}, "kindLabelsNote": "Green tiles are yours to edit; gray tiles are generated."}
json.dump({"meta": meta, "nodes": nodes, "evidence": {}, "tours": tours}, open("hax-anatomy.json", "w"), indent=1, ensure_ascii=False)
print(len(FILES), "files;", len(WRITERS), "portals")
