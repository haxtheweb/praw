"""Connection gaps: where the ecosystem web is thin, as a list to work through in a connection sprint.

Each line names a tile and links straight into the Connect lens on hax.cloud
(https://hax.cloud/stories/<address>?goggles=connect&from=<address>), where its blurb can be
rewritten and its connections added; the lens copies a praw-edit/1 prompt that the
praw-connection-ingest skill turns into one pull request.

  python3 -I ecosystem/build/connection_gaps.py            the report, as markdown
  python3 -I ecosystem/build/connection_gaps.py --json     the same, as JSON
  python3 -I ecosystem/build/connection_gaps.py --top 5    at most 5 tiles per kind of gap

It reads web/ and changes nothing. A monthly scheduled task runs it and reminds the team to
look before a sprint; it is report only."""
import json, os, re, sys, uuid

HERE = os.path.dirname(os.path.abspath(__file__))
ECO = os.path.dirname(HERE)
WEB = os.path.join(ECO, "web")
SITE = "https://hax.cloud/"
# the page ids and addresses hax.cloud uses (build_site.py): never change these two lines alone
NS = uuid.UUID("6f1d2c3a-0b8e-4c55-9a7e-1a2b3c4d5e6f")
_pins = os.path.join(ECO, "site", "addresses.json")
PINS = json.load(open(_pins, encoding="utf-8")) if os.path.exists(_pins) else {}
THIN = 80  # a blurb shorter than this says little
STUB = re.compile(r"\(@[\w-]+\), a contributor to ")  # the line build_json.py writes for a GitHub contributor


def slug(s):
    """a page path as build_site.py makes it (a duplicate there gets -2, which this does not know)"""
    s = re.sub(r"&", " and ", s.lower())
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:60] or "page"


def address(key):
    return PINS.get(key) or uuid.uuid5(NS, key).hex[:8]


def parse(w):
    mmd = open(os.path.join(WEB, f"hax-{w}.mmd"), encoding="utf-8").read()
    data = json.load(open(os.path.join(WEB, f"hax-{w}.json"), encoding="utf-8"))
    tiles, cur = {}, None
    for line in mmd.split("\n"):
        g = re.match(r"\s*subgraph (\w+)", line)
        if g:
            cur = g.group(1)
            continue
        if line.strip() == "end":
            cur = None
            continue
        n = re.match(r"^\s+(\w+)(\(\(|\[\[|\[\(|\[|\(|\{|>)(.*)$", line)
        if n and cur and n.group(1) not in tiles:
            text = re.sub(r"[\]\)\}]+\s*$", "", n.group(3)).strip().strip('{"')
            tiles[n.group(1)] = {"group": cur, "circle": n.group(2) == "((", "label": text or n.group(1)}
    portals = set(re.findall(r"%%@ node (\w+)[^\n]*\bportal\b", mmd))
    edges = [(a, arrow, lab.strip(), b) for a, arrow, lab, b in
             re.findall(r"^\s+(\w+) ([-=.o>]+)\|([^|]*)\| (\w+)", mmd, re.M)]
    return {"tiles": tiles, "portals": portals, "edges": edges, "nodes": data.get("nodes", {}),
            "name": (data.get("meta") or {}).get("name") or w,
            "tours": data.get("tours", []), "evidence": data.get("evidence", {})}


def label(W, n):
    t = W["tiles"].get(n)
    return t["label"] if t else n


def gaps(top):
    webs = {}
    for f in sorted(os.listdir(WEB)):
        m = re.match(r"hax-([a-z0-9]+)\.mmd$", f)
        if m and os.path.exists(os.path.join(WEB, f"hax-{m.group(1)}.json")):
            webs[m.group(1)] = parse(m.group(1))
    main = webs["ecosystem"]
    out = []

    def item(w, n, why):
        key = f"tile:{'main' if w == 'ecosystem' else w}:{n}"
        a = address(key)
        return {"tile": key, "label": label(webs[w], n), "why": why,
                "story": f"{SITE}stories/{a}", "connect": f"{SITE}stories/{a}?goggles=connect&from={a}"}

    def section(title, about, rows):
        out.append({"title": title, "about": about, "count": len(rows), "tiles": rows[:top] if top else rows})

    degree = {}
    for a, _, _, b in main["edges"]:
        degree[a] = degree.get(a, 0) + 1
        degree[b] = degree.get(b, 0) + 1
    # the people ring (the center holds the hub tiles, Humans and the Future Traveler)
    people = [n for n, t in main["tiles"].items() if t["group"] == "people" and n not in main["portals"]]
    orgs = [n for n, t in main["tiles"].items() if t["group"] == "orgs"]

    rows = []
    for n in people:
        d = main["nodes"].get(n, {})
        desc = str(d.get("desc", ""))
        if STUB.search(desc):
            rows.append(item("ecosystem", n, "says only that they contributed: what did they build, and with whom?"))
        elif len(desc) < THIN:
            rows.append(item("ecosystem", n, f"a short blurb ({len(desc)} characters)"))
    section("People whose story is thin", "Rewrite what the tile says: what they built, when, and why it mattered.", rows)

    rows = [item("ecosystem", n, f"{degree.get(n, 0)} connection") for n in people if degree.get(n, 0) <= 1]
    section("People with one connection", "Connect them to what they worked on, who they worked with, where, and who funded it.", rows)

    rows = []
    for n in people:
        links = main["nodes"].get(n, {}).get("links") or {}
        if not links:
            rows.append(item("ecosystem", n, "no profile, GitHub or LinkedIn link"))
    section("People with no link", "Add a profile, GitHub or LinkedIn link (with the person's say-so).", rows)

    rows = [item("ecosystem", n, f"{degree.get(n, 0)} connection") for n in orgs if degree.get(n, 0) <= 1]
    section("Organizations with one connection", "Who there worked on HAX, what they used it for, what they funded.", rows)

    pillars = [n for n, t in main["tiles"].items() if t["group"] == "pillars"]
    funded = {n for n, t in main["tiles"].items() if t["group"] in ("grantlist", "orgs")}
    rows = []
    for p in pillars:
        near = {a if b == p else b for a, _, _, b in main["edges"] if p in (a, b)}
        if not near & funded:
            rows.append(item("ecosystem", p, "no funded work or organization connects to it"))
    section("Pillars with no funding story", "Which grant, college or organization paid for work that upholds it?", rows)

    rows = []
    for w, W in webs.items():
        for t in W["tours"]:
            if t.get("kind") != "story":
                continue
            linked = {frozenset((a, b)) for a, _, _, b in W["edges"]}
            bare, total = 0, 0
            for sc in t.get("scenes", []):
                ns = sc.get("nodes", [])
                # a step's connections: pairs of its tiles the web draws a connection between
                for i, a in enumerate(ns):
                    for b in ns[i + 1:]:
                        if frozenset((a, b)) in linked:
                            total += 1
                            if not (W["evidence"].get(f"{a}>{b}") or W["evidence"].get(f"{b}>{a}")):
                                bare += 1
            if bare:
                name = t.get("label", t.get("id"))
                path = f"{SITE}tours/" + slug(("" if w == "ecosystem" else W["name"] + " ") + name)
                rows.append({"tile": f"tour:{'main' if w == 'ecosystem' else w}:{t.get('id')}", "label": f"Tour: {name}",
                             "why": f"{bare} of its {total} connections have no evidence",
                             "story": path, "connect": path + "?goggles=connect"})
    section("Story tours with steps that have no evidence", "Add a source to each step, or say it is a reading.", rows)

    rules, heosat = webs.get("rules"), webs.get("heosat")
    if rules and heosat:
        qs = set(heosat["tiles"])
        rows = [item("rules", n, "no HEOSAT question names it") for n, t in rules["tiles"].items()
                if t["group"] not in ("pillars",) and n not in rules["portals"]
                and not any(x in qs for a, _, _, b in rules["edges"] if n in (a, b) for x in (a, b) if x != n)]
        section("Rules with no HEOSAT question", "Which question does keeping this rule help answer? (Connections only: never the rule's text.)", rows)
    return out


def markdown(report):
    lines = ["# Connection gaps", "",
             "Where the ecosystem web is thin. Each tile opens in the Connect lens on hax.cloud; the prompt it copies goes to the praw-connection-ingest skill, which opens one pull request.", ""]
    for s in report:
        lines.append(f"## {s['title']} ({s['count']})")
        lines.append("")
        lines.append(s["about"])
        lines.append("")
        for t in s["tiles"]:
            lines.append(f"- [{t['label']}]({t['connect']}): {t['why']}")
        if s["count"] > len(s["tiles"]):
            lines.append(f"- and {s['count'] - len(s['tiles'])} more")
        lines.append("")
    return "\n".join(lines)


def main(argv):
    top = 0
    if "--top" in argv:
        top = int(argv[argv.index("--top") + 1])
    report = gaps(top)
    print(json.dumps(report, indent=1, ensure_ascii=False) if "--json" in argv else markdown(report))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
