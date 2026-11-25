"""The growth data layer (https://github.com/haxtheweb/issues/issues/3409): how HAX's themes, elements and platforms
grew over time, how they reuse each other, and what that reuse saves in bytes. Writes ecosystem/build/data/growth/.

    python3 -I ecosystem/build/build_growth.py [--src DIR]

Reads git history and source, so it needs full-history clones (no file contents for history, the element source
for sizes and imports). It keeps them in DIR (default ecosystem/.work/growth): blobless bare clones of every
repository in the network, and a blobless clone of webcomponents with its element JavaScript checked out. Clones
are reused and fetched on later runs. The Sunday drift run (ecosystem-drift.yml) runs it and reports the diff
without committing; to take it, run it here and commit the result; the hax.cloud build only publishes the committed snapshot (build_data.py), so a build never clones history.

Writes, each with a "meta" block saying when, from which commits and by which definitions:
  repos.json     first commit and commits per month for every repository in the network
  themes.json    every theme built on HAXCMSLitElementTheme: when it appeared, its base, its own code size
  elements.json  every element package: when it appeared, main file size, DDD or not, and what it imports
  payload.json   gzipped size of every file a theme or element loads, which files each one loads, the shared
                 core, and sample visitor journeys
  series.json    monthly series for charts: commits, merged PRs, issues closed, totals of themes, elements and
                 platforms, sites built

Definitions (also written into each file's meta):
  - a theme or element "appeared" when its file first existed at its current path in webcomponents' history;
    a repository's start is its first commit
  - bytes are gzip (level 9) of each file's source on the default branch, file by file, as the unbundled CDN
    serves them; lit, mobx and other third-party code are left out; this is source written, not minified output
  - a file "loads" another through a static import or export; dynamic import() is recorded but not followed
  - the shared core is haxcms-site-builder's static closure plus every module at least 80% of themes load
  - browsers keep one cache per site, so savings between sites apply to sites on the same host
Standard library only.
"""
import argparse, collections, csv, datetime, glob, gzip, json, os, re, subprocess, sys

ECO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(ECO)
OUT = os.path.join(ECO, "build", "data", "growth")
GH = "https://github.com/"
LICENSE = "https://www.apache.org/licenses/LICENSE-2.0"

# the runtimes and tools around the network-bar properties (ecosystem/network.json lists those); key -> repo, label
RUNTIMES = [
    ("haxcms-php", "haxtheweb/haxcms-php", "haxcms-php", "HAXcms on PHP: the original backend."),
    ("haxcms-nodejs", "haxtheweb/haxcms-nodejs", "haxcms-nodejs", "HAXcms on Node.js, kept at parity with PHP."),
    ("haxiam", "haxtheweb/haxiam", "HAXiam", "Many sites on one HAXcms core."),
    ("create", "haxtheweb/create", "HAX CLI", "The hax command: sites, elements and themes from the terminal."),
    ("haxcms-desktop", "haxtheweb/haxcms-desktop", "HAX desktop", "HAX as a desktop app."),
    ("hax11ty", "haxtheweb/hax11ty", "hax11ty", "HAX sites built as static pages with Eleventy."),
    ("haxcms-mcp", "haxtheweb/haxcms-mcp", "haxcms-mcp", "An MCP server so agents can work on HAX sites."),
]
# the contract every platform shares; drawn at the centre of the platforms view
CENTER = ("json-outline-schema", "haxtheweb/json-outline-schema", "site.json", "JSON Outline Schema: the site format every platform reads or writes.")
# sub-properties that live under a network-bar property
EXTRA_PROPS = [("rpg-me", "haxtheweb/rpg-me", "RPG me", "rpg.art.hax.cloud", "art", "Build a character; part of Art.")]
# sample visitor journeys for the cache view: (site, theme tag, [(page, [elements on the page])]); every page also
# uses grid-plate. Edit freely: payload.json recomputes from these.
JOURNEY = [
    ("Course", "clean-one", [("Syllabus", ["media-image", "a11y-collapse"]), ("Unit 1", ["video-player", "self-check"]),
                             ("Quiz", ["multiple-choice", "media-image"])]),
    ("Docs", "clean-two", [("Install", ["a11y-collapse", "editable-table"]), ("Guide", ["stop-note", "media-image", "video-player"])]),
    ("Blog", "journey-theme", [("Post", ["media-image", "citation-element"]), ("Episode", ["audio-player"])]),
    ("Lab", "polaris-invent-theme", [("Team", ["rpg-character", "media-image"]), ("Games", ["multiple-choice", "video-player"])]),
]
BUILDER = "elements/haxcms-elements/lib/core/haxcms-site-builder.js"
THEME_BASE = "HAXCMSLitElementTheme"
SKIP = re.compile(r"/(test|tests|demo|locales|node_modules|dist|build|public)/|\.stories\.js$|/gulpfile|/rollup\.config|/web-test-runner|/web-dev-server")
CLASS = re.compile(r"^(?:export\s+)?class\s+(\w+)\s+extends([\s\S]*?)\{", re.M)
DEFINE = re.compile(r"customElements\.define\(\s*([\w.]+|[\"'][\w-]+[\"'])")
STATIC = re.compile(r"""(?:^|[;\s}])(?:import|export)\s+(?:[^'";]*?\s+from\s+)?["']([^"']+)["']""", re.M)
DYNAMIC = re.compile(r"""import\(\s*["']([^"']+)["']\s*\)""")
DDD = re.compile(r"\bDDD(Super|Pulse)?\b|@haxtheweb/d-d-d/")


def git(repo, *args):
    return subprocess.run(["git", "-C", repo] + list(args), capture_output=True, text=True, check=False).stdout


def sync(src, name, repo, wc=False):
    """a blobless clone with full history; webcomponents also gets its element JavaScript checked out"""
    d = os.path.join(src, name)
    if os.path.isdir(d):
        if not wc:  # a bare clone has no fetch refspec of its own: keep its branches current
            subprocess.run(["git", "-C", d, "config", "remote.origin.fetch", "+refs/heads/*:refs/heads/*"], check=False)
        subprocess.run(["git", "-C", d, "fetch", "-q", "origin"], check=False)
        if git(d, "rev-parse", "--is-shallow-repository").strip() == "true":  # dates need the whole history
            subprocess.run(["git", "-C", d, "fetch", "-q", "--filter=blob:none", "--unshallow", "origin"], check=False)
        if wc:
            subprocess.run(["git", "-C", d, "reset", "-q", "--hard", "origin/HEAD"], check=False)
        return d
    if wc:
        subprocess.run(["git", "clone", "-q", "--filter=blob:none", "--no-checkout", GH + repo, d], check=True)
        pats = "/elements/*/package.json\n/elements/*/*.js\n/elements/*/lib/**/*.js\n"
        subprocess.run(["git", "-C", d, "sparse-checkout", "set", "--no-cone", "--stdin"], input=pats, text=True, check=True)
        subprocess.run(["git", "-C", d, "checkout", "-q"], check=True)
    else:
        r = subprocess.run(["git", "clone", "-q", "--bare", "--filter=blob:none", GH + repo, d], check=False)
        if r.returncode:
            return None
    return d


def first_added(wc, path):
    out = git(wc, "log", "--diff-filter=A", "--format=%ad", "--date=short", "--", path).split()
    return out[-1] if out else None


def monthly(repo):
    months = git(repo, "log", "--all", "--format=%ad", "--date=format:%Y-%m").split()
    first = git(repo, "log", "--all", "--reverse", "--format=%ad", "--date=short").split()
    return (first[0] if first else None), dict(sorted(collections.Counter(months).items()))


class Graph:
    """static import graph of the webcomponents checkout, file by file"""

    def __init__(self, wc):
        self.wc, self.pkg, self.cache, self.size = wc, {}, {}, {}
        for pj in glob.glob(os.path.join(wc, "elements", "*", "package.json")):
            try:
                d = json.load(open(pj))
            except ValueError:
                continue
            self.pkg[d.get("name", "")] = (os.path.relpath(os.path.dirname(pj), wc), d.get("main") or d.get("module") or "")

    def resolve(self, spec, frm):
        if spec.startswith("."):
            p = os.path.normpath(os.path.join(os.path.dirname(frm), spec))
        elif spec.startswith("@haxtheweb/"):
            parts = spec.split("/")
            name, rest = "/".join(parts[:2]), "/".join(parts[2:])
            if name not in self.pkg:
                return None
            d, main = self.pkg[name]
            p = os.path.join(d, rest) if rest else os.path.join(d, main or parts[1] + ".js")
        else:
            return None  # third-party: left out
        if not p.endswith(".js") and os.path.isfile(os.path.join(self.wc, p + ".js")):
            p += ".js"
        return p if os.path.isfile(os.path.join(self.wc, p)) else None

    def deps(self, f):
        if f not in self.cache:
            src = open(os.path.join(self.wc, f), encoding="utf-8", errors="ignore").read()
            st = [self.resolve(m, f) for m in STATIC.findall(src)]
            dy = [self.resolve(m, f) for m in DYNAMIC.findall(src)]
            self.cache[f] = ([x for x in st if x], [x for x in dy if x])
        return self.cache[f]

    def closure(self, entry):
        seen, stack = set(), [entry]
        while stack:
            f = stack.pop()
            if f in seen:
                continue
            seen.add(f)
            stack.extend(self.deps(f)[0])
        return seen

    def gz(self, f):
        if f not in self.size:
            b = open(os.path.join(self.wc, f), "rb").read()
            self.size[f] = (len(b), len(gzip.compress(b, 9)))
        return self.size[f]


def element_main(wc, name):
    try:
        main = json.load(open(os.path.join(wc, "elements", name, "package.json"))).get("main") or name + ".js"
    except ValueError:
        main = name + ".js"
    for p in ("elements/%s/%s" % (name, main), "elements/%s/%s.js" % (name, name)):
        if os.path.isfile(os.path.join(wc, p)):
            return p
    return None


def find_themes(wc):
    """every class whose chain reaches HAXCMSLitElementTheme, and the files that define a tag for one"""
    classes = {}  # class -> (file, parent names)
    for f in glob.glob(os.path.join(wc, "elements", "**", "*.js"), recursive=True):
        rel = os.path.relpath(f, wc)
        if SKIP.search("/" + rel):
            continue
        src = open(f, encoding="utf-8", errors="ignore").read()
        if "extends" not in src:
            continue
        for m in CLASS.finditer(src):
            classes.setdefault(m.group(1), (rel, re.findall(r"[A-Za-z_]\w*", m.group(2)), src))
    themed = {THEME_BASE}
    changed = True
    while changed:
        changed = False
        for c, (rel, parents, _) in classes.items():
            if c not in themed and any(p in themed for p in parents):
                themed.add(c)
                changed = True
    out = []
    for c, (rel, parents, src) in classes.items():
        if c == THEME_BASE or c not in themed or not DEFINE.search(src):
            continue
        if "/app-hax/" in rel or "haxcms-dev-theme" in rel:
            continue  # app shells, not site themes
        tag = os.path.basename(rel)[:-3]
        base = "core" if THEME_BASE in parents else next((p for p in parents if p in themed), "core")
        out.append({"tag": tag, "class": c, "path": rel, "base": base, "family": rel.split("/")[1]})
    return sorted(out, key=lambda t: t["path"])


def month_range(start, end):
    y, m = int(start[:4]), int(start[5:7])
    while (y, m) <= (int(end[:4]), int(end[5:7])):
        yield "%04d-%02d" % (y, m)
        m += 1
        if m > 12:
            y, m = y + 1, 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=os.path.join(ECO, ".work", "growth"))
    args = ap.parse_args()
    os.makedirs(args.src, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    today = datetime.date.today().isoformat()
    wc = sync(args.src, "webcomponents", "haxtheweb/webcomponents", wc=True)
    wc_sha = git(wc, "rev-parse", "HEAD").strip()
    meta = lambda about: {"generated": today, "generator": GH + "haxtheweb/praw/blob/main/ecosystem/build/build_growth.py",
                          "source": {"webcomponents": wc_sha}, "license": LICENSE, "about": about,
                          "issue": GH + "haxtheweb/issues/issues/3409"}

    # ---- repositories: the network-bar properties, their sub-properties, the runtimes and the shared contract
    net = json.load(open(os.path.join(ECO, "network.json")))
    props = []
    for k in net["order"]:
        p = net["properties"][k]
        props.append({"key": p["repo"], "repo": "haxtheweb/" + p["repo"], "kind": "property", "label": p["label"],
                      "url": p.get("url", ""), "color": p.get("color", ""), "purpose": p.get("purpose", ""), "parent": None})
    for key, repo, label, url, parent, purpose in EXTRA_PROPS:
        props.append({"key": key, "repo": repo, "kind": "property", "label": label, "url": "https://" + url,
                      "color": net["properties"][parent].get("color", ""), "purpose": purpose,
                      "parent": net["properties"][parent]["repo"]})
    props += [{"key": k, "repo": r, "kind": "platform", "label": l, "url": "", "color": "", "purpose": pu, "parent": None}
              for k, r, l, pu in RUNTIMES]
    props.append({"key": CENTER[0], "repo": CENTER[1], "kind": "contract", "label": CENTER[2], "url": "", "color": "",
                  "purpose": CENTER[3], "parent": None})
    repos, dirs = [], {}
    for p in props:
        d = wc if p["key"] == "webcomponents" else sync(args.src, p["key"], p["repo"])
        if not d:
            print("growth: skipped", p["repo"], "(not reachable)", file=sys.stderr)
            continue
        dirs[p["key"]] = d
        first, months = monthly(d)
        repos.append(dict(p, first=first, total=sum(months.values()), monthly=months))
    json.dump({"meta": meta("First commit and commits per month (all branches) for every repository in the HAX "
                            "network: the network-bar properties, the runtimes and the site.json contract."),
               "repos": repos}, open(os.path.join(OUT, "repos.json"), "w"), indent=1)

    # ---- themes
    g = Graph(wc)
    themes = find_themes(wc)
    for t in themes:
        t["appeared"] = first_added(wc, t["path"])
        t["bytes"], t["gz"] = g.gz(t["path"])
    homage = next((t for t in themes if t["base"].startswith("Homage")), None)
    family_bases = {}
    if homage:
        hb = os.path.join(os.path.dirname(homage["path"]), "HomageThemeBase.js")
        if os.path.isfile(os.path.join(wc, hb)):
            family_bases["HomageThemeBase"] = {"path": hb, "appeared": first_added(wc, hb), "gz": g.gz(hb)[1],
                                               "classes": [b for b in {t["base"] for t in themes} if b.startswith("Homage")]}
    core_file = "elements/haxcms-elements/lib/core/HAXCMSLitElementTheme.js"
    json.dump({"meta": meta("Every HAXcms theme built on the shared theme core (HAXCMSLitElementTheme): when its file "
                            "appeared, the class it extends ('core' or a family base), and its own code size (bytes "
                            "and gzipped)."),
               "core": {"path": core_file, "appeared": first_added(wc, core_file)},
               "familyBases": family_bases, "themes": sorted(themes, key=lambda t: (t["appeared"] or "", t["path"]))},
              open(os.path.join(OUT, "themes.json"), "w"), indent=1)

    # ---- elements: package-level dependency links from static and dynamic imports
    names = sorted(os.path.basename(os.path.dirname(p)) for p in glob.glob(os.path.join(wc, "elements", "*", "package.json")))
    deps = collections.defaultdict(set)
    for n in names:
        for f in glob.glob(os.path.join(wc, "elements", n, "**", "*.js"), recursive=True):
            rel = os.path.relpath(f, wc)
            if SKIP.search("/" + rel):
                continue
            st, dy = g.deps(rel)
            for x in st + dy:
                q = x.split("/")[1]
                if q != n:
                    deps[n].add(q)
    elements = []
    for n in names:
        mainf = element_main(wc, n)
        if not mainf:
            continue
        src = open(os.path.join(wc, mainf), encoding="utf-8", errors="ignore").read()
        elements.append({"name": n, "package": "@haxtheweb/" + n, "main": mainf,
                         "appeared": first_added(wc, "elements/%s/package.json" % n) or first_added(wc, mainf),
                         "gz": g.gz(mainf)[1], "ddd": bool(DDD.search(src)),
                         "dependsOn": sorted(q for q in deps[n] if q in names)})
    used_by = collections.Counter(q for e in elements for q in e["dependsOn"])
    for e in elements:
        e["usedBy"] = used_by[e["name"]]

    # ---- payload: which files each theme and element loads, and their gzipped sizes
    builder = g.closure(BUILDER)
    tsets = {t["tag"]: g.closure(t["path"]) | builder for t in themes}
    # an element's weight (the Weight lens, https://github.com/haxtheweb/issues/issues/3413): everything its main
    # file loads, and what of that a site with the shared core does not already have; its reach into themes
    # (the Reuse lens): how many themes load at least one of its files
    in_themes = collections.Counter(p for s in tsets.values() for p in {f.split("/")[1] for f in s})
    content = sorted({e for _, _, pages in JOURNEY for _, els in pages for e in els} | {"grid-plate"})
    esets = {n: g.closure(element_main(wc, n)) for n in content if element_main(wc, n)}
    freq = collections.Counter(f for s in tsets.values() for f in s)
    core = set(builder) | {f for f, c in freq.items() if c >= len(tsets) * 0.8}
    files = sorted(set().union(*tsets.values(), *esets.values()), key=lambda f: (-freq[f], f))
    idx = {f: i for i, f in enumerate(files)}
    gzs = lambda S: sum(g.gz(f)[1] for f in S)
    mods = [{"path": f, "package": f.split("/")[1], "bytes": g.gz(f)[0], "gz": g.gz(f)[1], "core": f in core,
             "themesUsing": freq[f]} for f in files]
    first_cl = tsets.get("clean-one", set())
    payload = {
        "meta": meta("What a visitor's browser loads for each theme and element, file by file, and the shared core. "
                     "Bytes are gzip of each file's source, not minified CDN output; third-party code (lit, mobx) "
                     "is left out; static imports are followed from haxcms-site-builder, the theme and each element."),
        "core": {"files": len(core), "gz": gzs(core), "bytes": sum(g.gz(f)[0] for f in core),
                 "definition": "haxcms-site-builder's static closure plus every module at least 80% of themes load"},
        "builder": {"files": len(builder), "gz": gzs(builder)},
        "modules": mods,
        "themes": {k: {"modules": sorted(idx[f] for f in s), "gz": gzs(s), "own": g.gz(next(t["path"] for t in themes if t["tag"] == k))[1],
                       "afterCleanOne": gzs(s - first_cl)} for k, s in sorted(tsets.items())},
        "elements": {k: {"modules": sorted(idx[f] for f in s), "gz": gzs(s)} for k, s in sorted(esets.items())},
        "journeys": {"siteBySite": [{"site": s, "theme": th, "pages": [{"page": p, "elements": els} for p, els in pages]}
                                    for s, th, pages in JOURNEY],
                     "note": "every page also uses grid-plate; moving between pages of one site keeps what is loaded"},
    }
    json.dump(payload, open(os.path.join(OUT, "payload.json"), "w"), separators=(",", ":"))
    for e in elements:
        s = g.closure(e["main"])
        e["load"], e["adds"], e["themes"] = gzs(s), gzs(s - core), in_themes[e["name"]]
    json.dump({"meta": meta("Every element package in webcomponents: when its package.json appeared, its main file's "
                            "gzipped size (gz), whether it builds on DDD, the packages it imports (statically or "
                            "dynamically), how many packages import it (usedBy) and how many themes load any of its "
                            "files (themes); load is the gzipped size of everything its main file loads (static "
                            "imports, third-party code left out) and adds is the part of that outside the shared "
                            "core (payload.json), what it costs a visitor on a site that already has the core. "
                            "History starts in September 2018, when the existing elements were moved into this "
                            "repository."),
               "elements": elements}, open(os.path.join(OUT, "elements.json"), "w"), indent=1)

    # ---- contributors: who connects to the network, when, and how (https://github.com/haxtheweb/issues/issues/3416)
    people = contributors(dirs, today)
    active = people.pop("active")
    people = dict({"meta": meta(people.pop("about"))}, **people)
    json.dump(people, open(os.path.join(OUT, "contributors.json"), "w"), separators=(",", ":"))

    # ---- series: one month axis for every chart
    start = min(r["first"] for r in repos if r["first"])[:7]
    months = list(month_range(start, today[:7]))
    commits = [sum(r["monthly"].get(m, 0) for r in repos) for m in months]
    prs = {r["month"]: int(r["total"]) for r in csv.DictReader(open(os.path.join(ROOT, "impact", "merged-prs-by-month.csv")))}
    vel = list(csv.DictReader(open(os.path.join(ROOT, "impact", "release-velocity.csv"))))
    siip = list(csv.DictReader(open(os.path.join(ROOT, "impact", "siip-timeline.csv"))))

    def issues(m):
        for w in vel:
            if w["start_date"][:7] <= m <= w["end_date"][:7]:
                return round(float(w["issues_per_month"]), 1)
        return None

    def sites(m):
        rows = [r for r in siip if int(r["year"]) <= int(m[:4]) and r.get("sites")]
        return int(rows[-1]["sites"]) if rows else None

    cum = lambda dates: [sum(1 for d in dates if d and d[:7] <= m) for m in months]
    series = {
        "meta": meta("Monthly series on one axis for charts. Commits: every repository in repos.json. Merged PRs, "
                     "issues closed and sites built come from PRAW's impact data (impact/), which is refreshed "
                     "separately and may end earlier than the other series."),
        "months": months,
        "series": [
            {"key": "commits", "label": "Commits per month, all HAX repositories", "values": commits},
            {"key": "prs", "label": "Merged pull requests per month", "values": [prs.get(m) for m in months]},
            {"key": "issues", "label": "Issues closed per month (release-window average)", "values": [issues(m) for m in months]},
            {"key": "elements", "label": "Element packages (running total)", "values": cum([e["appeared"] for e in elements])},
            {"key": "themes", "label": "Themes (running total)", "values": cum([t["appeared"] for t in themes])},
            {"key": "platforms", "label": "Network properties and platforms (running total)",
             "values": cum([r["first"] for r in repos if r["kind"] != "contract"])},
            {"key": "sites", "label": "Sites built with HAX (yearly, SIIP)", "values": [sites(m) for m in months]},
            {"key": "contributors", "label": "Contributors active that month", "values": active.get_series(months)},
            {"key": "people", "label": "Contributors (running total)",
             "values": cum([x["first"] for x in people["people"] if x["kind"] == "person"])},
        ],
    }
    json.dump(series, open(os.path.join(OUT, "series.json"), "w"), indent=1)
    print("growth: %d repos, %d themes, %d elements (%d links), %d modules (core %d files, %d KB gz)"
          % (len(repos), len(themes), len(elements), sum(len(e["dependsOn"]) for e in elements), len(files),
             len(core), payload["core"]["gz"] // 1000))


# ---- contributors

BOT = re.compile(r"\[bot\]|\bbot\b|dependabot|renovate|github-actions|greenkeeper|snyk|semantic-release", re.I)
# commits with no person behind them: a local development container's default identity
NOBODY = re.compile(r"^(ddev-local user|unknown|root|user|your name)$", re.I)
AGENT = re.compile(r"\b(claude|copilot|codex|warp|oz-agent|cursor|devin)\b|@anthropic\.com|@warp\.dev", re.I)
GENERIC = re.compile(r"example\.com$|localhost|\.local$|\.lan$|\.attlocal\.net$|\.$|^root@|^nobody@|users\.noreply\.github\.com$")
NOREPLY = re.compile(r"^(?:\d+\+)?([A-Za-z0-9-]+)@users\.noreply\.github\.com$")
KINDS = ("commits", "opened", "closed")  # the three kinds of contribution counted per month


class Active(dict):
    """month -> set of person ids active that month"""

    def get_series(self, months):
        return [len(self.get(m, ())) for m in months]


def people_tiles():
    """PRAW's main-web people with a GitHub login: login -> (tile id, label)"""
    try:
        nodes = json.load(open(os.path.join(ECO, "web", "hax-ecosystem.json")))["nodes"]
        mmd = open(os.path.join(ECO, "web", "hax-ecosystem.mmd")).read()
    except (OSError, ValueError, KeyError):
        return {}
    labels = dict(re.findall(r"^\s*(\w+)\(\(\"([^\"]+)\"\)\)", mmd, re.M))
    return {n["github"].lower(): (k, labels.get(k, n["github"])) for k, n in nodes.items() if n.get("github")}


def gh_lines(path, jq):
    """every page of a GitHub API list, each item through jq to one tab-separated line; None when gh can't read it.
    Pages are read one at a time, each tried three times, so one dropped connection doesn't lose the list."""
    rows, page = [], 1
    while True:
        for attempt in range(3):
            try:
                r = subprocess.run(["gh", "api", "%s&page=%d" % (path, page), "--jq", '"#\\(length)", (%s)' % jq], capture_output=True,
                                   text=True, timeout=120)
            except (OSError, subprocess.TimeoutExpired) as e:
                r = None
                err = str(e)
            if r is not None and r.returncode == 0:
                break
            err = r.stderr.strip()[-200:] if r is not None else err
        else:
            print("growth: contributors: could not read", path, "page", page, err, file=sys.stderr)
            return None
        lines = r.stdout.splitlines()
        if not lines or lines[0] == "#0":  # an empty page: the list is done
            return rows
        got = [ln.split("\t") for ln in lines[1:] if ln.count("\t") == 1]
        rows += got
        page += 1


def contributors(dirs, today):
    """people who contributed, merged across their git names, emails and GitHub logins, with what they did each month:
    commits to any network repository, issues opened and issues closed in the unified queue (haxtheweb/issues)"""
    parent_of = {}

    def find(x):
        while parent_of.setdefault(x, x) != x:
            parent_of[x] = parent_of[parent_of[x]]
            x = parent_of[x]
        return x

    def union(a, b):
        a, b = find(a), find(b)
        if a != b:
            parent_of[max(a, b)] = min(a, b)

    tiles = people_tiles()
    names = collections.defaultdict(collections.Counter)  # root -> names seen
    commits = []  # (key, month, repo)
    agents = []  # (month, repo): commits an AI agent authored
    for repo, d in dirs.items():
        log = git(d, "log", "--all", "--format=%as|%an|%ae")
        for line in log.splitlines():
            parts = line.split("|", 2)
            if len(parts) != 3:
                continue
            day, name, email = parts[0], parts[1].strip(), parts[2].strip().lower()
            if BOT.search(name) or BOT.search(email) or NOBODY.match(name):
                continue
            if AGENT.search(name) or AGENT.search(email):
                agents.append((day, repo))
                continue
            nk = "n:" + name.lower()
            m = NOREPLY.match(email)
            if m:
                union(nk, "l:" + m.group(1).lower())
            elif not GENERIC.search(email):
                union(nk, "e:" + email)
            if re.fullmatch(r"[A-Za-z0-9-]+", name):  # a name that looks like a login is one
                union(nk, "l:" + name.lower())
            names[nk][name] += 1
            commits.append((nk, day, repo))
    for login, (tile, label) in tiles.items():  # PRAW names who is who, also when git has a longer form of the name
        union("l:" + login, "n:" + label.lower())
        words = label.lower().split()
        for nk in list(names):
            if len(words) >= 2 and nk[2:].split()[:len(words)] == words:
                union("l:" + login, nk)
    issue_rows = {}
    for kind, path, jq in (("opened", "repos/haxtheweb/issues/issues?state=all&per_page=100",
                            '.[] | select(.pull_request | not) | [.user.login, .created_at[:10]] | @tsv'),
                           ("closed", "repos/haxtheweb/issues/issues/events?per_page=100",
                            '.[] | select(.event == "closed" and .actor != null) | [.actor.login, .created_at[:10]] | @tsv')):
        rows = gh_lines(path, jq)
        issue_rows[kind] = rows
        for login, day in rows or []:
            if BOT.search(login) or AGENT.search(login):
                continue
            find("l:" + login.lower())

    people = {}

    def person(key):
        r = find(key)
        if r not in people:
            people[r] = {"monthly": collections.defaultdict(lambda: [0, 0, 0]), "repos": collections.Counter(), "first": None, "firstRepo": None}
        return people[r]

    def add(p, day, i, repo=None):
        p["monthly"][day[:7]][i] += 1
        if repo:
            p["repos"][repo] += 1
        if p["first"] is None or day < p["first"]:
            p["first"], p["firstRepo"] = day, repo or "issues"

    for key, day, repo in commits:
        add(person(key), day, 0, repo)
    for i, kind in ((1, "opened"), (2, "closed")):
        for login, day in issue_rows[kind] or []:
            if not (BOT.search(login) or AGENT.search(login)):
                add(person("l:" + login.lower()), day, i)

    # a stable id and a name for each person: the GitHub login when one is known, else the most used git name
    members = collections.defaultdict(set)
    for k in list(parent_of):
        members[find(k)].add(k)
    out, ids = [], {}
    for r, p in people.items():
        logins = sorted(k[2:] for k in members[r] if k.startswith("l:"))
        login = next((l for l in logins if l in tiles), None) or (min(logins, key=len) if logins else None)
        seen = collections.Counter()
        for k in members[r]:
            seen.update(names.get(k, {}))
        tile = tiles.get(login) if login else None
        shown = tile[1] if tile else (login or (seen.most_common(1)[0][0] if seen else "?"))
        pid = login or re.sub(r"[^a-z0-9]+", "-", shown.lower()).strip("-")
        while pid in ids.values():
            pid += "-2"
        ids[r] = pid
        tot = [sum(v[i] for v in p["monthly"].values()) for i in range(3)]
        out.append({"id": pid, "name": shown, "login": login, "tile": tile[0] if tile else None, "kind": "person",
                    "first": p["first"], "firstRepo": p["firstRepo"], "totals": dict(zip(KINDS, tot)),
                    "monthly": {m: v for m, v in sorted(p["monthly"].items())}, "_repos": p["repos"]})
    # the root: whoever PRAW names as HAX's creator (the "bryan" tile); the drawing grows everyone else out from them
    root = next((x for x in out if x["tile"] == "bryan"), None) or min(out, key=lambda x: x["first"] or "9")
    for x in out:
        x.pop("_repos")
    out.sort(key=lambda x: (x["first"] or "9", x["id"]))
    if agents:
        am = collections.Counter(d[:7] for d, _ in agents)
        out.append({"id": "agents", "name": "AI agents", "login": None, "tile": None, "kind": "agents",
                    "first": min(d for d, _ in agents), "firstRepo": None,
                    "totals": {"commits": len(agents), "opened": 0, "closed": 0},
                    "monthly": {m: [n, 0, 0] for m, n in sorted(am.items())}})
    active = Active()
    for x in out:
        if x["kind"] == "person":
            for m in x["monthly"]:
                active.setdefault(m, set()).add(x["id"])
    sources = {"commits": sorted(dirs), "opened": issue_rows["opened"] is not None, "closed": issue_rows["closed"] is not None}
    return {
        "about": "Everyone who has contributed to the HAX network, by month: commits to any network repository "
                 "(repos.json), and issues opened and closed in the unified queue (haxtheweb/issues). A person's git "
                 "names, emails and GitHub login are merged into one; PRAW's people tiles name who is who. Bots are "
                 "left out. Commits an AI agent authored are counted together as 'AI agents', not as people. "
                 "monthly maps YYYY-MM to [commits, issues opened, issues closed]; first is a person's earliest "
                 "contribution of any kind and firstRepo where it was ('issues' for the queue). root is the network's "
                 "creator, as PRAW's people tiles name them.",
        "root": root["id"], "kinds": list(KINDS), "sources": sources, "people": out, "active": active}


if __name__ == "__main__":
    main()
