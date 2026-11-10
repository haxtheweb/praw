"""Drift check for the generated webs.

Pulls the latest source, reruns every builder that is generated from source, and reports what changed:
tiles added or gone in each generated web (commands, endpoints, MCP tools, field types, schema parts,
skeletons, importers, tutorials, languages, release steps, HAX Lab entries) plus inventories that a
builder reads from a saved extract (MCP tools, xAPI verbs). The ecosystem web's versions are checked
by graph-drift.mjs.

  python3 -I drift.py            pull, rebuild, report
  python3 -I drift.py --no-pull  rebuild from what is on disk
  python3 -I drift.py --strict   exit 1 when anything drifted (for the end of a ubiquity build)
  python3 -I drift.py --accept   also take new versions and new MCP tools into the saved data

Writes ext/drift-report.json and ext/drift-report.md. Commit the rebuilt .mmd/.json files to accept the drift."""
import json, os, re, subprocess, sys, datetime, glob
ARGS = sys.argv[1:]
HERE = os.path.dirname(os.path.abspath(__file__))  # the generators live beside this script; run it from the working folder
CLONES = ["haxcms-nodejs", "haxcms-php", "createrepo", "mcprepo", "hs", "josrepo", "learnrepo"]  # praw is this repo: never pulled here
# builder -> webs it writes; every one of these reads its source directly
BUILDERS = [("build_generated.py", ["openapi", "mcptools", "xapi", "cli"]), ("build_schemas.py", ["haxschema", "jos", "appstore", "merlin", "oerschema"]),
            ("build_importers.py", ["importers"]), ("build_tutorials.py", ["tutorials"]), ("build_skeletons.py", ["skeletons"]),
            ("build_languages.py", ["languages"]), ("build_more.py", ["release", "community", "psu", "haxlab"]), ("build_layers.py", [])]
WEBS = [w for _, ws in BUILDERS for w in ws]
def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    return r.returncode, (r.stdout + r.stderr).strip()
def snapshot():
    out = {}
    for w in WEBS:
        try:
            t = open(f"hax-{w}.mmd").read()
            out[w] = {i: lab for i, lab in re.findall(r'^\s{4}(\w+)[\[\(\{>]+"?([^"\]\)]*)', t, re.M)}
        except FileNotFoundError: out[w] = {}
    return out
report = {"checked": datetime.date.today().isoformat(), "pulled": {}, "webs": {}, "inventories": {}, "builders": {}}
if "--no-pull" not in ARGS:
    for c in CLONES:
        if os.path.isdir(os.path.join(c, ".git")):
            code, out = run(["git", "-C", c, "pull", "--ff-only", "-q"])
            _, head = run(["git", "-C", c, "log", "-1", "--format=%h %cs"])
            report["pulled"][c] = head if code == 0 else "pull failed: " + out[-200:]
    # files the builders read that live in other repos
    for path, repo, src in [("ext/ubiquity-push.sh", "webcomponents", "scripts/ubiquity-push.sh"), ("ext/haxlab-readme.md", "hax-lab", "README.md")]:
        code, out = run(["gh", "api", f"repos/haxtheweb/{repo}/contents/{src}", "--jq", ".content"])
        if code == 0 and out:
            import base64
            open(path, "w").write(base64.b64decode(out).decode())
B = "haxcms-nodejs/src/public/build/es6/node_modules/@haxtheweb"
before = snapshot()
# inventories read from saved extracts: compare the extract with the source it came from
mcp_src = set()
for f in glob.glob("mcprepo/src/haxcms_mcp/tools/*.py"):
    mcp_src |= set(re.findall(r"@mcp\.tool\((?:[^()]|\((?:[^()]|\([^()]*\))*\))*\)\s*(?:async\s+)?def\s+(\w+)", open(f).read()))
mcp_saved = set(json.load(open("ext/mcp_tools.json")))
report["inventories"]["mcp tools"] = {"added": sorted(mcp_src - mcp_saved), "gone": sorted(mcp_saved - mcp_src) if mcp_src else []}
# the vocabulary on webcomponents main, not the last released build
code, out = run(["gh", "api", "repos/haxtheweb/webcomponents/contents/elements/user-action/lib/xapi-vocabulary.json", "--jq", ".content"])
if code == 0 and out:
    import base64
    new, old = json.loads(base64.b64decode(out)), json.load(open("ext/xapi-vocabulary.json"))
    report["inventories"]["xapi elements"] = {"added": sorted(set(new) - set(old)), "gone": sorted(set(old) - set(new))}
    if new != old: open("ext/xapi-vocabulary.json", "w").write(json.dumps(new, indent=1))
for b, ws in BUILDERS:
    code, out = run([sys.executable, "-I", os.path.join(HERE, b)])
    report["builders"][b] = "ok" if code == 0 else "failed: " + out[-300:]
after = snapshot()
drift = False
for w in WEBS:
    a, b = before[w], after[w]
    add = {k: b[k] for k in b if k not in a}; gone = {k: a[k] for k in a if k not in b}
    if add or gone: drift = True
    report["webs"][w] = {"added": add, "gone": gone, "tiles": len(b)}
for k, v in report["inventories"].items():
    if v["added"] or v["gone"]: drift = True
ACCEPT = "--accept" in ARGS
if ACCEPT:
    # take the new MCP tools into the saved extract (their API calls are filled in by the next full extract)
    T = json.load(open("ext/mcp_tools.json"))
    for f in glob.glob("mcprepo/src/haxcms_mcp/tools/*.py"):
        src = open(f).read(); mod = os.path.basename(f)[:-3]
        for name in re.findall(r"@mcp\.tool\((?:[^()]|\((?:[^()]|\([^()]*\))*\))*\)\s*(?:async\s+)?def\s+(\w+)", src):
            if name in T: continue
            k = src.index("def " + name); m = re.findall(r'tool_annotations\(\s*"([^"]+)"', src[max(0, k - 400):k])
            T[name] = {"module": mod, "title": m[-1] if m else name.replace("_", " ").capitalize(), "ops": [], "tags": []}
    for name in report["inventories"]["mcp tools"]["gone"]: T.pop(name, None)
    json.dump(T, open("ext/mcp_tools.json", "w"), indent=1)
    run([sys.executable, "-I", os.path.join(HERE, "build_generated.py")])
code, out = run(["node", os.path.join(HERE, "graph-drift.mjs"), "hax-ecosystem.json"] + (["--write"] if ACCEPT else []))
if ACCEPT:
    E = json.load(open("hax-ecosystem.json"))
    keep = {k: {f: n[f] for f in ("version", "status") if f in n} for k, n in E["nodes"].items() if n.get("release")}
    json.dump({"checked": E.get("meta", {}).get("checked", report["checked"]), "nodes": keep}, open("ext/versions.json", "w"), indent=1)
    code = 0
report["versions"] = out[-2000:]
if code != 0: drift = True
report["drift"] = drift
json.dump(report, open("ext/drift-report.json", "w"), indent=1, ensure_ascii=False)
md = [f"# Drift check {report['checked']}", "", "**Drift found.**" if drift else "**No drift.** The generated webs match their sources.", ""]
for w, v in report["webs"].items():
    if v["added"] or v["gone"]:
        md.append(f"## {w} ({v['tiles']} tiles)")
        md += [f"- new: `{k}` {lab}" for k, lab in v["added"].items()] + [f"- gone: `{k}` {lab}" for k, lab in v["gone"].items()] + [""]
for k, v in report["inventories"].items():
    if v["added"] or v["gone"]:
        md.append(f"## {k} (saved extract vs source)")
        md += [f"- in source, not in the extract: `{x}`" for x in v["added"]] + [f"- in the extract, gone from source: `{x}`" for x in v["gone"]] + [""]
bad = {b: s for b, s in report["builders"].items() if s != "ok"}
if bad: md += ["## Builders that failed"] + [f"- {b}: {s}" for b, s in bad.items()] + [""]
md += ["## Versions (graph-drift.mjs)", "", "```", report["versions"], "```"]
open("ext/drift-report.md", "w").write("\n".join(md) + "\n")
print("\n".join(md[:60]))
if "--strict" in ARGS and drift: sys.exit(1)
