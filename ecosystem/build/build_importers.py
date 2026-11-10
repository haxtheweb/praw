"""Importers sub-web: every way content gets into HAX. Whole sites from other platforms, sites from a file, and content into a page.
Generated from haxcms-nodejs (system-spec.yaml, the importers folder, micro-frontend-registry) and the site editor's drop handling. Details in hax-importers.json."""
import json, yaml, os, re
GH = "https://github.com/haxtheweb"
NODE = GH + "/haxcms-nodejs/blob/main/"
def L(a, b): return {"label": a, "url": b}
def S(c, *i): return {"caption": c, "nodes": list(i)}
y = yaml.safe_load(open("haxcms-nodejs/src/openapi/system-spec.yaml"))
ops = {}
for p, methods in y["paths"].items():
    for m, o in methods.items():
        if isinstance(o, dict) and ("import" in p or "/actions/" in p): ops[p] = o.get("summary", "")
IMPORTERS_DIR = "haxcms-nodejs/src/systemRoutes/v1/routes/imports/"
# platform importers: id, label, kind (cms|docs|publisher), desc
PLATFORMS = [
 ("p_wordpress", "WordPress", "cms", "Pages and posts from a WordPress site, through its REST API."),
 ("p_drupal", "Drupal", "cms", "Nodes from a Drupal site; the platform ELMS:LN and much of HAX's history were built on."),
 ("p_plone", "Plone", "cms", "Content from a Plone site."),
 ("p_elmsln", "ELMS:LN", "cms", "Courses from an ELMS:LN network, the system HAXcms grew out of."),
 ("p_haxcms", "HAXcms", "cms", "Another HAXcms site or export: site.json plus pages, the same files a skeleton ships as."),
 ("p_notion", "Notion", "docs", "A Notion export or workspace tree."),
 ("p_gitbook", "GitBook", "docs", "A GitBook documentation site, from its summary and markdown."),
 ("p_vitepress", "VitePress", "docs", "A VitePress documentation site, from its config and markdown."),
 ("p_quarto", "Quarto", "docs", "A Quarto book or website project."),
 ("p_pressbooks", "Pressbooks", "publisher", "An open textbook from Pressbooks."),
 ("p_openstax", "OpenStax", "publisher", "An OpenStax textbook; the openstax2hax plugin prepares the book for conversion."),
 ("p_html", "Any HTML site", "cms", "A plain HTML page or site, crawled from a URL."),
]
# file formats: id, label, site-level endpoint, page-level handling, desc
FORMATS = [
 ("f_docx", "DOCX", "/system/api/v1/actions/import-docx", "Drop it in the editor to insert as HTML, or create sibling or child pages from its headings.", "Word documents (.docx, .doc). Headings become pages when you import as a site; drop one into a page to insert its content."),
 ("f_pptx", "PPTX", "/system/api/v1/actions/import-pptx", "Drop it in the editor: one page per slide, or inserted as HTML.", "PowerPoint files (.pptx). Each slide can become a page."),
 ("f_pdf", "PDF", "/system/api/v1/actions/import-pdf", "Drop it in the editor to insert as semantic HTML, or embed the PDF in the page.", "PDF files, converted to semantic HTML."),
 ("f_xlsx", "XLSX", "/system/api/v1/actions/import-xlsx", "Drop it in the editor to insert as an editable table, or convert to CSV.", "Spreadsheets (.xlsx, .xls, .ods). Rows become pages when imported as a site, or a table inside a page."),
 ("f_html", "HTML", "/system/api/v1/actions/import-html", "Drop or paste HTML into the editor.", "HTML files and pages."),
 ("f_md", "Markdown", None, "Drop a .md or .txt file in the editor; it is converted to HTML.", "Markdown and plain text, converted to HTML on the way in."),
 ("f_media", "Images, audio, video", None, "Drop or paste a file; it is uploaded to files/ and placed as the right block.", "Media files become media-image, audio-player or video-player blocks, uploaded to the site's files folder."),
 ("f_url", "A URL", None, "Paste a link into the editor or Merlin: the page's metadata is read and it is embedded or linked.", "Any link: YouTube, Vimeo, Wikipedia and other sources the app store knows become embeds; other pages become link cards."),
 ("f_jos", "JOS items (site.json)", None, None, "An item export in JSON Outline Schema, imported with hax site site:items-import."),
]
WAYS = [("w_platform", "A whole site from another platform", "Point HAXcms at a site elsewhere and it becomes a new HAX site: one importer per platform, all behind site/import/{platform}."),
        ("w_file", "A site from one file", "Upload a document and its structure becomes pages: headings in Word, slides in PowerPoint, rows in Excel."),
        ("w_page", "Content into a page", "While editing, drop a file or paste a link; the editor converts it and places it where you are.")]
ENTRY = {"dashboard": ("Create a site: pick Import and choose a platform or a file.", None), "editor": ("Drop a file or paste a URL while editing.", None), "merlin": ("Import from a URL, or drop a file on the top bar.", None),
         "cli": ("hax site --import-site <url> --import-structure <platform>, and site:items-import for JOS items.", None), "mcp": ("import_document, create_site_from_document and create_site_from_platform.", "mcptools"),
         "tag_actions": ("The converter and import actions in the OpenAPI system spec.", "openapi")}
lines = ["%% Importers sub-web: every way content gets into HAX, generated from haxcms-nodejs and the site editor.",
         "%% Portals: ids from hax-ecosystem.mmd, hax-mcptools.mmd and hax-openapi.mmd. Details in hax-importers.json.",
         "flowchart TB", "  %%@ layout rings=0,230,500,780 sizes=92,70,56,52",
         '  subgraph hub ["Importers"]', '    importers["importers"]', "  end", '  subgraph ways ["Three ways in"]']
for wid, lab, d in WAYS: lines.append(f'    {wid}["{lab}"]')
lines += ["  end", '  subgraph sources ["Platforms and file formats"]']
for pid, lab, kind, d in PLATFORMS: lines.append(f'    {pid}[["{lab}"]]')
for fid, lab, *_ in FORMATS: lines.append(f'    {fid}["{lab}"]')
lines += ["  end", '  subgraph entry ["Where you start an import"]']
for e in ENTRY: lines.append(f'    {e}["{e}"]')
lines += ['    elmsln["elmsln"]', "  end", ""]
for wid, lab, d in WAYS: lines.append(f"  importers -->|offers| {wid}")
for pid, *_ in PLATFORMS: lines.append(f"  w_platform -->|imports from| {pid}")
for fid, lab, site_ep, page, d in FORMATS:
    if site_ep: lines.append(f"  w_file -->|builds a site from| {fid}")
    if page: lines.append(f"  w_page -->|accepts| {fid}")
    if fid == "f_jos": lines.append(f"  w_platform -->|also accepts| {fid}")
lines += ["  p_elmsln --o|is| elmsln", "  dashboard -->|starts| w_platform", "  dashboard -->|starts| w_file", "  editor -->|starts| w_page", "  merlin -->|starts| w_page", "  merlin -->|starts| w_file",
          "  cli -->|starts| w_platform", "  cli -->|imports| f_jos", "  mcp -->|starts| w_platform", "  mcp -->|starts| w_file", "  tag_actions -.->|serves| w_file", "  tag_actions -.->|serves| w_page", "",
          "  %%@ group hub tier=0", "  %%@ group ways tier=1", "  %%@ group sources tier=2", "  %%@ group entry tier=3", "  %%@ node importers portal"]
for wid, *_ in WAYS: lines.append(f"  %%@ node {wid} icon=icons:cloud-upload color=inventOrange motion=pop")
KINDCOL = {"cms": "wonderPurple", "docs": "skyBlue", "publisher": "forestGreen"}
MONO = {"p_wordpress": "WP", "p_drupal": "DRPL", "p_plone": "PLON", "p_elmsln": "ELMS", "p_haxcms": "HAX", "p_notion": "NOTN", "p_gitbook": "GITB", "p_vitepress": "VITE", "p_quarto": "QRTO", "p_pressbooks": "PRBK", "p_openstax": "OSTX", "p_html": "HTML",
        "f_docx": "DOCX", "f_pptx": "PPTX", "f_pdf": "PDF", "f_xlsx": "XLSX", "f_html": "HTML", "f_md": "MD", "f_media": "MEDIA", "f_url": "URL", "f_jos": "JOS"}
for pid, lab, kind, d in PLATFORMS: lines.append(f"  %%@ node {pid} mono={MONO[pid]} color={KINDCOL[kind]} motion=lift")
for fid, lab, *_ in FORMATS: lines.append(f"  %%@ node {fid} mono={MONO[fid]} color=roarGolden motion=nudge")
for e, (d, web) in ENTRY.items(): lines.append(f"  %%@ node {e} portal" + (f"={web}" if web else ""))
lines.append("  %%@ node elmsln portal")
open("hax-importers.mmd", "w").write("\n".join(lines) + "\n")

nodes = {"importers": {"always": True}}
for wid, lab, d in WAYS: nodes[wid] = {"desc": d, "kind": "way"}
for pid, lab, kind, d in PLATFORMS:
    key = pid[2:]; ep = f"/system/api/v1/site/import/{key}"
    f = f"convert{key.capitalize()}ToSite.js"
    nodes[pid] = {"desc": d + (f" {ops.get(ep, '')}" if ep in ops else ""), "kind": kind, "links": ({"code": NODE + "src/systemRoutes/v1/routes/imports/" + f} if os.path.exists(IMPORTERS_DIR + f) else {}), "note": f"POST {ep}"}
for fid, lab, site_ep, page, d in FORMATS:
    nodes[fid] = {"desc": d + (" " + page if page else ""), "kind": "format", "note": (f"Site import: POST {site_ep}. " if site_ep else "") + ("Page import: handled by the site editor." if page else "")}
for e, (d, web) in ENTRY.items(): nodes[e] = {"desc": d} if e == "tag_actions" else {}
nodes["tag_actions"] = {"desc": ENTRY["tag_actions"][0]}
for e in ["dashboard", "editor", "merlin", "cli", "mcp"]: nodes[e] = {"note": ENTRY[e][0]}
tours = [{"id": "importers", "label": "Get your content in", "message": "Three ways in: a whole site from another platform, a site from one file, or content dropped into the page you are writing.", "scenes": [
    S("Everything you already have can come into HAX.", "importers"),
    S("Three ways in.", *[w for w, *_ in WAYS]),
    S("From another platform: the CMSs.", "w_platform", "p_wordpress", "p_drupal", "p_plone", "p_elmsln", "p_haxcms", "p_html"),
    S("From documentation tools and textbook publishers.", "p_notion", "p_gitbook", "p_vitepress", "p_quarto", "p_pressbooks", "p_openstax"),
    S("From one file: Word headings, PowerPoint slides or Excel rows become pages.", "w_file", "f_docx", "f_pptx", "f_xlsx", "f_pdf", "f_html"),
    S("Into the page you are writing: drop a document, a spreadsheet, media, or paste a link.", "w_page", "f_docx", "f_pdf", "f_md", "f_media", "f_url"),
    S("Start from the dashboard, the editor, Merlin, the CLI or the MCP; the same OpenAPI actions do the work.", *ENTRY),
    S("All the ways in."),
]}]
meta = {"name": "Importers", "parent": "main", "noTimeline": True, "sectionLabels": {"way": "ways in", "cms": "content systems", "docs": "documentation tools", "publisher": "textbook publishers", "format": "file formats"},
        "about": f"Every way content gets into HAX: {len(PLATFORMS)} platform importers, {len([f for f in FORMATS if f[2]])} file formats that become a site, and what the editor accepts dropped or pasted into a page. Generated from haxcms-nodejs and the site editor.",
        "kindLabels": {"rel": "way in to source; entry point to way in", "org": "platform identity", "schema": "served by the API"}}
json.dump({"meta": meta, "nodes": nodes, "evidence": {}, "tours": tours}, open("hax-importers.json", "w"), indent=1, ensure_ascii=False)
print(len(PLATFORMS), "platforms;", len(FORMATS), "formats")
