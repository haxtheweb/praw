"""Recent activity on hax.cloud, from a build-time GitHub snapshot (https://github.com/haxtheweb/issues/issues/3387).

Runs after build_site.py, on the site it wrote:

  recent.json                 the snapshot: the latest merged pull requests, releases and new issues across the HAX
                              repositories, and which tiles each repository's activity belongs to
  the Recent page             (ecosystem/site/extra-pages.json lists it; ecosystem/site/pages/recent.html is its
                              hand-written opening) gets the three lists
  each repository's tile page gets that repository's own merges and releases: a tile whose `repo` link, or whose
                              `release: git:…`, is a haxtheweb repository. Where more than three tiles of one web
                              share a repository (the CLI's commands), none of them repeat it.

The repositories are the ones the webs and ecosystem/network.json name. Everything is read from the public
GitHub REST API with no account. GITHUB_TOKEN (or HAX_CLOUD_GITHUB_TOKEN), when the build has one, only raises
the rate limit.

Invariants:
- The build never fails here. When GitHub can't be reached or the rate limit is spent, each part that could not be
  read is kept from the last published snapshot (https://hax.cloud/recent.json); with no snapshot either, the page
  says there is nothing to show. Any other error is reported and leaves the site as build_site.py wrote it.
- No credential reaches the output: a token is sent to api.github.com as a request header and nowhere else,
  redirects are refused, and nothing read from the environment is written to a file.
- Text from GitHub is data. Every entry is rebuilt from checked fields (a link has to be a github.com/haxtheweb
  pull request, issue or release address; names and dates have to match their patterns), from GitHub or from the
  last snapshot alike, and every value is escaped where it enters HTML.

Usage: python3 -I ecosystem/build/build_recent.py <site folder>
HAX_CLOUD_RECENT=off skips the network (the last snapshot is not read either): an empty Recent page."""
import datetime, html, json, os, re, sys, time, traceback, urllib.error, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ECO = os.path.dirname(HERE)
ORG = "haxtheweb"
API = "https://api.github.com"
PREVIOUS = "https://hax.cloud/recent.json"
PAGE_KEY = "page:recent"
PER_REPO, SHOWN, SHOWN_ON_TILE = 20, 40, 5  # read per repository; listed on the Recent page; listed on a tile's page
SHARED_MAX = 3  # more tiles than this sharing one repository in one web: none of them carry its activity
MAX_BYTES = 4 * 1024 * 1024
DEADLINE = 90  # seconds for every request together; what is left unread is kept from the last snapshot
E = html.escape

REPO_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,99}")
LOGIN = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}(\[bot\])?")
STAMP = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
ROOT_URL = re.compile(r"https://github\.com/haxtheweb/([A-Za-z0-9][A-Za-z0-9._-]{0,99}?)(?:\.git)?/?")
ENTRY_URL = {
    "merges": re.compile(r"https://github\.com/haxtheweb/([A-Za-z0-9][A-Za-z0-9._-]{0,99})/pull/(\d{1,9})"),
    "issues": re.compile(r"https://github\.com/haxtheweb/([A-Za-z0-9][A-Za-z0-9._-]{0,99})/issues/(\d{1,9})"),
    "releases": re.compile(r"https://github\.com/haxtheweb/([A-Za-z0-9][A-Za-z0-9._-]{0,99})/releases/tag/([A-Za-z0-9][A-Za-z0-9._+-]{0,99})"),
}
SECTIONS = ("merges", "releases", "issues")


def text(v, limit=200):
    """one line of plain text: no control characters, runs of space collapsed, cut to limit"""
    if not isinstance(v, str): return ""
    v = "".join(c if c.isprintable() else " " for c in v)
    return " ".join(v.split())[:limit]


def entry(section, raw):
    """a snapshot entry rebuilt from checked fields, or None; raw is one already in snapshot form"""
    if not isinstance(raw, dict): return None
    url, date = raw.get("url"), raw.get("date")
    m = ENTRY_URL[section].fullmatch(url) if isinstance(url, str) else None
    if not m or not isinstance(date, str) or not STAMP.fullmatch(date): return None
    title = text(raw.get("title"))
    if not title: return None
    out = {"repo": m.group(1), "title": title, "url": url, "date": date}
    if section == "releases": out["tag"] = m.group(2)
    else: out["number"] = int(m.group(2))
    by = raw.get("by")
    if isinstance(by, str) and LOGIN.fullmatch(by): out["by"] = by
    return out


def from_github(section, item):
    """one GitHub API object (a pull request, release or issue) as a snapshot entry, or None"""
    if not isinstance(item, dict): return None
    user = item.get("user") if isinstance(item.get("user"), dict) else item.get("author") if isinstance(item.get("author"), dict) else {}
    raw = {"url": item.get("html_url"), "by": user.get("login")}
    if section == "merges":
        raw.update(title=item.get("title"), date=item.get("merged_at"))  # a closed pull request that never merged has no date
    elif section == "releases":
        if item.get("draft"): return None
        raw.update(title=item.get("name") or item.get("tag_name"), date=item.get("published_at"))
    else:
        if "pull_request" in item: return None
        raw.update(title=item.get("title"), date=item.get("created_at"))
    return entry(section, raw)


# ---------- which repositories, and whose tiles they are ----------
def webs():
    """[(web id, mmd text, details)] in assemble.py's order"""
    order = re.findall(r'\("(\w+)","(hax-[\w-]+)"\)', open(os.path.join(HERE, "assemble.py")).read())
    out = []
    for w, f in order:
        base = os.path.join(ECO, "web", f)
        if os.path.exists(base + ".json") and os.path.exists(base + ".mmd"):
            out.append((w, open(base + ".mmd").read(), json.load(open(base + ".json"))))
    return out


def repo_of(node):
    """the haxtheweb repository a tile is, or None: its `repo` link when that is a repository's own address, or its git release"""
    if not isinstance(node, dict): return None
    link = (node.get("links") or {}).get("repo") if isinstance(node.get("links"), dict) else None
    m = ROOT_URL.fullmatch(link) if isinstance(link, str) else None
    if m: return m.group(1)
    rel = node.get("release")
    if isinstance(rel, str) and rel.startswith(f"git:{ORG}/") and REPO_NAME.fullmatch(rel[len(ORG) + 5:]): return rel[len(ORG) + 5:]
    return None


def tiles_and_repos(slugs):
    """({page key: repository}, [repositories]): the pages that carry a repository's activity, and every repository to read"""
    pages, repos = {}, []
    def want(r):
        if r and REPO_NAME.fullmatch(r) and r not in repos: repos.append(r)
    for w, mmd, data in webs():
        opens = dict(re.findall(r"^\s*%%@ node (\w+) .*?\bweb=(\w+)", mmd, re.M))
        mine = {}
        for nid, node in (data.get("nodes") or {}).items():
            r = repo_of(node)
            if r: mine[nid] = r; want(r)
        count = {}
        for r in mine.values(): count[r] = count.get(r, 0) + 1
        for nid, r in mine.items():
            if count[r] > SHARED_MAX: continue
            # the tile's own page, or the page of the web it opens
            key = f"tile:{w}:{nid}" if f"tile:{w}:{nid}" in slugs else f"web:{opens[nid]}" if nid in opens and f"web:{opens[nid]}" in slugs else None
            if key: pages.setdefault(key, r)
    net = os.path.join(ECO, "network.json")
    if os.path.exists(net):
        for p in (json.load(open(net)).get("properties") or {}).values():
            if isinstance(p, dict) and isinstance(p.get("repo"), str): want(p["repo"])
    want("issues")
    return pages, repos


# ---------- reading GitHub ----------
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None  # a request's headers never follow a redirect to another host


OPENER = urllib.request.build_opener(NoRedirect)


class Spent(Exception):
    """the rate limit is used up, or GitHub can't be reached: stop asking"""


def get_json(url, token=None):
    headers = {"User-Agent": "hax-cloud-site-build", "Accept": "application/json"}
    if url.startswith(API + "/"):
        headers.update({"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"})
        if token: headers["Authorization"] = "Bearer " + token
    with OPENER.open(urllib.request.Request(url, headers=headers), timeout=15) as r:
        return json.loads(r.read(MAX_BYTES + 1)[:MAX_BYTES].decode("utf-8", "replace"))


def read_github(repos, token=None, get=get_json):
    """({section: {repo: [entries]}}, [what could not be read as (section, repo)], {sections cut short}); issues are
    one org-wide unit, repo None. A section is cut short when GitHub stopped answering before it was read; one
    repository GitHub has no answer for (moved, private) is missed without that."""
    got, missed, short = {s: {} for s in SECTIONS}, [], set()
    start, stopped = time.monotonic(), None
    units = [("merges", r, f"{API}/repos/{ORG}/{r}/pulls?state=closed&sort=updated&direction=desc&per_page={PER_REPO}") for r in repos]
    units.append(("issues", None, f"{API}/search/issues?q={urllib.parse.quote(f'org:{ORG} is:issue')}&sort=created&order=desc&per_page={SHOWN}"))
    units += [("releases", r, f"{API}/repos/{ORG}/{r}/releases?per_page=5") for r in repos]
    for section, r, url in units:
        if stopped or time.monotonic() - start > DEADLINE:
            stopped = stopped or "out of time"; missed.append((section, r)); short.add(section); continue
        try:
            data = get(url, token)
            rows = data.get("items") if section == "issues" and isinstance(data, dict) else data
            if not isinstance(rows, list): raise ValueError("not a list")
            got[section][r] = [e for e in (from_github(section, x) for x in rows) if e]
        except urllib.error.HTTPError as e:
            missed.append((section, r))
            h = e.headers or {}
            if section == "issues": short.add(section)
            # out of requests (or a token GitHub refuses): every later request would get the same answer
            if e.code in (401, 429) or (e.code == 403 and (h.get("x-ratelimit-remaining") == "0" or h.get("retry-after"))):
                stopped = f"GitHub answered {e.code}: the rate limit is spent"; short.add(section)
            # anything else (404, a 403 on one repository, a refused redirect): only this one is missed
            else: print(f"recent: no {section} for {r or ORG} (GitHub answered {e.code})")
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            missed.append((section, r)); short.add(section); stopped = f"GitHub can't be reached ({type(e).__name__})"
        except (ValueError, UnicodeError):
            missed.append((section, r))
            if section == "issues": short.add(section)
    if stopped: print("recent:", stopped)
    return got, missed, short


def read_previous(get=get_json):
    """the last published snapshot's entries, rebuilt from checked fields, or None"""
    url = os.environ.get("HAX_CLOUD_RECENT_PREVIOUS", PREVIOUS)
    if not url.startswith("https://"): return None
    try: old = get(url)
    except Exception as e:
        print(f"recent: no earlier snapshot ({type(e).__name__})"); return None
    if not isinstance(old, dict): return None
    out = {s: [e for e in (entry(s, x) for x in (old.get(s) if isinstance(old.get(s), list) else [])) if e] for s in SECTIONS}
    out["fetched"] = {s: v for s, v in (old.get("fetched") if isinstance(old.get("fetched"), dict) else {}).items() if s in SECTIONS and isinstance(v, str) and STAMP.fullmatch(v)}
    return out


def snapshot(repos, pages, token=None, get=get_json, offline=False, now=None):
    """the snapshot to publish: what GitHub gave, with each part it did not give kept from the last snapshot"""
    now = now or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if offline: got, missed, short = {s: {} for s in SECTIONS}, [(s, None) for s in SECTIONS], set(SECTIONS)
    else: got, missed, short = read_github(repos, token, get)
    prev = read_previous(get) if missed and not offline else None
    snap = {"about": "Recent activity across the HAX repositories, read from the public GitHub API when hax.cloud was built. "
                     "fetched says when each list was last read in full; a list GitHub would not give is kept from the last snapshot.",
            "generated": now, "fetched": {}, "kept": [], "repos": [f"{ORG}/{r}" for r in repos], "pages": pages}
    for s in SECTIONS:
        rows = [e for es in got[s].values() for e in es]
        lost = [r for sec, r in missed if sec == s]
        if lost and prev:
            # the last snapshot's entries for exactly the repositories that could not be read (all of them, for issues)
            kept = [e for e in prev[s] if s == "issues" or None in lost or e["repo"] in lost]
            if kept: snap["kept"].append(s)
            rows += kept
        seen, uniq = set(), []
        for e in sorted(rows, key=lambda e: e["date"], reverse=True):
            if e["url"] not in seen: seen.add(e["url"]); uniq.append(e)
        cap = SHOWN if s == "issues" else PER_REPO * max(1, len(repos))
        snap[s] = uniq[:cap]
        if s not in short: snap["fetched"][s] = now
        elif prev and prev["fetched"].get(s): snap["fetched"][s] = prev["fetched"][s]
    return snap


# ---------- the pages ----------
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
def day(stamp): return f"{int(stamp[8:10])} {MONTHS[int(stamp[5:7]) - 1]} {stamp[:4]}"


def line(section, e, with_repo=True):
    ref = e["tag"] if section == "releases" else f"#{e['number']}"
    if ref.lstrip("v") == e["title"].lstrip("v"): ref = ""  # a release named after its tag
    where = ", ".join(x for x in (f"{e['repo']} {ref}".strip() if with_repo else ref, day(e["date"])) if x)
    return f'<li><a href="{E(e["url"], quote=True)}">{E(e["title"])}</a> ({E(where)})</li>'


def listing(section, rows, with_repo=True): return "<ul>" + "".join(line(section, e, with_repo) for e in rows) + "</ul>"


def recent_page(snap):
    if not any(snap[s] for s in SECTIONS):
        return (f'<p>There is no recent activity to show right now. Everything HAX is working on is at '
                f'<a href="https://github.com/{ORG}">github.com/{ORG}</a>, and the issue queue is at '
                f'<a href="https://github.com/{ORG}/issues/issues">{ORG}/issues</a>.</p>')
    read = sorted(snap["fetched"].values())
    out = [f"<p>Read from GitHub on {E(day(read[0]))}.</p>" if read else ""]
    for s, title in (("merges", "Merged"), ("releases", "Releases"), ("issues", "New issues")):
        if snap[s]: out.append(f"<h2>{title}</h2>" + listing(s, snap[s][:SHOWN]))
    return "\n".join(x for x in out if x)


def tile_section(snap, repo, recent_href):
    merges = [e for e in snap["merges"] if e["repo"] == repo][:SHOWN_ON_TILE]
    releases = [e for e in snap["releases"] if e["repo"] == repo][:SHOWN_ON_TILE]
    if not merges and not releases: return ""
    out = ["<h2>Recent activity</h2>"]
    if releases: out.append("<h3>Releases</h3>" + listing("releases", releases, False))
    if merges: out.append("<h3>Merged</h3>" + listing("merges", merges, False))
    out.append(f'<p><a href="{E(recent_href, quote=True)}">Recent activity across HAX</a></p>')
    return "\n".join(out)


def page_file(site, items, slug):
    """the HTML file of the page at slug, inside the site, or None"""
    it = next((i for i in items if i.get("slug") == slug), None)
    loc = it.get("location") if it else None
    if not isinstance(loc, str) or not re.fullmatch(r"pages/[A-Za-z0-9-]+/index\.html", loc): return None
    p = os.path.join(site, loc)
    return p if os.path.isfile(p) else None


def main(site):
    slugs = json.load(open(os.path.join(site, "slugs.json")))
    items = json.load(open(os.path.join(site, "site.json")))["items"]
    pages, repos = tiles_and_repos(slugs)
    token = os.environ.get("HAX_CLOUD_GITHUB_TOKEN") or os.environ.get("GITHUB_TOKEN") or None
    snap = snapshot(repos, pages, token, offline=os.environ.get("HAX_CLOUD_RECENT", "").lower() == "off")
    # everything is worked out before anything is written
    writes = []
    recent = page_file(site, items, slugs.get(PAGE_KEY, "")) if PAGE_KEY in slugs else None
    if recent: writes.append((recent, recent_page(snap)))
    else: print("recent: no Recent page in the site (ecosystem/site/extra-pages.json)")
    recent_href = "/" + slugs[PAGE_KEY] if recent else f"https://github.com/{ORG}"
    carried = 0
    for key, repo in pages.items():
        f, sec = page_file(site, items, slugs[key]), tile_section(snap, repo, recent_href)
        if f and sec: writes.append((f, sec)); carried += 1
    for f, more in writes:
        with open(f, "a") as fh: fh.write(more + "\n")
    with open(os.path.join(site, "recent.json"), "w") as fh: json.dump(snap, fh, indent=1, ensure_ascii=False)
    print(f"recent: {len(snap['merges'])} merges, {len(snap['releases'])} releases, {len(snap['issues'])} issues from {len(repos)} repositories; "
          f"{carried} tile pages carry their own" + (f"; kept from the last snapshot: {', '.join(snap['kept'])}" if snap["kept"] else ""))


if __name__ == "__main__":
    if len(sys.argv) != 2: sys.exit("usage: build_recent.py <site folder>")
    try: main(sys.argv[1])
    except Exception:
        # the Recent page is an extra: the site still publishes without it
        traceback.print_exc()
        print("recent: skipped; the site is as build_site.py wrote it")
