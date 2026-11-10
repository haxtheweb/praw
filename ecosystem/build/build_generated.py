"""Generated sub-webs: OpenAPI endpoints, HAX MCP tools, xAPI verbs, HAX CLI commands.
Each is built from the source that defines it (specs, haxcms-mcp, xapi-vocabulary.json, create), so rerunning this after a release refreshes them."""
import json, re, os, collections, yaml
GH = "https://github.com/haxtheweb"
NODE = GH + "/haxcms-nodejs/blob/main/"
PHP = GH + "/haxcms-php/blob/master/"
def L(a, b): return {"label": a, "url": b}
def S(c, *i): return {"caption": c, "nodes": list(i)}
def slug(s): return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")
def write(name, lines, meta, nodes, tours, ev=None):
    open(f"hax-{name}.mmd", "w").write("\n".join(lines) + "\n")
    json.dump({"meta": meta, "nodes": nodes, "evidence": ev or {}, "tours": tours}, open(f"hax-{name}.json", "w"), indent=1, ensure_ascii=False)

# ---------------- OpenAPI endpoints ----------------
SPECS = {"site": "haxcms-nodejs/src/openapi/site-spec.yaml", "system": "haxcms-nodejs/src/openapi/system-spec.yaml"}
TAGDESC = {"discovery": "Where the API describes itself: capabilities, the OpenAPI document, the api-catalog.", "site": "The site itself: manifest, summary, settings and info.",
           "items": "Pages as items in the outline: list, create, update, move, delete.", "content": "Page content as HTML, markdown and blocks.", "files": "Uploads: list, upload, rename, delete, transform.",
           "reports": "Reports computed from the site.", "entities": "Entity lookups.", "schemas": "Schema documents the site exposes.", "tags": "Tags across pages.", "search": "Full-text search.",
           "custom-elements": "The custom elements a site knows about.", "blocks": "Block definitions the editor can place.", "regions": "Theme regions.", "themes": "Themes and theme options.",
           "analytics": "Analytics the site records.", "views": "Saved views of the outline.", "session": "Login, logout, tokens and who you are.", "lifecycle": "Create, clone, delete, archive and list sites.",
           "settings": "Site settings written through the system: info, appearance, SEO, author, features, git, allowed blocks.", "actions": "Operations on a site: import, export, convert, rebuild, publish."}
ops = {}; tags = collections.OrderedDict()
for spec, path in SPECS.items():
    y = yaml.safe_load(open(path))
    for p, methods in y["paths"].items():
        for m, o in methods.items():
            if not isinstance(o, dict) or "operationId" not in o: continue
            tag = (o.get("tags") or ["untagged"])[0]; tid = f"tag_{slug(tag)}"
            tags.setdefault(tid, {"label": tag, "spec": spec, "ops": []})
            oid = "op_" + slug(o["operationId"])
            ops[oid] = {"label": f"{m.upper()} {p}", "method": m.upper(), "path": p, "summary": o.get("summary") or "", "desc": (o.get("description") or o.get("summary") or "").strip(), "tag": tid, "spec": spec, "opid": o["operationId"]}
            tags[tid]["ops"].append(oid)
lines = ["%% OpenAPI sub-web: every endpoint HAXcms promises, grouped by tag, generated from site-spec.yaml and system-spec.yaml (identical in haxcms-nodejs and haxcms-php).",
         "%% Portals: ids from hax-ecosystem.mmd. Regenerate with build_generated.py after a release; details in hax-openapi.json.",
         "flowchart TB", "  %%@ layout rings=0,230,470,760 sizes=92,66,58,34",
         '  subgraph hub ["OpenAPI"]', '    openapi[("openapi")]', "  end", '  subgraph specs ["The two spec files"]', '    spec_site[("site-spec.yaml")]', '    spec_system[("system-spec.yaml")]', "  end",
         '  subgraph tagsg ["Areas (tags)"]']
for tid, t in tags.items(): lines.append(f'    {tid}["{t["label"]}"]')
lines += ["  end", '  subgraph opsg ["Operations"]']
for oid, o in ops.items(): lines.append(f'    {oid}["{o["label"]}"]')
lines += ["  end", '  subgraph who ["Who implements and calls it"]', '    php["php"]', '    nodejs["nodejs"]', '    mcp["mcp"]', '    cli["cli"]', "  end", "",
          "  openapi -.->|is written as| spec_site", "  openapi -.->|is written as| spec_system"]
for tid, t in tags.items(): lines.append(f"  spec_{t['spec']} -->|groups| {tid}")
for oid, o in ops.items(): lines.append(f"  {o['tag']} -->|offers| {oid}")
lines += ["  php -.->|implements| openapi", "  nodejs -.->|implements| openapi", "  mcp -.->|calls| openapi", "  cli -.->|calls| openapi", "",
          "  %%@ group hub tier=0", "  %%@ group specs tier=1", "  %%@ group tagsg tier=2", "  %%@ group opsg tier=3", "  %%@ group who tier=1",
          "  %%@ node openapi portal", "  %%@ node spec_site icon=hax:code-json color=forestGreen motion=nudge", "  %%@ node spec_system icon=hax:code-json color=forestGreen motion=nudge"]
for tid, t in tags.items(): lines.append(f"  %%@ node {tid} icon=hax:code-json color={'creekTeal' if t['spec']=='site' else 'beaverBlue'} motion=pop")
METHOD_COL = {"GET": "skyBlue", "POST": "opportunityGreen", "PUT": "roarGolden", "PATCH": "roarGolden", "DELETE": "original87Pink"}
for oid, o in ops.items(): lines.append(f"  %%@ node {oid} mono={o['method'][:5]} color={METHOD_COL.get(o['method'],'slateGray')} motion=nudge")
for p in ["php", "nodejs", "mcp", "cli"]: lines.append(f"  %%@ node {p} portal")
nodes = {"openapi": {"always": True},
         "spec_site": {"desc": f"{sum(1 for o in ops.values() if o['spec']=='site')} operations on one site: pages, content, files, themes, search, reports.", "links": {"nodejs": NODE + "src/openapi/site-spec.yaml", "php": PHP + "system/backend/php/lib/siteRoutes/openapi/site-spec.yaml"}},
         "spec_system": {"desc": f"{sum(1 for o in ops.values() if o['spec']=='system')} operations on the system: sessions, site lifecycle, settings, actions.", "links": {"nodejs": NODE + "src/openapi/system-spec.yaml", "php": PHP + "system/backend/php/lib/systemRoutes/openapi/system-spec.yaml"}}}
for tid, t in tags.items(): nodes[tid] = {"desc": f"{TAGDESC.get(t['label'], t['label'])} {len(t['ops'])} operations in the {t['spec']} spec.", "kind": "tag"}
for oid, o in ops.items(): nodes[oid] = {"desc": o["desc"] or o["label"], "note": f"operationId {o['opid']}", "kind": "operation"}
tours = [{"id": "openapi", "label": "Walk the API", "message": f"{len(ops)} operations across {len(tags)} areas, generated from the two spec files both backends keep identical.", "scenes": [
    S("HAXcms is built on one OpenAPI contract.", "openapi", "php", "nodejs", "mcp", "cli"),
    S("Two spec files: one for a site, one for the system.", "spec_site", "spec_system"),
    S("The site spec: pages, content, files, themes, search, reports.", *[t for t, v in tags.items() if v["spec"] == "site"]),
    S("The system spec: sessions, lifecycle, settings and actions.", *[t for t, v in tags.items() if v["spec"] == "system"]),
    S(f"Every one of the {len(ops)} operations. Select any for its summary."),
]}]
meta = {"name": "OpenAPI endpoints", "parent": "main", "noTimeline": True, "sectionLabels": {"tag": "areas", "operation": "operations"},
        "about": f"Every endpoint HAXcms promises: {len(ops)} operations in {len(tags)} areas, generated from site-spec.yaml and system-spec.yaml. Both backends implement them; the MCP and the CLI call them. Tiles are colored by HTTP method.",
        "kindLabels": {"rel": "spec to area to operation", "schema": "who implements or calls the contract"}}
write("openapi", lines, meta, nodes, tours)
print("openapi:", len(ops), "ops,", len(tags), "tags")

# ---------------- HAX MCP tools ----------------
T = json.load(open("ext/mcp_tools.json"))
MODDESC = {"auth": "Sign in and sessions", "sites": "Sites", "pages": "Pages", "content": "Page content and blocks", "blocks_typed": "Typed block tools, one per HAX element", "outline": "Outline", "files": "Files", "settings": "Settings", "exports": "Exports", "imports": "Imports"}
mods = collections.OrderedDict()
for t, v in T.items(): mods.setdefault(v["module"], []).append(t)
lines = ["%% HAX MCP tools sub-web: every tool the HAXcms MCP server exposes, grouped by module, with the OpenAPI areas each one calls. Generated from haxcms-mcp.",
         "%% Portals: ids from hax-ecosystem.mmd and hax-openapi.mmd. Details in hax-mcptools.json.",
         "flowchart TB", "  %%@ layout rings=0,230,500,800 sizes=92,64,44,52",
         '  subgraph hub ["HAX MCP"]', '    mcp["mcp"]', "  end", '  subgraph modsg ["Tool groups"]']
for m in mods: lines.append(f'    mod_{m}["{MODDESC.get(m, m)}"]')
lines += ["  end", '  subgraph toolsg ["Tools"]']
for t in T: lines.append(f'    t_{t}["{t}"]')
used_tags = sorted({tg for v in T.values() for tg in v["tags"]})
lines += ["  end", '  subgraph api ["OpenAPI areas called"]']
for tg in used_tags: lines.append(f'    tag_{slug(tg)}["{tg}"]')
lines += ["    traveler((\"traveler\"))", "  end", ""]
for m, ts in mods.items():
    lines.append(f"  mcp -->|offers| mod_{m}")
    for t in ts: lines.append(f"  mod_{m} -->|includes| t_{t}")
modtags = {m: sorted({tg for t in ts for tg in T[t]["tags"]}) for m, ts in mods.items()}
for m, tgs in modtags.items():
    for tg in tgs: lines.append(f"  mod_{m} -.->|calls| tag_{slug(tg)}")
lines += ["  traveler -->|works through| mcp", "", "  %%@ group hub tier=0", "  %%@ group modsg tier=1", "  %%@ group toolsg tier=2", "  %%@ group api tier=3", "  %%@ node mcp portal"]
for m in mods: lines.append(f"  %%@ node mod_{m} icon=hax:file-ai color=roarGolden motion=pop")
for t, v in T.items(): lines.append(f"  %%@ node t_{t} mono={''.join(w[0] for w in t.split('_'))[:4].upper()} color={'wonderPurple' if v['module']=='blocks_typed' else 'roarGolden'} motion=nudge")
for tg in used_tags: lines.append(f"  %%@ node tag_{slug(tg)} portal=openapi")
lines.append("  %%@ node traveler portal")
nodes = {"mcp": {"always": True}}
for m, ts in mods.items(): nodes[f"mod_{m}"] = {"desc": f"{MODDESC.get(m, m)}: {len(ts)} tools in tools/{m}.py, calling the {', '.join(modtags[m]) or 'local'} areas of the API.", "links": {"code": GH + f"/haxcms-mcp/blob/main/src/haxcms_mcp/tools/{m}.py"}, "kind": "group"}
for t, v in T.items(): nodes[f"t_{t}"] = {"desc": f"{v['title']}. Calls: {', '.join(v['ops']) or 'no HTTP call traced'}.", "kind": "tool", "note": f"Module {v['module']}"}
tours = [{"id": "mcptools", "label": "What an agent can do", "message": f"{len(T)} tools in {len(mods)} groups, generated from haxcms-mcp, each tied to the OpenAPI areas it calls.", "scenes": [
    S("The Future Traveler reaches HAXcms through the MCP.", "traveler", "mcp"),
    S("Ten groups of tools.", *[f"mod_{m}" for m in mods]),
    S("Sign in, pick a site, create pages.", "mod_auth", "mod_sites", "mod_pages", "t_list_sites", "t_create_page"),
    S("Write content: one typed tool per HAX element, so an agent places the right block.", "mod_content", "mod_blocks_typed"),
    S("Files, settings, outline, exports and imports.", "mod_files", "mod_settings", "mod_outline", "mod_exports", "mod_imports"),
    S("Every tool calls the same OpenAPI areas people use; open OpenAPI to see them.", *[f"tag_{slug(tg)}" for tg in used_tags]),
    S("All the tools."),
]}]
meta = {"name": "HAX MCP tools", "parent": "main", "noTimeline": True, "sectionLabels": {"group": "tool groups", "tool": "tools"},
        "about": f"Every tool the HAXcms MCP server exposes ({len(T)} in {len(mods)} groups), generated from the haxcms-mcp source, with the OpenAPI areas each group calls traced through its services and client.",
        "kindLabels": {"rel": "group to tool", "schema": "OpenAPI areas called"}}
write("mcptools", lines, meta, nodes, tours)
print("mcptools:", len(T), "tools")

# ---------------- xAPI verbs ----------------
X = json.load(open("ext/xapi-vocabulary.json"))
el_ids = set(re.findall(r"^    (b_[a-z0-9_]+)", open("hax-elements.mmd").read(), re.M))
VERBDESC = {"experienced": "The learner opened or saw it. Never required for completion.", "attempted": "The learner started it.", "progressed": "The learner got part way; media and multi-step activities report progress.",
            "completed": "The learner finished it as the element defines done.", "answered": "The learner gave an answer; result carries success and the response.", "interacted": "The learner did something with it that is not an answer."}
verbs = collections.OrderedDict((v, []) for v in ["experienced", "attempted", "progressed", "completed", "answered", "interacted"])
for tag, v in X.items():
    for vb in v["verbs"]: verbs.setdefault(vb, []).append(tag)
lines = ["%% xAPI verbs sub-web: the verbs HAX elements send, and which element sends each, generated from user-action/lib/xapi-vocabulary.json.",
         "%% Portals: ids from hax-ecosystem.mmd and hax-elements.mmd. Details in hax-xapi.json.",
         "flowchart TB", "  %%@ layout rings=0,230,520 sizes=92,66,54",
         '  subgraph hub ["xAPI"]', '    xapi[("xapi")]', "  end", '  subgraph verbsg ["Verbs"]']
for vb in verbs: lines.append(f'    v_{vb}[("{vb}")]')
lines += ["  end", '  subgraph els ["Elements that send them"]']
for tag in X: lines.append(f'    x_{slug(tag)}["{tag}"]')
lines += ["  end", '  subgraph sink ["Where statements go"]', '    insights["insights"]', '    course["course"]', "  end", ""]
for vb in verbs: lines.append(f"  xapi -.->|defines| v_{vb}")
for tag, v in X.items():
    for vb in v["verbs"]: lines.append(f"  x_{slug(tag)} -->|sends| v_{vb}")
lines += ["  xapi -.->|feeds| insights", "  course -->|records learning through| xapi", "", "  %%@ group hub tier=0", "  %%@ group verbsg tier=1", "  %%@ group els tier=2", "  %%@ group sink tier=1", "  %%@ node xapi portal"]
for vb in verbs: lines.append(f"  %%@ node v_{vb} icon=hax:clipboard-pulse color=roarGolden motion=pulse")
for tag, v in X.items():
    bid = "b_" + tag.replace("-", "_")
    lines.append(f"  %%@ node x_{slug(tag)} portal=elements" if bid in el_ids and False else f"  %%@ node x_{slug(tag)} icon=hax:bricks color={'opportunityGreen' if v.get('countsTowardCompletion') else 'slateGray'} motion=nudge")
lines += ["  %%@ node insights portal=haxcms", "  %%@ node course portal"]
nodes = {"xapi": {"always": True}}
for vb, tgs in verbs.items(): nodes[f"v_{vb}"] = {"desc": f"{VERBDESC.get(vb, vb)} Sent by {len(tgs)} elements.", "links": {"verb": f"http://adlnet.gov/expapi/verbs/{vb}"}, "kind": "verb"}
for tag, v in X.items():
    nodes[f"x_{slug(tag)}"] = {"desc": f"Sends {', '.join(v['verbs'])} on {v['event']}. Done means: {v.get('done','')} {'Counts toward completion.' if v.get('countsTowardCompletion') else 'Does not count toward completion.'}",
                               "links": {"source": GH + "/webcomponents/blob/master/" + v["source"]}, "kind": "element", "note": f"object type {v['objectType'].split('/')[-1]}; result: {', '.join(v['result']) or 'none'}"}
tours = [{"id": "xapi", "label": "What learners generate", "message": f"Six verbs, {len(X)} elements that send them, all from one vocabulary file so every statement is shaped the same way.", "scenes": [
    S("Every HAX activity speaks xAPI through one shared vocabulary.", "xapi"),
    S("Six verbs cover everything an element reports.", *[f"v_{vb}" for vb in verbs]),
    S("Answered: the question elements.", "v_answered", *[f"x_{slug(t)}" for t in verbs["answered"]]),
    S("Attempted, progressed, completed: media, games and multi-step activities.", "v_attempted", "v_progressed", "v_completed", *[f"x_{slug(t)}" for t in sorted(set(verbs["completed"]) - set(verbs["answered"]))]),
    S("Experienced and interacted: things a learner opened or touched.", "v_experienced", "v_interacted", *[f"x_{slug(t)}" for t in sorted(set(verbs["experienced"]) | set(verbs["interacted"]))]),
    S("Statements feed Insights and describe learning in a course.", "insights", "course"),
    S("The whole vocabulary."),
]}]
meta = {"name": "xAPI verbs", "parent": "main", "noTimeline": True, "sectionLabels": {"verb": "verbs", "element": "elements"},
        "about": f"The six xAPI verbs HAX elements send and which of {len(X)} elements sends each, generated from user-action/lib/xapi-vocabulary.json. Green elements count toward completion.",
        "kindLabels": {"rel": "element sends verb", "schema": "the vocabulary"}}
write("xapi", lines, meta, nodes, tours)
print("xapi:", len(verbs), "verbs,", len(X), "elements")

# ---------------- HAX CLI commands ----------------
en = json.load(open("createrepo/src/locales/create.en.json"))
src = open("createrepo/src/create.js").read()
TOP = []
for m in re.finditer(r'\.command\("(\w+)"\)\s*(?:\.alias\("[^"]*"\)\s*)?\.description\(t\("(\w+)"\)', src): TOP.append((m.group(1), en.get(m.group(2), m.group(2))))
site_src = open("createrepo/src/lib/programs/site.js").read()
SITE = [(v, en.get(k, k)) for v, k in re.findall(r'value:\s*"([\w:-]+)",\s*label:\s*t\("(\w+)"\)', site_src)]
HIDDEN = re.findall(r'"([\w:-]+)"', site_src[site_src.index("siteHiddenActions"):site_src.index("siteHiddenActions") + 400])
HIDDEN = [h for h in HIDDEN if ":" in h]
party_src = open("createrepo/src/lib/programs/party.js").read()
PARTY = [(v, en.get(k, k)) for v, k in re.findall(r'value:\s*"([\w:-]+)",\s*label:\s*t\("(\w+)"\)', party_src)]
skills_src = open("createrepo/src/lib/programs/skills.js").read()
SKILLS = [(v, en.get(k, k)) for v, k in re.findall(r'value:\s*"([\w:-]+)",\s*label:\s*t\("(\w+)"\)', skills_src)]
AUDITS = [("audit", "DDD and HAXSchema compliance for an element"), ("audit:i18n", "Translation coverage audit"), ("audit:schema", "haxProperties schema audit"), ("audit:ssr", "Lit SSR safety audit"), ("audit:theme", "Theme audit")]
AUDITS = [a for a in AUDITS if os.path.exists("createrepo/src/lib/programs/" + a[0].replace(":", "-") + ".js") or a[0] == "audit"]
def prefix(v): return v.split(":")[0] if ":" in v else "site"
GROUPS = collections.OrderedDict([("top", ("hax …", "Top-level commands")), ("node", ("node:*", "Pages")), ("site", ("site:*", "Sites")), ("setup", ("setup:*", "CI and hosting setup")), ("issue", ("issue:*", "Filing issues")), ("audit", ("audit*", "Audits")), ("party", ("hax party", "Community")), ("skills", ("hax skills", "Agent skills"))])
cmds = collections.OrderedDict()
for v, d in TOP: cmds[f"c_{slug(v)}"] = {"label": f"hax {v}", "desc": d, "group": "top"}
for v, d in SITE + [(h, "Scripted or alias action, not listed in the menu") for h in HIDDEN]:
    g = prefix(v) if prefix(v) in GROUPS else "site"
    cmds[f"c_{slug(v)}"] = {"label": v, "desc": d, "group": g}
for v, d in AUDITS: cmds[f"c_{slug(v)}"] = {"label": f"hax {v}", "desc": d, "group": "audit"}
for v, d in PARTY: cmds[f"c_party_{slug(v)}"] = {"label": f"party {v}", "desc": d, "group": "party"}
for v, d in SKILLS: cmds[f"c_skills_{slug(v)}"] = {"label": f"skills {v}", "desc": d, "group": "skills"}
TOUCH = {"c_wc": ["components", "ddd", "haxschema"], "c_site": ["haxcms", "skeletons"], "c_audit": ["ddd", "haxschema", "testing"], "c_skills": ["agents", "praw"], "c_party": ["issues"], "c_site_surge": ["deploy"], "c_site_netlify": ["deploy"], "c_site_vercel": ["deploy"], "c_site_skeleton_export": ["skeletons"], "c_site_skeleton_install": ["skeletons"], "c_site_theme": ["themes"], "c_site_element": ["components"], "c_site_schema": ["jos"], "c_site_validate": ["jos"], "c_setup_github_actions": ["github"], "c_issue_general": ["issues"], "c_issue_theme": ["issues", "themes"], "c_update": ["npm"], "c_start": ["haxcms"], "c_serve": ["haxcms"]}
portals = sorted({p for ps in TOUCH.values() for p in ps})
lines = ["%% HAX CLI sub-web: every command the hax CLI offers, grouped by area, generated from haxtheweb/create (create.js, programs/*.js and the English locale).",
         "%% Portals: ids from hax-ecosystem.mmd. Regenerate with build_generated.py when commands change; details in hax-cli.json.",
         "flowchart TB", "  %%@ layout rings=0,230,500,780 sizes=92,66,46,52",
         '  subgraph hub ["HAX CLI"]', '    cli["cli"]', "  end", '  subgraph groups ["Areas"]']
for g, (lab, desc) in GROUPS.items(): lines.append(f'    g_{g}["{desc}"]')
lines += ["  end", '  subgraph cmdsg ["Commands"]']
for cid, c in cmds.items(): lines.append(f'    {cid}["{c["label"]}"]')
lines += ["  end", '  subgraph touches ["What they touch"]']
for p in portals: lines.append(f'    {p}["{p}"]')
lines += ["  end", ""]
for g in GROUPS: lines.append(f"  cli -->|offers| g_{g}")
for cid, c in cmds.items(): lines.append(f"  g_{c['group']} -->|includes| {cid}")
for cid, ps in TOUCH.items():
    if cid in cmds:
        for p in ps: lines.append(f"  {cid} -->|touches| {p}")
lines += ["", "  %%@ group hub tier=0", "  %%@ group groups tier=1", "  %%@ group cmdsg tier=2", "  %%@ group touches tier=3", "  %%@ node cli portal"]
for g in GROUPS: lines.append(f"  %%@ node g_{g} icon=hax:wand color=skyBlue motion=pop")
for cid, c in cmds.items(): lines.append(f"  %%@ node {cid} mono={c['label'].split(':')[-1].split(' ')[-1][:5].upper()} color={'limestoneGray' if 'alias' in c['desc'] else 'skyBlue'} motion=nudge")
for p in portals: lines.append(f"  %%@ node {p} portal")
nodes = {"cli": {"always": True}}
for g, (lab, desc) in GROUPS.items(): nodes[f"g_{g}"] = {"desc": f"{desc} ({lab}): {sum(1 for c in cmds.values() if c['group']==g)} commands.", "kind": "group"}
for cid, c in cmds.items(): nodes[cid] = {"desc": c["desc"], "kind": "command", "links": {"repo": GH + "/create"}}
tours = [{"id": "cli", "label": "Everything the CLI does", "message": f"{len(cmds)} commands in {len(GROUPS)} areas, generated from the create repo so it never drifts from the real CLI.", "scenes": [
    S("One CLI for sites, elements, audits and the community.", "cli"),
    S("Top-level commands.", "g_top", *[c for c, v in cmds.items() if v["group"] == "top"]),
    S("Pages and sites, drush-style.", "g_node", "g_site"),
    S("Publishing and CI setup.", "g_setup", "c_site_surge", "c_site_netlify", "c_site_vercel", "deploy"),
    S("Audits keep elements honest.", "g_audit", "ddd", "haxschema", "testing"),
    S("Community and agent skills.", "g_party", "g_skills", "g_issue", "issues", "agents", "praw"),
    S("All of it."),
]}]
meta = {"name": "HAX CLI commands", "parent": "main", "noTimeline": True, "sectionLabels": {"group": "areas", "command": "commands"},
        "about": f"Every command the hax CLI offers ({len(cmds)} in {len(GROUPS)} areas), generated from haxtheweb/create: the top-level commands in create.js, the site, party and skills action menus, and the audits. Gray tiles are aliases or scripted-only actions.",
        "kindLabels": {"rel": "area to command, command to what it touches"}}
write("cli", lines, meta, nodes, tours)
print("cli:", len(cmds), "commands;", len(TOP), "top-level")
