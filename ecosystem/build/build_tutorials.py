"""Tutorials sub-web: Learn HAX, generated from the haxtheweb/learn site.json and pages, with each tutorial tied to the part of HAX it teaches.
Portals: ids from hax-ecosystem.mmd and the other sub-webs. Details in hax-tutorials.json."""
import json, re, os
GH = "https://github.com/haxtheweb"
LEARN = "https://learn.haxtheweb.org/"
base = "learnrepo/"
def L(a, b): return {"label": a, "url": b}
def S(c, *i): return {"caption": c, "nodes": list(i)}
d = json.load(open(base + "site.json")); byid = {i["id"]: i for i in d["items"]}
def slug(s): return "tu_" + re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")
def text(i):
    p = base + i["location"]
    if not os.path.exists(p): return ""
    h = open(p).read(); t = re.sub(r"<[^>]+>", " ", h); return re.sub(r"\s+", " ", t).strip()
def yt(i):
    p = base + i["location"]
    if not os.path.exists(p): return None
    m = re.search(r"(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]+)", open(p).read()); return m.group(1) if m else None
# what each tutorial is about: slug -> [(portal id, web or None)]
ABOUT = {
 "tutorial-library/dashboard-site-basics/haxcms-dashboard": [("dashboard", None)],
 "tutorial-library/dashboard-site-basics/site-admin-settings-dashboard": [("settings", "haxcms"), ("dashboard", None)],
 "tutorial-library/dashboard-site-basics/system-settings-dashboard": [("haxiam", None), ("dashboard", None)],
 "tutorial-library/creating-structuring-content/create-a-new-page": [("editor", None), ("jos", None)],
 "tutorial-library/creating-structuring-content/reorder-organize-pages": [("outline", "haxcms")],
 "tutorial-library/creating-structuring-content/managing-course-structure": [("outline", "haxcms"), ("course", None)],
 "tutorial-library/editing-authoring/edit-a-page": [("editor", None)],
 "tutorial-library/editing-authoring/adding-blocks": [("editor", None), ("components", None), ("appstore", None)],
 "tutorial-library/editing-authoring/slash-commands": [("merlin", None), ("editor", None)],
 "tutorial-library/working-with-media/adding-video-blocks": [("b_video_player", "elements"), ("f_url", "importers")],
 "tutorial-library/working-with-media/working-with-images": [("b_media_image", "elements"), ("files", "haxcms")],
 "tutorial-library/site-health-reports/reports": [("insights", "haxcms"), ("xapi", None)],
 "tutorial-library/developer-onboarding/developer-onboarding": [("wcstandard", None), ("cli", None), ("issues", None)],
 "import-content/create-site-from-docx": [("f_docx", "importers"), ("w_file", "importers")],
 "import-content/xlsx-data-table-and-site-import": [("f_xlsx", "importers")],
 "import-content/migrate-data-to-hax": [("importers", None), ("jos", None)],
 "using-hax-for/club-websites": [("k_club_website", "skeletons")],
 "using-hax-for/portfolios": [("portfolio", None), ("k_portfolio", "skeletons")],
 "using-hax-for/courses-and-resumes": [("course", None), ("k_online_course", "skeletons"), ("k_resume_journey", "skeletons")],
 "start-here/cat": [("editor", None)], "start-here/chuck": [("dashboard", None), ("themes", None)], "start-here/sven": [("skeletons", None), ("importers", None)], "start-here/luna": [("wcstandard", None), ("cli", None)],
}
tops = sorted([i for i in d["items"] if not i.get("parent")], key=lambda i: i["order"])
sections = [t for t in tops if t["slug"] in ("start-here", "tutorial-library", "import-content", "using-hax-for")]
cats = []; tuts = []
for t in sections:
    kids = sorted([i for i in d["items"] if i.get("parent") == t["id"]], key=lambda i: i["order"])
    if t["slug"] == "tutorial-library":
        for k in kids:
            cats.append((k, t)); tuts += [(x, k) for x in sorted([i for i in d["items"] if i.get("parent") == k["id"]], key=lambda i: i["order"])]
    else:
        cats.append((t, None)); tuts += [(x, t) for x in kids]
portals = {}
for s, ab in ABOUT.items():
    for pid, web in ab: portals[pid] = web
lines = ["%% Tutorials sub-web: Learn HAX, generated from haxtheweb/learn (site.json and pages), each tutorial tied to the part of HAX it teaches.",
         "%% Portals: ids from hax-ecosystem.mmd and the other sub-webs. Details in hax-tutorials.json.",
         "flowchart TB", "  %%@ layout rings=0,220,470,760 sizes=92,66,56,52",
         '  subgraph hub ["Learn HAX"]', '    learnhax["learnhax"]', "  end", '  subgraph catsg ["Sections"]']
for c, parent in cats: lines.append(f'    {slug(c["slug"])}["{c["title"]}"]')
lines += ["  end", '  subgraph tutsg ["Tutorials and personas"]']
for x, c in tuts: lines.append(f'    {slug(x["slug"])}>"{x["title"]}"]')
lines += ["  end", '  subgraph about ["What they teach"]']
for pid in portals: lines.append(f'    {pid}["{pid}"]')
lines += ["  end", ""]
for c, parent in cats: lines.append(f"  learnhax -->|has| {slug(c['slug'])}")
for x, c in tuts: lines.append(f"  {slug(c['slug'])} -->|includes| {slug(x['slug'])}")
for x, c in tuts:
    for pid, web in ABOUT.get(x["slug"], []): lines.append(f"  {slug(x['slug'])} -->|teaches| {pid}")
lines += ["", "  %%@ group hub tier=0", "  %%@ group catsg tier=1", "  %%@ group tutsg tier=2", "  %%@ group about tier=3", "  %%@ node learnhax portal"]
for c, parent in cats: lines.append(f"  %%@ node {slug(c['slug'])} icon=icons:book color=skyBlue motion=pop")
for x, c in tuts: lines.append(f"  %%@ node {slug(x['slug'])} icon={'social:people' if c['slug']=='start-here' else 'image:slideshow' if yt(x) else 'hax:documents'} color={'keystoneYellow' if c['slug']=='start-here' else 'skyBlue'} motion=nudge")
for pid, web in portals.items(): lines.append(f"  %%@ node {pid} portal" + (f"={web}" if web else ""))
open("hax-tutorials.mmd", "w").write("\n".join(lines) + "\n")
nodes = {"learnhax": {"always": True}}
for c, parent in cats: nodes[slug(c["slug"])] = {"desc": (c.get("description") or f"{sum(1 for x, cc in tuts if cc['id']==c['id'])} pages in Learn HAX.").strip(), "links": {"page": LEARN + c["slug"]}, "kind": "section"}
for x, c in tuts:
    v = yt(x); tx = text(x)
    nodes[slug(x["slug"])] = {"desc": (x.get("description") or tx[:220] + ("…" if len(tx) > 220 else "")).strip() or x["title"], "links": {"page": LEARN + x["slug"], **({"video": f"https://www.youtube.com/watch?v={v}"} if v else {})},
                              "kind": "persona" if c["slug"] == "start-here" else "tutorial", "note": "Video tutorial with screenshots." if v else ""}
tours = [{"id": "tutorials", "label": "Learn HAX", "message": f"{sum(1 for x, c in tuts if c['slug']!='start-here')} tutorials and 4 personas from learn.haxtheweb.org, each tied to the part of HAX it teaches.", "scenes": [
    S("Learn HAX is where the tutorials live; this web will fold into it.", "learnhax"),
    S("Start as one of four people: Cat, Chuck, Sven or Luna.", *[slug(x["slug"]) for x, c in tuts if c["slug"] == "start-here"]),
    S("Dashboard and site basics.", *[slug(x["slug"]) for x, c in tuts if c["slug"] == "tutorial-library/dashboard-site-basics"], "dashboard"),
    S("Creating, structuring and editing content.", *[slug(x["slug"]) for x, c in tuts if c["slug"] in ("tutorial-library/creating-structuring-content", "tutorial-library/editing-authoring")], "editor", "merlin"),
    S("Media, reports and developer onboarding.", *[slug(x["slug"]) for x, c in tuts if c["slug"] in ("tutorial-library/working-with-media", "tutorial-library/site-health-reports", "tutorial-library/developer-onboarding")]),
    S("Getting content in, and what to use HAX for.", *[slug(x["slug"]) for x, c in tuts if c["slug"] in ("import-content", "using-hax-for")], "importers", "skeletons"),
    S("Every tutorial and what it teaches."),
]}]
meta = {"name": "Learn HAX tutorials", "parent": "main", "noTimeline": True, "sectionLabels": {"section": "sections", "tutorial": "tutorials", "persona": "personas"},
        "about": f"The {sum(1 for x, c in tuts if c['slug']!='start-here')} tutorials and 4 personas of Learn HAX (learn.haxtheweb.org), generated from the haxtheweb/learn site, each tied to the part of HAX it teaches. Tiles with a slideshow icon have a video.",
        "kindLabels": {"rel": "section to tutorial; tutorial to what it teaches"}}
json.dump({"meta": meta, "nodes": nodes, "evidence": {}, "tours": tours}, open("hax-tutorials.json", "w"), indent=1, ensure_ascii=False)
print(len(cats), "sections;", len(tuts), "pages;", len(portals), "portals")
