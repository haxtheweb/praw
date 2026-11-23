"""Build the hax.cloud HAXsite from the ecosystem webs (phase 1 of https://github.com/haxtheweb/issues/issues/3310).

Reads the same webs assemble.py does (web/*.mmd + web/*.json, in assemble.py's order) and writes a static HAXsite:

  site.json        JSON Outline Schema: the main web is the home page with its own tiles under it; each sub-web is
                   its own page with its tiles under it, filed under a category (ecosystem/site/categories.json,
                   e.g. Organizations > Penn State, Courses > IST > IST 256) or nested under the web that opens it;
                   then a Tours branch: one page per tour, its related items the pages of its tiles in tour order.
  pages/<id>/      one index.html per page: generated HAX page HTML (description, links, what it connects to).
  ecosystem.html   today's player, embedded on every web page while the site uses clean-one. With ecosystem-theme
                   (HAX_CLOUD_THEME=ecosystem-theme, set by the workflow once the theme is on npm) every page has
                   <ecosystem-web> built in, routed by the page's metadata.ecosystem ({web, node, tour}).
  ecosystem-webs.json  the bundle <ecosystem-web> loads: every web's source, the slugs, the tile art and the tile glyphs.

Webs and tours have readable slugs (hax.cloud/penn-state/strategic-plan/aa-plan, hax.cloud/tours/everyone). A tile's
page is at hax.cloud/stories/<address>: the address comes from the tile's key (its web and node id), never from its
label, so the link holds when the tile is renamed. The path a tile's label used to give it (/ecosystem/<label>)
still answers, as a page that forwards to the address; it follows the current label, so no former name is kept.
A tile drawn as a portal in another web is not a second page: links to it go to its page in the web that owns it.
Categories only arrange the outline: a web's slug still comes from the web that opens it, so moving a web to
another category never changes its address. Hand-written pages live in ecosystem/site/pages/<slug>.html; when one exists its HTML goes above the generated
content of that page.

Usage (from ecosystem/.work, after assemble.py): python3 -I ../build/build_site.py <out-dir> <player.html>
The HAXcms boilerplate (index.html, build.js, 404.html …) is copied in by the workflow, not here."""
import json, os, re, sys, uuid, html, time, shutil
OUT, PLAYER = sys.argv[1], sys.argv[2]
# the theme: ecosystem-theme once it is on npm (the workflow checks and sets HAX_CLOUD_THEME), clean-one until then.
# With ecosystem-theme every page has the interactive web built in, so pages drop the embedded player and its links.
ECO_THEME = os.environ.get("HAX_CLOUD_THEME") == "ecosystem-theme"
HERE = os.path.dirname(os.path.abspath(__file__))
ECO = os.path.dirname(HERE)
AUTHORED = os.path.join(ECO, "site", "pages")
NS = uuid.UUID("6f1d2c3a-0b8e-4c55-9a7e-1a2b3c4d5e6f")  # fixed namespace for page ids
def iid(key): return "item-" + str(uuid.uuid5(NS, key))  # stable ids: the same tile keeps its page id across builds
def slug(s):
    s = re.sub(r"&", " and ", s.lower())
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:60] or "page"
E = html.escape
# Invariant: a tile's address depends only on its key (tile:<web>:<node id>): the first 8 hex digits of the same
# uuid its page id is made from. ecosystem/site/addresses.json ({key: address}) pins an address to a new key when a
# node id or its web has to change, so the links people hold keep working. Two tiles never share an address: the
# build stops instead.
_pins_file = os.path.join(ECO, "site", "addresses.json")
PINS = json.load(open(_pins_file)) if os.path.exists(_pins_file) else {}
addr_of = {}
def address(key):
    a = PINS.get(key) or uuid.uuid5(NS, key).hex[:8]
    if not re.fullmatch(r"[a-z0-9]{4,16}", a): sys.exit(f"address for {key} must be 4-16 of a-z, 0-9: {a!r}")
    if addr_of.setdefault(a, key) != key: sys.exit(f"{key} and {addr_of[a]} share the address {a}: pin one in ecosystem/site/addresses.json")
    return a

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
SITE_DESCRIPTION = "The HAX ecosystem: every part, the people behind it, and how it all connects."
def web_name(w): return WEBS[w]["data"].get("meta", {}).get("name") or ("Ecosystem web" if w == "main" else w)
def web_parent(w):
    p = WEBS[w]["data"].get("meta", {}).get("parent")
    if p in WEBS and p != w: return p
    if w in opens: return opens[w][0]
    return "main" if w != "main" else None
# the outline's categories (ecosystem/site/categories.json): {categories: [{id, title, description, parent}],
# webs: {web id: category id, or "web:<id>" to file it under that web's page}, tiles: {"<web>:<node id>": "web:<id>"
# or a category id}}. Categories group the webs that open from the main web; a nested web (Data contracts > JSON
# Outline Schema) stays under its parent web. tiles files a tile's page somewhere other than the web that owns it,
# such as Penn State's colleges (main-web tiles) under Penn State; its address does not change.
_cat_file = os.path.join(ECO, "site", "categories.json")
CATS = json.load(open(_cat_file)) if os.path.exists(_cat_file) else {"categories": [], "webs": {}}
CAT = {c["id"]: c for c in CATS["categories"]}
for c in CATS["categories"]:
    if c.get("parent") and c["parent"] not in CAT: sys.exit(f"category {c['id']}: unknown parent {c['parent']}")
def cat_id(c): return iid(f"category:{c}")
unfiled = []
def outline_parent(w, par):
    """the page a web sits under in the outline: its category, the web categories.json files it under, or the web that opens it"""
    if par != "main": return page_of[("web", par)]
    to = CATS["webs"].get(w)
    if to and to.startswith("web:") and to[4:] in WEBS and to[4:] != w:
        place_web(to[4:]); return page_of[("web", to[4:])]
    if to in CAT: return cat_id(to)
    unfiled.append(w)
    return page_of[("web", "main")]
def add(key, title, parent, slugpath, desc="", order=0):
    i = iid(key)
    items.append({"id": i, "indent": 0, "location": f"pages/{i}/index.html", "slug": slugpath, "order": order, "parent": parent,
                  "title": title, "description": desc[:200], "metadata": {"created": int(time.time()), "updated": int(time.time()), "published": True}, "_key": key})
    return i
web_slug, used, legacy = {}, set(), {}  # legacy: {label path: item id}, the paths tiles had before addresses
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
        # the home page: its description is what search results and link previews show for hax.cloud, so it is
        # the site's own, not the main web's "about" (notes for whoever edits the web)
        page_of[("web", w)] = add("web:main", "Ecosystem web", None, unique("ecosystem"), SITE_DESCRIPTION, 0)
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
    op = outline_parent(w, par)
    page_of[("web", w)] = add(f"web:{w}", nm, op, s, WEBS[w]["data"].get("meta", {}).get("about", ""), len([x for x in items if x["parent"] == op]))
for w, _ in order: place_web(w)
if unfiled: print("not in ecosystem/site/categories.json, left under the home page:", ", ".join(unfiled))
# the categories, after the webs so a web's slug never gives way to a category's; a category nobody files a web
# in is left out
def cat_used(c):
    return any(x["parent"] == cat_id(c) for x in items) or any(k.get("parent") == c and cat_used(k["id"]) for k in CATS["categories"])
cat_roots = 0
for c in CATS["categories"]:
    if not cat_used(c["id"]): continue
    par = cat_id(c["parent"]) if c.get("parent") else None
    n = cat_roots if not par else len([x for x in items if x["parent"] == par])
    if not par: cat_roots += 1
    i = add(f"category:{c['id']}", c["title"], par, unique(slug(c["id"].split("/")[0]) + "".join("/" + slug(x) for x in c["id"].split("/")[1:])), c.get("description", ""), 1 + n if not par else n)
    assert i == cat_id(c["id"])
# tiles owned by each web (not portals, not the tile that opens a sub-web, not the hub)
for w, _ in order:
    W = WEBS[w]; n = 0
    for nid, t in W["tiles"].items():
        if is_portal(w, nid): continue
        sub = W["meta"].get(nid, {}).get("web")
        if sub and sub in WEBS and opens.get(sub) == (w, nid): page_of[(w, nid)] = page_of[("web", sub)]; continue
        if t["group"] == W["groups"][0]: page_of[(w, nid)] = page_of[("web", w)]; continue  # the hub (first group) is the web's own page
        base = web_slug[w] or "ecosystem"
        key = f"tile:{w}:{nid}"
        page_of[(w, nid)] = add(key, t["label"], page_of[("web", w)], unique("stories/" + address(key)), W["data"]["nodes"].get(nid, {}).get("desc", ""), n)
        legacy[unique(base + "/" + slug(t["label"]))] = page_of[(w, nid)]
        n += 1
# tiles filed elsewhere in the outline (categories.json "tiles")
for k, to in CATS.get("tiles", {}).items():
    w, _, nid = k.partition(":")
    p = page_of.get((w, nid))
    tgt = page_of.get(("web", to[4:])) if to.startswith("web:") else (cat_id(to) if to in CAT else None)
    it = next((x for x in items if x["id"] == p), None)
    if not it or not it["_key"].startswith("tile:") or not tgt: print("categories.json tiles: skipped", k, "->", to); continue
    it["parent"], it["order"] = tgt, 1000 + len([x for x in items if x["parent"] == tgt])
# pages that are not part of a web (ecosystem/site/extra-pages.json: [{slug, title, description}]); their HTML is the
# hand-written ecosystem/site/pages/<slug>.html, and with no metadata.ecosystem the theme opens them in the Site view
EXTRA = json.load(open(os.path.join(ECO, "site", "extra-pages.json"))) if os.path.exists(os.path.join(ECO, "site", "extra-pages.json")) else []
# tours
tours_root = add("tours", "Tours", None, unique("tours"), "Walks through the ecosystem web, one step at a time.", 1 + cat_roots)
for n, x in enumerate(EXTRA):
    add(f"page:{x['slug']}", x["title"], None, unique(slug(x["slug"])), x.get("description", ""), 2 + cat_roots + n)
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
    body = [f"<p>{E(M.get('about', ''))}</p>" if M.get("about") else "", "" if ECO_THEME else player(w)]
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
        if not ECO_THEME: b.append(f'<p><a href="/ecosystem.html{"#" + w if w != "main" else ""}">Open {E(web_name(w))} in the interactive web</a></p>')
        c = connects(w, nid)
        if c: b.append("<h2>Connects to</h2>" + c)
        if N.get("links"): b.append("<h2>Links</h2>" + links_html(N["links"]))
        pages[p] = b
    for t in tours:
        # each step names the tiles it lights up, linked to their pages, so the walk reads without the web
        def stops(s):
            ls = [f'<a href="{href(resolve(w, n))}">{E(label(w, n))}</a>' for n in s.get("nodes", []) if n in W["tiles"] and resolve(w, n)]
            return f" ({', '.join(ls)})" if ls else ""
        steps = "".join(f"<li>{E(s.get('caption', ''))}{stops(s)}</li>" for s in t.get("scenes", []))
        pages[page_of[("tour", w, t["id"])]] = [f"<p>{E(t.get('message', ''))}</p>", f'<p><a href="{href(page_of[("web", w)])}">{E(web_name(w))}</a></p>', f"<ol>{steps}</ol>"]
# a category page: what it holds, each with its description
def full_desc(x):  # a web's whole "about" (an item's description is cut to 200 characters for the outline)
    k = x["_key"].split(":")
    return WEBS[k[1]]["data"].get("meta", {}).get("about", "") if k[0] == "web" else x["description"]
for it in [x for x in items if x["_key"].startswith("category:")]:
    kids = sorted([x for x in items if x["parent"] == it["id"]], key=lambda x: x["order"])
    pages[it["id"]] = [f"<p>{E(CAT[it['_key'][9:]].get('description', ''))}</p>" if CAT[it["_key"][9:]].get("description") else "",
                       "<ul>" + "".join(f'<li><a href="{href(x["id"])}">{E(x["title"])}</a>' + (f": {E(full_desc(x))}" if full_desc(x) else "") + "</li>" for x in kids) + "</ul>"]
# the Tours page: every tour with what it teaches
pages[tours_root] = ["<ul>" + "".join(f'<li><a href="{href(i["id"])}">{E(i["title"])}</a>' + (f': {E(i["description"])}' if i["description"] else "") + "</li>" for i in items if i["parent"] == tours_root) + "</ul>"]

# ---------- write ----------
os.makedirs(os.path.join(OUT, "pages"), exist_ok=True)
by_id = {it["id"]: it for it in items}
def depth(it):  # a category is added after the webs under it, so count up the parents rather than in list order
    d = 0
    while it["parent"]: it, d = by_id[it["parent"]], d + 1
    return d
for it in items:
    it["indent"] = depth(it)
    body = pages.get(it["id"], [])
    authored = os.path.join(AUTHORED, it["slug"].replace("/", "__") + ".html")
    pre = open(authored).read() if os.path.exists(authored) else ""
    os.makedirs(os.path.join(OUT, "pages", it["id"]), exist_ok=True)
    open(os.path.join(OUT, it["location"]), "w").write(pre + "\n".join(x for x in body if x) + "\n")
# what each page shows, for ecosystem-theme to route <ecosystem-web>: {"web"} for a web, plus "node" for a tile or
# "tour" for a tour (from the same keys the slugs use: web:<w>, tile:<w>:<id>, tour:<w>:<id>)
for it in items:
    k = it["_key"].split(":")
    if k[0] == "web": it["metadata"]["ecosystem"] = {"web": k[1]}
    elif k[0] == "tile": it["metadata"]["ecosystem"] = {"web": k[1], "node": k[2]}
    elif k[0] == "tour":
        it["metadata"]["ecosystem"] = {"web": k[1], "tour": k[2]}
        # a tour's related items are its tiles' pages, in tour order (https://github.com/haxtheweb/issues/issues/3258)
        t = next(x for x in WEBS[k[1]]["data"].get("tours", []) if x["id"] == k[2])
        stops = [resolve(k[1], n) for s in t.get("scenes", []) for n in s.get("nodes", []) if n in WEBS[k[1]]["tiles"]]
        it["metadata"]["relatedItems"] = list(dict.fromkeys(p for p in stops if p))
THEME = {"element": "clean-one", "path": "@haxtheweb/clean-one/clean-one.js", "name": "Clean One", "variables": {}}
if ECO_THEME:
    THEME = {"element": "ecosystem-theme", "path": "@haxtheweb/ecosystem-theme/ecosystem-theme.js", "name": "Ecosystem",
             "variables": {"ecosystemSrc": "ecosystem-webs.json",
                           "nav": [{"label": "Explore", "slug": items[0]["slug"]}, {"label": "Tours", "slug": by_id[tours_root]["slug"]}]
                                  + [{"label": x["title"], "slug": slug(x["slug"])} for x in EXTRA if x.get("nav")],
                           # no "links": HAXTheWeb, Build now and Web components are in the network bar above
                           # the home page's greeting: before anything else, that it is all one network
                           "welcome": {"title": "Everything in HAX is connected",
                                       "text": "Every part of HAX, every site in the HAX network and everyone who builds it, in one web. "
                                               "Select a tile to see what it connects to, take a tour, or ask Merlin to take you anywhere in the network.",
                                       "tour": by_id[page_of[("tour", "main", "everyone")]]["slug"] if ("tour", "main", "everyone") in page_of else by_id[tours_root]["slug"],
                                       "tourLabel": "Take the tour"},
                           "footerNote": "Built from PRAW on every push to main.",
                           "footer": [{"label": "Source: praw/ecosystem", "href": "https://github.com/haxtheweb/praw/tree/main/ecosystem"},
                                      {"label": "Roadmap", "href": "https://github.com/haxtheweb/issues/issues/3310"}]}}
site = {"id": str(uuid.uuid5(NS, "hax.cloud")), "title": "hax.cloud", "author": "HAXTheWeb", "description": SITE_DESCRIPTION,
        "license": "by-sa",
        "metadata": {"author": {"name": "HAXTheWeb", "socialLink": "https://github.com/haxtheweb"},
                     "site": {"name": "hax-cloud", "domain": "https://hax.cloud", "lang": "en", "created": int(time.time()), "updated": int(time.time()),
                              "settings": {"pathauto": False, "publishPagesOn": True, "sw": False, "lang": "en"}},
                     "theme": THEME,
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
    images["future-traveler-15"] = "/files/future-traveler." + ext
bundle = {"order": [w for w, _ in order], "webs": {}, "images": images, "icons": {},
          "slugs": {it["_key"]: it["slug"] for it in items}}
for w, f in order:
    bundle["webs"][w] = {"mmd": open(f + ".mmd").read(), "json": WEBS[w]["data"]}
# the tile glyphs the webs name, as SVG markup, so the element draws them inline (no icon fetches, no flash
# when tiles redraw); the same data the player embeds
icon_src = "icons_inline.json" if os.path.exists("icons_inline.json") else os.path.join(ECO, "player", "icons_inline.json")
glyphs = json.load(open(icon_src))
used = sorted({m for w in bundle["webs"].values() for m in re.findall(r"icon=([\w:-]+)", w["mmd"])})
bundle["icons"] = {name: glyphs[name] for name in used if name in glyphs}
# art the main web's tiles name that its JSON does not carry (assemble.py merges the same file into the player):
# Bryan's rpg-character. Each web's own "images" (the theme thumbnails) travel inside its JSON already.
main_art = "images-main.json" if os.path.exists("images-main.json") else os.path.join(ECO, "player", "images-main.json")
bundle["images"].update(json.load(open(main_art)))
# outside facts the element's lenses read (freshness, parity, release dates; see build_layers.py), the same
# data the player embeds. Maintainers are left out of the bus factor: GOVERNANCE.md names Bryan and Bill
# primary and backup owner in every repo's CODEOWNERS, so they stand behind every part.
layers_src = os.path.join("ext", "layers.json") if os.path.exists(os.path.join("ext", "layers.json")) else os.path.join(ECO, "build", "data", "layers.json")
bundle["layers"] = json.load(open(layers_src))
bundle["layers"]["maintainers"] = ["bryan", "billrose"]
json.dump(bundle, open(os.path.join(OUT, "ecosystem-webs.json"), "w"), ensure_ascii=False, separators=(",", ":"))
# a slug index: every page's path by its key
json.dump({it["_key"]: it["slug"] for it in items}, open(os.path.join(OUT, "slugs.json"), "w"), indent=0, sort_keys=True)
# the label paths tiles had before addresses: each a small page that forwards to the tile's address and names it
# as canonical, so links and search results from before keep working
for path, i in legacy.items():
    to, title = E(href(i), quote=True), E(by_id[i]["title"])
    os.makedirs(os.path.join(OUT, path), exist_ok=True)
    open(os.path.join(OUT, path, "index.html"), "w").write(
        f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>{title}</title>\n'
        f'<link rel="canonical" href="https://hax.cloud{to}">\n<meta name="robots" content="noindex">\n'
        f'<meta http-equiv="refresh" content="0; url={to}">\n</head>\n<body>\n<p><a href="{to}">{title}</a></p>\n</body>\n</html>\n')
print(len([k for k in page_of if k[0] == "web"]), "webs;", len(items), "pages;", sum(1 for i in items if i["parent"] == tours_root), "tours;", len(legacy), "label paths forwarded")
