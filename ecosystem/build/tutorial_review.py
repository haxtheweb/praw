"""Which Learn HAX tutorials to look at again when code changes (https://github.com/haxtheweb/issues/issues/2946).

The ecosystem web already holds both halves: the tutorials web says what each tutorial teaches (a `teaches` line
from the tutorial to a tile, written by build_tutorials.py), and a tile says where its code lives (its repo, code,
source or docs link on GitHub, or its entry in build/data/concept-code.json). This joins them: a changed path
inside a tile's code names the tutorials that teach that tile, with the screencast to re-record when there is one.

  python3 -I ecosystem/build/tutorial_review.py webcomponents:elements/super-daemon/super-daemon.js
  git diff --name-only v1..v2 | python3 -I ecosystem/build/tutorial_review.py --repo webcomponents -
  python3 -I ecosystem/build/tutorial_review.py --since "7 days ago"     every clone in ecosystem/.work (sources.sh)
  python3 -I ecosystem/build/tutorial_review.py --map                    the whole record: tile, code, tutorials

A change is `<repository>:<path>` (the repository's name in haxtheweb), or a bare path with --repo. A tile whose
code is a whole repository (Web components) would name its tutorials on every change there, so those only count
with --whole-repos. --json prints the result as JSON. Nothing is written and nothing outside this repo is read,
except `git log` in the clones --since names. Paths and names are only ever compared, never run."""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ECO = os.path.dirname(HERE)
WEB = os.path.join(ECO, "web")
GITHUB = re.compile(r"https://github\.com/haxtheweb/([A-Za-z0-9][A-Za-z0-9._-]*)(?:/(?:tree|blob)/[^/#?]+/?([^#?]*))?/?")
CLONES = {"haxcms-nodejs": "haxcms-nodejs", "haxcms-php": "haxcms-php", "createrepo": "create", "mcprepo": "haxcms-mcp", "hs": "hax-schema",
          "josrepo": "json-outline-schema", "learnrepo": "learn", "wcrepo": "webcomponents"}  # sources.sh folder -> repository


def web_file(web): return os.path.join(WEB, "hax-ecosystem" if web == "main" else "hax-" + web)


def code_of(web, node, details, record):
    """(repository, path) for a tile, or None: its own GitHub link first, then the record for main-web tiles"""
    links = (details.get(node) or {}).get("links") or {}
    for key in ("repo", "code", "source", "docs"):
        m = GITHUB.fullmatch(links.get(key) or "") if isinstance(links.get(key), str) else None
        if m and m.group(1) != "issues": return m.group(1), (m.group(2) or "").strip("/")
    if web == "main" and node in record:
        repo, path = record[node]
        return repo.split("/", 1)[-1], path.strip("/")
    return None


def build_map():
    """[{tile, web, label, code: [repo, path] or None, tutorials: [{id, title, page, video}]}] for every tile a tutorial teaches"""
    mmd = open(web_file("tutorials") + ".mmd").read()
    tut = json.load(open(web_file("tutorials") + ".json"))["nodes"]
    titles = dict(re.findall(r'^\s+(\w+)[\[\(\{>]+"([^"]*)"', mmd, re.M))
    home = {}
    for nid, rest in re.findall(r"^\s*%%@ node (\w+) (.*)$", mmd, re.M):
        for tok in rest.split():
            if tok == "portal": home[nid] = "main"
            elif tok.startswith("portal="): home[nid] = tok[7:]
    record = json.load(open(os.path.join(HERE, "data", "concept-code.json")))["main"]
    details, labels, out = {}, {}, {}
    for t, c in re.findall(r"^\s+(\w+) -->\|teaches\| (\w+)\s*$", mmd, re.M):
        web = home.get(c, "main")
        if web not in details:
            try:
                details[web] = json.load(open(web_file(web) + ".json")).get("nodes", {})
                labels[web] = dict(re.findall(r'^\s+(\w+)[\[\(\{>]+"([^"]*)"', open(web_file(web) + ".mmd").read(), re.M))
            except (OSError, ValueError): details[web], labels[web] = {}, {}
        row = out.setdefault((web, c), {"tile": c, "web": web, "label": labels[web].get(c, c), "code": None, "tutorials": []})
        code = code_of(web, c, details[web], record)
        row["code"] = list(code) if code else None
        links = (tut.get(t) or {}).get("links") or {}
        row["tutorials"].append({"id": t, "title": titles.get(t, t), "page": links.get("page"), "video": links.get("video")})
    return list(out.values())


def review(rows, changes, whole_repos=False):
    """{tutorial id: {title, page, video, because: [{tile, label, paths}]}} for the changes [(repository, path)]"""
    hits = {}
    for row in rows:
        if not row["code"]: continue
        repo, path = row["code"]
        if not path and not whole_repos: continue
        touched = sorted({p for r, p in changes if r == repo and (not path or p == path or p.startswith(path + "/"))})
        if not touched: continue
        for t in row["tutorials"]:
            h = hits.setdefault(t["id"], {"title": t["title"], "page": t["page"], "video": t["video"], "because": []})
            h["because"].append({"tile": row["tile"], "label": row["label"], "paths": [f"{repo}:{p}" for p in touched]})
    return hits


def changed_since(since, work):
    """[(repository, path)] changed since `since` in the clones sources.sh keeps in the working folder"""
    out = []
    for folder, repo in CLONES.items():
        d = os.path.join(work, folder)
        if not os.path.isdir(os.path.join(d, ".git")): continue
        r = subprocess.run(["git", "-C", d, "log", "--since=" + since, "--name-only", "--format="], capture_output=True, text=True)
        out += [(repo, p.strip()) for p in r.stdout.splitlines() if p.strip()]
    return out


def main(argv):
    opts = {"--json": False, "--map": False, "--whole-repos": False}
    repo = since = None
    work = os.path.join(ECO, ".work")
    changes, args = [], list(argv)
    while args:
        a = args.pop(0)
        if a in opts: opts[a] = True
        elif a in ("--repo", "--since", "--work") and args:
            v = args.pop(0)
            if a == "--repo": repo = v.split("/")[-1]
            elif a == "--since": since = v
            else: work = v
        elif a == "-": changes += [(repo, ln.strip()) for ln in sys.stdin if ln.strip()] if repo else sys.exit("- needs --repo <repository> first")
        elif ":" in a and not a.startswith("-"): changes.append(tuple(a.split(":", 1)))
        elif repo and not a.startswith("-"): changes.append((repo, a))
        else: sys.exit(__doc__)
    rows = build_map()
    if opts["--map"]:
        print(json.dumps(rows, indent=1, ensure_ascii=False)); return
    if since: changes += changed_since(since, work)
    changes = [(r.split("/")[-1], p[2:] if p.startswith("./") else p) for r, p in changes]
    hits = review(rows, changes, opts["--whole-repos"])
    unmapped = sorted({f"{r['web']}:{r['tile']}" for r in rows if not r["code"]})
    if opts["--json"]:
        print(json.dumps({"changes": len(changes), "review": hits, "no_code_on_record": unmapped}, indent=1, ensure_ascii=False)); return
    print(f"# Tutorials to review ({len(changes)} changed paths)\n")
    if not hits: print("None: no changed path is inside the code of a tile a tutorial teaches.\n")
    for h in sorted(hits.values(), key=lambda h: h["title"]):
        print(f"- **{h['title']}**: {h['page'] or 'no page on record'}" + (f" (screencast: {h['video']})" if h["video"] else ""))
        for b in h["because"]:
            print(f"  - teaches {b['label']} (`{b['tile']}`); changed: " + ", ".join(f"`{p}`" for p in b["paths"][:5]) + (f" and {len(b['paths']) - 5} more" if len(b["paths"]) > 5 else ""))
    if unmapped:
        print("\n## Taught tiles with no code on record\n\nA change to these can't be traced to a tutorial until the tile links its code or build/data/concept-code.json names it:\n")
        print(", ".join(f"`{u}`" for u in unmapped))


if __name__ == "__main__": main(sys.argv[1:])
