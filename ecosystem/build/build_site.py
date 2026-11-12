"""Build the hax.cloud HAXsite from the ecosystem webs (phase 1 of https://github.com/haxtheweb/issues/issues/3310).

Reads the same webs assemble.py does (web/*.mmd + web/*.json, in assemble.py's order) and writes a static HAXsite:

  site.json        JSON Outline Schema: the main web is the home page, each sub-web a page nested under the web
                   that opens it, each tile a page under the web that owns it, and a Tours branch.
  pages/<id>/      one index.html per page: generated HAX page HTML (description, links, what it connects to).
  ecosystem.html   today's player, embedded on every web page until <ecosystem-web> replaces it (phase 2).
  ecosystem-webs.json  the bundle <ecosystem-web> loads: every web's source, the slugs and the tile art.

Slugs are readable and nested (hax.cloud/penn-state/strategic-plan/aa-plan). A tile drawn as a portal in another web
is not a second page: links to it go to its page in the web that owns it. Hand-written pages live in
ecosystem/site/pages/<slug>.html; when one exists its HTML goes above the generated content of that page.

Usage (from ecosystem/.work, after assemble.py): python3 -I ../build/build_site.py <out-dir> <player.html>
The HAXcms boilerplate (index.html, build.js, 404.html …) is copied in by the workflow, not here."""
import json, os, re, sys, uuid, html, time, shutil
OUT, PLAYER = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
ECO = os.path.dirname(HERE)
AUTHORED = os.path.join(ECO, "site", "pages")
NS = uuid.UUID("6f1d2c3a-0b8e-4c55-9a7e-1a2b3c4d5e6f")  # fixed namespace for page ids
def iid(key): return "item-" + str(uuid.uuid5(NS, key))  # stable ids: the same tile keeps its page id across builds
def slug(s):
    s = re.sub(r"&", " and ", s.lower())
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:60] or "page"
E = html.escape

# ---------- read the webs in assemble.py's order ----------
order = re.findall(r'\("(\w+)","(hax-[\w-]+)"\)', open(os.path.join(HERE, "assemble.py")).read())
ANS = json.load(open("gap-answers.json"))
WEBS = {}
TILE = r'^\s+(\w+)[\[\(\{>/\\]+(?:"([^"]*)"|([^\]\)\}"]*))'
for w, f in order:
    m = open(f + ".mmd").read(); D = json.load(open(f + ".json"))
    for nid, v in ANS.get(w, {}).items():
        D["nodes"].setdefault(nid, {}).update({k: x for k, x in v.items() if k not in ("confirmed", "skip")})
    tiles, group, groups = {}, None, []
    for ln in m.splitlines():
        g = re.match(r'^\s*subgraph (\w+) \["([^"]*)"\]', ln)
        if g: group = g.group(2); groups.append(group); continue
        if re.match(r"^\s*end\s*$", ln): group = None; continue
        t = re.match(TILE, ln)
        if t and group is not None and not ln.strip().startswith("%%"): tiles[t.group(1)] = {"label": (t.group(2) if t.group(2) is not None else t.group(3) or "").strip() or t.group(1), "group": group}
    meta = {}
    for ln in re.findall(r"^\s*%%@ node (\w+) (.*)$", m, re.M):
        nid, rest = ln
        d = meta.setdefault(nid, {})
        for tok in rest.split():
            k, _, v = tok.partition("=")
            d[k] = v if _ else True
    edges = re.findall(r"^\s+(\w+) ([-=.o>]+)\|([^|]+)\| (\w+)", m, re.M)
    WEBS[w] = {"tiles": tiles, "meta": meta, "edges": edges, "data": D, "groups": groups}

# ---------- which tile is whose: owners, portals, and the tile that opens each web ----------
opens = {}  # web id -> (web, tile) that opens it
for w, W in WEBS.items():
    for nid, d in W["meta"].items():
        if d.get("web") and d["web"] in WEBS and d["web"] != w and d["web"] not in opens: opens[d["web"]] = (w, nid)
def is_portal(w, nid):
    d = WEBS[w]["meta"].get(nid, {})
    return "portal" in d
def portal_home(w, nid):
    d = WEBS[w]["meta"].get(nid, {})
    p = d.get("portal")
    return "main" if p is True else p

# ---------- the outline ----------
items, page_of = [], {}  # page_of[(web, tile)] = item id; page_of[("web", w)] = item id
def web_name(w): return WEBS[w]["data"].get("meta", {}).get("name") or ("Ecosystem web" if w == "main" else w)
def web_parent(w):
    p = WEBS[w]["data"].get("meta", {}).get("parent")
    if p in WEBS and p != w: return p
    if w in opens: return opens[w][0]
    return "main" if w != "main" else None
def add(key, title, parent, slugpath, desc="", order=0):
    i = iid(key)
    items.append({"id": i, "indent": 0, "location": f"pages/{i}/index.html", "slug": slugpath, "order": order, "parent": parent,
                  "title": title, "description": desc[:200], "metadata": {"created": int(time.time()), "updated": int(time.time()), "published": True}, "_key": key})
    return i
web_slug, used = {}, set()
def unique(path):
    p, n = path, 2
    while p in used: p, n = f"{path}-{n}", n + 1
    used.add(p); return p
# webs, parents before children
done = set()
def place_web(w, depth=0):
    if w in done: return
    par = web_parent(w)
    if par and par not in done: place_web(par)
    done.add(w)
    if w == "main":
        web_slug[w] = ""
        page_of[("web", w)] = add("web:main", "Ecosystem web", None, unique("ecosystem"), WEBS[w]["data"].get("meta", {}).get("about", ""), 0)
        return
    base = web_slug[par] if par else ""
    nm = web_name(w)
    own = WEBS[w]["data"].get("meta", {}).get("slug")  # a web may name its own slug (meta.slug)
    if not own:  # else its name, without the parent's name in front ("Penn State strategic plan" under Penn State: strategic-plan)
        pn = slug(web_name(par)) if par and par != "main" else ""
        own = slug(nm)
        if pn and own.startswith(pn + "-"): own = own[len(pn) + 1:]
    s = unique((base + "/" if base else "") + own)
    web_slug[w] = s
    page_of[("web", w)] = add(f"web:{w}", nm, page_of[("web", par)] if par else None, s, WEBS[w]["data"].get("meta", {}).get("about", ""), len([x for x in items if x["parent"] == page_of.get(("web", par))]))
for w, _ in order: place_web(w)
# tiles owned by each web (not portals, not the tile that opens a sub-web, not the hub)
for w, _ in order:
    W = WEBS[w]; n = 0
    for nid, t in W["tiles"].items():
        if is_portal(w, nid): continue
        sub = W["meta"].get(nid, {}).get("web")
        if sub and sub in WEBS and opens.get(sub) == (w, nid): page_of[(w, nid)] = page_of[("web", sub)]; continue
        if t["group"] == W["groups"][0]: page_of[(w, nid)] = page_of[("web", w)]; continue  # the hub (first group) is the web's own page
        base = web_slug[w] or "ecosystem"
        page_of[(w, nid)] = add(f"tile:{w}:{nid}", t["label"], page_of[("web", w)], unique(base + "/" + slug(t["label"])), W["data"]["nodes"].get(nid, {}).get("desc", ""), n)
        n += 1
# tours
tours_root = add("tours", "Tours", None, unique("tours"), "Walks through the ecosystem web, one step at a time.", 1)
tn = 0
for w, _ in order:
    for t in WEBS[w]["data"].get("tours", []):
        page_of[("tour", w, t["id"])] = add(f"tour:{w}:{t['id']}", t.get("label", t["id"]), tours_root, unique("tours/" + slug(((web_name(w) + " ") if w != "main" else "") + t.get("label", t["id"]))), t.get("message", ""), tn)
        tn += 1
by_id = {it["id"]: it for it in items}
def href(item_id): return "/" + by_id[item_id]["slug"]
def resolve(w, nid):
    """the page for a tile as drawn in web w: its own page, or its page in the web that owns it"""
    if (w, nid) in page_of: return page_of[(w, nid)]
    home = portal_home(w, nid)
    if home and (home, nid) in page_of: return page_of[(home, nid)]
    for (ww, n2), v in [(k, v) for k, v in page_of.items() if len(k) == 2 and k[1] == nid]:
        return v
    return None
def label(w, nid):
    p = page_of.get((w, nid))
    if p and by_id[p]["_key"].startswith("web:"): return by_id[p]["title"]  # a hub or the tile that opens a web: the web's name
    home = portal_home(w, nid) if is_portal(w, nid) else w
    t = WEBS.get(home or w, WEBS[w])["tiles"].get(nid) or WEBS[w]["tiles"].get(nid) or {"label": nid}
    return t["label"]

# ---------- page bodies ----------
def player(w):
    return (f'<iframe src="/ecosystem.html{"#" + w if w != "main" else ""}" title="{E(web_name(w))}: the interactive web" '
            f'style="width:100%;height:80vh;border:0" loading="lazy"></iframe>')
def links_html(links):
    if not links: return ""
    return "<ul>" + "".join(f'<li><a href="{E(u)}">{E(k)}</a></li>' for k, u in links.items() if isinstance(u, str) and u.startswith(("http", "/"))) + "</ul>"
def connects(w, nid):
    out = []
    for a, arrow, lab, b in WEBS[w]["edges"]:
        if a == nid: other, incoming = b, False
        elif b == nid: other, incoming = a, True
        else: continue
        p = resolve(w, other)
        tgt = f'<a href="{href(p)}">{E(label(w, other))}</a>' if p else E(label(w, other))
        out.append(f"<li>{tgt} {E(lab.strip())} this</li>" if incoming else f"<li>{E(lab.strip()).capitalize()} {tgt}</li>")
    return "<ul>" + "".join(out) + "</ul>" if out else ""
pages = {}
for w, _ in order:
    W = WEBS[w]; M = W["data"].get("meta", {})
    body = [f"<p>{E(M.get('about', ''))}</p>" if M.get("about") else "", player(w)]
    for g in W["groups"]:
        ts = [(nid, t) for nid, t in W["tiles"].items() if t["group"] == g]
        if not ts: continue
        body.append(f"<h2>{E(g)}</h2><ul>" + "".join(f'<li><a href="{href(resolve(w, nid))}">{E(label(w, nid))}</a></li>' if resolve(w, nid) else f"<li>{E(label(w, nid))}</li>" for nid, t in ts) + "</ul>")
    tours = W["data"].get("tours", [])
    if tours: body.append("<h2>Tours</h2><ul>" + "".join(f'<li><a href="{href(page_of[("tour", w, t["id"])])}">{E(t.get("label", t["id"]))}</a></li>' for t in tours) + "</ul>")
    if M.get("links"): body.append("<h2>Links</h2>" + links_html(M["links"]))
    pages[page_of[("web", w)]] = body
    for nid, t in W["tiles"].items():
        p = page_of.get((w, nid))
        if not p or p == page_of[("web", w)] or p in pages: continue
        N = W["data"]["nodes"].get(nid, {})
        b = [f'<p data-eyebrow>{E(t["group"])}</p>' if t["group"] else ""]
        if N.get("desc"): b.append(f"<p>{E(N['desc'])}</p>")
        if N.get("note"): b.append(f"<p><em>{E(N['note'])}</em></p>")
        if N.get("status"): b.append(f"<p>Status: {E(str(N['status']))}</p>")
        b.append(f'<p><a href="/ecosystem.html{"#" + w if w != "main" else ""}">Open {E(web_name(w))} in the interactive web</a></p>')
        c = connects(w, nid)
        if c: b.append("<h2>Connects to</h2>" + c)
        if N.get("links"): b.append("<h2>Links</h2>" + links_html(N["links"]))
        pages[p] = b
    for t in tours:
        steps = "".join(f"<li>{E(s.get('caption', ''))}</li>" for s in t.get("scenes", []))
        pages[page_of[("tour", w, t["id"])]] = [f"<p>{E(t.get('message', ''))}</p>", f'<p><a href="{href(page_of[("web", w)])}">{E(web_name(w))}</a></p>', f"<ol>{steps}</ol>"]
pages[tours_root] = ["<ul>" + "".join(f'<li><a href="{href(i["id"])}">{E(i["title"])}</a></li>' for i in items if i["parent"] == tours_root) + "</ul>"]

# ---------- write ----------
os.makedirs(os.path.join(OUT, "pages"), exist_ok=True)
indent_of = {}
for it in items:
    it["indent"] = 0 if not it["parent"] else indent_of.get(it["parent"], 0) + 1
    indent_of[it["id"]] = it["indent"]
    body = pages.get(it["id"], [])
    authored = os.path.join(AUTHORED, it["slug"].replace("/", "__") + ".html")
    pre = open(authored).read() if os.path.exists(authored) else ""
    os.makedirs(os.path.join(OUT, "pages", it["id"]), exist_ok=True)
    open(os.path.join(OUT, it["location"]), "w").write(pre + "\n".join(x for x in body if x) + "\n")
site = {"id": str(uuid.uuid5(NS, "hax.cloud")), "title": "hax.cloud", "author": "HAXTheWeb", "description": "The HAX ecosystem: every part, the people behind it, and how it all connects.",
        "license": "by-sa",
        "metadata": {"author": {"name": "HAXTheWeb", "socialLink": "https://github.com/haxtheweb"},
                     "site": {"name": "hax-cloud", "domain": "https://hax.cloud", "lang": "en", "created": int(time.time()), "updated": int(time.time()),
                              "settings": {"pathauto": False, "publishPagesOn": True, "sw": False, "lang": "en"}},
                     "theme": {"element": "clean-one", "path": "@haxtheweb/clean-one/clean-one.js", "name": "Clean One", "variables": {}},
                     "build": {"structure": "ecosystem-web", "type": "praw"}, "node": {"fields": {}}},
        "items": [{k: v for k, v in it.items() if k != "_key"} for it in items]}
json.dump(site, open(os.path.join(OUT, "site.json"), "w"), indent=1, ensure_ascii=False)
shutil.copy(PLAYER, os.path.join(OUT, "ecosystem.html"))
# the bundle <ecosystem-web> loads (src): every web's source, in assemble.py's order, with the slugs above so the
# element can report the page path for whatever the viewer selects, and the art its image= tiles name
img_dir = os.path.join(OUT, "files")
os.makedirs(img_dir, exist_ok=True)
images = {}
if os.path.exists("traveler.uri"):
    import base64
    uri = open("traveler.uri").read().strip()
    head, _, b64 = uri.partition(",")
    ext = "webp" if "webp" in head else "png" if "png" in head else "jpg"
    open(os.path.join(img_dir, "future-traveler." + ext), "wb").write(base64.b64decode(b64))
    images["world-traveler-15"] = "/files/future-traveler." + ext
bundle = {"order": [w for w, _ in order], "webs": {}, "images": images,
          "slugs": {it["_key"]: it["slug"] for it in items}}
for w, f in order:
    bundle["webs"][w] = {"mmd": open(f + ".mmd").read(), "json": WEBS[w]["data"]}
json.dump(bundle, open(os.path.join(OUT, "ecosystem-webs.json"), "w"), ensure_ascii=False, separators=(",", ":"))
# a slug index, so a later rename can keep old links working (redirects.json is checked against it in a later phase)
json.dump({it["_key"]: it["slug"] for it in items}, open(os.path.join(OUT, "slugs.json"), "w"), indent=0, sort_keys=True)
print(len([k for k in page_of if k[0] == "web"]), "webs;", len(items), "pages;", sum(1 for i in items if i["parent"] == tours_root), "tours")
