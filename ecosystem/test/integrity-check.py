#!/usr/bin/env python3
"""Integrity check for the ecosystem web (https://github.com/haxtheweb/issues/issues/3259).

Reads every web in ecosystem/web (hax-<web>.mmd and hax-<web>.json) and exits 1 when one breaks a rule:

  title and type   every tile has a label and sits in a subgraph (its group is its type)
  references       connections, annotations, details, evidence and tours name tiles that exist; a portal's
                   tile exists in the web it comes from; a tile that opens a web (web=<id>) opens one that
                   exists
  pillars          the main web's pillars are the seven in build/data/pillars.json, with their icon and color
  path to a pillar every tile in the main web reaches a pillar along its connections without passing through
                   the center (people and their companion, who touch every pillar); every sub-web is
                   opened by a tile and its parents (meta.parent) lead back to the main web
  no orphans       every tile has a connection. In a sub-web a tile may stand alone only as a gap
                   (status "gap": something a coverage map says is missing), as a portal (the same tile,
                   connected in the web it comes from) or when integrity-allow.json names it with a reason

  python3 -I ecosystem/test/integrity-check.py            check ecosystem/web
  python3 -I ecosystem/test/integrity-check.py <folder>   check another folder of webs
  python3 -I ecosystem/test/integrity-check.py --self-test

Standard library only. The structure rules follow the player's own parser (player/template.html), so a
web that passes here reads the same way there; ecosystem/test/parse-check.js runs the player itself."""
import glob, json, os, re, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ECO = os.path.dirname(HERE)
MAIN = "main"  # the web hax-ecosystem is called "main" everywhere a web is named
NODE = re.compile(r'^(\w+)\s*(\(\(|\{\{|\[\[|\[\(|\(\[|\[|>)\s*"?(.*?)"?\s*(\)\)|\}\}|\]\]|\)\]|\]\)|\])$')
EDGE = re.compile(r"^(\w+)\s*(-->|---|--o|==>|-\.->)\s*(?:\|([^|]*)\|)?\s*(\w+)$")
SUBGRAPH = re.compile(r'^subgraph\s+(\w+)\s*(?:\[\s*"?([^"\]]*)"?\s*\])?$')
ANNOTATION = re.compile(r"^(group|node)\s+(\w+)\s*(.*)$")


def parse(text):
    """The Mermaid subset the player reads: subgraphs, tiles, connections and %%@ annotations."""
    web = {"nodes": {}, "edges": [], "groups": set(), "ann": {}, "errors": []}
    group = None
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        if line.startswith("%%@"):
            found = ANNOTATION.match(line[3:].strip())
            if found:
                values = {}
                for part in found.group(3).split():
                    key, eq, value = part.partition("=")
                    values[key] = value if eq else True
                web["ann"].setdefault((found.group(1), found.group(2)), {"line": number}).update(values)
            continue
        if line.startswith("%%") or re.match(r"^(flowchart|graph)\b", line):
            continue
        found = SUBGRAPH.match(line)
        if found:
            group = found.group(1)
            web["groups"].add(group)
            continue
        if line == "end":
            group = None
            continue
        found = EDGE.match(line)
        if found:
            web["edges"].append((found.group(1), found.group(4), number))
            continue
        found = NODE.match(line)
        if found:
            if found.group(1) in web["nodes"]:
                web["errors"].append(f'line {number}: "{found.group(1)}" is declared twice')
            else:
                web["nodes"][found.group(1)] = {"label": found.group(3).strip(), "group": group, "line": number}
            continue
        web["errors"].append(f'line {number}: couldn\'t read "{line[:40]}"')
    return web


def load(folder):
    webs = {}
    for path in sorted(glob.glob(os.path.join(folder, "hax-*.mmd"))):
        name = os.path.basename(path)[4:-4]
        with open(path, encoding="utf-8") as f:
            web = parse(f.read())
        details = path[:-4] + ".json"
        if os.path.isfile(details):
            try:
                with open(details, encoding="utf-8") as f:
                    web["doc"] = json.load(f)
            except ValueError as e:
                web["doc"] = {}
                web["errors"].append(f"hax-{name}.json is not valid JSON: {e}")
        else:
            web["doc"] = {}
            web["errors"].append(f"hax-{name}.json is missing")
        webs[MAIN if name == "ecosystem" else name] = web
    return webs


def neighbors(web):
    out = {i: set() for i in web["nodes"]}
    for a, b, _ in web["edges"]:
        if a in out and b in out and a != b:
            out[a].add(b)
            out[b].add(a)
    return out


def check(webs, pillars=None, allow=None):
    """Every broken rule, as {web: [message]}. pillars is build/data/pillars.json's list, allow is integrity-allow.json's orphans."""
    allow = allow or {}
    errors = {w: list(web["errors"]) for w, web in webs.items()}
    if MAIN not in webs:
        return {MAIN: ["hax-ecosystem.mmd is missing"]}
    used_allow = set()
    opened_by = {}  # web -> [(web, tile)] that open it
    for w, web in webs.items():
        E, nodes, doc = errors[w], web["nodes"], web["doc"]
        details = doc.get("nodes") or {}
        for (kind, i), a in web["ann"].items():
            if kind == "group" and i not in web["groups"]:
                E.append(f'line {a["line"]}: no subgraph "{i}"')
            if kind == "node" and i not in nodes:
                E.append(f'line {a["line"]}: no tile "{i}"')
            if kind == "node" and i in nodes and a.get("web"):
                opened_by.setdefault(a["web"], []).append((w, i))
                if a["web"] not in webs:
                    E.append(f'line {a["line"]}: "{i}" opens the web "{a["web"]}", which doesn\'t exist')
        for a, b, line in web["edges"]:
            for i in (a, b):
                if i not in nodes:
                    E.append(f'line {line}: connection uses undeclared tile "{i}"')
        linked = neighbors(web)
        pairs = {a + ">" + b for a, b, _ in web["edges"]}
        for i, n in nodes.items():
            a = web["ann"].get(("node", i), {})
            portal = a.get("portal")
            if portal:  # the same tile as in another web: its title, look and details come from there
                source = MAIN if portal is True else portal
                if source not in webs or i not in webs[source]["nodes"] or source == w:
                    E.append(f'line {n["line"]}: portal "{i}" has no tile in the {source} web')
            elif not n["label"]:
                E.append(f'line {n["line"]}: "{i}" has no title')
            if not n["group"]:
                E.append(f'line {n["line"]}: "{i}" is outside every subgraph, so it has no type')
            if not linked[i]:
                key = f"{w}:{i}"
                if w != MAIN and (portal or (details.get(i) or {}).get("status") == "gap"):
                    continue
                if w != MAIN and key in allow:
                    used_allow.add(key)
                    continue
                E.append(f'line {n["line"]}: "{i}" is an orphan: no connection to any other tile')
        for i in details:
            if i not in nodes:
                E.append(f'details for unknown tile "{i}"')
        for key in doc.get("evidence") or {}:
            if key not in pairs:
                E.append(f'evidence "{key}" has no matching connection')
        for tour in doc.get("tours") or []:
            for scene in tour.get("scenes") or []:
                for i in scene.get("nodes") or []:
                    if i not in nodes:
                        E.append(f'tour "{tour.get("id")}" uses unknown tile "{i}"')
    for key in sorted(set(allow) - used_allow):
        errors.setdefault(key.split(":")[0], []).append(f'integrity-allow.json lists "{key}", which is no longer an orphan (or no longer exists): remove it')

    # pillars, and a path to one for every tile in the main web
    main = webs[MAIN]
    E = errors[MAIN]
    pillar_ids = {i for i, n in main["nodes"].items() if n["group"] == "pillars"}
    if not pillar_ids:
        E.append('no "pillars" subgraph with tiles in it')
    if pillars is not None:
        want = {p["id"]: p for p in pillars}
        for i in sorted(set(want) - pillar_ids):
            E.append(f'pillar "{i}" (build/data/pillars.json) is not in the pillars subgraph')
        for i in sorted(pillar_ids - set(want)):
            E.append(f'"{i}" is in the pillars subgraph but not in build/data/pillars.json')
        for i in sorted(pillar_ids & set(want)):
            a = main["ann"].get(("node", i), {})
            for field in ("icon", "color"):
                if a.get(field) != want[i].get(field):
                    E.append(f'pillar "{i}" has {field} "{a.get(field)}"; build/data/pillars.json says "{want[i].get(field)}"')
    center = {i for i, n in main["nodes"].items() if n["group"] == "center"}
    linked = neighbors(main)
    reached, todo = set(pillar_ids), list(pillar_ids)
    while todo:
        for other in linked[todo.pop()]:
            if other not in reached and other not in center:
                reached.add(other)
                todo.append(other)
    for i, n in main["nodes"].items():
        if i not in reached and i not in center:
            E.append(f'line {n["line"]}: "{i}" has no path to a pillar (other than through the center)')

    # every sub-web is opened by a tile, and its parents lead back to the main web
    for w, web in webs.items():
        if w == MAIN:
            continue
        E = errors[w]
        parent = (web["doc"].get("meta") or {}).get("parent")
        if not parent:
            E.append("meta.parent is missing: name the web this one opens from")
            continue
        if parent not in webs or parent == w:
            E.append(f'meta.parent is "{parent}", which isn\'t a web')
            continue
        if not opened_by.get(w):
            E.append(f'no tile opens this web (web={w}), so nothing leads here')
        seen, at = {w}, parent
        while at != MAIN:
            if at in seen or at not in webs:
                E.append("its parents never lead back to the main web")
                break
            seen.add(at)
            at = (webs[at]["doc"].get("meta") or {}).get("parent")
    return {w: e for w, e in errors.items() if e}


def self_test():
    """The rules against small webs written here: one that passes, then one break per rule."""
    good_main = 'flowchart TB\n  subgraph center ["c"]\n    human(("Humans"))\n  end\n  subgraph pillars ["p"]\n    open{{"Open"}}\n  end\n' \
                '  subgraph core ["core"]\n    cms["CMS"]\n    cli["CLI"]\n  end\n  human ==> open\n  cms ==> open\n  cli --> cms\n' \
                "  %%@ node open icon=icons:lock-open color=keystoneYellow\n  %%@ node cli web=cli\n"
    good_sub = 'flowchart TB\n  subgraph g ["g"]\n    cli["cli"]\n    a["A"]\n    lone["Lone"]\n  end\n  cli --> a\n  %%@ node cli portal\n'
    good_main_doc = {"nodes": {"cms": {"desc": "x"}}, "evidence": {"cms>open": {}}, "tours": [{"id": "t", "scenes": [{"nodes": ["cms", "cli"]}]}]}
    good_sub_doc = {"meta": {"parent": "main"}, "nodes": {"lone": {"status": "gap"}}}
    pillars = [{"id": "open", "icon": "icons:lock-open", "color": "keystoneYellow"}]

    def run(main=good_main, sub=good_sub, main_doc=good_main_doc, sub_doc=good_sub_doc, allow=None):
        with tempfile.TemporaryDirectory() as d:
            for name, text, doc in (("ecosystem", main, main_doc), ("cli", sub, sub_doc)):
                with open(os.path.join(d, f"hax-{name}.mmd"), "w", encoding="utf-8") as f:
                    f.write(text)
                with open(os.path.join(d, f"hax-{name}.json"), "w", encoding="utf-8") as f:
                    json.dump(doc, f)
            return " | ".join(m for e in check(load(d), pillars, allow).values() for m in e)

    cases = [
        ("a sound web passes", run(), None),
        ("no title", run(main=good_main.replace('cms["CMS"]', 'cms[""]')), "has no title"),
        ("no type", run(main=good_main + '  loose["Loose"]\n  loose --> cms\n'), "has no type"),
        ("orphan", run(main=good_main.replace("  cli --> cms\n", "")), '"cli" is an orphan'),
        ("no path to a pillar", run(main=good_main.replace("  cms ==> open\n", "  cms --> human\n")), '"cms" has no path to a pillar'),
        ("pillar color", run(main=good_main.replace("keystoneYellow", "skyBlue")), 'pillar "open" has color'),
        ("tour reference", run(main_doc=dict(good_main_doc, tours=[{"id": "t", "scenes": [{"nodes": ["nope"]}]}])), 'tour "t" uses unknown tile "nope"'),
        ("evidence reference", run(main_doc=dict(good_main_doc, evidence={"cms>cli": {}})), 'evidence "cms>cli"'),
        ("details reference", run(main_doc=dict(good_main_doc, nodes={"nope": {}})), 'details for unknown tile "nope"'),
        ("connection reference", run(main=good_main + "  cms --> nope\n"), 'undeclared tile "nope"'),
        ("portal reference", run(sub=good_sub + '  subgraph h ["h"]\n    ghost["ghost"]\n  end\n  ghost --> a\n  %%@ node ghost portal\n'), 'portal "ghost" has no tile in the main web'),
        ("web reference", run(main=good_main.replace("web=cli", "web=nope")), 'opens the web "nope"'),
        ("sub-web nothing opens", run(main=good_main.replace("  %%@ node cli web=cli\n", "")), "no tile opens this web"),
        ("sub-web without a parent", run(sub_doc={"nodes": {"lone": {"status": "gap"}}}), "meta.parent is missing"),
        ("sub-web orphan", run(sub_doc={"meta": {"parent": "main"}}), '"lone" is an orphan'),
        ("sub-web orphan allowed by name", run(sub_doc={"meta": {"parent": "main"}}, allow={"cli:lone": "why"}), None),
        ("stale allow entry", run(allow={"cli:a": "why"}), 'lists "cli:a"'),
    ]
    failed = 0
    for name, got, want in cases:
        ok = (got == "") if want is None else (want in got)
        if not ok:
            failed += 1
            print(f"self-test FAILED: {name}: got {got!r}, wanted {want!r}")
    print(f"self-test: {len(cases) - failed} of {len(cases)} cases pass")
    return 1 if failed else 0


def main(argv):
    if "--self-test" in argv:
        return self_test()
    folders = [a for a in argv if not a.startswith("--")]
    folder = folders[0] if folders else os.path.join(ECO, "web")
    with open(os.path.join(ECO, "build", "data", "pillars.json"), encoding="utf-8") as f:
        pillars = json.load(f)["pillars"]
    with open(os.path.join(HERE, "integrity-allow.json"), encoding="utf-8") as f:
        allow = json.load(f)["orphans"]
    webs = load(folder)
    errors = check(webs, pillars, allow)
    total = 0
    for w in sorted(errors):
        name = "hax-ecosystem" if w == MAIN else "hax-" + w
        print(f"## {name}")
        for message in errors[w]:
            total += 1
            # names come from the files under review: keep each message on one line and out of the runner's command syntax
            message = re.sub(r"\s+", " ", message).replace("::", ": :")
            print("  " + message)
            if os.environ.get("GITHUB_ACTIONS"):
                found = re.match(r"line (\d+): (.*)", message)
                where = f"file=ecosystem/web/{name}.mmd,line={found.group(1)}" if found else f"file=ecosystem/web/{name}.json"
                print(f"::error {where},title=Ecosystem web integrity::{(found.group(2) if found else message).replace('%', '%25')}")
    tiles = sum(len(web["nodes"]) for web in webs.values())
    print(f"integrity: {total} errors in {len(webs)} webs, {tiles} tiles")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
