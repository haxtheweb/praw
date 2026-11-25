"""Rules and guarantees sub-web: every rule HAX keeps, where it's written down, what it serves and what enforces it.

Rules come from PRAW's RULES.md (each entry with a Rule ID) and from the bold-key rules in each repo's AGENTS.md
(Code Style & Standards, Security Considerations), plus the rules the HAX Scheduled Background Jobs Plan proposes that
aren't written down yet (build/data/rule-links.json, shown as planned). Each rule links up to the pillars it serves,
across to the parts it touches, and down to the Quality control checks that enforce it. A rule nothing enforces shows
as a gap: that list is the backlog of what to automate next. A rule marked "automation": "guidance" in rule-links.json
is guidance by design (how an agent or person works, which no check could decide): it shows as guidance, not as a gap,
so "not automatable" and "not automated yet" stay apart. Details in hax-rules.json."""
import json, re, subprocess, base64, collections
GH = "https://github.com/haxtheweb"
PRAW = GH + "/praw/blob/main/"
def S(c, *i): return {"caption": c, "nodes": list(i)}
def slug(s): return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")
def anchor(h): return re.sub(r"\s", "-", re.sub(r"[^\w\s-]", "", h.lower()).strip())
LINKS = json.load(open("ext/rule-links.json"))
MAIN = set(re.findall(r"^\s+(\w+)[\[\(\{>]", open("hax-ecosystem.mmd").read(), re.M))
QUALITY = set(re.findall(r"^\s+(\w+)[\[\(\{>]", open("hax-quality.mmd").read(), re.M))
PILLARS = ["accessible", "efficient", "extensible", "open", "agnostic", "remixable", "sustainable"]

# ---------- RULES.md ----------
rules = []; sec = None; cur = None
for ln in open("prawrepo/RULES.md").read().splitlines():
    m = re.match(r"^## (.+)", ln)
    if m: sec = re.sub(r"^[^\w]+", "", m.group(1)).strip(); cur = None; continue
    m = re.match(r"^### (.+)", ln)
    if m: cur = {"title": m.group(1).strip(), "group": sec, "rid": None, "scope": "", "text": "", "src": "RULES.md"}; rules.append(cur); continue
    if cur:
        for key, field in (("Rule ID", "rid"), ("Scope", "scope"), ("Content", "text")):
            m = re.match(r"^- \*\*" + key + r"\*\*:\s*`?(.*?)`?\s*$", ln)
            if m: cur[field] = m.group(1)
rules = [r for r in rules if r["rid"]]
for r in rules:
    r["id"] = "r_" + slug(r["rid"]); r["key"] = r["rid"]; r["url"] = PRAW + "RULES.md#" + anchor(r["title"]); r["repos"] = ["praw"]

# ---------- AGENTS.md in each repo ----------
REPOS = {"webcomponents": "components", "haxcms-nodejs": "nodejs", "haxcms-php": "php", "create": "cli"}
agents = collections.OrderedDict()
for repo, nid in REPOS.items():
    info = json.loads(subprocess.run(["gh", "api", f"repos/haxtheweb/{repo}/contents/AGENTS.md"], capture_output=True, text=True).stdout or "{}")
    if "content" not in info: continue
    top = None
    for ln in base64.b64decode(info["content"]).decode().splitlines():
        m = re.match(r"^## (.+)", ln)
        if m: top = m.group(1).strip(); continue
        b = re.match(r"^- \*\*([^*]+)\*\*:?\s*(.*)", ln)
        if b and top in ("Code Style & Standards", "Security Considerations"):
            key = b.group(1).strip().rstrip(":")
            if "agents:" + key in LINKS["aliases"]:
                rid = LINKS["aliases"]["agents:" + key]
                for r in rules:
                    if r["rid"].startswith(rid) and nid not in r["repos"]: r["repos"].append(nid); r.setdefault("also", []).append(f"{repo} AGENTS.md")
                continue
            a = agents.setdefault(key, {"title": key, "group": "AGENTS.md: " + ("security" if top.startswith("Security") else "code style"), "text": b.group(2).strip(), "src": "AGENTS.md",
                                        "key": "agents:" + key, "id": "ra_" + slug(key), "repos": [], "url": info["html_url"]})
            if nid not in a["repos"]: a["repos"].append(nid)
# ---------- proposed rules (not written down yet) ----------
cands = [{"title": c["title"], "group": "Proposed: " + c["group"], "text": c["text"], "src": "plan", "key": "candidate:" + c["id"], "id": "rc_" + c["id"], "repos": [], "written": c.get("written")} for c in LINKS["candidates"]]
for c in cands:  # a candidate a RULES.md rule now covers points at that rule
    if c["written"]:
        hit = [r for r in rules if r["rid"].startswith(c["written"])]
        if len(hit) != 1: raise SystemExit(f"candidate {c['key']}: written {c['written']} matches {len(hit)} RULES.md rules")
        c["written"] = hit[0]; c["url"] = hit[0]["url"]
ALL = rules + list(agents.values()) + cands
def links_for(key):  # RULES.md Rule IDs may be given in full or by their first characters
    if key in LINKS["rules"]: return LINKS["rules"][key]
    hit = [k for k in LINKS["rules"] if ":" not in k and key.startswith(k)]
    if len(hit) > 1: raise SystemExit(f"rule-links.json: {', '.join(hit)} all name Rule ID {key}; merge them into one entry")
    return LINKS["rules"][hit[0]] if hit else {}
for r in ALL:
    L = links_for(r["key"])
    r["enf"] = [q for q in L.get("enforced_by", []) if q in QUALITY]
    r["lost"] = [q for q in L.get("enforced_by", []) if q not in QUALITY]
    r["pillars"] = [p for p in L.get("pillars", []) if p in MAIN]
    r["touches"] = [t for t in L.get("touches", []) if t in MAIN and t not in PILLARS]
    r["how"] = L.get("how", "")
    r["guidance"] = L.get("automation") == "guidance" and not r["enf"]  # a check wins over the mark
groups = list(dict.fromkeys(r["group"] for r in ALL))
checks = sorted({q for r in ALL for q in r["enf"]})
parts = sorted({t for r in ALL for t in r["touches"]} | {r for x in ALL for r in x["repos"] if r != "praw"} - set(PILLARS))
guidance = [r for r in ALL if r["guidance"]]
gaps = [r for r in ALL if not r["enf"] and not r["guidance"]]

lines = ["%% Rules and guarantees sub-web, generated by build_rules.py from praw RULES.md, each repo's AGENTS.md and build/data/rule-links.json.",
         "%% Checks are portals to hax-quality.mmd; pillars and parts to hax-ecosystem.mmd. Details in hax-rules.json.",
         "flowchart TB", "  %%@ layout rings=0,310,620,860,1070 sizes=92,56,32,36,46",
         '  subgraph hub ["Rules and guarantees"]', '    rules["rules"]', "  end", '  subgraph groupsg ["Where rules come from"]']
for g in groups: lines.append(f'    rg_{slug(g)}["{g}"]')
lines += ["  end", '  subgraph rulesmd ["RULES.md"]']
for r in rules: lines.append(f'    {r["id"]}["{r["title"].replace(chr(34), "")}"]')
lines += ["  end", '  subgraph more ["AGENTS.md and proposed"]']
for r in list(agents.values()) + cands: lines.append(f'    {r["id"]}["{r["title"].replace(chr(34), "")}"]')
lines += ["  end", '  subgraph outer ["Checks, pillars and parts"]']
for x in checks + PILLARS + parts: lines.append(f'    {x}["{x}"]')
lines += ["  end", ""]
for g in groups: lines.append(f"  rules -->|collects| rg_{slug(g)}")
for r in ALL:
    lines.append(f"  rg_{slug(r['group'])} -->|includes| {r['id']}")
    for q in r["enf"]: lines.append(f"  {q} -->|enforces| {r['id']}")
    for p in r["pillars"]: lines.append(f"  {r['id']} ==>|serves| {p}")
    for t in r["touches"]: lines.append(f"  {r['id']} -.->|applies to| {t}")
    for t in r["repos"]:
        if t != "praw" and t not in r["touches"]: lines.append(f"  {r['id']} -.->|is written in| {t}")
lines += ["", "  %%@ group hub tier=0", "  %%@ group groupsg tier=1", "  %%@ group rulesmd tier=2", "  %%@ group more tier=3", "  %%@ group outer tier=4", "  %%@ node rules portal"]
for g in groups: lines.append(f"  %%@ node rg_{slug(g)} icon=icons:gavel color={'athertonViolet' if g.startswith('Proposed') else 'slateGray'} motion=pop")
for r in ALL: lines.append(f"  %%@ node {r['id']} icon={'icons:verified-user' if r['enf'] else 'icons:book' if r['guidance'] else 'icons:gavel'} color={'forestGreen' if r['enf'] else 'skyBlue' if r['guidance'] else 'limestoneGray'} motion=nudge")
for q in checks: lines.append(f"  %%@ node {q} portal=quality")
for x in PILLARS + parts: lines.append(f"  %%@ node {x} portal")
open("hax-rules.mmd", "w").write("\n".join(lines) + "\n")

QL = json.load(open("hax-quality.json"))["nodes"]
def qlabel(q): return re.search(r'^\s+' + q + r'\["([^"]+)"', open("hax-quality.mmd").read(), re.M).group(1)
nodes = {"rules": {"always": True}}
for g in groups:
    rs = [r for r in ALL if r["group"] == g]
    nodes[f"rg_{slug(g)}"] = {"desc": f"{g}: {len(rs)} rule{'s' if len(rs) != 1 else ''}, {sum(1 for r in rs if r['enf'])} enforced by a check.", "kind": "group"}
for r in ALL:
    how = f" {r['how']}" if r["how"] else ""
    enf = f"Enforced by {', '.join(qlabel(q) for q in r['enf'])}.{how}" if r["enf"] else f"Guidance by design: no check enforces this, and none is planned.{how}" if r["guidance"] else f"Nothing enforces this yet.{'' if r['lost'] else how}"
    plan = f"Proposed in the HAX Scheduled Background Jobs Plan; now written into PRAW RULES.md as part of \"{r['written']['title']}\"." if r.get("written") else "Proposed in the HAX Scheduled Background Jobs Plan; not written into RULES.md or AGENTS.md yet."
    where = {"RULES.md": f"In PRAW RULES.md (scope: {r.get('scope') or 'none'}).", "AGENTS.md": f"In the AGENTS.md of {', '.join(sorted(r['repos']))}.", "plan": plan}[r["src"]]
    if r.get("also"): where += f" Also in {', '.join(r['also'])}."
    # a proposal is planned only while nothing backs it: a check that enforces it or a RULES.md rule that covers it means it landed
    planned = r["src"] == "plan" and not r["enf"] and not r.get("written")
    d = {"desc": f"{r['text']} {where} {enf}".strip(), "kind": "proposed" if planned else ("enforced" if r["enf"] else "guidance" if r["guidance"] else "gap")}
    if planned: d["status"] = "planned"
    elif r["guidance"]: d["status"] = "guidance"
    elif not r["enf"]: d["status"] = "gap"
    if r.get("url"): d["links"] = {"rule": r["url"]}
    if r["lost"]: d["note"] = f"A check that enforced this is gone from Quality control: {', '.join(r['lost'])}."
    nodes[r["id"]] = d
enforced = [r for r in ALL if r["enf"]]
tours = [{"id": "rules", "label": "Rules and what guarantees them", "kind": "story", "message": f"{len(ALL)} rules: {len(enforced)} enforced by a check, {len(guidance)} guidance by design, {len(gaps)} not yet.", "scenes": [
    S("Rules come from PRAW's RULES.md, each repo's AGENTS.md, and the plan's proposals.", *[f"rg_{slug(g)}" for g in groups]),
    S(f"{len(enforced)} rules have a check that enforces them.", *[r["id"] for r in enforced], *checks),
    S("Rules serve the pillars.", *PILLARS, *[r["id"] for r in ALL if r["pillars"]]),
    S(f"{len(guidance)} rules are guidance by design: how agents and people work, which no check could decide.", *[r["id"] for r in guidance]),
    S(f"{len(gaps)} rules nothing enforces yet: the backlog of what to automate next.", *[r["id"] for r in gaps if r["src"] != "plan" or r.get("written")]),
    S("Proposed rules still waiting: not written down and not enforced yet.", *[r["id"] for r in cands if not r["enf"] and not r.get("written")]),
    S("All of it.")]}]
meta = {"name": "Rules and guarantees", "parent": "main", "noTimeline": True, "sectionLabels": {"group": "where rules come from", "enforced": "enforced", "guidance": "guidance by design", "gap": "nothing enforces it yet", "proposed": "proposed"},
        "about": f"Every rule HAX keeps, generated from PRAW's RULES.md ({len(rules)} rules) and each repo's AGENTS.md ({len(agents)}), plus {len(cands)} the plan proposes. Each links up to the pillars it serves, across to the parts it touches and down to the Quality control checks that enforce it. {len(enforced)} are enforced; {len(guidance)} are guidance by design, which no check could decide; {len(gaps)} are gaps, the backlog of what to automate next.",
        "kindLabels": {"rel": "where a rule comes from and what enforces it", "pillar": "pillars a rule serves", "schema": "parts a rule applies to"},
        "links": {"RULES.md": PRAW + "RULES.md", "rule links": PRAW + "ecosystem/build/data/rule-links.json"}}
json.dump({"meta": meta, "nodes": nodes, "evidence": {}, "tours": tours}, open("hax-rules.json", "w"), indent=1, ensure_ascii=False)
print(len(rules), "RULES.md;", len(agents), "AGENTS.md;", len(cands), "proposed;", len(enforced), "enforced;", len(guidance), "guidance;", len(gaps), "gaps;", "lost:", [r["id"] for r in ALL if r["lost"]])
