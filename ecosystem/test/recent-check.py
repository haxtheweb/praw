"""Checks for ecosystem/build/build_recent.py, with no network: python3 -I ecosystem/test/recent-check.py

- an entry is only kept when its link, date and names match their patterns, from GitHub and from the last snapshot
- text from GitHub is escaped where it enters HTML
- when GitHub can't be read the last snapshot is kept; with neither, the page has its empty state; a rate limit
  part way through keeps what was read and takes the rest from the last snapshot
- a token is sent to api.github.com only, and is in no file the step writes
- run as the build runs it, against a site folder, it writes recent.json and the pages and exits 0 with GitHub off
"""
import importlib.util, io, json, os, subprocess, sys, tempfile, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
STEP = os.path.join(os.path.dirname(HERE), "build", "build_recent.py")
spec = importlib.util.spec_from_file_location("build_recent", STEP)
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)

NASTY = '<script>alert(1)</script> "quoted" & <img src=x onerror=alert(2)>\x00\x1b[31m\n second line'
def pull(repo, n, title="A change", merged="2026-11-20T10:00:00Z", url=None, login="octocat"):
    return {"html_url": url or f"https://github.com/haxtheweb/{repo}/pull/{n}", "title": title, "merged_at": merged, "user": {"login": login}}
def release(repo, tag, name=None):
    return {"html_url": f"https://github.com/haxtheweb/{repo}/releases/tag/{tag}", "tag_name": tag, "name": name or tag, "published_at": "2026-11-19T10:00:00Z", "author": {"login": "octocat"}}
def issue(n, title="An idea"):
    return {"html_url": f"https://github.com/haxtheweb/issues/issues/{n}", "title": title, "created_at": "2026-11-18T10:00:00Z", "user": {"login": "octocat"}}

def github(fail_after=None, code=403, headers=None, previous=None):
    """a stand-in for get_json: answers like the API, then fails every request after fail_after of them"""
    calls = []
    def get(url, token=None):
        if url.startswith("https://hax.cloud/"):
            if previous is None: raise urllib.error.HTTPError(url, 404, "Not Found", {}, io.BytesIO(b""))
            return previous
        calls.append((url, token))
        if fail_after is not None and len(calls) > fail_after:
            if code is None: raise urllib.error.URLError("unreachable")
            raise urllib.error.HTTPError(url, code, "no", headers or {"x-ratelimit-remaining": "0"}, io.BytesIO(b""))
        repo = url.split("/repos/haxtheweb/")[1].split("/")[0] if "/repos/" in url else None
        if "/pulls" in url: return [pull(repo, 7, NASTY), pull(repo, 8, "Never merged", merged=None)]
        if "/releases" in url: return [release(repo, "v1.2.3"), dict(release(repo, "v9"), draft=True)]
        if "/search/issues" in url: return {"items": [issue(11, NASTY), dict(issue(12), pull_request={})]}
        raise AssertionError(url)
    get.calls = calls
    return get

PREVIOUS = {"generated": "2026-11-01T00:00:00Z", "fetched": {"merges": "2026-11-01T00:00:00Z", "releases": "2026-11-01T00:00:00Z", "issues": "not a date"},
            "merges": [{"repo": "lies", "title": "Kept merge", "url": "https://github.com/haxtheweb/praw/pull/1", "date": "2026-10-30T00:00:00Z", "number": 999, "by": "<b>"},
                       {"title": "javascript link", "url": "javascript:alert(1)", "date": "2026-10-30T00:00:00Z"},
                       {"title": "elsewhere", "url": "https://github.com/someone-else/praw/pull/1", "date": "2026-10-30T00:00:00Z"},
                       {"title": "tail", "url": "https://github.com/haxtheweb/praw/pull/1\"><script>", "date": "2026-10-30T00:00:00Z"},
                       {"title": "bad date", "url": "https://github.com/haxtheweb/praw/pull/2", "date": "<script>"}, "junk", None],
            "releases": [{"title": "Kept release", "url": "https://github.com/haxtheweb/create/releases/tag/v1.0.0", "date": "2026-10-29T00:00:00Z"}],
            "issues": [{"title": "Kept issue", "url": "https://github.com/haxtheweb/issues/issues/5", "date": "2026-10-28T00:00:00Z"}]}
REPOS = ["praw", "create"]
ok = 0
def check(cond, what):
    global ok
    if not cond: sys.exit("FAILED: " + what)
    ok += 1

# entries are rebuilt from checked fields
for bad in ["javascript:alert(1)", "https://github.com/someone-else/praw/pull/1", "https://github.com.evil.example/haxtheweb/praw/pull/1",
            "https://github.com/haxtheweb/praw/pull/1/../../x", "https://github.com/haxtheweb/praw/pull/1?x=<script>", "http://github.com/haxtheweb/praw/pull/1", None, 7]:
    check(R.from_github("merges", dict(pull("praw", 1), html_url=bad)) is None, f"a link that is not a haxtheweb pull request is dropped: {bad!r}")
check(R.from_github("merges", pull("praw", 1, merged=None)) is None, "a closed pull request that never merged is dropped")
check("by" not in R.from_github("merges", pull("praw", 1, login="<img>")), "a login that is not a login is dropped")
e = R.from_github("merges", pull("praw", 1, NASTY))
check(e and "\x00" not in e["title"] and "\n" not in e["title"] and "\x1b" not in e["title"] and len(e["title"]) <= 200, "a title is one line of printable text")
check(R.text("x" * 500) == "x" * 200, "a title is cut to 200 characters")

# everything read: lists, escaping, a token only to api.github.com
get = github()
snap = R.snapshot(REPOS, {"tile:main:praw": "praw"}, token="s3cret-token", get=get, now="2026-11-21T00:00:00Z")
check([len(snap[s]) for s in R.SECTIONS] == [2, 2, 1], "merged pull requests, published releases and issues are kept; unmerged, draft and pull-request rows are not")
check(snap["fetched"] == {s: "2026-11-21T00:00:00Z" for s in R.SECTIONS} and snap["kept"] == [], "a full read is dated now and keeps nothing")
check(all(t == "s3cret-token" for u, t in get.calls) and all(u.startswith("https://api.github.com/") for u, t in get.calls), "a full read asks api.github.com only")
check("s3cret-token" not in json.dumps(snap), "the token is not in the snapshot")
page = R.recent_page(snap) + R.tile_section(snap, "praw", "/recent")
for raw in ["<script", "<img", "onerror=alert(2)>", '"quoted"']:
    check(raw not in page, f"text from GitHub is escaped in HTML: {raw}")
check("&lt;script&gt;alert(1)&lt;/script&gt;" in page and "<h2>Merged</h2>" in page and "<h2>Releases</h2>" in page and "<h2>New issues</h2>" in page, "the Recent page has its three lists")
check("<h2>Recent activity</h2>" in R.tile_section(snap, "praw", "/recent") and R.tile_section(snap, "nothing-here", "/recent") == "", "a tile carries its repository's activity, or nothing")

# GitHub unreachable: the last snapshot, checked the same way
snap = R.snapshot(REPOS, {}, get=github(fail_after=0, code=None), now="2026-11-21T00:00:00Z")
check(snap["merges"] == [] and snap["fetched"] == {}, "unreachable and no last snapshot: empty")
check("no recent activity" in R.recent_page(snap), "the empty state is a page, not an error")
def offline_then_previous(url, token=None):
    if url.startswith("https://hax.cloud/"):
        check(token is None, "no token goes to the last snapshot's address")
        return PREVIOUS
    raise urllib.error.URLError("unreachable")
snap = R.snapshot(REPOS, {}, token="s3cret-token", get=offline_then_previous, now="2026-11-21T00:00:00Z")
check([e["title"] for e in snap["merges"]] == ["Kept merge"], "only the last snapshot's well-formed entries are kept")
check(snap["merges"][0] == {"repo": "praw", "title": "Kept merge", "url": "https://github.com/haxtheweb/praw/pull/1", "date": "2026-10-30T00:00:00Z", "number": 1},
      "a kept entry's repository and number come from its link, not from what the snapshot claims")
check(snap["kept"] == ["merges", "releases", "issues"] and snap["fetched"] == {"merges": "2026-11-01T00:00:00Z", "releases": "2026-11-01T00:00:00Z"}, "kept lists keep the date they were read")
check("Read from GitHub on 1 November 2026" in R.recent_page(snap), "the page says when its lists were read")

# rate limited after the first repository's merges: that much is new, the rest is kept
get = github(fail_after=1, previous=PREVIOUS)
snap = R.snapshot(REPOS, {}, get=get, now="2026-11-21T00:00:00Z")
check(len(get.calls) == 2, "a spent rate limit stops the requests")
check({e["repo"] for e in snap["merges"]} == {"praw"} and "Kept release" in [e["title"] for e in snap["releases"]], "a part read stays; the rest comes from the last snapshot")
# one repository GitHub has no answer for is missed alone
def one_missing(url, token=None):
    if "/repos/haxtheweb/create/" in url: raise urllib.error.HTTPError(url, 404, "Not Found", {}, io.BytesIO(b""))
    return github()(url, token)
snap = R.snapshot(REPOS, {}, get=one_missing, now="2026-11-21T00:00:00Z")
check(snap["fetched"]["merges"] == "2026-11-21T00:00:00Z" and {e["repo"] for e in snap["merges"]} == {"praw"}, "a repository with no answer does not hold the others back")

# as the build runs it: a site folder in, recent.json and pages out, exit 0 with GitHub off
with tempfile.TemporaryDirectory() as site:
    os.makedirs(os.path.join(site, "pages", "item-1"))
    open(os.path.join(site, "pages", "item-1", "index.html"), "w").write("<p>Opening.</p>\n")
    json.dump({"page:recent": "recent"}, open(os.path.join(site, "slugs.json"), "w"))
    json.dump({"items": [{"id": "item-1", "slug": "recent", "location": "pages/item-1/index.html"}]}, open(os.path.join(site, "site.json"), "w"))
    env = dict(os.environ, HAX_CLOUD_RECENT="off", GITHUB_TOKEN="s3cret-token")
    run = subprocess.run([sys.executable, "-I", STEP, site], env=env, capture_output=True, text=True)
    check(run.returncode == 0, "the step exits 0 with GitHub off: " + run.stderr[-300:])
    body = open(os.path.join(site, "pages", "item-1", "index.html")).read()
    check(body.startswith("<p>Opening.</p>") and "no recent activity" in body, "the Recent page keeps its opening and gets the empty state")
    out = open(os.path.join(site, "recent.json")).read()
    check(json.loads(out)["merges"] == [] and "s3cret-token" not in out + body + run.stdout + run.stderr, "recent.json is written and the token is nowhere")
    # a site it can't make sense of: reported, exit 0, the site untouched
    open(os.path.join(site, "site.json"), "w").write("not json")
    run = subprocess.run([sys.executable, "-I", STEP, site], env=env, capture_output=True, text=True)
    check(run.returncode == 0 and "recent: skipped" in run.stdout, "any other error is reported and does not stop the build")
print(f"recent-check: {ok} checks passed")
