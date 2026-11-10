"""Agent skills index sub-web: the agentskills.io discovery index that tells an agent which HAX skills a place offers.

Generated from the files themselves: PRAW's canonical .well-known/agent-skills/index.json and agent-skills-sets.json,
and every copy of the index in haxcms-nodejs and haxcms-php (deployment roots and the per-site boilerplate). Fields are
read from the index entries, sets from agent-skills-sets.json, copies by walking the clones. Each copy is compared with
PRAW skill by skill (digest and set membership) and its files with its own digests; a copy that differs is marked stale, and drift.py reports it.
Details in hax-skillsindex.json."""
import json, os, re, hashlib
GH = "https://github.com/haxtheweb"
PRAW = GH + "/praw/blob/main/"
def S(c, *i): return {"caption": c, "nodes": list(i)}
def slug(s): return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")
MAIN = set(re.findall(r"^\s+(\w+)[\[\(\{>]", open("hax-ecosystem.mmd").read(), re.M))

CANON = json.load(open("prawrepo/.well-known/agent-skills/index.json"))
SETS = json.load(open("prawrepo/.well-known/agent-skills/agent-skills-sets.json"))
FULL = json.load(open("prawrepo/skills/index.json"))  # the copy with files[] for the managed-file copy step
by_name = {s["name"]: s for s in CANON["skills"]}
def members(name):
    want = SETS[name]["skills"]
    return sorted(by_name) if want == "*" or want == ["*"] else sorted(want)

# ---------- fields, read from the entries ----------
ABOUT = {"$schema": "The discovery spec the index follows; HAX uses agentskills.io discovery v0.2.0.",
         "skills": "The list of skills this place offers.",
         "name": "The skill's name: lowercase letters, digits and hyphens, at most 64 characters.",
         "type": "How the skill is packaged; every HAX skill is skill-md (a SKILL.md with YAML frontmatter).",
         "description": "What the skill does and when to use it, from the SKILL.md frontmatter (at most 1,024 characters).",
         "url": "Where the SKILL.md is, relative to the index, so the same entry works from PRAW, a deployment root or a site.",
         "digest": "The sha256 of the SKILL.md, so a client can tell whether its copy is current.",
         "files": "Not in the spec: the skill's other files (references and the like) with their own digests, so the HAXcms copy step can copy and verify each one. Spec clients ignore it."}
top = [k for k in CANON if k != "skills"] + ["skills"]
entry = list(dict.fromkeys(k for idx in (CANON, FULL) for s in idx["skills"] for k in s))
fields = top + entry
def fid(k): return "f_" + slug(k.replace("$", "dollar_"))

# ---------- copies, found by walking the clones ----------
REPOS = {"haxcms-nodejs": ("nodejs", GH + "/haxcms-nodejs/blob/main/"), "haxcms-php": ("php", GH + "/haxcms-php/blob/master/")}
copies = []
for repo, (owner, base) in REPOS.items():
    for dp, dn, fn in os.walk(repo):
        dn[:] = [d for d in dn if d not in ("node_modules", ".git")]
        if dp.endswith(os.path.join(".well-known", "agent-skills")) and "index.json" in fn:
            rel = os.path.relpath(dp, repo)
            tier = "site" if "boilerplate" in rel else "system"
            copies.append({"id": slug(f"{owner}_{tier}"), "repo": repo, "owner": owner, "tier": tier, "rel": rel,
                           "url": base + rel + "/index.json", "data": json.load(open(os.path.join(dp, "index.json")))})
copies.sort(key=lambda c: c["id"])
for c in copies:
    have = {s["name"]: s for s in c["data"]["skills"]}
    want = members(c["tier"])
    c["missing"] = [n for n in want if n not in have]
    c["extra"] = [n for n in have if n not in want]
    c["old"] = [n for n in want if n in have and n in by_name and have[n].get("digest") != by_name[n].get("digest")]
    # bytes that no longer match the copy's own digest (a formatter or hand edit): agents that check digests refuse them
    c["edited"] = [s["name"] for s in c["data"]["skills"] if os.path.exists(os.path.join(c["repo"], c["rel"], s["url"])) and
                   "sha256:" + hashlib.sha256(open(os.path.join(c["repo"], c["rel"], s["url"]), "rb").read()).hexdigest() != s.get("digest")]
    c["stale"] = list(dict.fromkeys(c["missing"] + c["extra"] + c["old"] + c["edited"]))
stale = [c for c in copies if c["stale"]]

SETIDS = {"all": "set_all", **{k: "set_" + slug(k) for k in SETS}}
READERS = [  # id, label, owner portal, what it does, verb, which ids, link
    ("w_build", "build-agent-skills-index.js", "praw", "Scans PRAW's skills folder, reads each SKILL.md's frontmatter, computes the digests and writes the index.", "writes", ["praw_index", "praw_full"], PRAW + "scripts/build-agent-skills-index.js"),
    ("w_snapshot", "snapshot-agent-skills.js", "praw", "Copies one set (site or system) into a .well-known/agent-skills folder for the ubiquity build: a filtered index plus every file, each checked against its digest.", "copies a set into", [c["id"] for c in copies], PRAW + "scripts/snapshot-agent-skills.js"),
    ("w_php", "HAXCMSSite.php", "php", "Copies the site set into each new site as a managed file, links it from llms.txt and the page head.", "links and copies", ["php_site"], GH + "/haxcms-php/blob/master/system/backend/php/lib/HAXCMSSite.php"),
    ("w_node", "app.js", "nodejs", "Serves the system set from the deployment root and advertises it in a Link header.", "serves", ["nodejs_system"], GH + "/haxcms-nodejs/blob/main/src/app.js"),
    ("w_cli", "site.js", "cli", "Lists the index among a site's managed files, so the CLI keeps it when it rebuilds a site.", "keeps", ["nodejs_site", "php_site"], GH + "/create/blob/main/src/lib/programs/site.js"),
]
PORTALS = [p for p in ["praw", "nodejs", "php", "cli", "traveler"] if p in MAIN]

lines = ["%% Agent skills index sub-web, generated by build_skillsindex.py from PRAW's .well-known/agent-skills and every copy in haxcms-nodejs and haxcms-php.",
         "%% Portals: ids from hax-ecosystem.mmd (traveler opens the skills web). Details in hax-skillsindex.json.",
         "flowchart TB", "  %%@ layout rings=0,230,470,720,960 sizes=92,52,58,54,46",
         '  subgraph hub ["Agent skills index"]', '    skillsindex[("skillsindex")]', "  end", '  subgraph fieldsg ["Fields"]']
for k in fields: lines.append(f'    {fid(k)}["{k}"]')
lines += ["  end", '  subgraph setsg ["Skill sets"]']
lines.append(f'    set_all["all of PRAW ({len(by_name)})"]')
for k in SETS: lines.append(f'    {SETIDS[k]}["{k} ({len(members(k))})"]')
lines += ["  end", '  subgraph copiesg ["Files that conform"]', '    praw_index[("praw .well-known index")]', '    praw_full[("praw skills/index.json")]']
for c in copies: lines.append(f'    {c["id"]}[("{c["repo"]} {c["tier"]}")]')
lines += ["  end", '  subgraph rwg ["Readers, writers and owners"]']
for r in READERS: lines.append(f'    {r[0]}["{r[1]}"]')
for p in PORTALS: lines.append(f'    {p}["{p}"]')
lines += ["  end", ""]
for k in fields: lines.append(f"  skillsindex -->|{'has' if k in top else 'gives each skill a'}| {fid(k)}")
lines.append("  skillsindex -->|is cut into| set_all")
for k in SETS: lines.append(f"  set_all -->|narrows to| {SETIDS[k]}")
lines += ["  praw_index -.->|conforms to| skillsindex", "  praw_full -.->|conforms to| skillsindex", "  praw_index -->|lists| set_all", "  praw_full -->|lists| set_all"]
for c in copies:
    lines.append(f"  {c['id']} -.->|conforms to| skillsindex")
    lines.append(f"  {c['id']} -->|lists| {SETIDS[c['tier']]}")
for r in READERS:
    for t in r[5]: lines.append(f"  {r[0]} -->|{r[4]}| {t}")
    if r[2] in PORTALS: lines.append(f"  {r[2]} --o|owns| {r[0]}")
if "traveler" in PORTALS: lines.append("  traveler -->|offers its skills through| set_all")
lines += ["", "  %%@ group hub tier=0", "  %%@ group fieldsg tier=1", "  %%@ group setsg tier=2", "  %%@ group copiesg tier=3", "  %%@ group rwg tier=4",
          "  %%@ node skillsindex icon=hax:code-json color=creekTeal motion=pulse"]
for k in fields: lines.append(f"  %%@ node {fid(k)} icon=hax:code-json color={'limestoneGray' if k == 'files' else 'creekTeal'} motion=nudge")
for s in ["set_all"] + [SETIDS[k] for k in SETS]: lines.append(f"  %%@ node {s} icon=icons:folder-open color=original87Pink motion=pop")
for c in ["praw_index", "praw_full"] + [c["id"] for c in copies]:
    lines.append(f"  %%@ node {c} icon=hax:code-json color={'roarGolden' if any(x['id'] == c and x['stale'] for x in copies) else 'forestGreen'} motion=nudge")
for r in READERS: lines.append(f"  %%@ node {r[0]} icon=hax:code-json color=slateGray motion=nudge")
for p in PORTALS: lines.append(f"  %%@ node {p} portal")
open("hax-skillsindex.mmd", "w").write("\n".join(lines) + "\n")

nodes = {"skillsindex": {"always": True, "desc": f"The agentskills.io discovery index ({CANON.get('$schema', '').split('/discovery/')[-1].split('/')[0] or 'v0.2.0'}): one JSON file that tells an agent which skills a place offers and where to read each one. PRAW keeps the canonical index of all {len(by_name)} skills; HAXcms deployment roots carry the system set and every site carries the site set.",
                         "links": {"spec": "https://github.com/cloudflare/agent-skills-discovery-rfc", "index": PRAW + ".well-known/agent-skills/index.json"}}}
for k in fields:
    n = sum(1 for s in FULL["skills"] if k in s) if k in entry else None
    nodes[fid(k)] = {"desc": ABOUT.get(k, "Found in the index entries; not described here yet.") + (f" On {n} of {len(FULL['skills'])} skills." if n is not None else ""), "kind": "field"}
    if k == "files": nodes[fid(k)]["status"] = "in-progress"; nodes[fid(k)]["note"] = "A HAX extension, not part of the discovery spec."
nodes["set_all"] = {"desc": f"Every skill in PRAW: {len(by_name)}. Served from PRAW itself; developer and ecosystem tooling stays here only.", "kind": "set",
                    "links": {"skills": PRAW + "skills"}}
for k, v in SETS.items():
    nodes[SETIDS[k]] = {"desc": f"{v.get('description', '')} {len(members(k))} skills: {', '.join(members(k))}.".strip(), "kind": "set",
                        "links": {"sets": PRAW + ".well-known/agent-skills/agent-skills-sets.json"}}
nodes["praw_index"] = {"desc": f"The canonical index: {len(CANON['skills'])} skills, written by build-agent-skills-index.js.", "kind": "copy", "links": {"file": PRAW + ".well-known/agent-skills/index.json"}}
nodes["praw_full"] = {"desc": f"The same skills with files[] filled in ({sum(1 for s in FULL['skills'] if s.get('files'))} skills have extra files), read by the copy step.", "kind": "copy", "links": {"file": PRAW + "skills/index.json"}}
for c in copies:
    d = {"desc": f"{c['repo']}, {c['rel']}: the {c['tier']} set, {len(c['data']['skills'])} skills.", "kind": "copy", "links": {"file": c["url"]}}
    if c["stale"]:
        parts = []
        if c["old"]: parts.append(f"older than PRAW: {', '.join(c['old'])}")
        if c["missing"]: parts.append(f"missing: {', '.join(c['missing'])}")
        if c["extra"]: parts.append(f"not in the {c['tier']} set: {', '.join(c['extra'])}")
        if c["edited"]: parts.append(f"changed since the snapshot, so they no longer match their digests: {', '.join(c['edited'])}")
        d.update(status="in-progress", note="Out of step with PRAW (" + "; ".join(parts) + "). The next ubiquity build's snapshot step refreshes it.", stale=c["stale"])
    else: d["note"] = "In step with PRAW: every skill's digest matches."
    nodes[c["id"]] = d
for r in READERS: nodes[r[0]] = {"desc": r[3], "kind": "tool", "links": {"code": r[6]}}

tours = [{"id": "skillsindex", "label": "How an agent finds HAX skills", "kind": "story",
          "message": f"{len(by_name)} skills in PRAW, cut into {len(SETS)} sets and copied to {len(copies)} places; {len(stale)} cop{'y is' if len(stale) == 1 else 'ies are'} out of step.",
          "scenes": [S("The index is one JSON file in .well-known: the spec it follows and a list of skills.", "skillsindex", *[fid(k) for k in top]),
                     S("Each skill entry carries a name, a description, where to read it and a digest.", *[fid(k) for k in entry]),
                     S("PRAW writes the canonical index from its skills folder.", "w_build", "praw_index", "praw_full", "set_all", *[p for p in ["praw"] if p in PORTALS]),
                     S("The sets decide what ships where: a deployment root gets the system set, every site the smaller site set.", "set_all", *[SETIDS[k] for k in SETS], "w_snapshot"),
                     S("The copies in each backend, and what serves or keeps them.", *[c["id"] for c in copies], "w_php", "w_node", "w_cli", *[p for p in ["nodejs", "php", "cli"] if p in PORTALS]),
                     S("Copies out of step with PRAW." if stale else "Every copy is in step with PRAW.", *([c["id"] for c in stale] or [c["id"] for c in copies])),
                     S("The whole index.")]}]
meta = {"name": "Agent skills index", "parent": "main", "noTimeline": True,
        "sectionLabels": {"field": "fields", "set": "skill sets", "copy": "files that conform", "tool": "readers and writers"},
        "about": f"The agentskills.io discovery index HAX publishes, generated from PRAW's .well-known/agent-skills and every copy in the two backends: {len(fields)} fields, {len(SETS) + 1} sets, {len(copies) + 2} files. Each copy is checked skill by skill against PRAW; {len(stale)} {'is' if len(stale) == 1 else 'are'} out of step. The skills themselves are in the Future Traveler skills web.",
        "kindLabels": {"rel": "fields, sets and copies", "schema": "conforms to"},
        "links": {"spec": "https://github.com/cloudflare/agent-skills-discovery-rfc", "sets": PRAW + ".well-known/agent-skills/agent-skills-sets.json"}}
json.dump({"meta": meta, "nodes": nodes, "evidence": {}, "tours": tours}, open("hax-skillsindex.json", "w"), indent=1, ensure_ascii=False)
print(len(fields), "fields;", len(SETS) + 1, "sets;", len(copies), "copies;", "stale:", {c["id"]: len(c["stale"]) for c in stale})
