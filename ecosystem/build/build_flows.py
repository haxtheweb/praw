"""Step-by-step paths sub-web: what happens, in order, when a page loads, when you add a page, and when you restructure a site with the outline designer.
Sequence from a published site's index.html and build.js, haxcms-site-builder.js, wc-autoload and the OpenAPI site spec. Details in hax-flows.json."""
import json
GH = "https://github.com/haxtheweb"
WC = GH + "/webcomponents/tree/master/elements/"
def L(a, b): return {"label": a, "url": b}
def S(c, *i): return {"caption": c, "nodes": list(i)}
# flow id, label, desc, steps: (id, label, desc, parts (portal id -> web or None))
FLOWS = [
 ("fl_load", "A page loads", "From the request to a rendered page: the site builder tag, site.json, the theme, the page HTML, then the elements the page uses, lazily.", [
   ("l1", "1. Request", "The browser asks for a URL. HAXcms on PHP or Node.js, a static host or a HAX11ty build answers with the site's index.html.", {"haxcms": None, "php": None, "nodejs": None, "deploy": None, "f_static": "anatomy"}),
   ("l2", "2. index.html", "A small page: an import map, a preload of wc-registry.json and base.css, the web app manifest, the <haxcms-site-builder file=\"site.json?hash\"> tag already in the markup, then build-haxcms.js and build.js.", {"f_static": "anatomy", "f_registry": "anatomy"}),
   ("l3", "3. build.js boots", "Detects module support, sets up WCAutoload and loads the haxcms-site-builder module. Nothing else is loaded yet.", {"f_autoload": "anatomy", "f_magic": "anatomy"}),
   ("l4", "4. site.json", "haxcms-site-builder upgrades and fetches its file attribute: site.json, the JSON Outline Schema manifest. haxcms-site-store holds it for everything else.", {"jos": None, "f_sitejson": "anatomy", "sitejson": "contracts"}),
   ("l5", "5. The theme", "From manifest.metadata.theme, the builder imports the theme element by path, waits for customElements.whenDefined, and stamps it. The theme draws menu, breadcrumb and regions from the store.", {"themes": None, "f_theme": "anatomy"}),
   ("l6", "6. Route to a page", "The router turns the URL slug into the active item. The builder fetches that item's location, pages/<id>/index.html, with the build timestamp; a missing page shows the 404.", {"f_pages": "anatomy", "outline": "haxcms"}),
   ("l7", "7. Content into the theme", "The HTML is placed in the theme's content slot and an active-item event fires, so menus, previous and next, and xAPI listeners update.", {"editor": None, "xapi": None}),
   ("l8", "8. Elements load lazily", "wc-autoload watches the DOM for tags that are not defined, looks each up in wc-registry.json and imports its module. Only the elements this page uses are loaded, and they upgrade in place.", {"components": None, "f_registry": "anatomy", "f_autoload": "anatomy", "wcstandard": None}),
   ("l9", "9. After render", "The service worker registers for offline use, search is ready at x/search, and if you are logged in the editor UI loads and the registry graph warms the editor's own elements.", {"f_pwa": "anatomy", "f_search": "anatomy", "merlin": None}),
 ]),
 ("fl_add", "Add a page", "From logging in to a new page readers can see.", [
   ("a1", "1. Log in", "POST session login. haxcms-site-editor-ui appears: the top bar with Add page, Edit, Outline designer and the dashboard.", {"op_sessionlogin": "openapi", "editor": None}),
   ("a2", "2. Add page", "Choose Add page from the top bar, or ask Merlin. Pick a title, where it goes, and what to start from: blank, a template, a clone, or an imported file.", {"merlin": None, "importers": None, "skeletons": None}),
   ("a3", "3. The item is created", "POST /x/api/v1/items. The backend writes pages/<id>/index.html and appends the item (id, parent, order, slug, location) to site.json.", {"op_createitem": "openapi", "jos": None, "f_pages": "anatomy"}),
   ("a4", "4. The store updates", "haxcms-site-store refreshes the manifest; menus and breadcrumbs show the page and the router moves to its slug.", {"f_sitejson": "anatomy"}),
   ("a5", "5. Write", "Edit mode opens hax-body with the blocks the app store allows for this site. Type / for Merlin's slash commands, drop a file or paste a link to import.", {"editor": None, "components": None, "appstore": None, "importers": None}),
   ("a6", "6. Save", "PATCH /x/api/v1/content/{id} saves the HTML to pages/<id>/index.html; PATCH /x/api/v1/items/{id} saves title, published state and metadata to site.json. Git keeps a revision.", {"op_updatecontentbyidorslug": "openapi", "op_updateitem": "openapi"}),
   ("a7", "7. Readers see it", "The page renders through the same load path as every other page; sitemap, search index and feeds regenerate.", {"fl_load": None, "f_maps": "anatomy", "f_search": "anatomy"}),
 ]),
 ("fl_outline", "Restructure with the outline designer", "Many changes to a site's structure, staged in one view and saved in one operation.", [
   ("o1", "1. Open the outline designer", "From the top bar or the dashboard. outline-designer loads the items from the store's manifest.", {"outline": "haxcms", "dashboard": None}),
   ("o2", "2. Stage changes", "Drag to reorder, indent or outdent to nest, rename, add, duplicate, delete, lock, publish or unpublish. Every change is staged locally as a diff; nothing is written yet.", {"outline": "haxcms", "jos": None}),
   ("o3", "3. Save once", "PATCH /x/api/v1/site/outline: the whole set of operations in one atomic call. The backend validates it, writes site.json, and creates or removes page files as needed. Both backends behave identically.", {"op_updatesiteoutline": "openapi", "php": None, "nodejs": None, "openapi": None}),
   ("o4", "4. Everything follows", "The store refreshes the manifest; menus, breadcrumbs, previous and next, the sitemap and search follow the new structure.", {"f_sitejson": "anatomy", "themes": None}),
   ("o5", "5. Why it is guarded", "Bulk structure changes are mission critical, so outline-designer and saveOutline are covered by end-to-end and conformance tests; save and failure behavior cannot change from a data-model change.", {"q_e2e": "quality", "q_parity": "quality"}),
 ]),
]
portals = {}
for fid, lab, d, steps in FLOWS:
    for sid, slab, sd, parts in steps:
        for p, web in parts.items():
            if p not in ("fl_load",): portals[p] = web
lines = ["%% Step-by-step paths sub-web: what happens, in order, when a page loads, when you add a page, and when you restructure a site with the outline designer.",
         "%% Sources: a published site's index.html and build.js, haxcms-site-builder.js, wc-autoload, the OpenAPI site spec. Portals: ids from hax-ecosystem.mmd and the other sub-webs. Details in hax-flows.json.",
         "flowchart TB", "  %%@ layout rings=0,220,480,780 sizes=92,72,60,50",
         '  subgraph hub ["Step by step"]', '    flows["Step by step"]', "  end", '  subgraph flowsg ["Three paths"]']
for fid, lab, *_ in FLOWS: lines.append(f'    {fid}["{lab}"]')
lines += ["  end", '  subgraph steps ["Steps, in order"]']
for fid, lab, d, steps in FLOWS:
    for sid, slab, *_ in steps: lines.append(f'    {sid}>"{slab}"]')
lines += ["  end", '  subgraph parts ["What each step touches"]']
for p in portals: lines.append(f'    {p}["{p}"]')
lines += ["  end", ""]
for fid, lab, d, steps in FLOWS:
    lines.append(f"  flows -->|shows| {fid}")
    lines.append(f"  {fid} -->|starts with| {steps[0][0]}")
    for a, b in zip(steps, steps[1:]): lines.append(f"  {a[0]} -->|then| {b[0]}")
    for sid, slab, sd, parts in steps:
        for p in parts:
            if p == "fl_load": lines.append(f"  {sid} -->|uses| fl_load")
            else: lines.append(f"  {sid} -.->|touches| {p}")
lines += ["", "  %%@ group hub tier=0", "  %%@ group flowsg tier=1", "  %%@ group steps tier=2", "  %%@ group parts tier=3",
          "  %%@ node flows icon=hax:site-map color=nittanyNavy motion=pulse"]
COL = {"fl_load": "skyBlue", "fl_add": "opportunityGreen", "fl_outline": "inventOrange"}
for fid, lab, d, steps in FLOWS:
    lines.append(f"  %%@ node {fid} icon=hax:site-map color={COL[fid]} motion=pop")
    for sid, slab, *_ in steps: lines.append(f"  %%@ node {sid} mono={sid[1:]} color={COL[fid]} motion=nudge")
for p, web in portals.items(): lines.append(f"  %%@ node {p} portal" + (f"={web}" if web else ""))
open("hax-flows.mmd", "w").write("\n".join(lines) + "\n")
nodes = {"flows": {"always": True, "desc": "Three things that happen in HAX, in order. Play a path and the steps light up one at a time; each step points at the parts of the ecosystem it touches."}}
SRC = {"fl_load": L("haxcms-site-builder.js", WC + "haxcms-elements/lib/core/haxcms-site-builder.js"), "fl_add": L("site-spec.yaml", GH + "/haxcms-nodejs/blob/main/src/openapi/site-spec.yaml"), "fl_outline": L("outline-designer", WC + "outline-designer")}
for fid, lab, d, steps in FLOWS:
    nodes[fid] = {"desc": d, "kind": "path", "source": SRC[fid]}
    for sid, slab, sd, parts in steps: nodes[sid] = {"desc": sd, "kind": "step", "note": f"Part of: {lab}"}
tours = []
for fid, lab, d, steps in FLOWS:
    tours.append({"id": fid, "label": lab, "kind": "story", "message": d, "scenes": [S(f"{s[1]}. {s[2]}", s[0], *[p for p in s[3] if p != 'fl_load']) for s in steps] + [S(f"{lab}: the whole path.", fid, *[s[0] for s in steps])]})
meta = {"name": "Step by step", "parent": "main", "noTimeline": True, "sectionLabels": {"path": "paths", "step": "steps"},
        "about": "Three paths through HAX in order: how a page loads (index.html, the site builder tag, site.json, the theme, the page, then only the elements it uses), how a page is added, and how a site is restructured with the outline designer in one atomic save. Solid arrows are the order; dotted lines are what each step touches.",
        "kindLabels": {"rel": "the order of steps", "schema": "what a step touches"}}
json.dump({"meta": meta, "nodes": nodes, "evidence": {}, "tours": tours}, open("hax-flows.json", "w"), indent=1, ensure_ascii=False)
print(len(FLOWS), "paths;", sum(len(f[3]) for f in FLOWS), "steps;", len(portals), "portals")
