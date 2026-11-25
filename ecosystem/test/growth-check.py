"""Check the growth data layer's committed snapshot (ecosystem/build/data/growth/, https://github.com/haxtheweb/issues/issues/3409)
holds together before hax.cloud publishes it. Standard library only; no network.

    python3 -I ecosystem/test/growth-check.py

Fails (exit 1) when a file is missing or unreadable, a date is not YYYY-MM-DD, a repository's monthly commits don't
add up to its total, an element depends on a package that isn't listed or its usedBy count is wrong, a payload
references a module that doesn't exist or its sums disagree, a journey names a theme or element with no payload, or
a series doesn't cover every month.
"""
import json, os, re, sys

DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "build", "data", "growth")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
errors = []


def err(msg):
    errors.append(msg)


def load(name):
    try:
        d = json.load(open(os.path.join(DIR, name + ".json")))
    except (OSError, ValueError) as e:
        err("%s.json: %s" % (name, e))
        return None
    for k in ("generated", "about", "license"):
        if not (d.get("meta") or {}).get(k):
            err("%s.json: meta.%s missing" % (name, k))
    return d


repos, themes, elements, payload, series = (load(n) for n in ("repos", "themes", "elements", "payload", "series"))
if repos:
    for r in repos["repos"]:
        if not DATE.match(r.get("first") or ""):
            err("repos: %s has no first commit date" % r.get("key"))
        if sum(r["monthly"].values()) != r["total"]:
            err("repos: %s monthly commits don't add up to its total" % r["key"])
if themes:
    tags = [t["tag"] for t in themes["themes"]]
    if len(tags) != len(set(tags)):
        err("themes: a tag is listed twice")
    for t in themes["themes"]:
        if not DATE.match(t.get("appeared") or ""):
            err("themes: %s has no date" % t["tag"])
        if t["gz"] <= 0 or t["gz"] > t["bytes"]:
            err("themes: %s sizes are wrong" % t["tag"])
if elements:
    names = {e["name"] for e in elements["elements"]}
    used = {}
    for e in elements["elements"]:
        if not DATE.match(e.get("appeared") or ""):
            err("elements: %s has no date" % e["name"])
        for d in e["dependsOn"]:
            if d not in names:
                err("elements: %s depends on unknown %s" % (e["name"], d))
            used[d] = used.get(d, 0) + 1
    for e in elements["elements"]:
        if e["usedBy"] != used.get(e["name"], 0):
            err("elements: %s usedBy is %d, links say %d" % (e["name"], e["usedBy"], used.get(e["name"], 0)))
if payload:
    mods = payload["modules"]
    n = len(mods)
    for group in ("themes", "elements"):
        for k, v in payload[group].items():
            if any(i < 0 or i >= n for i in v["modules"]):
                err("payload: %s %s references a missing module" % (group, k))
            elif sum(mods[i]["gz"] for i in v["modules"]) != v["gz"]:
                err("payload: %s %s gz doesn't match its modules" % (group, k))
    if sum(m["gz"] for m in mods if m["core"]) != payload["core"]["gz"]:
        err("payload: core gz doesn't match the modules marked core")
    if themes and set(payload["themes"]) != {t["tag"] for t in themes["themes"]}:
        err("payload: themes don't match themes.json")
    for j in payload["journeys"]["siteBySite"]:
        if j["theme"] not in payload["themes"]:
            err("payload: journey %s uses theme %s with no payload" % (j["site"], j["theme"]))
        for p in j["pages"]:
            for e in p["elements"] + ["grid-plate"]:
                if e not in payload["elements"]:
                    err("payload: journey %s / %s uses %s with no payload" % (j["site"], p["page"], e))
if series:
    m = series["months"]
    if m != sorted(m) or len(m) != len(set(m)):
        err("series: months out of order")
    for s in series["series"]:
        if len(s["values"]) != len(m):
            err("series: %s has %d values for %d months" % (s["key"], len(s["values"]), len(m)))

if errors:
    print("growth check: %d problem(s)" % len(errors))
    for e in errors:
        print("  " + e)
    sys.exit(1)
print("growth check: ok (%d repos, %d themes, %d elements, %d modules, %d months)" % (
    len(repos["repos"]), len(themes["themes"]), len(elements["elements"]), len(payload["modules"]), len(series["months"])))
