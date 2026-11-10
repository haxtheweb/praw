"""Quality control sub-web: every safeguard on what enters HAX, generated from the CI that actually runs.

Reads each repo's .github/workflows on its default branch (GitHub REST API), so the web only shows checks that are
merged and running. Three groups: blocking pull request gates, advisory pull request checks, and scheduled jobs
(GitHub Actions on a cron, plus the Claude scheduled tasks in build/data/scheduled-tasks.json, whose output is
checked on GitHub). Open PRs that add a workflow file, and the PRs in build/data/quality-planned.json, are planned
tiles linking to the PR. Details in hax-quality.json."""
import json, re, subprocess, base64, collections, datetime, yaml
GH = "https://github.com/haxtheweb"
REPOS = {"webcomponents": "components", "haxcms-nodejs": "nodejs", "haxcms-php": "php", "create": "cli", "praw": "praw", "haxcms-mcp": "mcp", "issues": "issues"}
def api(q):
    r = subprocess.run(["gh", "api", q], capture_output=True, text=True, timeout=90)
    try: return json.loads(r.stdout)
    except Exception: return None
def S(c, *i): return {"caption": c, "nodes": list(i)}
def slug(s): return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")

# ---------- what each kind of check guards (matched on the check's name) ----------
GUARDS = [
 (r"color contrast", "Text in the demos of the elements a pull request touches meets WCAG AA contrast in light and dark mode. Known failures are baselined, and the baseline can only shrink."),
 (r"old-site", "Sites made from 2021 on keep working: one fixture site per year is upgraded to the latest code and edited the way an author would."),
 (r"codeql", "Code with known vulnerability patterns doesn't merge."),
 (r"licen", "No dependency under an incompatible license enters the repo, and the project stays Apache-2.0."),
 (r"dependency audit|composer audit", "Dependencies with known security advisories are caught."),
 (r"^cla$", "Every contributor has signed the contributor license agreement."),
 (r"security lint", "Unsafe patterns (eval, shell injection and the like) don't merge into the CLI."),
 (r"eslint", "Code follows the repo's lint rules, such as no optional chaining in webcomponents."),
 (r"stylelint", "CSS follows the stylesheet rules."),
 (r"format check", "Formatting stays consistent (Prettier)."),
 (r"ddd token", "Only real DDD design tokens are referenced, and the token export stays current."),
 (r"template", "CSS and HTML templates inside elements are well formed."),
 (r"api snapshot", "The front-end API of authorable elements doesn't change, so all content ever made keeps working."),
 (r"pseudo-locale|rtl", "Changed elements still lay out with long pseudo-locale strings and right to left."),
 (r"memory leak", "Changed elements don't leak memory when added and removed."),
 (r"locale guard", "Feature PRs change English strings only; translations come from the nightly job."),
 (r"walkthrough", "Element walkthroughs are flagged when the element they show has changed."),
 (r"render bench", "Render performance of changed elements is measured on the PR."),
 (r"knip", "Unused files, exports and dependencies are found."),
 (r"test all elements", "Every element's test suite passes in Chromium; element suites include axe accessibility tests where an element has them."),
 (r"script tests", "The repo's build and maintenance scripts keep working."),
 (r"unit|phpunit|^test$", "Changes don't break existing behavior."),
 (r"conformance", "The API keeps matching its OpenAPI spec."),
 (r"e2e", "End-to-end flows in the real UI keep working."),
 (r"smoke", "A fresh install can create a site, add a page and serve it."),
 (r"^build$", "The project still builds."),
 (r"gallery", "The component gallery still builds."),
 (r"phpstan", "New PHP static-analysis errors don't merge."),
 (r"parity harness", "The same seeded operations sent to haxcms-nodejs, haxcms-php and the HAX CLI write the same sites (report only)."),
 (r"parity", "haxcms-nodejs and haxcms-php give the same results for the same operations."),
 (r"performance|perf", "Memory, page load and outline save time stay inside the budgets in test/perf/budgets.json."),
 (r"mutation", "The tests catch real faults: deliberate mutations of the code must make them fail."),
 (r"scorecard", "Supply-chain security practices are scored (OpenSSF Scorecard)."),
 (r"sbom", "Every build has a software bill of materials."),
]
def guards(label):
    l = label.lower()
    for rx, g in GUARDS:
        if re.search(rx, l): return g
    return ""
# names: workflow names and step names to the label shown on the tile
PRETTY = {"codeql": "CodeQL", "license-check": "Dependency licenses", "license check": "Dependency licenses", "dependency license": "Dependency licenses",
          "dependency-audit": "Dependency audit", "fresh-install-smoke": "Fresh-install smoke test", "mutation testing": "Mutation testing",
          "mutation testing (outline-designer)": "Mutation testing", "knip": "Unused code (knip)", "ddd-token-lint": "DDD token lint", "template-lint": "Template lint",
          "api-snapshot": "Element API snapshot", "i18n-layout": "Pseudo-locale and RTL layout", "leak-check": "Memory leaks", "locale-guard": "Locale guard",
          "walkthrough-status": "Walkthrough status", "render-bench": "Render benchmarks", "phpstan": "PHPStan", "ossf scorecard": "OpenSSF Scorecard",
          "cla assistant": "CLA", "backend parity": "Backend parity", "build": "Build and tests", "tests": "Build and tests", "sbom": "SBOM", "perf": "Performance and memory budgets", "parity-nightly": "Parity harness (nodejs, PHP, CLI)", "contrast": "Color contrast (light and dark)", "old-sites-weekly": "Old-site compatibility"}
STEP = [(r"^prettier format check|^format check", "Format check"), (r"^eslint$|^lint$", "ESLint"), (r"^security lint", "Security lint"),
        (r"^stylelint", "Stylelint"), (r"^audit production dependencies|^dependency audit|^composer audit", "Dependency audit"),
        (r"^run phpunit", "PHPUnit"), (r"^unit \+ api conformance", "Unit and API conformance tests"), (r"^e2e", "E2E UI tests"),
        (r"^test all elements", "Test all elements"), (r"^script tests", "Script tests"), (r"^smoke tests", "Smoke tests"), (r"^test$", "Unit tests"),
        (r"^build$", "Build"), (r"^validate component gallery", "Gallery build")]
SKIP = re.compile(r"^(checkout|set ?up|setup|install|cache|get (yarn|composer)|upload|download|restore|job summary|note a failed|decide|comment|read license|"
                  r"generate|show|validate tag|log in|derive|build and push|pack|attach|fill|flag|rebuild elements readme|coverage|checkout base|run analysis|"
                  r"initialize|perform|analyze|check out)", re.I)
ADVISORY_WORDS = re.compile(r"warning only|report[- ]only", re.I)
ID = {"E2E UI tests": "q_e2e", "Backend parity": "q_parity", "CodeQL": "q_codeql", "CLA": "q_cla", "Dependency audit": "q_audit", "ESLint": "q_lint"}
def node_id(label): return ID.get(label) or "q_" + slug(label)
def step_label(name):
    n = name.strip()
    for rx, lab in STEP:
        if re.search(rx, n, re.I): return lab
    return re.sub(r"\s*\(.*?\)\s*", " ", n).strip()

checks = {}  # id -> {label, mode per repo, kind}
def add(label, repo, mode, wf, extra=""):
    i = node_id(label)
    c = checks.setdefault(i, {"label": label, "repos": {}, "wf": set(), "extra": set()})
    prev = c["repos"].get(repo)
    rank = {"blocking": 3, "advisory": 2, "nightly": 1, "weekly": 1}
    if not prev or rank.get(mode, 0) > rank.get(prev, 0): c["repos"][repo] = mode
    c["wf"].add(wf)
    if extra: c["extra"].add(extra)
sched = {}  # id -> {label, repos:{repo:cadence}, wf, last}
def cadence(cron):
    f = cron.split()
    return "nightly" if f[4] == "*" else "weekly"
EXCLUDE = re.compile(r"^(release|docker|gallery-deeplinks|release-checksums|release-notes|sbom)", re.I)
default_branch = {}
for repo, nid in REPOS.items():
    info = api(f"repos/haxtheweb/{repo}") or {}
    default_branch[repo] = info.get("default_branch", "main")
    files = api(f"repos/haxtheweb/{repo}/contents/.github/workflows") or []
    if not isinstance(files, list): continue
    states = {w["path"].split("/")[-1]: w for w in ((api(f"repos/haxtheweb/{repo}/actions/workflows?per_page=100") or {}).get("workflows") or [])}
    for f in files:
        if not f["name"].endswith((".yml", ".yaml")): continue
        st = states.get(f["name"])
        if st and st.get("state") != "active": continue  # disabled workflows aren't running
        y = yaml.safe_load(base64.b64decode((api(f"repos/haxtheweb/{repo}/contents/{f['path']}") or {}).get("content", "")).decode() or "{}") or {}
        on = y.get(True) or y.get("on") or {}
        trig = set(on) if isinstance(on, dict) else ({on} if isinstance(on, str) else set(on))
        wname = (y.get("name") or f["name"].rsplit(".", 1)[0]).strip()
        if EXCLUDE.match(f["name"]): continue
        wl = PRETTY.get(wname.lower(), wname)
        wf = f"{GH}/{repo}/blob/{default_branch[repo]}/{f['path']}"
        crons = [c["cron"] for c in (on.get("schedule") or [])] if isinstance(on, dict) else []
        if crons and "scorecard" not in f["name"] or "scorecard" in f["name"]:
            if crons:
                s = sched.setdefault(wl, {"label": wl, "repos": {}, "wf": set(), "last": {}})
                s["repos"][nid] = cadence(crons[0]); s["wf"].add(wf)
                runs = (api(f"repos/haxtheweb/{repo}/actions/workflows/{f['name']}/runs?per_page=1&event=schedule") or {}).get("workflow_runs") or []
                if runs: s["last"][nid] = (runs[0].get("conclusion") or runs[0].get("status"), runs[0]["created_at"][:10])
        if not (trig & {"pull_request", "pull_request_target"}): continue
        for jname, job in (y.get("jobs") or {}).items():
            if "sweep" in jname.lower() and "pull_request" not in str(job.get("if", "pull_request")): continue
            if re.search(r"sweep|attach", jname, re.I): continue
            cond = str(job.get("if", ""))
            # jobs gated to another event (a manual dispatch, a release) never run on a pull request
            if re.search(r"github\.event_name\s*==\s*'(?!pull_request)", cond) and "pull_request" not in cond.replace("!= 'pull_request'", ""): continue
            on_label = re.search(r"labels\.\*\.name,\s*'([^']+)'", cond)
            job_adv = bool(job.get("continue-on-error")) or bool(ADVISORY_WORDS.search(jname)) or bool(on_label)
            extra = f"Opt-in: runs on a pull request only when it is labeled {on_label.group(1)}, and then fails it when the check fails." if on_label else ""
            steps = [s for s in job.get("steps", []) if isinstance(s, dict) and s.get("name") and not SKIP.match(s["name"].strip())]
            all_names = [s.get("name", "") for s in job.get("steps", []) if isinstance(s, dict)]
            if all_names and all(re.match(r"^(comment|attach|upload|download|checkout)", n, re.I) for n in all_names): continue  # housekeeping jobs check nothing
            multi = len(steps) > 2 or wname.lower() in ("build", "tests")
            if not multi:
                adv = job_adv or any(s.get("continue-on-error") for s in steps) and all(s.get("continue-on-error") for s in steps) or any(ADVISORY_WORDS.search(s["name"]) for s in steps)
                add(wl, nid, "advisory" if adv else "blocking", wf, extra)
            else:
                for s in steps:
                    lab = step_label(s["name"])
                    adv = job_adv or bool(s.get("continue-on-error")) or bool(ADVISORY_WORDS.search(s["name"]))
                    add(lab, nid, "advisory" if adv else "blocking", wf, extra)

# scheduled jobs: a tile of their own, named with how often they run; the id is the check's own id when no PR check uses it
_s = {}
for wl, s in sched.items():
    cads = set(s["repos"].values()); cad = "nightly" if cads == {"nightly"} else "weekly" if cads == {"weekly"} else "nightly and weekly"
    s["label"] = "Nightly build and tests" if wl == "Build and tests" else f"{wl}, {cad}"
    base = node_id(wl); _s[base if base not in checks else base + "_sched"] = s
sched = _s

# ---------- Claude scheduled tasks: does each produce output? ----------
T = json.load(open("ext/scheduled-tasks.json"))["tasks"]
REPO_OF = {"webcomponents": "webcomponents", "praw": "praw", "issues": "issues"}
for t in T:
    o = t["output"]; t["state"], t["out_url"] = "scheduled", None
    if "pr_branch" in o:
        r, b = o["pr_branch"].split(":")
        prs = api(f"repos/haxtheweb/{r}/pulls?state=all&head=haxtheweb:{b}&per_page=1") or []
        if prs: t["state"], t["out_url"] = "producing", prs[0]["html_url"]
    elif "issue_comment" in o:
        r, n = o["issue_comment"].split(":")
        cs = api(f"repos/haxtheweb/{r}/issues/{n}/comments?per_page=100") or []
        hit = [c for c in cs if o.get("contains", "") in (c.get("body") or "")]
        if hit: t["state"], t["out_url"] = "producing", hit[-1]["html_url"]
    else: t["state"] = "flag-only"

# ---------- planned: open PRs adding a workflow file, plus listed PRs ----------
planned = []
for repo, nid in REPOS.items():
    for pr in api(f"repos/haxtheweb/{repo}/pulls?state=open&per_page=100") or []:
        if not isinstance(pr, dict): continue
        files = api(f"repos/haxtheweb/{repo}/pulls/{pr['number']}/files?per_page=100") or []
        new = [x["filename"] for x in files if isinstance(x, dict) and x["filename"].startswith(".github/workflows/") and x.get("status") == "added"]
        if new: planned.append({"id": f"qp_{slug(repo)}_{pr['number']}", "label": re.sub(r"^\[[^\]]+\]\s*", "", pr["title"]), "repo": nid, "url": pr["html_url"], "files": new})
for p in json.load(open("ext/quality-planned.json"))["prs"]:
    r, n = p["pr"].split("#"); pr = api(f"repos/{r}/pulls/{n}") or {}
    if pr.get("state") == "open": planned.append({"id": f"qp_{slug(r.split('/')[1])}_{n}", "label": p["label"], "repo": p["repo"], "url": pr["html_url"], "files": []})

# ---------- write the web ----------
blocking = {i: c for i, c in checks.items() if "blocking" in c["repos"].values()}
advisory = {i: c for i, c in checks.items() if i not in blocking}
repos_used = sorted({r for c in checks.values() for r in c["repos"]} | {r for s in sched.values() for r in s["repos"]} | {r for t in T for r in t["repos"]} | {p["repo"] for p in planned})
lines = ["%% Quality control sub-web: every safeguard on what enters HAX, generated by build_quality.py from each repo's .github/workflows on its default branch,",
         "%% the Claude scheduled tasks in build/data/scheduled-tasks.json and open PRs that add checks. Portals: ids from hax-ecosystem.mmd. Details in hax-quality.json.",
         "flowchart TB", "  %%@ layout rings=0,200,430,690,920 sizes=92,64,50,46,54",
         '  subgraph hub ["Quality control"]', '    quality["quality"]', "  end",
         '  subgraph groupsg ["Three kinds of safeguard"]', '    qg_block["Blocking PR gates"]', '    qg_adv["Advisory PR checks"]', '    qg_sched["Scheduled jobs"]', '    testing["testing"]', "  end",
         '  subgraph blockg ["Blocking gates"]']
for i, c in sorted(blocking.items(), key=lambda x: x[1]["label"]): lines.append(f'    {i}["{c["label"]}"]')
lines += ["  end", '  subgraph advg ["Advisory checks and planned"]']
for i, c in sorted(advisory.items(), key=lambda x: x[1]["label"]): lines.append(f'    {i}["{c["label"]}"]')
for p in planned: lines.append(f'    {p["id"]}["{p["label"] if len(p["label"]) <= 44 else p["label"][:44].rsplit(" ", 1)[0] + "…"}"]')
lines += ["  end", '  subgraph schedg ["Scheduled"]']
for i, s in sorted(sched.items(), key=lambda x: x[1]["label"]): lines.append(f'    {i}["{s["label"]}"]')
for t in T: lines.append(f'    {t["id"]}["{t["name"]}"]')
lines += ["  end", '  subgraph reposg ["Repos guarded"]']
for r in repos_used: lines.append(f'    {r}["{r}"]')
lines += ["  end", "", "  quality -->|has| qg_block", "  quality -->|has| qg_adv", "  quality -->|has| qg_sched", "  testing -->|is part of| quality"]
VERB = {"blocking": "fails PRs in", "advisory": "advises on PRs in", "nightly": "runs nightly in", "weekly": "runs weekly in"}
for i, c in blocking.items():
    lines.append(f"  qg_block -->|includes| {i}")
    for r, m in c["repos"].items(): lines.append(f"  {i} -.->|{VERB[m]}| {r}")
for i, c in advisory.items():
    lines.append(f"  qg_adv -->|includes| {i}")
    for r, m in c["repos"].items(): lines.append(f"  {i} -.->|{VERB[m]}| {r}")
for p in planned: lines += [f"  qg_adv -->|planned| {p['id']}", f"  {p['id']} -.->|would run in| {p['repo']}"]
for i, s in sched.items():
    lines.append(f"  qg_sched -->|includes| {i}")
    for r, cad in s["repos"].items(): lines.append(f"  {i} -.->|{VERB[cad]}| {r}")
for t in T:
    lines.append(f"  qg_sched -->|includes| {t['id']}")
    for r in t["repos"]: lines.append(f"  {t['id']} -.->|{VERB[t['cadence']]}| {r}")
lines += ["", "  %%@ group hub tier=0", "  %%@ group groupsg tier=1", "  %%@ group blockg tier=2", "  %%@ group advg tier=3", "  %%@ group schedg tier=3", "  %%@ group reposg tier=4",
          "  %%@ node quality portal", "  %%@ node testing portal",
          "  %%@ node qg_block icon=icons:verified-user color=forestGreen motion=pop", "  %%@ node qg_adv icon=icons:report color=roarGolden motion=pop", "  %%@ node qg_sched icon=hax:timeline color=beaverBlue motion=pop"]
for i in blocking: lines.append(f"  %%@ node {i} icon=icons:check-circle color=forestGreen motion=nudge")
for i in advisory: lines.append(f"  %%@ node {i} icon=icons:report color=roarGolden motion=nudge")
for p in planned: lines.append(f"  %%@ node {p['id']} icon=icons:build color=athertonViolet motion=nudge")
for i in sched: lines.append(f"  %%@ node {i} icon=hax:timeline color=beaverBlue motion=nudge")
for t in T: lines.append(f"  %%@ node {t['id']} icon=hax:wand color={'wonderPurple' if t['state'] != 'scheduled' else 'limestoneGray'} motion=nudge")
for r in repos_used: lines.append(f"  %%@ node {r} portal")
open("hax-quality.mmd", "w").write("\n".join(lines) + "\n")

NAME = {"components": "webcomponents", "nodejs": "haxcms-nodejs", "php": "haxcms-php", "cli": "create", "praw": "praw", "mcp": "haxcms-mcp", "issues": "issues"}
def where(c):
    by = collections.defaultdict(list)
    for r, m in c["repos"].items(): by[m].append(NAME[r])
    return " ".join(f"{'Fails the pull request when it fails' if m == 'blocking' else 'Reports without failing the pull request'} in {', '.join(sorted(rs))}." for m, rs in sorted(by.items()))
nodes = {"quality": {"always": True}, "testing": {},
         "qg_block": {"desc": f"{len(blocking)} checks that fail a pull request when they fail, in at least one repo; whether a failing check stops the merge is up to each repo's branch rules. Each is read from the repo's workflow files on its default branch, so only checks that are merged and running appear.", "kind": "group"},
         "qg_adv": {"desc": f"{len(advisory)} checks that run on pull requests but don't stop a merge (continue-on-error, warning only or report only), plus {len(planned)} planned checks still in open pull requests. ESLint stays here until it blocks.", "kind": "group"},
         "qg_sched": {"desc": f"{len(sched)} GitHub Actions jobs on a schedule and {len(T)} Claude scheduled tasks. Nothing auto-merges: every PR waits for review, and every flag lands in the unified issue queue.", "kind": "group", "links": {"tracking": "https://github.com/haxtheweb/issues/issues/3262"}}}
for i, c in checks.items():
    wf = sorted(c["wf"])
    nodes[i] = {"desc": " ".join(x for x in [guards(c["label"]), "" if any("Opt-in" in e for e in c["extra"]) else where(c), *sorted(c["extra"])] if x), "kind": "gate" if i in blocking else "advisory", "status": "deployed",
                "links": {f"workflow {k + 1}" if len(wf) > 1 else "workflow": u for k, u in enumerate(wf[:4])}}
for p in planned:
    nodes[p["id"]] = {"desc": f"In an open pull request, not running yet. {guards(p['label'])}".strip(), "status": "planned", "kind": "planned", "links": {"pr": p["url"]}}
for i, s in sched.items():
    last = "; ".join(f"{NAME[r]}: last scheduled run {v[1]}, {v[0]}" for r, v in s["last"].items())
    nodes[i] = {"desc": " ".join(x for x in [guards(s["label"]).replace("doesn't merge", "in main is caught, including patterns found after it merged"), "Runs " + ", ".join(f"{cad} in {NAME[r]}" for r, cad in s["repos"].items()) + ".", (last + ".") if last else ""] if x),
                "kind": "scheduled", "status": "deployed", "links": {f"workflow {k + 1}" if len(s["wf"]) > 1 else "workflow": u for k, u in enumerate(sorted(s["wf"])[:4])}}
STATE = {"producing": "Running and producing output.", "scheduled": "Scheduled, but no output on GitHub yet.", "flag-only": "Running; it only produces output when it finds something."}
for t in T:
    nodes[t["id"]] = {"desc": f"Claude scheduled task, {t['cadence']}. {t['guards']} {STATE[t['state']]}", "kind": "task",
                      "status": "deployed" if t["state"] != "scheduled" else "in-progress", "links": ({"latest output": t["out_url"]} if t["out_url"] else {}) | {"tracking": "https://github.com/haxtheweb/issues/issues/3262"}}
quiet = [t["name"] for t in T if t["state"] == "scheduled"]
tours = [{"id": "quality", "label": "What guards a change", "message": "Every safeguard on what enters HAX, read from the CI that actually runs.", "scenes": [
    S(f"{len(blocking)} blocking gates: a pull request can't merge until these pass.", "qg_block", *blocking),
    S(f"{len(advisory)} advisory checks report on the pull request without stopping it.", "qg_adv", *advisory),
    S("Planned checks, still in open pull requests.", *[p["id"] for p in planned]) if planned else S("No checks are waiting in open pull requests.", "qg_adv"),
    S("Scheduled GitHub Actions run nightly and weekly against main.", "qg_sched", *sched),
    S("Claude scheduled tasks take the jobs that need judgment: translating, docs, triage." + (f" Not producing output yet: {', '.join(quiet)}." if quiet else ""), "qg_sched", *[t["id"] for t in T]),
    S("Everything that guards HAX.")]}]
meta = {"name": "Quality control", "parent": "main", "noTimeline": True,
        "sectionLabels": {"group": "kinds", "gate": "blocking gates", "advisory": "advisory checks", "planned": "planned", "scheduled": "scheduled jobs", "task": "Claude scheduled tasks"},
        "about": f"Every safeguard on what enters HAX, generated from the workflow files on each repo's default branch, so only checks that are merged and running appear: {len(blocking)} blocking gates, {len(advisory)} advisory checks, {len(sched)} scheduled jobs and {len(T)} Claude scheduled tasks. Planned tiles are open pull requests. Element test suites include axe accessibility tests where an element has them; whole-project accessibility is covered by the weekly sweep, not a blocking gate.",
        "kindLabels": {"rel": "kind of safeguard", "schema": "where it runs"}, "generated": datetime.date.today().isoformat()}
json.dump({"meta": meta, "nodes": nodes, "evidence": {}, "tours": tours}, open("hax-quality.json", "w"), indent=1, ensure_ascii=False)
print(len(blocking), "blocking;", len(advisory), "advisory;", len(planned), "planned;", len(sched), "scheduled;", len(T), "tasks;", "quiet:", quiet)
