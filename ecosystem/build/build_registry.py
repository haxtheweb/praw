"""Registry and manifests sub-web: the generated JSON files that tell HAX which elements exist, where each loads from,
what each declares and which languages each speaks.

Generated from the webcomponents source (a sparse clone, see sources.sh): the manifests themselves (counted from their
contents), the ubiquity build in the root package.json (each step's gulp task or script is read to see which manifests
it writes or reads), the cem analyze step in each element's package.json, and every place that reads a manifest: the
built packages, haxcms-nodejs, haxcms-php, the CLI and the MCP. Which files count as manifests is the one list kept by
hand (MANIFESTS); everything about them is read from source. Details in hax-registry.json."""
import json, re, os, glob, collections
GH = "https://github.com/haxtheweb"
WCB = GH + "/webcomponents/blob/master/"
W = "wcrepo"
B = "haxcms-nodejs/src/public/build/es6/node_modules/@haxtheweb"
def S(c, *i): return {"caption": c, "nodes": list(i)}
def slug(s): return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")
MAIN = set(re.findall(r"^\s+(\w+)[\[\(\{>]", open("hax-ecosystem.mmd").read(), re.M))
EL_IDS = set(re.findall(r"^    (b_[a-z0-9_]+)", open("hax-elements.mmd").read(), re.M))
def J(p):
    try: return json.load(open(os.path.join(W, p)))
    except (FileNotFoundError, ValueError): return None

# ---------- the manifests (the one hand-kept list) and what is in each ----------
cems = sorted(glob.glob(f"{W}/elements/*/custom-elements.json"))
def count_cem():
    n = 0
    for f in cems:
        for mod in json.load(open(f)).get("modules", []):
            n += sum(1 for d in mod.get("declarations", []) if d.get("customElement") or d.get("tagName"))
    return n
MANIFESTS = [  # id, file name, path in webcomponents (None = one per element), what it is
    ("m_wcregistry", "wc-registry.json", "wc-registry.json", "Every tag the autoloader can load, mapped to the module that defines it. Copied into each HAXcms build and site."),
    ("m_wcgraph", "wc-registry-graph.json", "wc-registry-graph.json", "The import graph behind the registry, so a page can preload what a tag will pull in."),
    ("m_cem", "custom-elements.json", None, "The Custom Elements Manifest of a package: its elements' properties, attributes, events, slots and CSS parts, written by cem analyze."),
    ("m_catalog", "elements-catalog.json", "elements-catalog.json", "One entry per element (tag, title, package, import, whether HAX can author it) for search: hax wc --search."),
    ("m_haxreg", "hax-elements-registry.json", "hax-elements-registry.json", "The tags HAX can author, with their display titles."),
    ("m_translations", "translation-manifest.json", "elements/i18n-manager/lib/translation-manifest.json", "Which elements ship which locale files, scanned from every element's locales folder."),
    ("m_languages", "languages.json", "elements/i18n-manager/lib/languages.json", "The languages HAX offers, with their names and direction; kept in sync wherever it is copied."),
]
MANIFESTS = [m for m in MANIFESTS if (m[2] is None and cems) or (m[2] and os.path.exists(os.path.join(W, m[2])))]
def size(mid):
    if mid == "m_wcregistry": d = J("wc-registry.json"); return f"{len(d)} tags, {sum(1 for v in d.values() if v.startswith('@haxtheweb/'))} of them HAX packages"
    if mid == "m_wcgraph": d = J("wc-registry-graph.json"); return f"{len(d.get('tags', []))} tags over {len(d.get('paths', []))} module paths"
    if mid == "m_cem": return f"{len(cems)} packages declare {count_cem()} elements"
    if mid == "m_catalog": d = J("elements-catalog.json"); e = d.get("elements", []); return f"{len(e)} elements, {sum(1 for x in e if x.get('haxCapable'))} HAX can author"
    if mid == "m_haxreg": return f"{len(J('hax-elements-registry.json'))} authorable tags"
    if mid == "m_translations": m = J("elements/i18n-manager/lib/translation-manifest.json")["_meta"]; return f"{m['elementsWithTranslations']} of {m['elementsScanned']} elements translated, {m['translationFilesFound']:,} files, {len(m['languagesSupported'])} languages"
    if mid == "m_languages": return f"{len(J('elements/i18n-manager/lib/languages.json')['languages'])} languages"
    return ""

# ---------- who writes and reads them inside webcomponents: the ubiquity steps and other scripts ----------
pkg = J("package.json"); scripts = pkg["scripts"]
gulp = open(f"{W}/gulpfile.mjs").read()
def gulp_task(name):
    """the text of one gulp.task(...) call: scan to its closing parenthesis, skipping strings and comments"""
    m = re.search(r'gulp\.task\(\s*["\']' + re.escape(name) + r'["\']', gulp)
    if not m: return ""
    nxt = gulp.find("gulp.task(", m.end())  # never run past the next task, even if a regex literal confuses the scan
    i, depth, n = m.start() + len("gulp.task"), 0, nxt if nxt > 0 else len(gulp)
    while i < n:
        c = gulp[i]
        if gulp.startswith("//", i): i = gulp.find("\n", i); i = n if i < 0 else i; continue
        if gulp.startswith("/*", i): i = gulp.find("*/", i + 2); i = n if i < 0 else i + 2; continue
        if c in "\"'`":
            j = i + 1
            while j < n and gulp[j] != c: j += 2 if gulp[j] == "\\" else 1
            i = j + 1; continue
        if c == "(": depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0: return gulp[m.start(): i + 1]
        i += 1
    return gulp[m.start(): n]
def source_of(cmd):
    text, files = "", []
    m = re.match(r"gulp ([\w-]+)", cmd)
    if m: text += gulp_task(m.group(1)); files.append("gulpfile.mjs")
    for f in re.findall(r"scripts/[\w./-]+\.(?:m?js|cjs)", cmd + text):
        if os.path.exists(os.path.join(W, f)): text += open(os.path.join(W, f)).read(); files.append(f)
    return text, files
def touches(text):
    """manifests a source writes and reads: written when a writeFileSync call's target names it, directly or through a variable"""
    targets = re.findall(r"writeFileSync\(\s*([^,]+?)\s*,", text)
    out = {}
    for mid, name, *_ in MANIFESTS:
        if name not in text: continue
        names_var = set(re.findall(r"(?:const|let|var)\s+(\w+)\s*=[^;\n]*" + re.escape(name), text))
        if any(name in t or t.strip() in names_var for t in targets): out[mid] = "writes"
        elif re.search(r"source\W[^\n]*" + re.escape(name), text) and targets: out[mid] = "copies"  # a sync step: name is a copy source
        else: out[mid] = "reads"
    return out
steps = []
for i, raw in enumerate(x.strip() for x in scripts.get("ubiquity", "").split("&&")):
    name = raw.replace("yarn run ", "")
    text, files = source_of(scripts.get(name, raw))
    t = touches(text)
    if t: steps.append({"id": "st_" + slug(name), "label": name, "n": i + 1, "files": files, "t": t, "ubiquity": True})
in_ubiq = {f for s in steps for f in s["files"] if f != "gulpfile.mjs"}
for f in sorted(glob.glob(f"{W}/scripts/*.*js")):
    rel = os.path.relpath(f, W)
    if rel in in_ubiq: continue
    t = touches(open(f).read())
    if t: steps.append({"id": "sc_" + slug(os.path.basename(f).rsplit(".", 1)[0]), "label": os.path.basename(f), "n": None, "files": [rel], "t": t, "ubiquity": False})
cem_pkgs = []
for f in sorted(glob.glob(f"{W}/elements/*/package.json")):
    if "cem analyze" in json.load(open(f)).get("scripts", {}).get("build", ""): cem_pkgs.append(f.split("/")[-2])
if cem_pkgs and any(m[0] == "m_cem" for m in MANIFESTS):
    steps.append({"id": "st_cem_analyze", "label": "cem analyze", "n": None, "files": [], "t": {"m_cem": "writes"}, "ubiquity": False, "cem": len(cem_pkgs)})

# ---------- who reads them outside webcomponents ----------
CODE = (".js", ".mjs", ".cjs", ".php", ".py", ".ts")
def scan(root, skip=("node_modules", ".git", "test", "tests", "locales", "build", "boilerplate", "skills", ".well-known")):
    hits = collections.defaultdict(set)
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in skip]
        for f in fn:
            if not f.endswith(CODE) or ".test." in f or ".spec." in f: continue
            try: s = open(os.path.join(dp, f), errors="ignore").read()
            except OSError: continue
            for mid, name, *_ in MANIFESTS:
                if name in s: hits[mid].add(os.path.relpath(os.path.join(dp, f), root))
    return hits
readers = collections.OrderedDict()  # tile id -> {label, portal, uses: {mid: [files]}}
for owner, root, url in [("nodejs", "haxcms-nodejs/src", GH + "/haxcms-nodejs/blob/main/src/"), ("php", "haxcms-php/system/backend", GH + "/haxcms-php/blob/master/system/backend/"),
                         ("cli", "createrepo/src", GH + "/create/blob/main/src/"), ("mcp", "mcprepo/src", GH + "/haxcms-mcp/blob/main/src/")]:
    if owner not in MAIN or not os.path.isdir(root): continue
    h = scan(root)
    if h: readers[owner] = {"portal": "", "uses": {m: sorted(v) for m, v in h.items()}, "url": url}
if os.path.isdir(B):
    for p in sorted(os.listdir(B)):
        h = scan(os.path.join(B, p), skip=("node_modules", "test", "demo", "locales"))
        if not h: continue
        bid = "b_" + slug(p)
        readers[bid if bid in EL_IDS else "pk_" + slug(p)] = {"portal": "elements" if bid in EL_IDS else None, "label": p, "uses": {m: sorted(v) for m, v in h.items()},
                                                                "url": GH + f"/webcomponents/tree/master/elements/{p}"}

# ---------- write the web ----------
UB = [p for p in ["ubiquity", "components", "languages", "efficient"] if p in MAIN]
lines = ["%% Registry and manifests sub-web, generated by build_registry.py from the webcomponents source, the built packages and the backends.",
         "%% Portals: ids from hax-ecosystem.mmd and hax-elements.mmd. Details in hax-registry.json.",
         "flowchart TB", "  %%@ layout rings=0,240,480,740,980 sizes=92,60,50,48,46",
         '  subgraph hub ["Registry and manifests"]', '    registry[("registry")]', "  end", '  subgraph mans ["Manifests"]']
for mid, name, *_ in MANIFESTS: lines.append(f'    {mid}[("{name}")]')
lines += ["  end", '  subgraph stepsg ["Steps that write and read them"]']
for s in steps: lines.append(f'    {s["id"]}["{(str(s["n"]) + ". ") if s["n"] else ""}{s["label"]}"]')
lines += ["  end", '  subgraph readg ["Who reads them"]']
for rid, r in readers.items(): lines.append(f'    {rid}["{r.get("label", rid)}"]')
lines += ["  end", '  subgraph ctx ["Around it"]']
for p in UB: lines.append(f'    {p}["{p}"]')
lines += ["  end", ""]
for mid, *_ in MANIFESTS: lines.append(f"  registry -->|includes| {mid}")
for s in steps:
    for mid, how in s["t"].items(): lines.append(f"  {s['id']} -->|{how}| {mid}" if how in ("writes", "copies") else f"  {mid} -.->|is read by| {s['id']}")
    if s["ubiquity"] and "ubiquity" in UB: lines.append(f"  ubiquity -->|runs| {s['id']}")
for rid, r in readers.items():
    for mid in r["uses"]: lines.append(f"  {mid} -.->|is read by| {rid}")
if "components" in UB: lines.append("  registry -.->|describes| components")
if "languages" in UB and any(m[0] == "m_translations" for m in MANIFESTS): lines.append("  m_translations -.->|counts| languages")
if "efficient" in UB and any(m[0] == "m_wcregistry" for m in MANIFESTS): lines.append("  m_wcregistry ==>|keeps it| efficient")
lines += ["", "  %%@ group hub tier=0", "  %%@ group mans tier=1", "  %%@ group stepsg tier=2", "  %%@ group readg tier=3", "  %%@ group ctx tier=4",
          "  %%@ node registry icon=hax:apps color=creekTeal motion=pulse"]
for mid, *_ in MANIFESTS: lines.append(f"  %%@ node {mid} icon=hax:code-json color=creekTeal motion=nudge")
for s in steps: lines.append(f"  %%@ node {s['id']} icon=hax:code-json color={'beaverBlue' if s['ubiquity'] else 'slateGray'} motion=nudge")
for rid, r in readers.items():
    if r["portal"] == "": lines.append(f"  %%@ node {rid} portal")
    elif r["portal"]: lines.append(f"  %%@ node {rid} portal={r['portal']}")
    else: lines.append(f"  %%@ node {rid} icon=hax:code-json color=limestoneGray motion=nudge")
for p in UB: lines.append(f"  %%@ node {p} portal")
open("hax-registry.mmd", "w").write("\n".join(lines) + "\n")

nodes = {"registry": {"always": True, "desc": f"The generated files that tell HAX which elements exist, where each loads from, what each declares and which languages each speaks: {len(MANIFESTS)} kinds of manifest, written by the ubiquity build and the cem analyzer, read by {len(readers)} packages and tools."}}
for mid, name, path, about in MANIFESTS:
    nodes[mid] = {"desc": f"{about} Today: {size(mid)}.", "kind": "manifest", "links": {"file": WCB + path} if path else {"example": WCB + "elements/a11y-collapse/custom-elements.json"}}
for s in steps:
    w = [n for m, h in s["t"].items() if h == "writes" for i, n, *_ in MANIFESTS if i == m]
    r = [n for m, h in s["t"].items() if h == "reads" for i, n, *_ in MANIFESTS if i == m]
    c = [n for m, h in s["t"].items() if h == "copies" for i, n, *_ in MANIFESTS if i == m]
    where = f"Step {s['n']} of the ubiquity build." if s["n"] else (f"Run by the build script of {s['cem']} element packages; {len(cems)} commit the result." if s.get("cem") else "A script outside the ubiquity build.")
    d = {"desc": " ".join(x for x in [where, f"Writes {', '.join(w)}." if w else "", f"Reads {', '.join(r)}." if r else "", f"Copies {', '.join(c)} into the backends and the CLI." if c else ""] if x), "kind": "step"}
    if s["files"]: d["links"] = {f.rsplit("/", 1)[-1]: WCB + f for f in s["files"][:4]}
    nodes[s["id"]] = d
for rid, r in readers.items():
    names = {i: n for i, n, *_ in MANIFESTS}
    d = {"desc": "Reads " + "; ".join(f"{names[m]} in {', '.join(fs[:3])}{' and more' if len(fs) > 3 else ''}" for m, fs in r["uses"].items()) + ".", "kind": "reader"}
    if r["portal"] is None: d["links"] = {"package": r["url"]}
    nodes[rid] = d
written = {m for s in steps for m, h in s["t"].items() if h == "writes"}
for mid, name, *_ in MANIFESTS:
    copiers = [s["label"] for s in steps if s["t"].get(mid) == "copies"]
    if mid not in written: nodes[mid]["note"] = f"Kept by hand at its source; {', '.join(copiers)} copies it out." if copiers else "No step found that writes it: it may be written by a tool this generator does not read."
tours = [{"id": "registry", "label": "How HAX knows its own elements", "kind": "story",
          "message": f"{len(MANIFESTS)} manifests, {sum(1 for s in steps if s['ubiquity'])} ubiquity steps that touch them, {len(readers)} readers.",
          "scenes": [S("The registry: where every tag loads from, and the import graph behind it.", *[m for m in ("m_wcregistry", "m_wcgraph") if m in nodes], *[r for r, v in readers.items() if "m_wcregistry" in v["uses"] or "m_wcgraph" in v["uses"]]),
                     S("Each package describes its elements in a Custom Elements Manifest; the catalog and HAX's registry are built from them.", *[m for m in ("m_cem", "m_catalog", "m_haxreg") if m in nodes], *[s["id"] for s in steps if set(s["t"]) & {"m_cem", "m_catalog", "m_haxreg"}]),
                     S("Translations: which languages exist and which elements speak them.", *[m for m in ("m_languages", "m_translations") if m in nodes], *[r for r, v in readers.items() if set(v["uses"]) & {"m_languages", "m_translations"}], *[p for p in ["languages"] if p in UB]),
                     S("The ubiquity build writes them in order.", *[p for p in ["ubiquity"] if p in UB], *[s["id"] for s in steps if s["ubiquity"]]),
                     S("Everything at once.")]}]
meta = {"name": "Registry and manifests", "parent": "main", "noTimeline": True,
        "sectionLabels": {"manifest": "manifests", "step": "steps that write and read them", "reader": "who reads them"},
        "about": f"The manifests HAX generates about its own elements, from the webcomponents source: {'; '.join(f'{n}: {size(i)}' for i, n, *_ in MANIFESTS)}. Steps are read from the ubiquity build and each element's build script; readers are found by scanning the built packages and the backends.",
        "kindLabels": {"rel": "writes and includes", "schema": "is read by"},
        "links": {"package.json": WCB + "package.json", "gulpfile": WCB + "gulpfile.mjs"}}
json.dump({"meta": meta, "nodes": nodes, "evidence": {}, "tours": tours}, open("hax-registry.json", "w"), indent=1, ensure_ascii=False)
print(len(MANIFESTS), "manifests;", len(steps), "steps;", len(readers), "readers:", list(readers))
