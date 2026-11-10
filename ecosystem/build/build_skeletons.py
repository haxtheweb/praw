"""Skeletons sub-web: the starter sites HAXcms ships, the use case each serves and the theme each starts from.
Source: haxcms-nodejs src/coreConfig/skeletons (branch skeleton-names). Details in hax-skeletons.json."""
import json, glob, os
GH = "https://github.com/haxtheweb"
SRC = "haxcms-nodejs/src/coreConfig/skeletons/"
skels = {os.path.basename(f)[:-5]: json.load(open(f)) for f in sorted(glob.glob(SRC + "*.json"))}
def L(a, b): return {"label": a, "url": b}
def sid(n): return "k_" + n.replace("-", "_")
def tid(t): return "t_" + t.replace("-", "_")
def theme_of(d):
    th = d.get("theme") if isinstance(d.get("theme"), str) else (d.get("build", {}) or {}).get("theme") or d.get("site", {}).get("theme")
    return th.get("element") if isinstance(th, dict) else th
# use case per skeleton: main-web ids (course, portfolio, dept) are portals; blog, docs, club live here
USE = {"art-portfolio": "portfolio", "blog": "blog", "club-website": "club", "docs": "docs", "isc-graduate-portfolio": "portfolio",
       "online-course": "course", "portfolio": "portfolio", "resume-journey": "portfolio", "default-starter": None}
LOCAL_USE = {"blog": ("Blog", "hax:newspaper", "discoveryCoral", "Blogs and journals on HAXcms, like btopro.com, written in the same editor as courses."),
             "docs": ("Documentation", "hax:documents", "creekTeal", "Project documentation sites; haxtheweb.org's docs are being rebuilt as Learn HAX."),
             "club": ("Club website", "social:school", "pughBlue", "A website for a student club or group.")}
MAIN_USE = ["course", "portfolio", "dept"]
themes_used = sorted({theme_of(d) for d in skels.values() if theme_of(d)})

lines = ["%% HAX skeletons sub-web: the starter sites HAXcms ships, the use case each serves and the theme each starts from.",
         "%% Portals: ids from hax-ecosystem.mmd and hax-themes.mmd. Details in hax-skeletons.json.",
         "flowchart TB", "  %%@ layout rings=0,250,520,760 sizes=92,60,56,50",
         '  subgraph hub ["Skeletons"]', '    skeletons["skeletons"]', "  end",
         '  subgraph list ["Skeletons"]']
for n, d in skels.items(): lines.append(f'    {sid(n)}(["{d["meta"].get("useCaseTitle") or n}"])')
lines += ["  end", '  subgraph uses ["Use cases"]']
for u, (lab, ic, col, desc) in LOCAL_USE.items(): lines.append(f'    {u}(["{lab}"])')
for u in MAIN_USE: lines.append(f'    {u}(["{u}"])')
lines += ["  end", '  subgraph more ["Themes, tools and people"]']
for t in themes_used: lines.append(f'    {tid(t)}["{t}"]')
lines += ['    cli["cli"]', '    jos["jos"]', '    winston(("winston"))', "  end", ""]
for n, d in skels.items():
    lines.append(f"  skeletons -->|includes| {sid(n)}")
    if USE[n]: lines.append(f"  {sid(n)} -->|starts a| {USE[n]}")
    if theme_of(d): lines.append(f"  {sid(n)} -->|starts with| {tid(theme_of(d))}")
lines += ["  cli -->|creates sites from| skeletons", "  jos -.->|outlines| skeletons", "  winston ---|built the templating for| skeletons", "",
          "  %%@ group hub tier=0", "  %%@ group list tier=1", "  %%@ group uses tier=2", "  %%@ group more tier=3", "  %%@ node skeletons portal"]
for n in skels: lines.append(f"  %%@ node {sid(n)} icon=hax:templates color=original87Pink motion=lift")
for u, (lab, ic, col, desc) in LOCAL_USE.items(): lines.append(f"  %%@ node {u} icon={ic} color={col} motion=nudge")
for u in MAIN_USE: lines.append(f"  %%@ node {u} portal")
for t in themes_used: lines.append(f"  %%@ node {tid(t)} portal=themes")
lines += ["  %%@ node cli portal", "  %%@ node jos portal", "  %%@ node winston portal"]
open("hax-skeletons.mmd", "w").write("\n".join(lines) + "\n")

nodes = {"skeletons": {"always": True}}
for n, d in skels.items():
    m = d["meta"]
    nodes[sid(n)] = {"desc": (m.get("description") or "").strip() or "Skeleton.", "kind": "skeleton",
                     "links": {"source": f"{GH}/haxcms-nodejs/blob/main/src/coreConfig/skeletons/{n}.json"},
                     "note": f"Machine name {n}; theme {theme_of(d) or 'none'}" + (f"; tags {', '.join(m['tags'])}" if m.get("tags") else "") + "."}
for u, (lab, ic, col, desc) in LOCAL_USE.items(): nodes[u] = {"desc": desc}
nodes["docs"]["links"] = {"site": "https://haxtheweb.org/documentation"}
nodes["blog"]["links"] = {"site": "https://btopro.com"}
def S(c, *i): return {"caption": c, "nodes": list(i)}
tours = [{"id": "skeletons", "label": "Start a site from a skeleton", "message": f"The {len(skels)} skeletons HAXcms ships, the use case each serves and the theme each starts from.", "scenes": [
    S("A skeleton is a full working site you can start from and hand to someone else.", "skeletons"),
    S("Courses, portfolios, a blog, docs, a club site and a plain starter.", *[sid(n) for n in skels]),
    S("Each one serves a use case.", *LOCAL_USE, *MAIN_USE),
    S("Each one starts from a theme; open Themes to see them.", *[tid(t) for t in themes_used]),
    S("The CLI creates sites from skeletons; Winston built the templating.", "cli", "jos", "winston"),
    S("Skeletons, use cases and themes together."),
]}]
meta = {"name": "HAX skeletons", "parent": "main", "noTimeline": True,
        "about": f"{len(skels)} starter sites shipped with HAXcms (from haxcms-nodejs, branch skeleton-names), the use case each serves and the theme each starts from.",
        "kindLabels": {"rel": "skeleton to use case and theme", "schema": "data contracts", "contrib": "people who built the system"}}
json.dump({"meta": meta, "nodes": nodes, "evidence": {}, "tours": tours}, open("hax-skeletons.json", "w"), indent=1, ensure_ascii=False)
print(len(skels), "skeletons;", themes_used)
