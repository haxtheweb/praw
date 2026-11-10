import json, os, re

EL = "ext/el/"
blocks = json.load(open(EL + "blocks.json"))
pkgs = json.load(open(EL + "pkgs.json"))
dirs = set(open(EL + "elements-dirs.txt").read().split())
icons = json.load(open("icons.json"))
import glob as _glob
# icon sets unpacked by sources.sh (newest version present)
S = (sorted(_glob.glob("pkgs/haxtheweb-simple-icon-*/"))[-1:] or ["pkgs/none/"])[0] + "package/lib/svgs/"
H = (sorted(_glob.glob("pkgs/haxtheweb-hax-iconset-*/"))[-1:] or ["pkgs/none/"])[0] + "package/lib/svgs/"
WC = "https://github.com/haxtheweb/webcomponents/tree/master/elements/"
WINS = "https://github.com/haxtheweb/praw/blob/main/WINS.md"
HAXLAB = "https://github.com/haxtheweb/hax-lab"
WORLDVIEW = "https://github.com/haxtheweb/praw/blob/main/WORLDVIEW.md"

def L(label, url): return {"label": label, "url": url}

def get_icon(name):
    full = name if ":" in name else "icons:" + name
    if full in icons: return full
    s, n = full.split(":", 1)
    for base in (S, H):
        p = f"{base}{s}/{n}.svg"
        if os.path.exists(p):
            t = open(p).read()
            vb = re.search(r'viewBox="([^"]+)"', t).group(1)
            inner = re.sub(r"^.*?<svg[^>]*>", "", t, flags=re.S)
            inner = re.sub(r"</svg>\s*$", "", inner.strip())
            inner = re.sub(r'\s(style|class|id)="[^"]*"', "", inner)
            inner = re.sub(r'\sfill="currentColor"', "", inner)
            icons[full] = {"vb": vb, "d": inner}
            return full
    return None

CATS = {  # HAX's own block categories (first gizmo tag)
    "Instructional": ("cat_instructional", "hax:lesson", "opportunityGreen", "Blocks that teach: questions, self checks, vocabulary, math, timelines and more."),
    "Media": ("cat_media", "hax:multimedia", "skyBlue", "Video, audio, images, galleries and embeds."),
    "Layout": ("cat_layout", "hax:3-3-3-3", "inventOrange", "Columns, sections, cards, quotes and calls to action."),
    "Content": ("cat_content", "hax:paragraph", "wonderPurple", "Structured content like career timelines and bibliographies."),
    "Text": ("cat_text", "hax:format-textblock", "beaverBlue", "Text helpers such as citations and placeholders."),
    "Other": ("cat_other", "hax:apps", "slateGray", "Licenses, tags, remote content, QR codes, embeds and fun extras."),
}
for c in CATS.values(): assert get_icon(c[1]), c[1]

# Course ontology branches (WORLDVIEW.md, Bill Rose)
BR = {
    "assessment": ("br_assessment", "Assessment", "High, low and no stakes checks of understanding."),
    "instruction": ("br_instruction", "Instruction", "Direct instruction, facilitation and coaching."),
    "content_br": ("br_content", "Content", "Pre-instructional, instructional, checks, tips and summaries."),
    "structure": ("br_structure", "Structure", "Units, lessons, sub-lessons and pages."),
    "pedagogy": ("br_pedagogy", "Pedagogy", "The beliefs and method driving the course."),
}
def branches(tags, tag):
    t = {x.lower() for x in tags}
    out = []
    if t & {"quiz", "question", "self check", "assessment", "knowledge check", "test", "exam", "activity", "exercise", "flash card"}: out.append("assessment")
    if t & {"pedagogy", "instruction", "workflow"} or tag in ("learning-component", "stop-note"): out.append("pedagogy")
    if t & {"definition", "vocabulary", "math", "timeline", "code", "citation", "reference", "ebook", "worksheet", "glossary"}: out.append("content_br")
    if t & {"grid", "section", "container", "page", "layout"} or tag in ("a11y-collapse", "grid-plate", "page-break", "play-list"): out.append("structure")
    if t & {"media", "video", "audio", "player", "gallery", "image"} and "assessment" not in out: out.append("instruction")
    return out

ids = {}
def nid(tag): return "b_" + tag.replace("-", "_")

cat_of = {}
order = []
for tag, v in blocks.items():
    g = v["gizmo"]; tags = g.get("tags") or []
    cat = tags[0] if tags and tags[0] in CATS else ("Content" if tags and tags[0].lower() == "content" else "Other")
    cat_of[tag] = cat
    order.append(tag)
order.sort(key=lambda t: (list(CATS).index(cat_of[t]), blocks[t]["gizmo"].get("title", t).lower()))

# alternate blocks across two rings so labels have room
tier_of = {}
per_cat = {}
for t in order:
    i = per_cat.get(cat_of[t], 0); per_cat[cat_of[t]] = i + 1
    tier_of[t] = 2 if i % 2 == 0 else 3

BLOCKPEOPLE_IDS = ["kai", "kcharlton", "mcollins", "traveler", "winston", "zach"]
BLOCKPEOPLE = [["kcharlton", "citation-element", 2], ["kai", "tagging-question", 5], ["kcharlton", "simple-cta", 6], ["kai", "inline-audio", 4], ["kcharlton", "learning-component", 6], ["kai", "self-check", 3], ["kcharlton", "block-quote", 6], ["winston", "a11y-collapse", 3], ["kcharlton", "accent-card", 3], ["kcharlton", "ebook-button", 6], ["kcharlton", "worksheet-download", 6], ["mcollins", "ai-usage-license", 1], ["zach", "rpg-character", 2], ["winston", "career-org-item", 4], ["winston", "career-role-item", 4], ["winston", "career-timeline", 4], ["traveler", "site-remote-content", 74], ["traveler", "simple-tags", 33], ["traveler", "learning-component", 30], ["traveler", "block-quote", 30], ["traveler", "ebook-button", 30], ["traveler", "worksheet-download", 30], ["traveler", "multiple-choice", 29], ["traveler", "true-false-question", 29], ["traveler", "short-answer-question", 29], ["traveler", "sorting-question", 28]]
PORTALS = ["kai", "kcharlton", "mcollins", "traveler", "winston", "zach"] + ["components", "haxschema", "appstore", "editor", "accessible", "remixable", "course", "portfolio", "eberly", "wins", "ddd", "hanna", "jimmykane"]

lines = ["%% HAX blocks sub-web: the blocks in the HAX app store, grouped by HAX's own categories.",
         "%% Ids shared with hax-ecosystem.mmd are portals. Details live in hax-elements.json.",
         "flowchart TB",
         "  %%@ layout rings=0,250,520,740,980 sizes=92,56,46,46,44",
         '  subgraph hub ["Web components"]', '    components["components"]', "  end",
         '  subgraph cats ["Block categories"]']
for name, (cid, ic, col, d) in CATS.items(): lines.append(f'    {cid}["{name}"]')
lines += ["  end", '  subgraph blocksA ["Blocks"]']
for t in order:
    if tier_of[t] == 2: lines.append(f'    {nid(t)}["{blocks[t]["gizmo"].get("title", t)}"]')
lines += ["  end", '  subgraph blocksB ["Blocks"]']
for t in order:
    if tier_of[t] == 3: lines.append(f'    {nid(t)}["{blocks[t]["gizmo"].get("title", t)}"]')
lines += ["  end", '  subgraph ontology ["Course ontology and links"]']
for k, (bid, name, d) in BR.items(): lines.append(f'    {bid}{{{{"{name}"}}}}')
for p in PORTALS:
    if p == "components": continue
    shape = {**{p: ('(("', '"))') for p in BLOCKPEOPLE_IDS}, "accessible": ('{{"', '"}}'), "remixable": ('{{"', '"}}'), "haxschema": ('[("', '")]'), "appstore": ('[("', '")]'), "course": ('(["', '"])'), "portfolio": ('(["', '"])'), "eberly": ('[["', '"]]'), "hanna": ('(("', '"))'), "jimmykane": ('(("', '"))')}.get(p, ('["', '"]'))
    lines.append(f"    {p}{shape[0]}{p}{shape[1]}")
lines += ["  end", ""]

edges = []
for name, (cid, *_r) in CATS.items(): edges.append(f"  components -->|groups blocks into| {cid}")
edges += ["  haxschema -.->|describes the editing form of every block in| components",
          "  appstore -.->|loads these blocks into| editor",
          "  components -->|are placed with| editor"]
for t in order:
    g = blocks[t]["gizmo"]; tags = g.get("tags") or []
    edges.append(f"  {CATS[cat_of[t]][0]} -->|includes| {nid(t)}")
    for b in branches(tags, t): edges.append(f"  {nid(t)} ==>|serves| {BR[b][0]}")
    low = " ".join(tags).lower() + " " + (g.get("description") or "").lower()
    if "a11y" in low or "accessib" in low: edges.append(f"  {nid(t)} -->|keeps it| accessible")
    if "license" in [x.lower() for x in tags] or t in ("license-element", "ai-usage-license"): edges.append(f"  {nid(t)} -->|keeps it| remixable")
    if "portfolio" in [x.lower() for x in tags]: edges.append(f"  {nid(t)} -->|is used in| portfolio")
    if "course" in [x.lower() for x in tags]: edges.append(f"  {nid(t)} -->|is used in| course")
    if "eberly" in [x.lower() for x in tags]: edges.append(f"  {nid(t)} --o|was made with| eberly")
edges += [f"  hanna ---|built| {nid('vocab-term')}",
          f"  jimmykane ---|designed the 8-bit characters for| {nid('rpg-character')}",
          f"  wins -->|records a win for| {nid('accent-card')}",
          f"  ddd -->|styles| components"]
edges += [f"  {p} ---|made {n} commits{' as Claude' if p == 'traveler' else ''} to| {nid(t)}" for p, t, n in BLOCKPEOPLE]
lines += edges + ["",
    "  %%@ group hub tier=0", "  %%@ group cats tier=1", "  %%@ group blocksA tier=2", "  %%@ group blocksB tier=3", "  %%@ group ontology tier=4",
    "  %%@ node components portal"]
for name, (cid, ic, col, d) in CATS.items(): lines.append(f"  %%@ node {cid} icon={ic} color={col} motion=pop")
missing_icons = []
for t in order:
    g = blocks[t]["gizmo"]; ic = get_icon(g.get("icon") or "")
    if not ic: missing_icons.append((t, g.get("icon"))); ic = CATS[cat_of[t]][1]
    lines.append(f"  %%@ node {nid(t)} icon={ic} color={CATS[cat_of[t]][2]} motion=lift")
BRI = {"br_assessment": "hax:assess", "br_instruction": "hax:engage", "br_content": "hax:documents", "br_structure": "hax:module", "br_pedagogy": "hax:consult"}
for k, (bid, name, d) in BR.items(): lines.append(f"  %%@ node {bid} icon={get_icon(BRI[bid]) or 'hax:lesson'} color=nittanyNavy motion=pop")
for p in PORTALS:
    if p != "components": lines.append(f"  %%@ node {p} portal")
open("hax-elements.mmd", "w").write("\n".join(lines) + "\n")

nodes = {"components": {"always": True}}
for name, (cid, ic, col, d) in CATS.items():
    nodes[cid] = {"desc": d + f" {per_cat.get(name, 0)} blocks in the app store.", "source": L("HAX app store (haxcms-nodejs config)", "https://github.com/haxtheweb/haxcms-nodejs")}
for k, (bid, name, d) in BR.items():
    nodes[bid] = {"desc": f"Course ontology branch: {d}", "source": L("WORLDVIEW.md: Course ontology (Bill Rose)", WORLDVIEW + "#course-ontology-the-model-under-the-authoring")}
MISSION = {"video-player", "audio-player"}
for t in order:
    g = blocks[t]["gizmo"]; pkg = pkgs[t][0]; short = pkg.split("/")[-1]
    d = {"desc": (g.get("description") or "").strip(), "tag": t, "links": {}, "source": L(f"{t} HAX properties (gizmo)", WC + short if short in dirs else "https://github.com/haxtheweb/webcomponents")}
    if short in dirs: d["links"]["repo"] = WC + short
    d["links"]["npm"] = "https://www.npmjs.com/package/" + pkg
    d["release"] = "npm:" + pkg
    d["status"] = "released"
    if t in MISSION: d["note"] = "Mission-critical: redesigns are limited to wrapping it, so existing content keeps working."
    if (g.get("meta") or {}).get("author") and g["meta"]["author"] not in ("HAXTheWeb core team", "HAXTheWeb"): d["author"] = g["meta"]["author"]
    nodes[nid(t)] = d
ev = {
    f"hanna>{nid('vocab-term')}": [L("hax-lab README: Vocab web component (2021)", HAXLAB), L("haxtheweb/issues #848", "https://github.com/haxtheweb/issues/issues/848")],
    f"jimmykane>{nid('rpg-character')}": [L("WINS.md: Site Dashboard (8-bit characters)", WINS + "#site-dashboard-three-generations-of-students-20222026")],
    f"wins>{nid('accent-card')}": [L("WINS.md: The seven accent-cards", WINS + "#the-seven-accent-cards")],
    f"{nid('course-model')}>eberly": [L("course-model HAX properties tag: Eberly", WC + "course-model")],
}
def S(c, *i): return {"caption": c, "nodes": list(i)}
by = lambda cat: [nid(t) for t in order if cat_of[t] == cat]
tours = [{"id": "blocks", "label": "Blocks by what they do", "message": "The blocks authors can place in HAX, grouped the way the editor groups them, and tied to the course ontology branch each one serves.", "scenes": [
    S("Every block is a web component.", "components"),
    S("The editor groups blocks into six categories.", *[c[0] for c in CATS.values()]),
    S("Instructional blocks: questions, self checks, vocabulary, math and timelines.", *by("Instructional"), "br_assessment", "br_content", "br_pedagogy"),
    S("Media blocks: video, audio, images, galleries and embeds.", *by("Media"), "br_instruction", "accessible"),
    S("Layout blocks give pages structure.", *by("Layout"), "br_structure"),
    S("Content, text and other blocks fill out the set.", *by("Content"), *by("Text"), *by("Other"), "portfolio", "course", "remixable", "eberly"),
    S("HAXSchema and the app store make every block editable, by people and agents alike.", "haxschema", "appstore", "editor", "ddd"),
    S("People and wins behind the blocks.", "hanna", "jimmykane", "wins"),
    S("Every block points back into the ecosystem web."),
]}]
meta = {"name": "HAX blocks", "parent": "main", "noTimeline": True,
        "about": f"The {len(order)} blocks in the HAX app store, read from each element's HAX properties. Gold lines show which course ontology branch a block serves.",
        "layerLabels": {"pillar": "Course ontology", "rel": "Categories and links"},
        "sectionLabels": {"pillar": "Course ontology", "rel": "Category and links"},
        "kindLabels": {"rel": "blocks in each category and their links", "pillar": "course ontology branches served", "schema": "schema contracts", "contrib": "people who built blocks", "org": "organizations"},
        "links": {"repo": "https://github.com/haxtheweb/webcomponents"}}
json.dump({"meta": meta, "nodes": nodes, "evidence": ev, "tours": tours}, open("hax-elements.json", "w"), indent=1, ensure_ascii=False)
json.dump(icons, open("icons.json", "w"))
print(len(order), "blocks;", "tiers", sum(1 for t in order if tier_of[t] == 2), sum(1 for t in order if tier_of[t] == 3), "; missing icons:", missing_icons)
