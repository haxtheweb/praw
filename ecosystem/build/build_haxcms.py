"""HAXcms sub-web: the pieces of HAXcms a site owner touches, from the editor to the dashboard.
Portals: ids from hax-ecosystem.mmd. Details in hax-haxcms.json."""
import json
GH = "https://github.com/haxtheweb"
WC = GH + "/webcomponents/tree/master/elements/"
ISS = GH + "/issues/issues/"
NPM = "https://www.npmjs.com/package/@haxtheweb/"
def L(label, url): return {"label": label, "url": url}

MAIN = json.load(open("hax-ecosystem.json"))["nodes"]
MAIN.update({k: v for k, v in json.load(open("ext/main-moved.json")).items() if k not in MAIN})  # parts drawn here, not in the main web
ANS = json.load(open("gap-answers.json"))
def carry(id):
    """Description, links and status as the main web had them (plus the confirmed answers), minus timeline fields."""
    d = dict(MAIN.get(id, {})); d.update({k: v for k, v in ANS.get("main", {}).get(id, {}).items() if k not in ("confirmed", "skip")})
    return {k: v for k, v in d.items() if k in ("desc", "source", "links", "status", "release", "version", "note")}

# id, label, shape, icon, color, motion, details
PARTS = [
 ("editor", "HAX editor", None, None, None, None, None),  # portal
 ("merlin", "Merlin", None, None, None, None, None),  # portal
 ("dashboard", "Dashboard", None, None, None, None, None),  # portal
 ("outline", "Outline designer", "[", "hax:outline-designer-indent", "opportunityGreen", "nudge",
  {"desc": "Bulk structure editing for a whole site: add, move, nest, rename and delete pages in one view, saved back to site.json in one operation.",
   "links": {"repo": WC + "outline-designer", "npm": NPM + "outline-designer"}, "status": "released"}),
 ("files", "Admin files", "[", "icons:folder-open", "slateGray", "lift", carry("files")),
 ("settings", "Site settings", "[", "icons:build", "slateGray", "nudge",
  {"desc": "Site-level settings: title, description, theme and theme options, authoring defaults, publishing and integrations, edited from the dashboard.", "status": "released"}),
 ("insights", "Insights", "[", "hax:graph", "discoveryCoral", "pulse", carry("insights")),
 ("whatsnew", "What's New", "[", "icons:announcement", "forestGreen", "wiggle", carry("whatsnew")),
 ("tips", "HAX Tips", "[", "icons:lightbulb-outline", "beaverBlue", "glow", carry("tips")),
 ("themes", "Themes", None, None, None, None, None),  # portal
 ("deploy", "Publishing", None, None, None, None, None),  # portal
 ("jos", "JSON Outline Schema", None, None, None, None, None),  # portal
 ("xapi", "xAPI", None, None, None, None, None),  # portal
]
PORTALS = [p[0] for p in PARTS if p[2] is None]

lines = ["%% HAXcms sub-web: the pieces of HAXcms a site owner touches, from the editor to the dashboard.",
         "%% Portals: ids from hax-ecosystem.mmd. Details in hax-haxcms.json.",
         "flowchart TB", "  %%@ layout rings=0,260,520 sizes=92,64,56",
         '  subgraph hub ["HAXcms"]', '    haxcms["haxcms"]', "  end",
         '  subgraph auth ["Authoring"]']
for id, lab, sh, *_ in PARTS:
    if id in ("editor", "merlin", "outline", "files", "themes"): lines.append(f'    {id}["{lab}"]')
lines += ["  end", '  subgraph admin ["Site administration"]']
for id, lab, sh, *_ in PARTS:
    if id in ("dashboard", "settings", "insights", "whatsnew", "tips", "deploy", "jos", "xapi"): lines.append(f'    {id}["{lab}"]')
lines += ["  end", "",
 "  haxcms -->|edits pages with| editor",
 "  merlin -->|works inside| editor",
 "  haxcms -->|restructures sites with| outline",
 "  outline -.->|saves| jos",
 "  haxcms -->|stores uploads in| files",
 "  editor -->|inserts media from| files",
 "  haxcms -->|renders with| themes",
 "  settings -->|picks a theme from| themes",
 "  haxcms -->|is managed from| dashboard",
 "  dashboard -->|opens| settings",
 "  dashboard -->|opens| outline",
 "  insights -->|reports in| dashboard",
 "  xapi -.->|feeds| insights",
 "  whatsnew -->|appears in| dashboard",
 "  tips -->|appears in| merlin",
 "  tips -->|shares a system with| whatsnew",
 "  dashboard -->|publishes through| deploy",
 "", "  %%@ group hub tier=0", "  %%@ group auth tier=1", "  %%@ group admin tier=2", "  %%@ node haxcms portal"]
for id, lab, sh, ic, col, mo, det in PARTS:
    lines.append(f"  %%@ node {id} portal" if sh is None else f"  %%@ node {id} icon={ic} color={col} motion={mo}")
open("hax-haxcms.mmd", "w").write("\n".join(lines) + "\n")

nodes = {"haxcms": {"always": True}}
for id, lab, sh, ic, col, mo, det in PARTS:
    if det: nodes[id] = det
ev = {"whatsnew>dashboard": [L("Issue #3172: What's New and Tips", ISS + "3172")], "tips>merlin": [L("Issue #3172: What's New and Tips", ISS + "3172")]}
def S(c, *i): return {"caption": c, "nodes": list(i)}
tours = [{"id": "haxcms", "label": "Around a HAXcms site", "message": "The pieces of HAXcms a site owner touches, from writing a page to publishing the site.", "scenes": [
    S("A HAXcms site is edited, managed and published from a few pieces.", "haxcms"),
    S("Writing happens in the HAX editor, with Merlin for commands and the files area for media.", "editor", "merlin", "files"),
    S("The outline designer restructures a whole site at once and saves it as JSON Outline Schema.", "outline", "jos"),
    S("The dashboard holds settings, themes and publishing.", "dashboard", "settings", "themes", "deploy"),
    S("Insights, What's New and Tips close the loop back to people.", "insights", "whatsnew", "tips", "xapi"),
    S("All of HAXcms, in one view."),
]}]
meta = {"name": "HAXcms", "parent": "main", "noTimeline": True,
        "about": "The parts of HAXcms a site owner works in: the editor, Merlin, the outline designer, files, settings, the dashboard and the pieces that report back.",
        "kindLabels": {"rel": "which piece opens or feeds which", "schema": "data contracts"}}
json.dump({"meta": meta, "nodes": nodes, "evidence": ev, "tours": tours}, open("hax-haxcms.json", "w"), indent=1, ensure_ascii=False)
print(len(PARTS), "parts;", len(PORTALS), "portals")
