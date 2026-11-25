"""Checks for the connection sprint tools: python3 -I ecosystem/test/connection-tools-check.py

ecosystem/build/route_edit.py (where a praw-edit/1 change goes)
- finds the block inside a copied prompt, and refuses tiles that are not on disk
- sends the main web's text to build_json.py and its connections to the curated .mmd
- sends a generated web to its generator, never to its .mmd
- a connection the web already draws with the same verb gets evidence, not a second line
- a removal names the line it removes

ecosystem/build/connection_gaps.py (where the web is thin)
- every tile it names is a real tile, and its link is the tile's hax.cloud address with the Connect lens on
- the address is the one build_site.py gives the same key"""
import importlib.util, json, os, re, sys, uuid

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(os.path.dirname(HERE), "build")


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(BUILD, name + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R = load("route_edit")
G = load("connection_gaps")
ok = 0


def check(cond, what):
    global ok
    if not cond:
        sys.exit("FAILED: " + what)
    ok += 1


webs = R.load_webs()
gens = R.writers()
main = webs["main"]
# a person in the main web with at least one connection, and a tile they are not connected to
person = next(n for n, g in main["group"].items() if g == "people" and any(n in (e[0], e[3]) for e in main["edges"]))
edge = next(e for e in main["edges"] if person in (e[0], e[3]))
other = edge[3] if edge[0] == person else edge[0]
stranger = next(n for n, g in main["group"].items() if g == "core" and not any({person, n} == {e[0], e[3]} for e in main["edges"]))

block = {"format": R.FORMAT, "tile": f"tile:main:{person}", "label": "Someone",
         "says": {"now": "a", "proposed": "b"},
         "connections": [
             {"sentence": "same", "verb": edge[2], "to": f"tile:main:{other}", "claim": "sourced", "evidence": [{"url": "https://example.org"}]},
             {"sentence": "new", "verb": "worked on", "to": f"tile:main:{stranger}", "claim": "interpretive", "evidence": []},
             {"sentence": "gone", "remove": True, "replaces": {"web": "main", "from": edge[0], "to": edge[3], "label": edge[2]}, "claim": "interpretive", "evidence": []},
             {"sentence": "brand new", "verb": "presented at", "to": None, "new": {"label": "A conference", "kind": "event"}, "claim": "interpretive", "evidence": []},
         ],
         "links": [{"kind": "linkedin", "url": "https://www.linkedin.com/in/x"}]}
prompt = "Some words.\n\n```" + R.FORMAT + "\n" + json.dumps(block) + "\n```\n"
found = R.blocks(prompt)
check(len(found) == 1 and found[0]["tile"] == block["tile"], "finds the block inside a copied prompt")
check(R.blocks("```" + R.FORMAT + "\nnot json\n```") == [], "ignores a block that is not JSON")
out = "\n".join(R.plan(found[0], webs, gens))
check("says: replace the desc of `%s` in build/build_json.py" % person in out, "the main web's text goes to build_json.py")
check(f"already drawn as `{edge[0]} {edge[1]}|{edge[2]}| {edge[3]}`" in out, "the same connection gets evidence, not a second line")
check(re.search(r"draw `%s [-=.o>]+\|worked on\| %s` in web/hax-ecosystem\.mmd" % (person, stranger), out), "a new connection in the main web is drawn in its .mmd")
check(f"remove “gone”: found as `{edge[0]} {edge[1]}|{edge[2]}| {edge[3]}`" in out, "a removal names the line it removes")
check("NEW tile “A conference” (event)" in out and "subgraph `comms`" in out, "a new tile is placed by its kind")
check("link linkedin: https://www.linkedin.com/in/x" in out, "links go to the tile's links")
check(R.plan({"format": R.FORMAT, "tile": "tile:main:not_a_tile", "label": "X"}, webs, gens)[0].startswith("STOP"), "refuses a tile that is not on disk")
for w, g in [("rules", "build_rules.py"), ("heosat", "build_heosat.py"), ("tutorials", "build_tutorials.py"), ("openapi", "build_generated.py")]:
    check(R.route(w, gens)[0].startswith("build/" + g), f"{w} is changed through {g}")

report = G.gaps(0)
check(report and all(s["count"] == len(s["tiles"]) for s in report), "the report lists every tile when not cut short")
ns = uuid.UUID("6f1d2c3a-0b8e-4c55-9a7e-1a2b3c4d5e6f")
site = open(os.path.join(BUILD, "build_site.py"), encoding="utf-8").read()
check(f'uuid.UUID("{ns}")' in site, "the gaps report uses the namespace build_site.py uses for addresses")
pins = G.PINS
for s in report:
    for t in s["tiles"]:
        if not t["tile"].startswith("tile:"):
            continue
        _, w, n = t["tile"].split(":", 2)
        check(n in webs[w]["ids"], f"{t['tile']} is a real tile")
        a = pins.get(t["tile"]) or uuid.uuid5(ns, t["tile"]).hex[:8]
        check(t["connect"] == f"https://hax.cloud/stories/{a}?goggles=connect&from={a}", f"{t['tile']} links to its address with the Connect lens on")
print(f"connection tools: {ok} checks passed")
