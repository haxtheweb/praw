"""Four sub-webs from their sources:
  release    <- webcomponents scripts/ubiquity-push.sh (step headers and destinations) + each repo's .github/workflows
  community  <- haxtheweb/issues GOVERNANCE.md, SUPPORT.md, SUSTAINABILITY.md, CONTRIBUTING.md, labels and issue templates; per-repo community files
  psu        <- the ecosystem web's Penn State units and their edges, plus the hax.psu.edu snapshot in the sites web
  haxlab     <- hax-lab README (past contributors, by term)
Details in the matching .json."""
import json, re, subprocess, collections
GH = "https://github.com/haxtheweb"
ISS = GH + "/issues/blob/main/"
def S(c, *i): return {"caption": c, "nodes": list(i)}
def slug(s): return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")
MAIN = open("hax-ecosystem.mmd").read()
MAIN_IDS = set(re.findall(r"^\s+(\w+)[\[\(\{>]", MAIN, re.M))
MJ = json.load(open("hax-ecosystem.json"))["nodes"]
def gh(path):
    try: return json.loads(subprocess.run(["gh", "api", path], capture_output=True, text=True, timeout=60).stdout)
    except Exception: return None
def write(name, lines, meta, nodes, tours):
    open(f"hax-{name}.mmd", "w").write("\n".join(lines) + "\n")
    json.dump({"meta": meta, "nodes": nodes, "evidence": {}, "tours": tours}, open(f"hax-{name}.json", "w"), indent=1, ensure_ascii=False)
def portal_lines(ids): return [f"  %%@ node {i} portal" for i in ids]

# ================= Release and build =================
sh = open("ext/ubiquity-push.sh").read()
STEPS = [("r0", "1. Publish packages", "lerna publish sends every changed element to npm under @haxtheweb. It is the one step done by hand, because it needs a person to confirm versions.", ["npm", "components"]),
         ("r1", "2. Ubiquity build", "yarn run ubiquity: one build of every element into build/, plus wc-registry.json (tag to file) and wc-registry-graph.json (what loads what), so any site can lazy-load any element.", ["components"]),
         ("r2", "3. Agent skills index", "PRAW is the source for HAX agent skills. The index is built and snapshotted into the site boilerplate and both deployment roots as .well-known/agent-skills.", ["praw", "agents"]),
         ("r3", "4. Normalize every project", "The same build/, build.js, build-haxcms.js, wc-registry.json and version are copied into HAX11ty, haxcms-php, haxcms-nodejs, haxsite, HAXiam, the Penn State CDN, the waxam mirror and ELMS:LN.", ["hax11ty", "php", "nodejs", "haxiam", "rl_psucdn", "elmsln"]),
         ("r4", "5. Sync themes.json", "The theme list from haxcms-elements is copied into both backends' coreConfig, so both offer the same themes.", ["themes", "php", "nodejs"]),
         ("r5", "6. Outline designer contract", "Real outline-designer output is recaptured and replayed through both backends' saveOutline in a contract test, so the designer and the backends never drift.", ["outline", "php", "nodejs"]),
         ("r6", "7. Node.js is the boilerplate", "haxcms-nodejs's site boilerplate and coreConfig are mirrored into haxcms-php, and the CLI gets wc-registry.json to validate tags.", ["nodejs", "php", "cli"]),
         ("r7", "8. Rebuild the gallery", "The component gallery is rebuilt for CDN publishing; pull requests get a Vercel preview of it.", ["components"]),
         ("r8", "9. Version and tag everything", "Every repo commits, takes the same version with commit-and-tag-version and pushes with its tag.", ["github"])]
WF = {}
for r in ["webcomponents", "create", "haxcms-nodejs", "haxcms-php"]:
    x = gh(f"repos/haxtheweb/{r}/contents/.github/workflows")
    WF[r] = [f["name"] for f in x] if isinstance(x, list) else []
AFTER = [("rl_notes", "Release notes and checksums", "On every version tag, GitHub Actions builds a source archive and SHA256SUMS and publishes a GitHub release with generated notes.", [w for r in WF for w in WF[r] if re.match(r"release", w)]),
         ("rl_docker", "Container images", "On every version tag, the Node.js and PHP platforms are published to the GitHub Container Registry (ghcr.io/haxtheweb/...), with latest following the newest release.", [w for r in WF for w in WF[r] if "docker" in w]),
         ("rl_sbom", "Software bill of materials", "Every release gets an SBOM of its dependencies.", [w for r in WF for w in WF[r] if "sbom" in w]),
         ("rl_npm", "npm releases", "The CLI and haxcms-nodejs publish to npm from npm run release: build, tag with commit-and-tag-version, push, publish.", []),
         ("rl_vercel", "Gallery previews", "Every webcomponents pull request deploys the component gallery to a Vercel preview, where changes are reviewed.", [])]
GATES = [("rl_build", "Nightly build and tests", "build.yml on webcomponents runs on every push to master and nightly: install, lint, stylelint, Prettier, the full test suite in Playwright, then the gallery."),
         ("rl_parity", "Backend parity", "backend-parity.yml runs on both backends so the two stay identical."),
         ("rl_codeql", "CodeQL and scorecards", "CodeQL, dependency audits, license checks and OpenSSF Scorecard run on every repo.")]
lines = ["%% Release and build sub-web: how a HAX release goes out, generated from webcomponents scripts/ubiquity-push.sh and each repo's GitHub workflows.",
         "flowchart TB", "  %%@ layout rings=0,250,500,760 sizes=92,64,58,52",
         '  subgraph hub ["Release and build"]', '    ubiquity["ubiquity"]', "  end", '  subgraph stepsg ["The release, in order"]']
for i, lab, d, t in STEPS: lines.append(f'    {i}>"{lab}"]')
lines += ["  end", '  subgraph afterg ["When a tag lands"]']
for i, lab, d, w in AFTER + [(a, b, c, []) for a, b, c in GATES]: lines.append(f'    {i}["{lab}"]')
lines += ["  end", '  subgraph dest ["Where it goes"]']
dests = list(dict.fromkeys(x for s in STEPS for x in s[3]))
for x in dests: lines.append(f'    {x}["{x}"]' if x != "rl_psucdn" else '    rl_psucdn[("Penn State CDN")]')
lines += ["  end", "", f"  ubiquity -->|starts with| {STEPS[0][0]}"]
for a, b in zip(STEPS, STEPS[1:]): lines.append(f"  {a[0]} -->|then| {b[0]}")
for i, lab, d, t in STEPS:
    for x in t: lines.append(f"  {i} -.->|updates| {x}")
lines += ["  r8 -->|triggers| rl_notes", "  r8 -->|triggers| rl_docker", "  r8 -->|triggers| rl_sbom", "  r8 -->|triggers| rl_npm", "  r7 -->|previews on| rl_vercel",
          "  rl_build -->|guards| r1", "  rl_parity -->|guards| r6", "  rl_codeql -->|guards| r8", "  rl_npm -.->|publishes| cli", "  rl_docker -.->|ships| php", "  rl_docker -.->|ships| nodejs", "  rl_psucdn -->|serves| haxpsu" if "haxpsu" in MAIN_IDS else "",
          "", "  %%@ group hub tier=0", "  %%@ group stepsg tier=1", "  %%@ group afterg tier=2", "  %%@ group dest tier=3", "  %%@ node ubiquity portal"]
if "haxpsu" in MAIN_IDS: lines.insert(lines.index('  subgraph dest ["Where it goes"]') + 1, '    haxpsu["haxpsu"]'); dests.append("haxpsu")
for i, *_ in STEPS: lines.append(f"  %%@ node {i} mono={i[1:]} color=creekTeal motion=nudge")
for i, *_ in AFTER: lines.append(f"  %%@ node {i} icon=icons:cloud-upload color=forestGreen motion=lift")
for i, *_ in GATES: lines.append(f"  %%@ node {i} icon=icons:verified-user color=beaverBlue motion=pulse")
PW = {"outline": "haxcms"}  # tiles the main web doesn't draw, but another web does
for x in dests: lines.append("  %%@ node rl_psucdn icon=icons:dns color=nittanyNavy motion=lift" if x == "rl_psucdn" else f"  %%@ node {x} portal" + (f"={PW[x]}" if x in PW else ""))
lines = [l for l in lines if l != ""] if False else lines
UB = GH + "/webcomponents/blob/master/scripts/ubiquity-push.sh"
nodes = {"ubiquity": {"always": True}, "rl_psucdn": {"desc": "Penn State's copy of the HAX build, at both cdn/ and haxcms/ paths, which hax.psu.edu sites load from.", "source": {"label": "ubiquity-push.sh", "url": UB}}}
for i, lab, d, t in STEPS: nodes[i] = {"desc": d, "kind": "step", "source": {"label": "ubiquity-push.sh", "url": UB}}
for i, lab, d, w in AFTER: nodes[i] = {"desc": d + (f" Workflows: {', '.join(sorted(set(w)))}." if w else ""), "kind": "after"}
for i, lab, d in GATES: nodes[i] = {"desc": d, "kind": "gate", "links": {"code": GH + "/webcomponents/tree/master/.github/workflows"}}
tours = [{"id": "release", "label": "How a release goes out", "kind": "story", "message": "One script carries a HAX release from npm to every platform, then a tag sets off the automation.",
          "scenes": [S(f"{lab}. {d}", i, *t) for i, lab, d, t in STEPS] + [S("When the tag lands: release notes, checksums, containers, SBOMs and npm.", *[a[0] for a in AFTER]), S("What guards it: nightly builds, backend parity, CodeQL and scorecards.", *[g[0] for g in GATES]), S("The whole release.")]}]
write("release", lines, {"name": "Release and build", "parent": "main", "noTimeline": True, "sectionLabels": {"step": "steps", "after": "after the tag", "gate": "checks"},
      "about": "How a HAX release goes out, in order: generated from the ubiquity-push script in webcomponents and the GitHub workflows in each repo. One build of every element is copied into every platform, both backends are kept identical, and a shared version tag sets off release notes, containers and SBOMs.",
      "kindLabels": {"rel": "the order of steps and what triggers what", "schema": "what each step updates"}}, nodes, tours)

# ================= Community and governance =================
labels = [l["name"] for l in (gh("repos/haxtheweb/issues/labels?per_page=100") or [])]
tpls = [f["name"] for f in (gh("repos/haxtheweb/issues/contents/.github/ISSUE_TEMPLATE") or []) if f["name"] != "config.yml"]
FILES = {}
for r in ["webcomponents", "haxcms-nodejs", "haxcms-php", "create", "praw", "issues"]:
    x = gh(f"repos/haxtheweb/{r}/contents")
    FILES[r] = [f["name"] for f in x] if isinstance(x, list) else []
DOCS = [("cg_governance", "GOVERNANCE.md", "Roles, how decisions are made, the maintainer lifecycle, succession, conflicts of interest and a yearly governance review."),
        ("cg_contributing", "CONTRIBUTING.md", "How to contribute: an issue first, then a pull request that says which issue it fixes."),
        ("cg_conduct", "CODE_OF_CONDUCT.md", "The code of conduct every space follows."),
        ("cg_security", "SECURITY.md", "How to report a vulnerability privately, and the incident response that follows (INCIDENT_RESPONSE.md)."),
        ("cg_support", "SUPPORT.md", "Where to get help: Discord, the documentation, then the unified issue queue."),
        ("cg_sustain", "SUSTAINABILITY.md", "How HAX is resourced: Penn State employment and student interns, hosting partnerships, grants and community contributions; what free support covers."),
        ("cg_trademark", "TRADEMARK.md", "How the HAX name and marks may be used."),
        ("cg_agents", "AGENTS.md", "Rules for AI agents and people working in each repo: lint, precheck and the conventions the code keeps."),
        ("cg_cla", "CLA", "Apache-2.0 plus a contributor license agreement; CLA Assistant runs on every repo and signatures live in haxtheweb/cla.")]
ROLES = [("billrose", "Backup owner: the second name in every CODEOWNERS file; takes over merges and releases if the primary maintainer is away."),
         ("bryan", "Primary maintainer: holds the * slot in every CODEOWNERS file, merges, cuts releases and breaks ties."),
         ("psu", "Institutional steward: employs the primary maintainer, holds the copyright and keeps the infrastructure going.")]
STEPSD = [("cg_d1", "1. Open an issue", "Anyone can open an issue in the unified queue; it is the single source of truth for the whole ecosystem."),
          ("cg_d2", "2. Discuss and plan", "Discussion happens on the issue. Larger work gets a written plan as a comment, labeled Plan Created."),
          ("cg_d3", "3. Pull request", "Work lands as a pull request that says which issue it fixes, through CLA, CodeQL and review."),
          ("cg_d4", "4. Record it", "Breaking changes are called out on the issue and in release notes; decisions made on Discord or in person are written back to an issue.")]
CH = [("cg_discord", "Discord", "Real-time help and discussion.", "https://discord.gg/aCGxmRHEJP"), ("docs", None, None, None), ("haxcamp", None, None, None), ("issues", None, None, None)]
KEYLABELS = [l for l in labels if l in ("Good first issue", "Help Wanted", "Plan Created", "Community", "Documentation", "Pillars / Values", "Research / Ideas", "Design Challenge")]
lines = ["%% Community and governance sub-web: how HAX is run, generated from the governance files in haxtheweb/issues, its labels and issue templates, and each repo's community files.",
         "flowchart TB", "  %%@ layout rings=0,240,480,740 sizes=92,64,56,50",
         '  subgraph hub ["Community and governance"]', '    community["community"]', "  end", '  subgraph rolesg ["Roles"]']
for i, d in ROLES: lines.append(f'    {i}["{i}"]')
lines += ['    cg_contributors(("Contributors"))', "  end", '  subgraph decide ["How a decision is made"]']
for i, lab, d in STEPSD: lines.append(f'    {i}>"{lab}"]')
lines += ["  end", '  subgraph docsg ["The rules, in writing"]']
for i, lab, d in DOCS: lines.append(f'    {i}[("{lab}")]')
lines += ["  end", '  subgraph chan ["Where people meet"]', '    cg_discord["Discord"]', '    learnhax["learnhax"]', '    haxcamp["haxcamp"]', '    issues["issues"]']
for t in tpls: lines.append(f'    cg_t_{slug(t)}["{t.replace(".yml", "").replace("_", " ")}"]')
for l in KEYLABELS: lines.append(f'    cg_l_{slug(l)}["{l}"]')
lines += ["  end", ""]
for i, d in ROLES: lines.append(f"  community -->|is run by| {i}")
lines += ["  community -->|is open to| cg_contributors", "  bryan -->|names a backup in CODEOWNERS| billrose", "  psu -->|stewards| community", "  community -->|decides in| cg_d1"]
for a, b in zip(STEPSD, STEPSD[1:]): lines.append(f"  {a[0]} -->|then| {b[0]}")
lines += ["  cg_d1 -.->|happens in| issues", "  cg_d2 -.->|is labeled| cg_l_plan_created" if "Plan Created" in KEYLABELS else "", "  cg_d3 -.->|requires| cg_cla", "  cg_d3 -.->|follows| cg_contributing", "  cg_d3 -.->|follows| cg_agents"]
for i, lab, d in DOCS: lines.append(f"  cg_governance -->|links to| {i}" if i != "cg_governance" else "  community -->|is written down in| cg_governance")
lines += ["  cg_support -->|points to| cg_discord", "  cg_support -->|points to| learnhax", "  cg_support -->|points to| issues", "  cg_contributors -->|meet at| haxcamp", "  cg_contributors -->|follow| cg_conduct"]
for t in tpls: lines.append(f"  issues -->|offers| cg_t_{slug(t)}")
for l in KEYLABELS: lines.append(f"  issues -->|is sorted by| cg_l_{slug(l)}")
lines += ["", "  %%@ group hub tier=0", "  %%@ group rolesg tier=1", "  %%@ group decide tier=1", "  %%@ group docsg tier=2", "  %%@ group chan tier=3",
          "  %%@ node community portal", "  %%@ node cg_contributors icon=social:people color=skyBlue motion=pulse"]
lines += portal_lines([i for i, _ in ROLES] + ["learnhax", "haxcamp", "issues"])
for i, *_ in STEPSD: lines.append(f"  %%@ node {i} mono={i[-1]} color=futureLime motion=nudge")
for i, *_ in DOCS: lines.append(f"  %%@ node {i} icon={'icons:gavel' if i in ('cg_governance', 'cg_trademark', 'cg_cla') else 'icons:verified-user' if i == 'cg_security' else 'icons:book'} color=beaverBlue motion=nudge")
lines.append("  %%@ node cg_discord mono=DISC color=wonderPurple motion=wiggle")
for t in tpls: lines.append(f"  %%@ node cg_t_{slug(t)} icon={'icons:bug-report' if 'bug' in t else 'icons:lightbulb-outline'} color=futureLime motion=nudge")
for l in KEYLABELS: lines.append(f"  %%@ node cg_l_{slug(l)} icon=icons:bookmark color=limestoneGray motion=nudge")
lines = [l for l in lines if l]
hasf = lambda f: [r for r, fs in FILES.items() if any(x.startswith(f.split(".")[0]) for x in fs)]
nodes = {"community": {"always": True}, "cg_contributors": {"desc": "Anyone who files issues, submits pull requests, reviews, writes docs or translations, or helps on Discord. Maintainership is earned through contribution, not granted by affiliation; six months inactive and a maintainer is thanked and can return the same way.", "source": {"label": "GOVERNANCE.md", "url": ISS + "GOVERNANCE.md"}},
         "cg_discord": {"desc": "The HAXTheWeb Discord: real-time help and discussion. Decisions made here are written back to an issue.", "links": {"site": "https://discord.gg/aCGxmRHEJP"}, "source": {"label": "SUPPORT.md", "url": ISS + "SUPPORT.md"}}}
for i, d in ROLES: nodes[i] = {"note": d}
for i, lab, d in STEPSD: nodes[i] = {"desc": d, "kind": "step", "source": {"label": "GOVERNANCE.md", "url": ISS + "GOVERNANCE.md"}}
for i, lab, d in DOCS:
    f = lab if lab.endswith(".md") else "CLA.md"
    rs = hasf(f)
    nodes[i] = {"desc": d + (f" In {', '.join(rs)}." if rs else ""), "kind": "doc", "links": ({"doc": ISS + lab} if "issues" in rs and lab.endswith(".md") else {"doc": GH + "/webcomponents/blob/master/CLA.md"} if i == "cg_cla" else {})}
for t in tpls: nodes[f"cg_t_{slug(t)}"] = {"desc": f"Issue template: {t.replace('.yml', '').replace('_', ' ')}.", "links": {"code": GH + "/issues/blob/main/.github/ISSUE_TEMPLATE/" + t}, "kind": "channel"}
for l in KEYLABELS: nodes[f"cg_l_{slug(l)}"] = {"desc": f"Issue label \"{l}\" in the unified queue ({len(labels)} labels in all).", "links": {"issues": f"{GH}/issues/issues?q=label%3A%22{l.replace(' ', '+').replace('/', '%2F')}%22"}, "kind": "channel"}
tours = [{"id": "community", "label": "How HAX is run", "message": "Roles, how a decision is made, the rules in writing, and where people meet.", "scenes": [
    S("A primary maintainer, a backup owner, Penn State as steward, and contributors.", "bryan", "billrose", "psu", "cg_contributors"),
    *[S(f"{lab}. {d}", i) for i, lab, d in STEPSD],
    S("The rules, in writing, in every repo.", *[d[0] for d in DOCS]),
    S("Where people meet: Discord, Learn HAX, HAX Camp and the issue queue.", "cg_discord", "learnhax", "haxcamp", "issues", *[f"cg_t_{slug(t)}" for t in tpls]),
    S("All of it.")]}]
write("community", lines, {"name": "Community and governance", "parent": "main", "noTimeline": True, "sectionLabels": {"step": "how a decision is made", "doc": "the rules", "channel": "templates and labels"},
      "about": "How HAX is run, generated from the governance files in the unified issue queue: roles and succession, the four steps every decision goes through, the documents every repo keeps, and the places people meet.",
      "kindLabels": {"rel": "roles, steps and documents", "schema": "what a step relies on"}}, nodes, tours)

# ================= Penn State =================
E = re.findall(r"^\s+(\w+) ([-=.o>]+)\|([^|]+)\| (\w+)", MAIN, re.M)
UNITS = ["aa", "ist", "hhd", "eberly", "libraries", "innovationhub", "ccso", "uxdc", "haxlab"]
PEOPLE = ["bryan", "billrose", "keithbailey", "mcollins", "fusco", "jfrank", "blake", "agearhart"]
WORK = ["haxpsu", "haxiam", "elmsln", "ist256", "haxcamp", "course", "dept", "hax11ty", "security", "design", "g_hhd", "g_fusco", "g_frank", "wins", "sites_hub"]
keep = set(["psu"] + UNITS + PEOPLE + WORK)
lines = ["%% Penn State sub-web: the colleges, units, people and services where HAX is built and used. Generated from the ecosystem web's edges among Penn State tiles, plus the hax.psu.edu snapshot.",
         "flowchart TB", "  %%@ layout rings=0,240,480,740 sizes=92,64,56,52",
         '  subgraph hub ["Penn State"]', '    psu["psu"]', "  end", '  subgraph units ["Colleges and units"]']
for u in UNITS: lines.append(f'    {u}["{u}"]')
lines += ["  end", '  subgraph work ["What runs and happens here"]']
for w in WORK: lines.append(f'    {w}["{w}"]' if w != "sites_hub" else '    sites_hub["302 sites on hax.psu.edu"]')
lines += ["  end", '  subgraph ppl ["People"]']
for p in PEOPLE: lines.append(f'    {p}(("{p}"))')
lines += ["  end", ""]
seen = set()
for a, arrow, lab, b in E:
    if a in keep and b in keep and (a, b) not in seen:
        seen.add((a, b)); lines.append(f"  {a} {arrow}|{lab}| {b}")
for u in UNITS:
    if not any(a == u or b == u for a, b in seen): lines.append(f"  {u} -->|is part of| psu")
lines += ["  haxpsu -->|hosts| sites_hub", "  aa -->|publishes courses on| sites_hub", "  ist -->|publishes courses on| sites_hub", "  eberly -->|publishes courses on| sites_hub", "",
          "  %%@ group hub tier=0", "  %%@ group units tier=1", "  %%@ group work tier=2", "  %%@ group ppl tier=3"]
lines += portal_lines(["psu"] + UNITS + PEOPLE + [w for w in WORK if w != "sites_hub"])
lines.append("  %%@ node sites_hub icon=hax:site-map color=nittanyNavy motion=pop")
sitesmeta = json.load(open("hax-sites.json"))["meta"].get("about", "")
nodes = {"psu": {"always": True}, "sites_hub": {"desc": sitesmeta + " Open the hax.psu.edu web for every college and course.", "kind": "work"}}
tours = [{"id": "psu", "label": "HAX at Penn State", "message": "Where HAX is built and used at Penn State, from the ecosystem web's own connections.", "scenes": [
    S("Penn State backs HAX: it employs the maintainer and keeps the infrastructure going.", "psu", "bryan"),
    S("The colleges and units that use and build it.", *UNITS),
    S("hax.psu.edu and HAXiam run sites for courses and departments.", "haxpsu", "haxiam", "sites_hub", "course", "dept"),
    S("Where it came from and where it is taught: ELMS:LN, IST 256, HAX Camp and the HAX Lab.", "elmsln", "ist256", "haxcamp", "haxlab"),
    S("The people.", *PEOPLE), S("All of HAX at Penn State.")]}]
write("psu", lines, {"name": "Penn State", "parent": "main", "noTimeline": True,
      "about": "Where HAX is built and used at Penn State: the colleges and units, what runs there (hax.psu.edu, HAXiam, IST 256, HAX Camp, grants) and the people, generated from the ecosystem web's own connections among Penn State tiles.",
      "kindLabels": {"rel": "how the units and work connect", "org": "units and memberships", "contrib": "people", "pillar": "pillars", "schema": "contracts"}}, nodes, tours)

# ================= HAX Lab people over time =================
md = open("ext/haxlab-readme.md").read().split("## HAX Lab past contributors", 1)[1]
NAME2ID = {}
for k in MAIN_IDS:
    m = re.search(r"^\s+" + k + r"[\[\(\{>]+\"?([^\"\]\)]*)", MAIN, re.M)
    if m: NAME2ID[m.group(1).strip().lower()] = k
NAME2ID.update({"ccso": "ccso", "hanna kern": "hanna", "hannah kern": "hanna", "shiju \"tom\" varughese": "tom", "jonathan skeete": "jskeete", "james kane iv": "jimmykane"})
entries = []; cur = None
for ln in md.splitlines():
    m = re.match(r"^- (.+?) - (.+?) - (.+)$", ln)
    if m:
        names = re.findall(r"\[([^\]]+)\]\(", m.group(1)) or [m.group(1)]
        proj = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", m.group(2)); when = m.group(3).strip()
        cur = {"names": names, "proj": proj, "when": when, "crew": []}; entries.append(cur)
    m2 = re.match(r"^\s+- \[([^\]]+)\]\([^)]+\) - (.+)$", ln)
    if m2 and cur: cur["crew"].append((m2.group(1), m2.group(2)))
TERM = {"Spring": 1, "Summer": 2, "Fall": 3}
def yr(w): return int(re.search(r"(20\d\d)", w).group(1))
TOUCH = [("theme", "themes"), ("portfolio", "portfolio"), ("pentest", "security"), ("ddd", "ddd"), ("ai ", "ai"), ("camp", "haxcamp"), ("xapi", "xapi"), ("cli", "cli"), ("journey", "dashboard"), ("site creation", "dashboard"), ("vocab", "components"), ("bootstrap", "themes"), ("media dashboard", "dashboard"), ("ux study", "design"), ("multimedia", "presentations"), ("elms", "elmsln"), ("auth", "haxiam"), ("qa elements", "testing")]
years = sorted({yr(e["when"]) for e in entries})
lines = ["%% HAX Lab people over time: everyone the HAX Lab README credits, what they built and when. Generated from haxtheweb/hax-lab README.md.",
         "flowchart TB", "  %%@ layout rings=0,220,470,740 sizes=92,58,56,48",
         '  subgraph hub ["HAX Lab"]', '    haxlab["haxlab"]', "  end", '  subgraph yrs ["Years"]']
for y in years: lines.append(f'    hl_y{y}(["{y}"])')
lines += ["  end", '  subgraph projs ["What they built"]']
for i, e in enumerate(entries): lines.append(f'    hl_p{i}["{e["proj"][:60]}"]')
lines += ["  end", '  subgraph ppl ["People and what it touched"]']
pids = []; touched = []
for e in entries:
    for n in e["names"] + [c[0] for c in e["crew"]]:
        pid = NAME2ID.get(n.lower())
        if pid and pid not in pids: pids.append(pid)
    for k, t in TOUCH:
        if k in (e["proj"] + " ").lower() and t in MAIN_IDS and t not in touched: touched.append(t)
for p in pids + touched: lines.append(f'    {p}["{p}"]')
lines += ["  end", ""]
for y in years: lines.append(f"  haxlab -->|worked in| hl_y{y}")
for i, e in enumerate(entries):
    lines.append(f"  hl_y{yr(e['when'])} -->|built| hl_p{i}")
    for n in e["names"] + [c[0] for c in e["crew"]]:
        pid = NAME2ID.get(n.lower())
        if pid: lines.append(f"  {pid} ---|worked on| hl_p{i}")
    for k, t in TOUCH:
        if k in (e["proj"] + " ").lower() and t in MAIN_IDS: lines.append(f"  hl_p{i} -.->|added to| {t}")
lines += ["", "  %%@ group hub tier=0", "  %%@ group yrs tier=1", "  %%@ group projs tier=2", "  %%@ group ppl tier=3", "  %%@ node haxlab portal"]
for y in years: lines.append(f"  %%@ node hl_y{y} mono={str(y)[2:]} color=keystoneYellow motion=pop")
for i, e in enumerate(entries): lines.append(f"  %%@ node hl_p{i} icon=hax:hax2022 color=inventOrange motion=wiggle")
lines += portal_lines(pids + touched)
nodes = {"haxlab": {"always": True}}
for y in years: nodes[f"hl_y{y}"] = {"desc": f"{sum(1 for e in entries if yr(e['when']) == y)} HAX Lab projects in {y}.", "year": y, "kind": "year"}
for i, e in enumerate(entries):
    who = ", ".join(e["names"]) + ("" if not e["crew"] else ": " + "; ".join(f"{a} ({r})" for a, r in e["crew"]))
    nodes[f"hl_p{i}"] = {"desc": f"{e['proj']}. {who}. {e['when']}.", "year": yr(e["when"]), "yearLabel": e["when"], "kind": "project", "source": {"label": "hax-lab README", "url": GH + "/hax-lab#hax-lab-past-contributors"}}
tours = [{"id": "haxlab", "label": "Who built what, and when", "message": f"{len(entries)} HAX Lab projects from {years[0]} to {years[-1]}, from the hax-lab README.",
          "scenes": [S(f"{y}: " + "; ".join(e["proj"] for e in entries if yr(e["when"]) == y) + ".", f"hl_y{y}", *[f"hl_p{i}" for i, e in enumerate(entries) if yr(e["when"]) == y],
                       *[NAME2ID[n.lower()] for e in entries if yr(e["when"]) == y for n in e["names"] + [c[0] for c in e["crew"]] if n.lower() in NAME2ID]) for y in years] + [S("Everyone, every year.")]}]
write("haxlab", lines, {"name": "HAX Lab", "parent": "main", "timelineTier": 2, "sectionLabels": {"project": "projects", "year": "years"},
      "about": f"Everyone the HAX Lab README credits, what they built and when: {len(entries)} projects and {len(pids)} people from {years[0]} to {years[-1]}. Choose Over time to watch the lab grow, term by term.",
      "kindLabels": {"rel": "years and projects", "contrib": "who worked on it", "schema": "what it added to"}}, nodes, tours)
print("release", len(STEPS), "steps;", "community", len(DOCS), "docs", len(tpls), "templates;", "psu", len(seen), "edges;", "haxlab", len(entries), "projects", len(pids), "people", "missing:", [n for e in entries for n in e["names"] + [c[0] for c in e["crew"]] if n.lower() not in NAME2ID])
