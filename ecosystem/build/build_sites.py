import json, re

# hax.psu.edu snapshot with site owners removed: [slug, pages] pairs plus totals
raw = json.load(open("ext/hax-psu-sites.json"))
counts = {f"site{i}/{s}": p for i, (s, p) in enumerate(raw["sites"])}; overall = raw["overall"]

# slug (without owner) -> (course code, college). Duplicates collapse to one course; pages = largest copy.
MAP = {
 # Arts and Architecture
 "aa0121": ("AA 121", "aa"), "aa120": ("AA 120", "aa"), "aa120copy": ("AA 120", "aa"), "aa122": ("AA 122", "aa"),
 "aa113n": ("AA 113N", "aa"), "aa103": ("AA 103", "aa"), "aa100": ("AA 100", "aa"), "aa100-su23": ("AA 100", "aa"), "aa-0001": ("AA 1", "aa"),
 "art0001": ("ART 1", "aa"), "alt-art001": ("ART 1", "aa"), "art1-7-week": ("ART 1", "aa"),
 "art-10-fa23": ("ART 10", "aa"), "divinsky-art-010": ("ART 10", "aa"), "divinskyart010-fa-sp": ("ART 10", "aa"),
 "art0020": ("ART 20", "aa"), "art0030": ("ART 30", "aa"), "art0211y": ("ART 211Y", "aa"), "art-211y-mk1": ("ART 211Y", "aa"),
 "arth101": ("ARTH 101", "aa"), "arth111-root-s": ("ARTH 111", "aa"), "arth112-root-l": ("ARTH 112", "aa"), "arth250": ("ARTH 250", "aa"), "arth280": ("ARTH 280", "aa"),
 "artsa301": ("ARTSA 301", "aa"), "artsa301-s": ("ARTSA 301", "aa"), "artsadmin403": ("ARTSA 403", "aa"),
 "inart1": ("INART 1", "aa"), "inart1-1": ("INART 1", "aa"), "inart-1-staging-ground": ("INART 1", "aa"), "inart116": ("INART 116", "aa"), "inart125": ("INART 125", "aa"),
 "music004": ("MUSIC 4", "aa"), "music007": ("MUSIC 7", "aa"), "music007-draft": ("MUSIC 7", "aa"), "music009": ("MUSIC 9", "aa"),
 "music011": ("MUSIC 11", "aa"), "music011lesson04": ("MUSIC 11", "aa"), "music0109": ("MUSIC 109", "aa"), "music109": ("MUSIC 109", "aa"),
 "music0209": ("MUSIC 209", "aa"), "music207": ("MUSIC 207", "aa"),
 "dart202": ("DART 202", "aa"), "dart206": ("DART 206", "aa"), "gd100": ("GD 100", "aa"), "game220": ("GAME 220", "aa"), "dmd100": ("DMD 100", "aa"),
 "arch100": ("ARCH 100", "aa"), "larch0060": ("LARCH 60", "aa"), "larch-060-self-check": ("LARCH 60", "aa"), "larch0065": ("LARCH 65", "aa"),
 "shopsafety": ("Shop safety", "aa"),
 # Eberly College of Science
 "biol110": ("BIOL 110", "eberly"), "biol110-1": ("BIOL 110", "eberly"), "biol110-2": ("BIOL 110", "eberly"), "biol110-1-1": ("BIOL 110", "eberly"),
 "biol230-tutorials-1": ("BIOL 230", "eberly"), "biol230-tutorials-2": ("BIOL 230", "eberly"), "biol230-tutorials-3": ("BIOL 230", "eberly"),
 "bisc002": ("BISC 2", "eberly"), "bisc004": ("BISC 4", "eberly"),
 "chem005": ("CHEM 5", "eberly"), "chem005-1": ("CHEM 5", "eberly"), "chem110": ("CHEM 110", "eberly"), "chem110s": ("CHEM 110", "eberly"), "chem110f2021": ("CHEM 110", "eberly"),
 "chem202": ("CHEM 202", "eberly"), "chem210": ("CHEM 210", "eberly"), "chem-212": ("CHEM 212", "eberly"),
 "math-for-pchem": ("Math for physical chemistry", "eberly"), "math-for-pchem-1": ("Math for physical chemistry", "eberly"), "math-for-pchem-2": ("Math for physical chemistry", "eberly"),
 "micrb106": ("MICRB 106", "eberly"), "phys211": ("PHYS 211", "eberly"), "physics211-lesson": ("PHYS 211", "eberly"), "phys212": ("PHYS 212", "eberly"), "astro130": ("ASTRO 130", "eberly"),
 # IST
 "ist110": ("IST 110", "ist"), "ist210": ("IST 210", "ist"), "ist402": ("IST 402", "ist"), "ist584sp25": ("IST 584", "ist"), "ai285": ("AI 285", "ist"),
 "ist256": ("IST 256", "ist"), "ist256-sp24": ("IST 256", "ist"), "edtechjoker": ("IST 256", "ist"),
 # named sites
 "haxcellence": ("haxtheweb.org", "special"), "human-flourish": ("Learn to Flourish Hub", "special"),
}
courses = {}
for full, pages in counts.items():
    slug = full.split("/", 1)[1]
    if slug not in MAP: continue
    code, college = MAP[slug]
    c = courses.setdefault(code, {"college": college, "pages": 0, "copies": 0})
    c["pages"] = max(c["pages"], pages); c["copies"] += 1
skipped = raw["unmapped_sites"] + sum(1 for f in counts if f.split("/", 1)[1] not in MAP)

def nid(code): return "c_" + re.sub(r"[^a-z0-9]+", "_", code.lower()).strip("_")
COL = {"aa": "beaverBlue", "eberly": "opportunityGreen", "ist": "skyBlue"}
order = sorted([k for k, v in courses.items() if v["college"] in COL], key=lambda k: (["aa", "ist", "eberly"].index(courses[k]["college"]), -courses[k]["pages"]))
for i, k in enumerate(order): courses[k]["tier"] = 2 if i % 2 == 0 else 3

SPECIAL = {"haxtheweb.org": ("docs", "haxtheweb.org, the HAX project site"), "Learn to Flourish Hub": ("dept", "flourish.hhd.psu.edu, the Learn to Flourish Hub")}

L = ["%% Sites on hax.psu.edu (HAXiam): courses deduplicated by course code, grouped by college. Sized by page count.",
     "%% Portals: ids from hax-ecosystem.mmd. Details in hax-sites.json. Source: hax.psu.edu stats snapshot.",
     "flowchart TB",
     "  %%@ layout rings=0,260,560,800,980 sizes=92,56,40,40,46",
     '  subgraph hub ["hax.psu.edu"]', '    haxpsu["hax.psu.edu"]', "  end",
     '  subgraph colleges ["Colleges"]', '    aa[["aa"]]', '    ist[["ist"]]', '    eberly[["eberly"]]', "  end",
     '  subgraph coursesA ["Courses"]']
for k in order:
    if courses[k]["tier"] == 2: L.append(f'    {nid(k)}["{k}"]')
L += ["  end", '  subgraph coursesB ["Courses"]']
for k in order:
    if courses[k]["tier"] == 3: L.append(f'    {nid(k)}["{k}"]')
L += ["  end", '  subgraph named ["Named sites and use cases"]', '    site_htw["haxtheweb.org"]', '    site_flourish["Learn to Flourish Hub"]',
      '    docs(["docs"])', '    dept(["dept"])', '    course(["course"])', '    hhd[["hhd"]]', '    ist256["ist256"]', "  end", ""]
for col in ["aa", "ist", "eberly"]: L.append(f"  haxpsu -->|hosts courses from| {col}")
for k in order:
    if k == "IST 256": continue
    L.append(f"  {nid(k)} --o|is taught in| {courses[k]['college']}")
L += ["  ist256 --o|is taught in| ist", "  haxpsu -->|hosts| site_htw", "  haxpsu -->|hosts| site_flourish",
      "  site_htw -->|is the| docs", "  site_flourish -->|is a| dept", "  site_flourish --o|belongs to| hhd",
      "  course -->|is the use case of| aa", "  course -->|is the use case of| ist", "  course -->|is the use case of| eberly",
      "", "  %%@ group hub tier=0", "  %%@ group colleges tier=1", "  %%@ group coursesA tier=2", "  %%@ group coursesB tier=3", "  %%@ group named tier=4"]
for p in ["haxpsu", "aa", "ist", "eberly", "dept", "course", "hhd", "ist256"]: L.append(f"  %%@ node {p} portal")
L.append("  %%@ node docs portal=skeletons")
for k in order:
    if k == "IST 256": continue
    L.append(f"  %%@ node {nid(k)} icon=hax:lesson color={COL[courses[k]['college']]} motion=lift")
L += ["  %%@ node site_htw icon=hax:site-map color=discoveryCoral motion=pop", "  %%@ node site_flourish icon=hax:site-map color=beaverBlue motion=pop"]
mmd = "\n".join(L) + "\n"
# IST 256 is the existing portal node, not a duplicate course tile
mmd = mmd.replace(f'    {nid("IST 256")}["IST 256"]\n', "")
open("hax-sites.mmd", "w").write(mmd)

nodes = {"haxpsu": {"always": True, "pages": overall["total_pages"]}}
tot = {"aa": 0, "ist": 0, "eberly": 0}; n = {"aa": 0, "ist": 0, "eberly": 0}
for k in order:
    c = courses[k]; tot[c["college"]] += c["pages"]; n[c["college"]] += 1
    if k == "IST 256": nodes["ist256"] = {"pages": c["pages"]}; continue
    nodes[nid(k)] = {"desc": f"{c['pages']} pages on hax.psu.edu" + (f", across {c['copies']} copies (largest shown)." if c["copies"] > 1 else "."), "pages": c["pages"], "kind": "course"}
for col in tot: nodes[col] = {"desc": f"{n[col]} courses with {tot[col]:,} pages on hax.psu.edu (largest copy of each)."}
nodes["site_htw"] = {"desc": f"haxtheweb.org, the HAX project site: {courses['haxtheweb.org']['pages']} pages.", "pages": courses["haxtheweb.org"]["pages"], "links": {"site": "https://haxtheweb.org"}}
nodes["site_flourish"] = {"desc": f"flourish.hhd.psu.edu, the Learn to Flourish Hub: {courses['Learn to Flourish Hub']['pages']} pages.", "pages": courses["Learn to Flourish Hub"]["pages"], "links": {"site": "https://flourish.hhd.psu.edu"}}
big = sorted(order, key=lambda k: -courses[k]["pages"])
def S(c, *i): return {"caption": c, "nodes": list(i)}
tours = [{"id": "sites", "label": "What runs on hax.psu.edu", "message": f"A snapshot of hax.psu.edu: {overall['site_count']} sites, {overall['user_count']} users and {overall['total_pages']:,} pages. Courses are shown once per course code, sized by pages.", "scenes": [
  S(f"hax.psu.edu: {overall['site_count']} sites, {overall['user_count']} users, {overall['total_pages']:,} pages.", "haxpsu"),
  S(f"Arts and Architecture: {n['aa']} courses, {tot['aa']:,} pages.", "aa", *[nid(k) for k in order if courses[k]["college"] == "aa"]),
  S(f"Eberly College of Science: {n['eberly']} courses, {tot['eberly']:,} pages.", "eberly", *[nid(k) for k in order if courses[k]["college"] == "eberly"]),
  S(f"IST: {n['ist']} courses, including IST 256.", "ist", "ist256", *[nid(k) for k in order if courses[k]["college"] == "ist" and k != "IST 256"]),
  S("Named sites: haxtheweb.org and the Learn to Flourish Hub.", "site_htw", "site_flourish", "docs", "dept", "hhd", "course"),
  S("Every course is the Course use case in action."),
]}]
meta = {"name": "hax.psu.edu", "parent": "main", "noTimeline": True, "sizeBy": "pages",
        "about": f"Snapshot of hax.psu.edu: {overall['site_count']} sites, {overall['user_count']} users, {overall['total_pages']:,} pages. Courses are deduplicated by course code (largest copy counts) and grouped by college; blogs, tests and general sites are left out.",
        "kindLabels": {"rel": "what hax.psu.edu hosts", "org": "courses by college"}}
json.dump({"meta": meta, "nodes": nodes, "evidence": {}, "tours": tours}, open("hax-sites.json", "w"), indent=1, ensure_ascii=False)
print(len(order), "courses:", n, tot, "| skipped sites:", skipped, "| biggest:", [(k, courses[k]["pages"]) for k in big[:6]])
