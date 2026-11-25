"""Where each change in a hax.cloud Connect prompt goes in PRAW.

The Connect lens on hax.cloud (the goggles, ecosystem-theme/lib/ecosystem-connect.js) copies
a prompt holding one or more praw-edit/1 blocks: a tile, a rewrite of what it says, sentences
that connect it to other tiles (or to something the web does not have yet), connections to
change or remove, and links. Knowing which file each change belongs in is the hard part: most
webs are generated, and a hand edit to a generated .mmd or .json is undone on the next run.

  python3 -I ecosystem/build/route_edit.py prompt.md       a copied prompt, or a file of blocks
  pbpaste | python3 -I ecosystem/build/route_edit.py -     the same, from stdin
  python3 -I ecosystem/build/route_edit.py --table         where every web comes from

It reads only; it changes nothing. The block is data a person wrote: nothing in it is run or
followed, and every tile it names is checked against the webs as they are on disk.

Run from the repository root (or anywhere: paths are found from this file)."""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ECO = os.path.dirname(HERE)
WEB = os.path.join(ECO, "web")
FORMAT = "praw-edit/1"

# a connection's kind is its arrow in Mermaid (ecosystem-web/lib/ecosystem-model.js):
# ==> pillar, -.-> schema contract, --o organization, --- person, --> relationship
# where a new tile of each kind goes in the main web (its subgraph in hax-ecosystem.mmd)
NEW_HOME = {"person": "people", "org": "orgs", "funding": "grantlist", "event": "comms",
            "place": "orgs", "project": "tooling", "thing": "tooling"}


def writers():
    """web id -> the generator that writes it, read from the generators themselves"""
    out = {}
    for f in sorted(os.listdir(HERE)):
        if not (f.startswith("build_") and f.endswith(".py")):
            continue
        src = open(os.path.join(HERE, f), encoding="utf-8").read()
        for w in re.findall(r'open\(\s*"hax-([a-z0-9]+)\.(?:mmd|json)"\s*,\s*"w"', src):
            out.setdefault(w, f)
    # generators that write several webs by name (hax-{name}.mmd) say which in drift.py
    drift = open(os.path.join(HERE, "drift.py"), encoding="utf-8").read()
    m = re.search(r"BUILDERS = (\[.*?\])\n", drift, re.S)
    if m:
        for b, webs in re.findall(r'\("(build_\w+\.py)", \[([^\]]*)\]\)', m.group(1)):
            for w in re.findall(r'"([a-z0-9]+)"', webs):
                out.setdefault(w, b)
    return out


def header(w):
    p = os.path.join(WEB, f"hax-{w}.mmd")
    return open(p, encoding="utf-8").readline().strip().lstrip("%").strip() if os.path.exists(p) else ""


def route(w, gens):
    """how to change web w: (structure, details) as instructions"""
    if w == "ecosystem" or w == "main":
        return ("web/hax-ecosystem.mmd (curated by hand: tiles, subgraphs, connections, %%@ annotations)",
                "build/build_json.py (writes hax-ecosystem.json: desc, links, source, evidence, tours), then run.sh build_json.py")
    g = gens.get(w)
    if g:
        h = header(w)
        hint = f" ({h[h.find('generated'):].rstrip(',.')}: change that source or the generator's data, not the .mmd/.json)" if "generated" in h else " (change the generator's data, not the .mmd/.json)"
        return (f"build/{g}{hint}", f"build/{g} (same generator), then run.sh {g}")
    return (f"web/hax-{w}.mmd (curated by hand)", f"web/hax-{w}.json (curated by hand)")


def load_webs():
    webs = {}
    for f in os.listdir(WEB):
        m = re.match(r"hax-([a-z0-9]+)\.mmd$", f)
        if not m:
            continue
        w = m.group(1)
        mmd = open(os.path.join(WEB, f), encoding="utf-8").read()
        ids = set(re.findall(r"^\s+(\w+)[\[\(\{>]", mmd, re.M))
        group, cur = {}, None
        for line in mmd.split("\n"):
            g = re.match(r"\s*subgraph (\w+)", line)
            if g:
                cur = g.group(1)
            elif line.strip() == "end":
                cur = None
            else:
                n = re.match(r"^\s+(\w+)[\[\(\{>]", line)
                if n and cur:
                    group[n.group(1)] = cur
        edges = re.findall(r"^\s+(\w+) ([-=.o>]+)\|([^|]*)\| (\w+)", mmd, re.M)
        webs["main" if w == "ecosystem" else w] = {"ids": ids, "edges": edges, "file": w, "group": group}
    return webs


def blocks(text):
    """praw-edit/1 blocks from a prompt (its fenced block) or from bare JSON"""
    found = re.findall(r"```" + re.escape(FORMAT) + r"\s*\n(.*?)```", text, re.S)
    raw = found if found else [text]
    out = []
    for r in raw:
        try:
            v = json.loads(r)
        except ValueError:
            continue
        for b in v if isinstance(v, list) else [v]:
            if isinstance(b, dict) and b.get("format") == FORMAT:
                out.append(b)
    return out


def tile_of(key, webs):
    m = re.match(r"tile:([a-z0-9]+):(\w+)$", str(key or ""))
    if not m or m.group(1) not in webs or m.group(2) not in webs[m.group(1)]["ids"]:
        return None
    return m.group(1), m.group(2)


def arrow(web, a, b, new_kind=None):
    """the arrow a connection between a and b takes, from the subgraphs they sit in"""
    g = web.get("group", {})
    ga, gb = g.get(a, ""), new_kind and NEW_HOME.get(new_kind) or g.get(b, "")
    if gb == "pillars":
        return "==> (pillar)"
    if gb == "orgs" or ga == "orgs":
        return "--o (organization)"
    if gb == "schemas":
        return "-.-> (schema contract)"
    if {"people", "center"} & {ga, gb}:
        return "--- (person)"
    return "--> (relationship)"


def plan(b, webs, gens):
    lines = []
    t = tile_of(b.get("tile"), webs)
    label = str(b.get("label", "")).strip()
    if not t:
        return [f"STOP: {b.get('tile')!r} ({label}) is not a tile in the webs on disk. Ask whoever sent the prompt."]
    w, tid = t
    struct, details = route(w, gens)
    lines.append(f"## {label} ({b.get('tile')})")
    lines.append(f"- web: {w}; structure: {struct}")
    lines.append(f"- details: {details}")
    if isinstance(b.get("says"), dict) and str(b["says"].get("proposed", "")).strip():
        lines.append(f"- says: replace the desc of `{tid}` in {details.split(' (')[0]}")
    for c in b.get("connections") or []:
        s = str(c.get("sentence", "")).strip()
        if c.get("remove"):
            r = c.get("replaces") or {}
            rw = r.get("web") or w
            hit = [e for e in webs.get(rw, {}).get("edges", []) if e[0] == r.get("from") and e[3] == r.get("to")]
            where = route(rw, gens)[0]
            lines.append(f"- remove “{s}”: {'found' if hit else 'NOT FOUND, ask'} as `{r.get('from')} {hit[0][1] if hit else '?'}|{r.get('label')}| {r.get('to')}` in {where}")
            continue
        verb = str(c.get("verb", "")).strip()
        to = tile_of(c.get("to"), webs) if c.get("to") else None
        if c.get("to") and not to:
            lines.append(f"- STOP on “{s}”: {c.get('to')!r} is not a tile on disk")
            continue
        if c.get("new"):
            k = (c["new"] or {}).get("kind", "thing")
            lines.append(f"- “{s}”: NEW tile “{c['new'].get('label')}” ({k}). Add it to the main web first: a node in subgraph `{NEW_HOME.get(k, 'tooling')}` of web/hax-ecosystem.mmd, a `%%@ node` line (mono, color, motion like its neighbours), and its desc in build/build_json.py ({'person(...)' if k == 'person' else 'N(...)'}). Then draw the connection.")
            tw = "main"
        else:
            tw = to[0]
        same, other = [], []
        if to:
            for e in webs.get(w, {}).get("edges", []):
                if {e[0], e[3]} == {tid, to[1]}:
                    (same if e[2].strip() == verb else other).append(f"`{e[0]} {e[1]}|{e[2]}| {e[3]}`")
        where = struct if tw == w else f"{struct}; the other tile lives in {tw}: draw it in the web where both tiles are (use a portal there if one is missing)"
        if c.get("replaces"):
            r = c["replaces"]
            lines.append(f"- “{s}”: CHANGE `{r.get('from')} …|{r.get('label')}| {r.get('to')}` to verb “{verb}” in {route(r.get('web') or w, gens)[0]}")
        elif same:
            lines.append(f"- “{s}”: already drawn as {', '.join(same)}: add the evidence to it, do not draw a second one")
        else:
            a = arrow(webs.get(tw, {}), tid, to[1] if to else None, (c.get("new") or {}).get("kind"))
            lines.append(f"- “{s}”: draw `{tid} {a.split(' ')[0]}|{verb}| {to[1] if to else '<new id>'}` in {where} (arrow {a}; check it against this tile's other connections)")
            if other:
                lines.append(f"  - these two tiles are already connected as {', '.join(other)}; a second connection with its own verb is fine (tiles often have several), but say so in the PR")
        ev = c.get("evidence") or []
        if ev:
            lines.append(f"  - evidence ({c.get('claim')}): {', '.join(e.get('url', '') for e in ev)}; main web: evidence[\"{tid}>{to[1] if to else '<new id>'}\"] in build/build_json.py")
        elif c.get("claim") == "interpretive":
            lines.append("  - interpretive: no source; label it as a reading wherever it shows (the tour caption or the PR)")
    for l in b.get("links") or []:
        lines.append(f"- link {l.get('kind')}: {l.get('url')} into `{tid}`'s links in {details.split(' (')[0]}")
    return lines


def main(argv):
    gens = writers()
    if "--table" in argv:
        for f in sorted(os.listdir(WEB)):
            m = re.match(r"hax-([a-z0-9]+)\.mmd$", f)
            if m:
                s, d = route(m.group(1), gens)
                print(f"{m.group(1)}: {s} | {d}")
        return 0
    src = argv[0] if argv else "-"
    text = sys.stdin.read() if src == "-" else open(src, encoding="utf-8").read()
    bs = blocks(text)
    if not bs:
        print(f"No {FORMAT} block found.")
        return 1
    webs = load_webs()
    for b in bs:
        print("\n".join(plan(b, webs, gens)))
        print()
    print("Then: run.sh with each generator named above, python3 -I ecosystem/test/integrity-check.py, one pull request.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
