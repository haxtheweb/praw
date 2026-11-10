"""Quality control sub-web: every gate a change passes through, from a developer's machine to a release, and which repos each guards.
Facts from the repos' AGENTS.md, package scripts and the CI runs seen on recent PRs. Details in hax-quality.json."""
import json
GH = "https://github.com/haxtheweb"
def L(a, b): return {"label": a, "url": b}
def S(c, *i): return {"caption": c, "nodes": list(i)}
STAGES = [("st_local", "On your machine", "Before a commit: lint, precheck and the test suite run locally; AGENTS.md in each repo says which."),
          ("st_pr", "On the pull request", "GitHub Actions on every PR: CodeQL, unit and conformance tests, the CLA check. A PR is expected to pass CodeQL on its first push."),
          ("st_release", "At release", "Ubiquity builds and publishes every element; the drift check updates this web's versions.")]
# id, label, stage, desc, repos guarded, link
GATES = [
 ("q_lint", "Lint", "st_local", "ESLint rules per repo. In webcomponents the rules ban optional chaining (?.) so elements keep running in older browsers; lint catches it.", ["components", "nodejs", "cli"], GH + "/webcomponents/blob/master/AGENTS.md"),
 ("q_precheck", "precheck", "st_local", "haxcms-nodejs's npm run precheck: Prettier, ESLint and the fast tests on the files changed against main. haxcms-php has no precheck; the nodejs one covers files the two share.", ["nodejs"], GH + "/haxcms-nodejs/blob/main/scripts/precheck.mjs"),
 ("q_wtr", "Browser tests", "st_local", "web-test-runner suites in real browsers, with accessibility checks, for every element in the monorepo.", ["components"], GH + "/webcomponents/blob/master/web-test-runner.config.mjs"),
 ("q_dddaudit", "DDD audit", "st_local", "hax audit: design-system and HAXSchema compliance for an element, run from the CLI before a PR.", ["components"], GH + "/create"),
 ("q_unit", "Unit tests", "st_pr", "node:test suites in haxcms-nodejs and the CLI; PHPUnit (about 3,900 tests) in haxcms-php with its committed vendor folder.", ["nodejs", "php", "cli"], GH + "/haxcms-php/tree/master/system/backend/php/tests"),
 ("q_parity", "API conformance", "st_pr", "Conformance tests check both backends against the same OpenAPI specs, so haxcms-nodejs and haxcms-php keep identical behavior. Matching test names on both sides.", ["nodejs", "php"], GH + "/haxcms-nodejs/tree/main/test"),
 ("q_codeql", "CodeQL", "st_pr", "GitHub's security analysis (actions and javascript-typescript) on every PR to haxcms-nodejs, haxcms-php and webcomponents. Expected to pass on the first push.", ["nodejs", "php", "components", "cli"], GH + "/haxcms-nodejs/actions"),
 ("q_audit", "Dependency audit", "st_pr", "Composer audit on haxcms-php and npm audit on the Node repos flag vulnerable dependencies.", ["php", "nodejs"], GH + "/haxcms-php/actions"),
 ("q_cla", "CLA check", "st_pr", "Every contributor signs the contributor license agreement once; the check runs on each PR.", ["components", "nodejs", "php", "cli"], GH + "/issues/blob/master/CONTRIBUTING.md"),
 ("q_e2e", "Browser end-to-end", "st_pr", "Playwright runs against the HAXcms UI (site creation, templates, outline operations). Non-gating while its flakiness is characterized; some failures recur across PRs.", ["nodejs"], GH + "/haxcms-nodejs/actions"),
 ("q_ubiquity", "Ubiquity", "st_release", "The release build: every element built, tested and published to npm together, and wc-registry.json regenerated.", ["components"], GH + "/webcomponents/blob/master/scripts/ubiquity.sh"),
 ("q_drift", "Graph drift check", "st_release", "drift.py pulls the latest source, reruns every generated web and flags new or missing CLI commands, API endpoints, MCP tools, field types, schema parts, skeletons, importers, tutorials, languages and release steps; graph-drift.mjs checks every released part's version against npm and GitHub tags. --strict fails a ubiquity build when anything drifted.", ["praw"], GH + "/issues/issues/3173"),
]
REPOS = ["components", "nodejs", "php", "cli", "praw"]
lines = ["%% Quality control sub-web: every gate a change passes through, from a developer's machine to a release, and which repos each guards.",
         "%% Portals: ids from hax-ecosystem.mmd. Details in hax-quality.json.",
         "flowchart TB", "  %%@ layout rings=0,230,480,740 sizes=92,66,58,56",
         '  subgraph hub ["Quality control"]', '    testing["testing"]', "  end", '  subgraph stages ["Stages"]']
for sid, lab, d in STAGES: lines.append(f'    {sid}["{lab}"]')
lines += ["  end", '  subgraph gates ["Gates"]']
for gid, lab, *_ in GATES: lines.append(f'    {gid}["{lab}"]')
lines += ["  end", '  subgraph repos ["Repos guarded"]']
for r in REPOS: lines.append(f'    {r}["{r}"]')
lines += ['    security["security"]', '    ubiquity["ubiquity"]', "  end", ""]
for sid, lab, d in STAGES: lines.append(f"  testing -->|runs at| {sid}")
for gid, lab, st, d, rs, link in GATES:
    lines.append(f"  {st} -->|runs| {gid}")
    for r in rs: lines.append(f"  {gid} -->|guards| {r}")
lines += ["  q_codeql -->|feeds| security", "  q_ubiquity -->|is| ubiquity", "",
          "  %%@ group hub tier=0", "  %%@ group stages tier=1", "  %%@ group gates tier=2", "  %%@ group repos tier=3", "  %%@ node testing portal"]
for sid, lab, d in STAGES: lines.append(f"  %%@ node {sid} icon=icons:check-circle color=forestGreen motion=pop")
for gid, lab, st, *_ in GATES: lines.append(f"  %%@ node {gid} icon={'icons:bug-report' if gid in ('q_codeql','q_audit') else 'icons:check-circle'} color={'original87Pink' if gid=='q_e2e' else 'forestGreen'} motion=nudge")
for r in REPOS + ["security", "ubiquity"]: lines.append(f"  %%@ node {r} portal")
open("hax-quality.mmd", "w").write("\n".join(lines) + "\n")
nodes = {"testing": {"always": True}}
for sid, lab, d in STAGES: nodes[sid] = {"desc": d, "kind": "stage"}
for gid, lab, st, d, rs, link in GATES: nodes[gid] = {"desc": d, "kind": "gate", "links": {"source": link}}
tours = [{"id": "quality", "label": "From commit to release", "message": "Every gate a change passes through and which repos it guards.", "scenes": [
    S("Three stages: your machine, the pull request, the release.", *[s for s, *_ in STAGES]),
    S("Before you commit: lint, precheck, browser tests and the DDD audit.", "st_local", "q_lint", "q_precheck", "q_wtr", "q_dddaudit"),
    S("On the PR: unit tests, API conformance between the two backends, CodeQL, dependency audits, the CLA.", "st_pr", "q_unit", "q_parity", "q_codeql", "q_audit", "q_cla"),
    S("The browser end-to-end suite runs too, but does not gate yet.", "q_e2e"),
    S("At release: Ubiquity ships every element; the drift check keeps this web honest.", "st_release", "q_ubiquity", "q_drift"),
    S("Which repos each gate guards.", *REPOS),
    S("The whole pipeline."),
]}]
meta = {"name": "Quality control", "parent": "main", "noTimeline": True, "sectionLabels": {"stage": "stages", "gate": "gates"},
        "about": "Every quality gate a change passes through, from a developer's machine to a published release, and which repos each guards. The red gate is the one that does not block merging yet.",
        "kindLabels": {"rel": "stage runs gate; gate guards repo"}}
json.dump({"meta": meta, "nodes": nodes, "evidence": {}, "tours": tours}, open("hax-quality.json", "w"), indent=1, ensure_ascii=False)
print(len(GATES), "gates")
