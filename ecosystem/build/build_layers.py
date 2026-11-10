"""Data for the five layers that need outside facts. Writes ext/layers.json:
  fresh  {web: {node: "YYYY-MM-DD"}}  last commit touching the node's GitHub path
  bus    {web: {node: [names]}}       people with at least 10% of the last 100 commits on that path (bots left out)
  parity {web: {node: {php, nodejs, cli, mcp}}}  for API operations: which surfaces implement or call it
Impact and evidence strength are computed by the player from the webs themselves.
GitHub results are cached in ext/gh_cache.json; delete it to refresh."""
import json, glob, re, subprocess, collections, os, concurrent.futures as cf, yaml
CACHE = "ext/gh_cache.json"
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
RX = re.compile(r"https://github.com/([^/]+/[^/#?]+)(?:/(?:tree|blob)/([^/]+)/([^#?]*))?")
want = collections.defaultdict(dict)  # web -> node -> (repo, branch, path)
for f in sorted(glob.glob("hax-*.json")):
    web = f[4:-5]
    if web == "ecosystem": web = "main"
    try: d = json.load(open(f))
    except Exception: continue
    if not isinstance(d, dict) or "nodes" not in d: continue
    for k, n in d["nodes"].items():
        # only a tile's own code: its repo, code or docs link (not citations, which say where a fact came from)
        urls = [u for lk, u in (n.get("links") or {}).items() if lk in ("repo", "code", "docs")]
        for u in urls:
            m = RX.match(u or "")
            if m and m.group(1) != "haxtheweb/issues":
                path = (m.group(3) or "").rstrip("/")
                want[web][k] = (m.group(1), m.group(2), path); break
# main tiles whose own links point at npm or a site: the code that is them
E = "haxtheweb/webcomponents"
CODE = {"editor": (E, "elements/hax-body"), "dashboard": (E, "elements/app-hax"), "themes": (E, "elements/haxcms-elements/lib/core/themes"), "outline": (E, "elements/outline-designer"),
        "merlin": (E, "elements/super-daemon"), "ddd": (E, "elements/d-d-d"), "components": (E, ""), "haxcms": ("haxtheweb/haxcms-nodejs", ""), "praw": ("haxtheweb/praw", ""),
        "haxschema": ("haxtheweb/hax-schema", ""), "appstore": ("haxtheweb/haxcms-nodejs", "src/lib/HAXAppStoreService.js"), "oerschema": (E, "elements/oer-schema"),
        "importers": ("haxtheweb/haxcms-nodejs", "src/systemRoutes/v1/routes/imports"),
        "skeletons": ("haxtheweb/haxcms-nodejs", "src/coreConfig/skeletons"), "testing": (E, "web-test-runner.config.mjs"), "games": (E, "elements/rpg-character"), "xapi": (E, "elements/user-action"), "security": ("haxtheweb/haxcms-nodejs", "SECURITY.md"), "agents": ("haxtheweb/praw", "skills"), "learnhax": ("haxtheweb/learn", "")}
# OpenAPI is one spec file inside haxcms-nodejs: its commit date says little about the API, so it gets none
for k, (r, p) in CODE.items():
    if k not in want["main"]: want["main"][k] = (r, "main", p)
keys = {f"{r}|{p}" for w in want.values() for (r, b, p) in w.values()}
def fetch(key):
    r, p = key.split("|", 1)
    q = f"repos/{r}/commits?per_page=100" + (f"&path={p}" if p else "")
    try:
        out = subprocess.run(["gh", "api", q], capture_output=True, text=True, timeout=60)
        cs = json.loads(out.stdout)
        if not isinstance(cs, list) or not cs: return key, None
        who = collections.Counter()
        for c in cs:
            a = (c.get("author") or {}).get("login") or c["commit"]["author"]["name"]
            if a and "bot" not in a.lower(): who[a] += 1
        n = sum(who.values()) or 1
        return key, {"date": cs[0]["commit"]["committer"]["date"][:10], "people": [a for a, c in who.most_common() if c / n >= 0.10], "n": len(cs)}
    except Exception as e:
        return key, None
# repos this session's GitHub API can't read: use a local clone's history instead
LOCAL = {"haxtheweb/hax-schema": "hs", "haxtheweb/json-outline-schema": "josrepo", "haxtheweb/haxcms-mcp": "mcprepo", "haxtheweb/learn": "learnrepo"}
for r in ["haxtheweb/hax11ty", "haxtheweb/haxiam", "haxtheweb/haxcms-plugin-examples", "elmsln/elmsln", "btopro/edtechjoker"]: LOCAL[r] = "gitlog/" + r.replace("/", "_")
def local(key):
    r, p = key.split("|", 1); d = LOCAL.get(r)
    if not d or not os.path.isdir(d): return None
    out = subprocess.run(["git", "-C", d, "log", "-100", "--format=%cs|%an"] + (["--", p] if p else []), capture_output=True, text=True).stdout.split("\n")
    rows = [x.split("|", 1) for x in out if "|" in x]
    if not rows: return None
    who = collections.Counter(a for _, a in rows if "bot" not in a.lower()); n = sum(who.values()) or 1
    return {"date": rows[0][0], "people": [a for a, c in who.most_common() if c / n >= 0.10], "n": len(rows)}
for k in list(keys):
    if cache.get(k) is None and k.split("|")[0] in LOCAL: cache[k] = local(k)
todo = [k for k in keys if k not in cache]
print(len(keys), "paths;", len(todo), "to fetch")
with cf.ThreadPoolExecutor(8) as ex:
    for k, v in ex.map(fetch, todo): cache[k] = v
json.dump(cache, open(CACHE, "w"))
SAME = {"Bryan Ollendyke": "btopro"}  # git author names to GitHub logins
AI = {"claude", "copilot", "codex"}  # AI assistants commit too; bus factor counts people
fresh, bus = {}, {}
for web, ns in want.items():
    for k, (r, b, p) in ns.items():
        v = cache.get(f"{r}|{p}")
        if v:
            fresh.setdefault(web, {})[k] = v["date"]
            bus.setdefault(web, {})[k] = list(dict.fromkeys(SAME.get(x, x) for x in v["people"] if x.lower() not in AI))
# parity for API operations: in each backend's spec, implemented by a route handler, called by the CLI, called by the MCP
def ops_of(spec_glob):
    s = {}
    for f in glob.glob(spec_glob, recursive=True):
        y = yaml.safe_load(open(f))
        for pth, ms in (y.get("paths") or {}).items():
            for m, o in ms.items():
                if isinstance(o, dict) and o.get("operationId"): s[o["operationId"]] = pth
    return s
node_ops = ops_of("haxcms-nodejs/src/openapi/*.yaml")
php_ops = ops_of("haxcms-php/system/backend/php/lib/**/openapi/*.yaml")
def corpus(root, exts):
    t = []
    for dp, dn, fn in os.walk(root):
        if "node_modules" in dp or "/.git" in dp or "/build" in dp: continue
        for f in fn:
            if f.endswith(exts):
                try: t.append(open(os.path.join(dp, f), errors="ignore").read())
                except Exception: pass
    return "\n".join(t)
php_src = corpus("haxcms-php/system/backend/php", (".php",))
node_src = corpus("haxcms-nodejs/src/routes", (".js",)) + corpus("haxcms-nodejs/src/systemRoutes", (".js",)) + corpus("haxcms-nodejs/src/lib", (".js",))
cli_src = corpus("createrepo/src", (".js",))
mcp_src = corpus("mcprepo", (".py",))
cli_src += corpus("createrepo/src", (".mjs", ".ts"))
def norm(s): return re.sub(r"\$?\{[^}]*\}?", "{}", s).rstrip("/")
def client_paths(src): return {norm(m) for m in re.findall(r"api/v1/[A-Za-z0-9_/{}$().-]*", src)}
CLI_P, MCP_P = client_paths(cli_src), client_paths(mcp_src)
# the CLI also runs routes in process through haxcms-nodejs' route table
for scope, meth, key in re.findall(r"allRoutes\.(system|site)\.map\.(get|post|patch|put|delete)\[\s*[\"']([^\"']+)", cli_src):
    CLI_P.add("api/v1/" + norm(re.sub(r":\w+", "{}", key.replace("v1/", "", 1))))
def calls(P, path):
    k = norm(path.split("api/v1/", 1)[-1] if "api/v1/" in path else path)
    return ("api/v1/" + k) in P
def tail(p): return re.sub(r"\{[^}]+\}", "", p).rstrip("/").split("/")[-1] or p
parity = {"openapi": {}}
oj = json.load(open("hax-openapi.json"))["nodes"]
for nid, n in oj.items():
    m = re.search(r"operationId (\w+)", n.get("note", ""))
    if not m: continue
    op = m.group(1); path = node_ops.get(op) or php_ops.get(op) or ""
    t = tail(path)
    parity["openapi"][nid] = {
        "php": op in php_ops and (op in php_src or (t and t in php_src)),
        "nodejs": op in node_ops and (op in node_src or (t and t in node_src)),
        "cli": bool(path) and calls(CLI_P, path),
        "mcp": bool(path) and calls(MCP_P, path)}
# release dates, so freshness can flag main changing long after the last release
def release_date(src, version):
    kind, name = src.split(":", 1)
    if kind == "npm":
        out = subprocess.run(["npm", "view", name, "time", "--json"], capture_output=True, text=True, timeout=60).stdout
        try: tm = json.loads(out)
        except Exception: return None
        return (tm.get(version) or tm.get("modified") or "")[:10] or None
    tags = gh_json(f"repos/{name}/tags?per_page=30")
    if not isinstance(tags, list):
        d = LOCAL.get(name)
        if not d or not os.path.isdir(d): return None
        names = subprocess.run(["git", "-C", d, "tag", "--sort=-creatordate"], capture_output=True, text=True).stdout.split()
        tg = next((x for x in names if x.lstrip("v") == (version or "")), names[0] if names else None)
        return subprocess.run(["git", "-C", d, "log", "-1", "--format=%cs", tg], capture_output=True, text=True).stdout.strip() or None if tg else None
    tag = next((x for x in tags if x["name"].lstrip("v") == (version or "")), tags[0] if tags else None)
    if not tag: return None
    c = gh_json(f"repos/{name}/commits/{tag['commit']['sha']}")
    return c["commit"]["committer"]["date"][:10] if c else None
def gh_json(q):
    try: return json.loads(subprocess.run(["gh", "api", q], capture_output=True, text=True, timeout=60).stdout)
    except Exception: return None
EJ = json.load(open("hax-ecosystem.json"))["nodes"]
released = {}
for k, n in EJ.items():
    if n.get("release") and n.get("version"): released[k] = release_date(n["release"], n["version"])
# parts that ship inside the webcomponents release
WC_REL = released.get("ubiquity")
for k, (r, p) in CODE.items():
    if r == E and k not in released and WC_REL: released[k] = WC_REL
released = {k: v for k, v in released.items() if v}
parity["features"] = json.load(open("ext/parity-features.json"))
json.dump({"fresh": fresh, "bus": bus, "parity": parity, "released": {"main": released}}, open("ext/layers.json", "w"), indent=0)
pc = collections.Counter(tuple(v.values()) for v in parity["openapi"].values())
print({w: len(v) for w, v in fresh.items()}); print("parity", len(parity["openapi"]), pc.most_common(6))
