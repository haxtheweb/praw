import json, re

skills = json.load(open("ext/skills.json"))
GH = {"praw": "https://github.com/haxtheweb/praw/blob/main/", "create": "https://github.com/haxtheweb/create/blob/main/"}
def L(a, b): return {"label": a, "url": b}

GROUPS = {
 "use": ("Using HAX", "hax:site-map", "discoveryCoral"),
 "dev": ("Building HAX", "hax:code-json", "beaverBlue"),
 "id": ("Instructional design", "hax:lesson", "opportunityGreen"),
 "audit": ("Audits and quality", "icons:verified-user", "inventOrange"),
 "media": ("Media and import", "hax:multimedia", "skyBlue"),
 "community": ("Community and admin", "icons:gavel", "original87Pink"),
}
def group(n):
    if re.search(r"ubd|blooms|udl|chunking|multimedia-principles|feedback-design|practice-and-retrieval|proficiency|reflection|instructional|siip-course|reading-notes|lrs-rater", n): return "id"
    if re.search(r"a11y-audit|oerschema|heosat|pattern-library-audit", n): return "audit"
    if re.search(r"audio-program|youtube-vtt|openstax|importer", n): return "media"
    if re.search(r"issue-|rule-management|release-prep", n): return "community"
    if re.search(r"webcomponent|backend-dev|testing|design-system|element-demo|i18n|mental-model|rpg-character|claudehax", n): return "dev"
    return "use"

# skill -> parts it works on (by name, then by description keywords)
RULES = [
 (r"\bhax\b$|onboarding|site-ops|site-building|site-structure|managed-files|tutorial-site|content-authoring", ["haxcms", "cli"]),
 (r"theme-builder", ["themes"]), (r"content-authoring|element-demo", ["editor", "components"]),
 (r"webcomponent|element-demo|rpg-character|pattern-library", ["components"]), (r"design-system|pattern-library", ["ddd"]),
 (r"backend-dev", ["nodejs", "php", "openapi"]), (r"importer|openstax|audio-program", ["textbook"]),
 (r"i18n", ["languages"]), (r"testing", ["testing"]), (r"release-prep", ["ubiquity"]),
 (r"issue-", ["issues"]), (r"rule-management|mental-model", ["praw"]),
 (r"a11y|udl", ["accessible"]), (r"oerschema", ["oerschema"]), (r"lrs-rater|instructional-events", ["xapi"]),
 (r"ubd|blooms|chunking|multimedia-principles|feedback|practice|proficiency|reflection|instructional|siip|reading-notes|heosat", ["course"]),
 (r"tutorial-site", ["learnhax"]), (r"rpg-character", ["traveler"]),
]
def parts(n):
    out = []
    for rx, ps in RULES:
        if re.search(rx, n):
            for p in ps:
                if p not in out: out.append(p)
    return out or ["haxcms"]

def sid(n): return "s_" + re.sub(r"[^a-z0-9]+", "_", n.lower()).strip("_")
seen = {}
for s in skills:  # praw keeps both hax-openstax2hax and a plugin openstax2hax: keep one per name
    key = s["name"].replace("hax-openstax2hax", "openstax2hax")
    if key in seen: continue
    seen[key] = s
items = sorted(seen.values(), key=lambda s: (list(GROUPS).index(group(s["name"])), s["name"]))
for i, s in enumerate(items): s["tier"] = 2 if i % 2 == 0 else 3
portals = []
for s in items:
    for p in parts(s["name"]):
        if p not in portals: portals.append(p)
SHAPE = {"accessible": ('{{"', '"}}'), "oerschema": ('[("', '")]'), "xapi": ('[("', '")]'), "openapi": ('[("', '")]'),
         "course": ('(["', '"])'), "textbook": ('(["', '"])'), "learnhax": ('(["', '"])')}

lines = ["%% Future Traveler skills sub-web: the agent skills in PRAW and create, grouped by what they help with.",
         "%% Portals: ids from hax-ecosystem.mmd. Details in hax-skills.json.",
         "flowchart TB", "  %%@ layout rings=0,250,540,780,1000 sizes=92,56,42,42,46",
         '  subgraph hub ["HAX Future Traveler"]', '    traveler(("traveler"))', "  end", '  subgraph groups ["Skill groups"]']
for g, (lab, ic, col) in GROUPS.items(): lines.append(f'    g_{g}["{lab}"]')
lines += ["  end", '  subgraph sa ["Skills"]']
for s in items:
    if s["tier"] == 2: lines.append(f'    {sid(s["name"])}["{s["name"]}"]')
lines += ["  end", '  subgraph sb ["Skills"]']
for s in items:
    if s["tier"] == 3: lines.append(f'    {sid(s["name"])}["{s["name"]}"]')
lines += ["  end", '  subgraph parts ["Where skills live and what they work on"]', '    praw["praw"]', '    cli["cli"]']
for p in portals:
    if p in ("praw", "cli", "traveler"): continue
    a, b = SHAPE.get(p, ('["', '"]')); lines.append(f"    {p}{a}{p}{b}")
lines += ["  end", ""]
for g in GROUPS: lines.append(f"  traveler -->|uses| g_{g}")
for s in items:
    i = sid(s["name"]); lines.append(f"  g_{group(s['name'])} -->|includes| {i}")
    lines.append(f"  {i} --o|lives in| {'praw' if s['repo'] == 'praw' else 'cli'}")
    for p in parts(s["name"]):
        if p == "traveler": continue
        lines.append(f"  {i} -->|works on| {p}")
lines += ["", "  %%@ group hub tier=0", "  %%@ group groups tier=1", "  %%@ group sa tier=2", "  %%@ group sb tier=3", "  %%@ group parts tier=4", "  %%@ node traveler portal"]
for g, (lab, ic, col) in GROUPS.items(): lines.append(f"  %%@ node g_{g} icon={ic} color={col} motion=pop" + (" web=idskills" if g == "id" else ""))  # instructional design opens its own web (build_idskills.py)
for s in items: lines.append(f"  %%@ node {sid(s['name'])} icon=hax:file-ai color={GROUPS[group(s['name'])][2]} motion=pulse")
for p in ["praw", "cli"] + [p for p in portals if p not in ("praw", "cli", "traveler")]: lines.append(f"  %%@ node {p} portal")
open("hax-skills.mmd", "w").write("\n".join(lines) + "\n")

nodes = {"traveler": {"always": True}}
for g, (lab, ic, col) in GROUPS.items(): nodes["g_" + g] = {"desc": f"{sum(1 for s in items if group(s['name']) == g)} skills."}
for s in items:
    url = GH[s["repo"]] + s["path"]
    d = s["desc"]
    if len(d) > 420: d = d[:417].rsplit(" ", 1)[0] + "…"
    nodes[sid(s["name"])] = {"desc": d, "links": {"repo": url}, "source": L(f"{s['repo']}: {s['path']}", url), "kind": "skill"}
def S(c, *i): return {"caption": c, "nodes": list(i)}
by = lambda g: [sid(s["name"]) for s in items if group(s["name"]) == g]
tours = [{"id": "skills", "label": "What the Future Traveler can do", "message": f"The {len(items)} agent skills that let your AI companion work in HAX the way a person would, from PRAW and the HAX CLI.", "scenes": [
    S("The Future Traveler works through skills.", "traveler"),
    S("Six kinds of skills.", *["g_" + g for g in GROUPS]),
    S("Using HAX: build sites, author content, make themes.", *by("use"), "haxcms", "cli", "themes", "editor"),
    S("Building HAX: components, DDD, backends, tests.", *by("dev"), "components", "ddd", "nodejs", "php", "testing"),
    S("Instructional design: UbD, UDL, Bloom's and more.", *by("id"), "course", "xapi"),
    S("Audits keep it accessible and open.", *by("audit"), "accessible", "oerschema"),
    S("Media and import bring outside content in.", *by("media"), "textbook"),
    S("Community skills keep the issue queue and PRAW running.", *by("community"), "issues", "praw", "ubiquity"),
    S("Every skill is something people can do too, and check."),
]}]
meta = {"name": "Future Traveler skills", "parent": "main", "noTimeline": True,
        "about": f"{len(items)} agent skills ({sum(1 for s in items if s['repo'] == 'praw')} in PRAW, {sum(1 for s in items if s['repo'] == 'create')} in the HAX CLI's create repo), grouped by what they help with and linked to the parts of HAX they work on.",
        "kindLabels": {"rel": "groups and what each skill works on", "org": "where each skill lives"}}
json.dump({"meta": meta, "nodes": nodes, "evidence": {}, "tours": tours}, open("hax-skills.json", "w"), indent=1, ensure_ascii=False)
print(len(items), "skills", {g: len(by(g)) for g in GROUPS}, "portals", portals)
