import json, os, re

icons = json.load(open("icons.json"))
S = "pkgs/haxtheweb-simple-icon-26.8.0/package/lib/svgs/"
H = "pkgs/haxtheweb-hax-iconset-26.8.0/package/lib/svgs/"
def get_icon(full):
    if full in icons: return full
    s, n = full.split(":", 1)
    for base in (S, H):
        p = f"{base}{s}/{n}.svg"
        if os.path.exists(p):
            t = open(p).read(); vb = re.search(r'viewBox="([^"]+)"', t).group(1)
            inner = re.sub(r"^.*?<svg[^>]*>", "", t, flags=re.S); inner = re.sub(r"</svg>\s*$", "", inner.strip())
            inner = re.sub(r'\s(style|class|id)="[^"]*"', "", inner); inner = re.sub(r'\sfill="currentColor"', "", inner)
            icons[full] = {"vb": vb, "d": inner}; return full
    raise SystemExit("missing icon " + full)
for i in ["social:school", "hax:calendar", "editor:attach-money", "places:casino", "hax:task"]: get_icon(i)

ISS = "https://github.com/haxtheweb/issues/issues/"
REPO = "https://github.com/btopro/edtechjoker"
WINS = "https://github.com/haxtheweb/praw/blob/main/WINS.md"
def L(a, b): return {"label": a, "url": b}

# semesters: (id, label, sortable year, taught)
SEM = []
for y in range(2019, 2027):
    for term, frac in (("Spring", .2), ("Fall", .8)):
        if (y == 2019 and term == "Spring") or (y == 2026 and term == "Fall"): continue
        sid = f"s{str(y)[2:]}{'s' if term == 'Spring' else 'f'}"
        if y == 2022 and term == "Fall": continue  # not shown: the web only states fall 2019 through spring 2026
        SEM.append((sid, f"{term} {y}", round(y + frac, 1), True))

def era(y): return "limestoneGray" if y is None else "beaverBlue" if y < 2022 else "creekTeal" if y < 2024 else "inventOrange"

# class projects: id, title, semester, issues, outcome portals [(id, web)], verb, students, note
P = [
 ("p_service", "service-card widget", "s19f", [32], [("components", "main")], "fed into", [], None),
 ("p_datecard", "small date element", "s20s", [199, 200], [("b_date_card", "elements")], "became", [], None),
 ("p_ghpreview", "github-preview element", "s20f", [388], [("components", "main")], "fed into", [], None),
 ("p_tvguide", "TV-guide style web component app", "s21s", [656], [("components", "main")], "fed into", [], None),
 ("p_sorting", "sorting-question", "s21f", [872], [("b_sorting_question", "elements")], "became", [], None),
 ("p_flash", "flash-card", "s21f", [881], [("b_flash_card", "elements")], "became", [], None),
 ("p_mark", "mark-the-words", "s21f", [882], [("b_mark_the_words", "elements")], "became", [], None),
 ("p_vocab", "vocab-term in the HAX editor", "s22s", [965], [("b_vocab_term", "elements")], "became", [], None),
 ("p_apa", "APA style element", "s23s", [1285], [], "led to", [], ""),
 ("p_dragdrop", "drag and drop activity", "s23s", [1332], [("b_matching_question", "elements")], "led to", [], "The start of the matching question."),
 ("p_rpg", "RPG character that looks like... someone", "s23f", [1733], [("b_rpg_character", "elements")], "extended", [], None),
 ("p_linkpreview", "link-preview-card", "s23f", [1764], [("components", "main")], "fed into", [], None),
 ("p_lecture", "lecture-player", "s23f", [1788], [("components", "main")], "fed into", [], None),
 ("p_inline", "inline-audio", "s24s", [1102], [("b_inline_audio", "elements")], "became", ["winston"], "Winston White's class project; the issue was opened in December 2022."),
 ("p_playlist", "play-list", "s24s", [1914], [("b_play_list", "elements")], "became", [], None),
 ("p_testimonial", "block-quote with an image", "s24s", [1915], [("b_person_testimonial", "elements")], "became", [], None),
 ("p_gallery", "image gallery presentation", "s24s", [1946], [("b_image_gallery", "elements")], "became", [], None),
 ("p_party", "haxcms-party-ui", "s24s", [1950], [("dashboard", "main")], "fed into", [], None),
 ("p_search", "HAXsite search and visualization engine", "s24f", [2174], [("haxcms", "main")], "fed into", [], None),
 ("p_unsdg", "un-sdg goal icons", "s24f", [2147], [("components", "main")], "fed into", [], None),
 ("p_usecases", "use-cases dashboard", "s24f", [2182], [("dashboard", "main"), ("skeletons", "main")], "fed into", [], None),
 ("p_steps", "ddd-steps-list and ddd-card-list", "s25s", [2256, 2257], [("ddd", "main")], "became part of", [], None),
 ("p_aiul", "AI Usage License tag", "s25s", [2288], [("b_ai_usage_license", "elements")], "became", [], None),
 ("p_portthemes", "portfolio-sidebar and portfolio-very themes", "s25s", [2283, 2284], [("themes", "main")], "became", [], None),
 ("p_fox", "What the fox say", "s25f", [2476], [("components", "main")], "fed into", [], None),
 ("p_dyngallery", "dynamic image gallery app", "s26s", [2617], [("components", "main")], "fed into", [], None),
]
sem_year = {s[0]: s[2] for s in SEM}

outs = []
for p in P:
    for o in p[4]:
        if o not in outs: outs.append(o)
people = ["bryan", "winston", "kcharlton"]

lines = ["%% IST 256 sub-web: Bryan's course (repo btopro/edtechjoker), by semester, with class projects and what they became.",
         "%% Portals: ids from hax-ecosystem.mmd (portal) and hax-elements.mmd (portal=elements). Details in hax-ist256.json.",
         "flowchart TB",
         "  %%@ layout rings=0,330,640,900 sizes=92,48,44,44",
         '  subgraph hub ["IST 256"]', '    ist256["ist256"]', "  end",
         '  subgraph sems ["Semesters"]']
for sid, lab, y, taught in SEM: lines.append(f'    {sid}(["{lab}"])')
lines += ["  end", '  subgraph projects ["Class projects"]']
for p in P: lines.append(f'    {p[0]}["{p[1]}"]')
lines += ["  end", '  subgraph outcomes ["What they became, and who"]']
for o, w in outs: lines.append(f'    {o}["{o}"]')
for pid in people: lines.append(f'    {pid}(("{pid}"))')
lines += ['    ist[["ist"]]', '    haxlab[["haxlab"]]', "  end", ""]
lines += ["  ist256 --o|is taught in| ist", "  ist256 -->|sends its best students to| haxlab"]
for sid, lab, y, taught in SEM:
    if taught:
        lines.append(f"  ist256 -->|was taught in| {sid}")
        lines.append(f"  bryan ---|taught| {sid}")
for p in P:
    lines.append(f"  {p[2]} -->|assigned| {p[0]}")
    for o, w in p[4]: lines.append(f"  {p[0]} -->|{p[5]}| {o}")
    for st in p[6]: lines.append(f"  {st} ---|built| {p[0]}")
lines += ["  kcharlton ---|turned a class project into| ddd", "  winston --o|went on to intern in| haxlab"]
lines += ["", "  %%@ group hub tier=0", "  %%@ group sems tier=1", "  %%@ group projects tier=2", "  %%@ group outcomes tier=3",
          "  %%@ node ist256 portal"]
for sid, lab, y, taught in SEM:
    lines.append(f"  %%@ node {sid} icon=hax:calendar color={era(y) if taught else 'limestoneGray'} motion=pop")
for p in P: lines.append(f"  %%@ node {p[0]} icon=hax:task color={era(sem_year[p[2]])} motion=lift")
for o, w in outs: lines.append(f"  %%@ node {o} portal" + ("" if w == "main" else f"={w}"))
for pid in people: lines.append(f"  %%@ node {pid} portal")
lines += ["  %%@ node ist portal", "  %%@ node haxlab portal"]
open("hax-ist256.mmd", "w").write("\n".join(lines) + "\n")

nodes = {"ist256": {"always": True}}
for sid, lab, y, taught in SEM:
    d = {"year": y, "yearLabel": lab, "kind": "semester"}
    if taught: d["desc"] = f"Bryan taught IST 256 in {lab}."
    pass
    nodes[sid] = d
ev = {}
for p in P:
    d = {"desc": f"Projects developed and implemented as a result of btopro's IST 256 course and SIIP. From {dict((s[0], s[1]) for s in SEM)[p[2]]}.", "links": {"issue": ISS + str(p[3][0])}, "source": L(f"haxtheweb/issues #{p[3][0]}", ISS + str(p[3][0]))}
    if p[7]: d["note"] = p[7]
    nodes[p[0]] = d
    ev[f"{p[2]}>{p[0]}"] = [L(f"Issue #{n}", ISS + str(n)) for n in p[3]]
ev["kcharlton>ddd"] = [L("WINS.md: Students built the design system", WINS + "#students-built-the-design-system")]
ev["winston>haxlab"] = [L("WINS.md: Winston White, student to trainer", WINS + "#winston-white-student-to-trainer")]
ev["ist256>haxlab"] = [L("WORLDVIEW.md: SIIP", "https://github.com/haxtheweb/praw/blob/main/WORLDVIEW.md")]

def S(c, *i): return {"caption": c, "nodes": list(i)}
by = lambda *sids: [p[0] for p in P if p[2] in sids]
tours = [{"id": "semesters", "label": "Semester by semester", "message": "IST 256 from fall 2019 to spring 2026: what each class built, and which projects became parts of HAX.", "scenes": [
  S("IST 256 is taught in IST, and its best students go on to HAX Lab.", "ist256", "ist", "haxlab", "bryan"),
  S("2019–2020: the first semesters, and the date element that became Date card.", "s19f", "s20s", "s20f", *by("s19f", "s20s", "s20f"), "b_date_card", "components"),
  S("2021: question types built in class become blocks: sorting, flash cards, mark the words.", "s21s", "s21f", *by("s21s", "s21f"), "b_sorting_question", "b_flash_card", "b_mark_the_words"),
  S("2022: vocabulary lands in the HAX editor.", "s22s", *by("s22s"), "b_vocab_term"),
  S("2023: citations, drag and drop, link previews and the lecture player.", "s23s", "s23f", *by("s23s", "s23f"), "b_citation_element", "b_matching_question", "b_rpg_character"),
  S("Spring 2024: Winston White's inline audio, play lists, image quotes and galleries.", "s24s", *by("s24s"), "winston", "b_inline_audio", "b_play_list", "b_person_testimonial", "b_image_gallery", "dashboard"),
  S("Fall 2024: site search, the use-cases dashboard and skeletons.", "s24f", *by("s24f"), "haxcms", "skeletons"),
  S("2025: DDD lists, the AI Usage License and portfolio themes.", "s25s", "s25f", *by("s25s", "s25f"), "ddd", "kcharlton", "b_ai_usage_license", "themes"),
  S("Spring 2026: the latest class builds on the gallery.", "s26s", *by("s26s")),
  S("Seven years of classes, feeding the blocks, themes and dashboard people use every day."),
]}]
meta = {"name": "IST 256", "parent": "main", "timelineTier": 1,
        "about": f"Bryan's IST 256 course, {sum(1 for s in SEM if s[3])} semesters from fall 2019 to spring 2026, and {len(P)} class projects from the issue queue with what they became. Semesters are inferred from issue dates.",
        "kindLabels": {"rel": "semesters, projects and outcomes", "contrib": "teaching and student credits", "org": "where it's taught"},
        "links": {"repo": REPO}}
import re as _re
_ids = set(_re.findall(r"^\s+(\w+)[\[\(\{>]", open("hax-ist256.mmd").read(), _re.M))
for _t in tours:
    for _s in _t["scenes"]: _s["nodes"] = [i for i in _s["nodes"] if i in _ids]  # a tour only names tiles this web draws
json.dump({"meta": meta, "nodes": nodes, "evidence": ev, "tours": tours}, open("hax-ist256.json", "w"), indent=1, ensure_ascii=False)
json.dump(icons, open("icons.json", "w"))
print(len(SEM), "semesters;", len(P), "projects;", len(outs), "outcomes")
