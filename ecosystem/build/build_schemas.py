"""Per-schema sub-webs, each generated from the file that defines the schema:
  haxschema  <- hax-schema/schema/haxProperties.schema.json (+ field usage counted across the built element packages)
  jos        <- json-outline-schema/schema/*.schema.json
  appstore   <- haxcms-nodejs src/lib/HAXAppStoreService.js + generateAppStore.js
  merlin     <- super-daemon defineOption() + every defineOption call in the built packages
  oerschema  <- oer-schema/lib/oerschema.js (latestSchema)
Rerun after a release; build_drift.py compares the next run with this one."""
import json, re, os, collections
GH = "https://github.com/haxtheweb"
WC = GH + "/webcomponents/tree/master/elements/"
NODE = GH + "/haxcms-nodejs/blob/main/"
def L(a, b): return {"label": a, "url": b}
def S(c, *i): return {"caption": c, "nodes": list(i)}
def slug(s): return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")
EL_IDS = set(re.findall(r"^    (b_[a-z0-9_]+)", open("hax-elements.mmd").read(), re.M))
def write(name, lines, meta, nodes, tours):
    open(f"hax-{name}.mmd", "w").write("\n".join(lines) + "\n")
    json.dump({"meta": meta, "nodes": nodes, "evidence": {}, "tours": tours}, open(f"hax-{name}.json", "w"), indent=1, ensure_ascii=False)
def head(title, hub_id, hub_label, rings, sizes, comment, src):
    return [f"%% {title} sub-web: {comment}", f"%% Generated from {src}. Details in the matching .json.", "flowchart TB", f"  %%@ layout rings={rings} sizes={sizes}",
            '  subgraph hub ["' + hub_label + '"]', f'    {hub_id}[("{hub_id}")]', "  end"]
REPORT = {}

# ================= HAXSchema =================
hs = json.load(open("hs/schema/haxProperties.schema.json"))
use = json.load(open("ext/field_use.json"))
enum = hs["$defs"]["inputMethod"]["enum"]
TOP = [("api", "api"), ("type", "type"), ("gizmo", "gizmo"), ("settings", "settings"), ("demoSchema", "demoSchema"), ("saveOptions", "saveOptions"), ("canScale", "canScale"), ("canEditSource", "canEditSource"), ("contentEditable", "contentEditable"), ("designSystem", "designSystem"), ("editingElement", "editingElement"), ("editMode", "editMode"), ("documentation", "documentation"), ("hideDefaultSettings", "hideDefaultSettings")]
GROUPS = ["configure", "advanced", "developer", "inline"]
FAMILY = {"Text": ["textfield", "textarea", "alt", "url", "code", "code-editor", "markup", "html-block", "md-block"], "Choice": ["boolean", "select", "radio", "combo", "number", "slider"],
          "Pickers": ["color", "colorpicker", "iconpicker", "hax-palette-picker", "haxcms-theme-picker", "date-time", "datepicker", "monthpicker", "weekpicker", "timepicker"],
          "Media and files": ["fileupload", "haxupload", "screenRecorder", "srcset"], "Structure": ["array", "object", "fieldset", "tabs", "collapse"]}
fam_of = {f: k for k, fs in FAMILY.items() for f in fs}
# element packages: top users of fields, portal to the Elements web when that block exists there
pk = collections.Counter()
for f, v in use.items():
    for p, n in v["pkgs"]: pk[p] += n
TOPPKG = [p for p, _ in pk.most_common(24)]
def pkid(p): return "b_" + p.replace("-", "_")
lines = head("HAXSchema", "haxschema", "HAXSchema", "0,300,450,650,880", "92,58,60,46,46", "what an element tells the editor, built on JSON Schema, with every field type and the elements that use it", "hax-schema/schema/haxProperties.schema.json")
lines += ['  subgraph base ["Built on"]', '    jsonschema[("JSON Schema 2020-12")]', '    hsfile[("haxProperties.schema.json")]', '    hslocale[("haxProperties.locale.schema.json")]', "  end",
          '  subgraph parts ["Parts of a haxProperties file"]']
for k, lab in TOP: lines.append(f'    hp_{slug(k)}["{lab}"]')
for g in GROUPS: lines.append(f'    sg_{g}["settings.{g}"]')
lines += ["  end", '  subgraph fams ["Field families"]']
for fam in FAMILY: lines.append(f'    fam_{slug(fam)}["{fam}"]')
lines += ["  end", '  subgraph fields ["Field types (inputMethod)"]']
for f in enum: lines.append(f'    fd_{slug(f)}["{f}"]')
lines += ["  end", '  subgraph els ["Elements that use them most"]']
for p in TOPPKG: lines.append(f'    {pkid(p)}["{p}"]')
lines += ['    editor["editor"]', '    cli["cli"]', '    contracts["contracts"]', "  end", "",
          "  haxschema -.->|is written in| jsonschema", "  hsfile -.->|is a| jsonschema", "  hslocale -.->|is a| jsonschema", "  haxschema -.->|is defined by| hsfile", "  hslocale -.->|translates| hsfile"]
for k, lab in TOP: lines.append(f"  haxschema -->|has| hp_{slug(k)}")
for g in GROUPS: lines.append(f"  hp_settings -->|groups fields into| sg_{g}")
for fam in FAMILY: lines.append(f"  sg_configure -->|uses| fam_{slug(fam)}")
for f in enum: lines.append(f"  fam_{slug(fam_of.get(f, 'Text'))} -->|includes| fd_{slug(f)}")
for f in enum:
    for p, n in (use.get(f, {}).get("pkgs") or [])[:4]:
        if p in TOPPKG: lines.append(f"  fd_{slug(f)} -->|used by| {pkid(p)}")
lines += ["  editor -.->|builds forms from| hp_settings", "  editor -.->|lists blocks from| hp_gizmo", "  editor -.->|inserts| hp_demoschema", "  cli -.->|validates against| hsfile", "  contracts -.->|includes| haxschema", "",
          "  %%@ group hub tier=0", "  %%@ group base tier=1", "  %%@ group parts tier=1", "  %%@ group fams tier=2", "  %%@ group fields tier=3", "  %%@ group els tier=4",
          "  %%@ node haxschema portal", "  %%@ node jsonschema mono=JSON color=slateGray motion=nudge", "  %%@ node hsfile icon=hax:code-json color=creekTeal motion=nudge", "  %%@ node hslocale icon=icons:translate color=creekTeal motion=nudge"]
for k, lab in TOP: lines.append(f"  %%@ node hp_{slug(k)} icon=hax:code-json color=wonderPurple motion=nudge")
for g in GROUPS: lines.append(f"  %%@ node sg_{g} icon=icons:build color=wonderPurple motion=nudge")
for fam in FAMILY: lines.append(f"  %%@ node fam_{slug(fam)} icon=hax:blocks color=roarGolden motion=pop")
for f in enum: lines.append(f"  %%@ node fd_{slug(f)} mono={(f.replace('picker','').replace('-','')[:5] or f[:5]).upper()} color={'roarGolden' if use.get(f) else 'limestoneGray'} motion=nudge")
for p in TOPPKG: lines.append(f"  %%@ node {pkid(p)} portal=elements" if pkid(p) in EL_IDS else f"  %%@ node {pkid(p)} icon=hax:bricks color=slateGray motion=nudge")
lines += ["  %%@ node editor portal", "  %%@ node cli portal", "  %%@ node contracts portal=contracts"]
props = hs["properties"]; fdef = hs["$defs"]["field"]["properties"]; gz = hs["$defs"]["gizmo"]["properties"]
nodes = {"haxschema": {"always": True},
         "jsonschema": {"desc": "JSON Schema, draft 2020-12: the standard every HAX schema file is written in, so any JSON Schema validator, editor or AI agent can read them.", "links": {"spec": "https://json-schema.org/draft/2020-12"}},
         "hsfile": {"desc": "The JSON Schema for lib/<tag>.haxProperties.json, with the descriptions and defaults from the hax-schema README. Validate with npx -p @haxtheweb/hax-schema haxproperties-validate.", "links": {"repo": GH + "/hax-schema/blob/main/schema/haxProperties.schema.json", "docs": "https://haxtheweb.github.io/hax-schema/"}},
         "hslocale": {"desc": "The JSON Schema for locales/<tag>.<lang>.haxProperties.json, the translation overlays the editor uses for other languages.", "links": {"repo": GH + "/hax-schema/blob/main/schema/haxProperties.locale.schema.json"}}}
for k, lab in TOP:
    d = props.get(k, {}).get("description", "")
    if k == "gizmo": d += " Gizmo fields: " + ", ".join(gz) + "."
    if k == "settings": d += " Each field can set: " + ", ".join(list(fdef)[:16]) + " and more."
    nodes[f"hp_{slug(k)}"] = {"desc": d.strip(), "kind": "part"}
GDESC = {"configure": "The fields an author sees first when they select the block.", "advanced": "Fields shown under Advanced.", "developer": "Fields only developers need.", "inline": "Fields shown inline on the block while editing."}
for g in GROUPS: nodes[f"sg_{g}"] = {"desc": GDESC[g], "kind": "part"}
for fam, fs in FAMILY.items(): nodes[f"fam_{slug(fam)}"] = {"desc": f"{fam} fields: {', '.join(fs)}.", "kind": "family"}
for f in enum:
    u = use.get(f)
    nodes[f"fd_{slug(f)}"] = {"desc": (f"inputMethod \"{f}\": used {u['total']} times across {len(u['pkgs'])} element packages, most in {', '.join(p for p, _ in u['pkgs'][:3])}." if u else f"inputMethod \"{f}\": defined by the schema; no built element package uses it yet."), "kind": "field"}
for p in TOPPKG:
    if pkid(p) not in EL_IDS: nodes[pkid(p)] = {"desc": f"@haxtheweb/{p}: {pk[p]} editing fields across its haxProperties.", "links": {"repo": WC + p}, "kind": "element"}
unused = [f for f in enum if not use.get(f)]
tours = [{"id": "haxschema", "label": "How an element talks to the editor", "message": f"HAXSchema in parts: a JSON Schema file, {len(TOP)} top-level keys, four settings groups and {len(enum)} field types.", "scenes": [
    S("HAXSchema is written in JSON Schema, with a second schema for translations.", "haxschema", "jsonschema", "hsfile", "hslocale"),
    S("A haxProperties file has these parts.", *[f"hp_{slug(k)}" for k, _ in TOP]),
    S("The gizmo is how a block appears in the block browser, search and Merlin; demoSchema is what gets inserted.", "hp_gizmo", "hp_demoschema", "editor"),
    S("Settings group fields into configure, advanced, developer and inline.", "hp_settings", *[f"sg_{g}" for g in GROUPS]),
    S(f"{len(enum)} field types in five families.", *[f"fam_{slug(f)}" for f in FAMILY]),
    S("The most used: textfield, boolean, select, haxupload and number.", "fd_textfield", "fd_boolean", "fd_select", "fd_haxupload", "fd_number"),
    S(f"{len(unused)} field types no built element uses yet.", *[f"fd_{slug(f)}" for f in unused]),
    S("Which elements lean on which fields."), ]}]
write("haxschema", lines, {"name": "HAXSchema", "parent": "contracts", "noTimeline": True, "sectionLabels": {"part": "parts", "family": "field families", "field": "field types", "element": "elements"},
      "about": f"What an element tells the editor, generated from haxProperties.schema.json: the JSON Schema it is written in, {len(TOP)} top-level keys, the four settings groups, all {len(enum)} field types (inputMethod) and the {len(TOPPKG)} element packages that use fields most, counted across the built packages. Gray field tiles are defined but unused.",
      "kindLabels": {"rel": "part, family, field, element", "schema": "built on and validated by"}}, nodes, tours)
REPORT["haxschema"] = {"fields": enum, "parts": [k for k, _ in TOP]}

# ================= JSON Outline Schema =================
J = {f: json.load(open(f"josrepo/schema/{f}.schema.json")) for f in ["json-outline-schema", "haxcms-site", "skeleton"]}
core = J["json-outline-schema"]; site = J["haxcms-site"]; sk = J["skeleton"]
itemkeys = list(core["$defs"]["item"]["properties"])
itemmeta = list(site["$defs"]["itemMetadata"]["properties"])
sitemeta = list(site["$defs"]["siteMetadata"]["properties"])
lines = head("JSON Outline Schema", "jos", "JSON Outline Schema", "0,210,430,680", "92,64,54,50", "the core outline, the HAXcms site.json layer and the skeleton format, with what reads and writes each", "json-outline-schema/schema")
lines += ['  subgraph files ["Three schema files"]', '    js_core[("json-outline-schema.schema.json")]', '    js_site[("haxcms-site.schema.json")]', '    js_skel[("skeleton.schema.json")]', "  end", '  subgraph partsg ["Parts"]',
          '    jp_outline["the outline (id, title, author, license, metadata)"]', '    jp_items["items"]']
for k in itemkeys: lines.append(f'    ji_{slug(k)}["item.{k}"]')
for k in sitemeta: lines.append(f'    jm_{slug(k)}["metadata.{k}"]')
lines += ['    jp_itemmeta["item.metadata"]', '    jp_skelbuild["skeleton build.items"]', "  end", '  subgraph who ["Who reads and writes it"]']
RW = [("outline", "haxcms", "writes"), ("haxcms", None, "reads and writes"), ("editor", None, "writes page metadata to"), ("cli", None, "validates"), ("hax11ty", None, "renders from"), ("skeletons", None, "ship as"), ("importers", None, "produce"), ("themes", None, "draw menus from"), ("mcp", None, "edits through")]
for p, w, v in RW: lines.append(f'    {p}["{p}"]')
lines += ['    contracts["contracts"]', "  end", "",
          "  jos -.->|is defined by| js_core", "  js_site -.->|extends| js_core", "  js_skel -.->|extends| js_core", "  js_core -->|defines| jp_outline", "  js_core -->|defines| jp_items"]
for k in itemkeys: lines.append(f"  jp_items -->|each has| ji_{slug(k)}")
for k in sitemeta: lines.append(f"  js_site -->|adds| jm_{slug(k)}")
lines += ["  js_site -->|adds| jp_itemmeta", "  ji_metadata -->|is detailed by| jp_itemmeta", "  js_skel -->|adds| jp_skelbuild", "  ji_parent -.->|with| ji_order", "  ji_location -.->|points to| ji_slug"]
for p, w, v in RW: lines.append(f"  {p} -->|{v}| {'js_skel' if p == 'skeletons' else 'jp_items' if p in ('outline', 'importers') else 'js_site'}")
lines += ["  contracts -.->|includes| jos", "", "  %%@ group hub tier=0", "  %%@ group files tier=1", "  %%@ group partsg tier=2", "  %%@ group who tier=3", "  %%@ node jos portal"]
for i in ["js_core", "js_site", "js_skel"]: lines.append(f"  %%@ node {i} icon=hax:code-json color=forestGreen motion=nudge")
for i in ["jp_outline", "jp_items", "jp_itemmeta", "jp_skelbuild"] + [f"ji_{slug(k)}" for k in itemkeys] + [f"jm_{slug(k)}" for k in sitemeta]: lines.append(f"  %%@ node {i} icon=hax:site-map color=forestGreen motion=nudge")
for p, w, v in RW: lines.append(f"  %%@ node {p} portal" + (f"={w}" if w else ""))
lines.append("  %%@ node contracts portal=contracts")
nodes = {"jos": {"always": True},
         "js_core": {"desc": core.get("description", ""), "links": {"repo": GH + "/json-outline-schema/blob/main/schema/json-outline-schema.schema.json"}},
         "js_site": {"desc": site.get("description", ""), "links": {"repo": GH + "/json-outline-schema/blob/main/schema/haxcms-site.schema.json"}},
         "js_skel": {"desc": sk.get("description", ""), "links": {"repo": GH + "/json-outline-schema/blob/main/schema/skeleton.schema.json"}},
         "jp_outline": {"desc": "The work itself: id, title, author, description, license and metadata.", "kind": "part"},
         "jp_items": {"desc": "A flat list of items. The tree is expressed through parent and order, so moving a page never rewrites the pages around it.", "kind": "part"},
         "jp_itemmeta": {"desc": "What HAXcms keeps per page: " + ", ".join(itemmeta) + ".", "kind": "part"},
         "jp_skelbuild": {"desc": "A skeleton's items carry their page content inline, so one file is a whole starter site.", "kind": "part"}}
for k in itemkeys: nodes[f"ji_{slug(k)}"] = {"desc": (core["$defs"]["item"]["properties"][k].get("description") or f"The item's {k}."), "kind": "part"}
for k in sitemeta: nodes[f"jm_{slug(k)}"] = {"desc": (site["$defs"]["siteMetadata"]["properties"][k].get("description") or f"Site-level {k} settings.") + (" Fields: " + ", ".join(site["$defs"][k]["properties"]) + "." if k in site["$defs"] and "properties" in site["$defs"][k] else ""), "kind": "part"}
tours = [{"id": "jos", "label": "Inside site.json", "message": "The core outline, the HAXcms layer on top, and the skeleton format, generated from the three schema files.", "scenes": [
    S("Three schema files: the core, the HAXcms site.json layer, and skeletons.", "js_core", "js_site", "js_skel"),
    S("The core is an outline and a flat list of items.", "jp_outline", "jp_items"),
    S("Each item: id, parent and order for the tree, slug for the URL, location for the page file.", *[f"ji_{slug(k)}" for k in itemkeys]),
    S("HAXcms adds site, theme, platform, build and plugin metadata.", *[f"jm_{slug(k)}" for k in sitemeta], "jp_itemmeta"),
    S("The outline designer, the CLI, HAX11ty, importers and themes all read or write it.", *[p for p, _, _ in RW]),
    S("All of JSON Outline Schema."), ]}]
write("jos", lines, {"name": "JSON Outline Schema", "parent": "contracts", "noTimeline": True, "sectionLabels": {"part": "parts"},
      "about": "JSON Outline Schema in parts, generated from the json-outline-schema repo's three schema files: the core outline and items, the HAXcms site.json conventions layered on top, and the skeleton format, with everything that reads or writes it.",
      "kindLabels": {"rel": "file, part, reader or writer", "schema": "extends or points to"}}, nodes, tours)
REPORT["jos"] = {"items": itemkeys, "site": sitemeta}

# ================= App Store =================
svc = open("haxcms-nodejs/src/lib/HAXAppStoreService.js").read()
apps = re.findall(r'"details":\s*\{\s*"title":\s*"([^"]+)",\s*"icon":\s*"[^"]*",[\s\S]{0,300}?"tags":\s*\[([^\]]*)\]', svc)
lines = head("App Store spec", "appstore", "App Store spec", "0,220,460,700", "92,64,54,50", "what the editor is told it may place: apps, stax and the autoloader list", "HAXAppStoreService.js and generateAppStore.js")
lines += ['  subgraph partsg ["Parts of the manifest"]', '    as_apps["apps"]', '    as_stax["stax"]', '    as_autoloader["autoloader"]', '    as_conn["app connection"]', '    as_gizmo["app result gizmo"]', '    as_allowed["allowed blocks"]', "  end", '  subgraph appsg ["Built-in apps"]']
for a, t in apps: lines.append(f'    ap_{slug(a)}[["{a}"]]')
lines += ["  end", '  subgraph who ["Who uses it"]', '    editor["editor"]', '    haxcms["haxcms"]', '    plugins["plugins"]', '    op_generateappstore["op_generateappstore"]', '    settings["settings"]', '    contracts["contracts"]', "  end", "",
          "  appstore -->|has| as_apps", "  appstore -->|has| as_stax", "  appstore -->|has| as_autoloader", "  as_apps -->|each has a| as_conn", "  as_conn -->|maps results to a| as_gizmo", "  as_autoloader -->|is filtered by| as_allowed"]
for a, t in apps: lines.append(f"  as_apps -->|includes| ap_{slug(a)}")
lines += ["  haxcms -->|serves| appstore", "  op_generateappstore -.->|returns| appstore", "  editor -->|reads| appstore", "  plugins -->|will extend| as_autoloader", "  settings -->|sets| as_allowed", "  contracts -.->|includes| appstore", "",
          "  %%@ group hub tier=0", "  %%@ group partsg tier=1", "  %%@ group appsg tier=2", "  %%@ group who tier=3", "  %%@ node appstore portal"]
for i in ["as_apps", "as_stax", "as_autoloader", "as_conn", "as_gizmo", "as_allowed"]: lines.append(f"  %%@ node {i} icon=hax:code-json color=pughBlue motion=nudge")
for a, t in apps: lines.append(f"  %%@ node ap_{slug(a)} mono={a[:4].upper()} color=slateGray motion=lift")
lines += ["  %%@ node editor portal", "  %%@ node haxcms portal", "  %%@ node plugins portal", "  %%@ node op_generateappstore portal=openapi", "  %%@ node settings portal=haxcms", "  %%@ node contracts portal=contracts"]
nodes = {"appstore": {"always": True},
         "as_apps": {"desc": f"External media sources the editor can search and place from: {len(apps)} built in, each with its own connection and API key handling.", "kind": "part"},
         "as_stax": {"desc": "Stax: saved groups of blocks that insert together, set per deployment.", "kind": "part"},
         "as_autoloader": {"desc": "The list of elements the editor loads as placeable blocks for this site.", "kind": "part"},
         "as_conn": {"desc": "How the editor talks to an app: protocol, url, operations (browse, search) and how to read the results.", "kind": "part"},
         "as_gizmo": {"desc": "How one search result becomes a block: which result fields fill the title, source and preview.", "kind": "part"},
         "as_allowed": {"desc": "Site settings can switch blocks off; the autoloader list is filtered to the allowed blocks before it reaches the editor.", "kind": "part"}}
for a, t in apps: nodes[f"ap_{slug(a)}"] = {"desc": f"{a}: tagged {t.replace(chr(34), '')}.", "links": {"code": NODE + "src/lib/HAXAppStoreService.js"}, "kind": "app"}
tours = [{"id": "appstore", "label": "What the editor may place", "message": "The App Store manifest in parts, generated from the backend that serves it.", "scenes": [
    S("Three parts: apps, stax and the autoloader.", "as_apps", "as_stax", "as_autoloader"),
    S(f"{len(apps)} built-in apps the editor can search.", *[f"ap_{slug(a)}" for a, _ in apps]),
    S("Each app has a connection, and each result becomes a gizmo.", "as_conn", "as_gizmo"),
    S("Site settings decide which blocks are allowed; plugins will extend the list.", "as_allowed", "settings", "plugins"),
    S("HAXcms serves it and the editor reads it.", "haxcms", "editor", "op_generateappstore"), ]}]
write("appstore", lines, {"name": "App Store spec", "parent": "contracts", "noTimeline": True, "sectionLabels": {"part": "parts", "app": "apps"},
      "about": f"What the editor is told it may place, generated from haxcms-nodejs: the apps (external media sources, {len(apps)} built in), stax, and the autoloader list filtered by the site's allowed blocks.",
      "kindLabels": {"rel": "part, app, user", "schema": "returned or included by"}}, nodes, tours)
REPORT["appstore"] = {"apps": [a for a, _ in apps]}

# ================= Merlin =================
mu = json.load(open("ext/merlin_use.json"))
CID = {"*": "mc_all", ">": "mc_slash", "/": "mc_nav"}
def cid(c): return CID.get(c) or "mc_" + slug(c)
FIELDS = [("title", "What the person sees and searches."), ("icon", "Icon, or image or textCharacter instead."), ("tags", "Extra words to match on."), ("value", "Payload handed to the event."), ("eventName", "What fires when chosen."), ("path", "Where it lives in Merlin's menu, like CMS/action/create/page."), ("context", "When it shows: * everywhere, CMS, HAX, admin, logged-in, and more."), ("priority", "Sort order; lower shows first."), ("inline", "Runs inline without closing Merlin."), ("shortcut", "A keyboard shortcut, labeled automatically."), ("i18n", "Binds title and other strings to the element's translations."), ("more", "A second line of detail.")]
EVENTS = {"super-daemon-element-method": "Calls a method on the element that defined the option.", "super-daemon-run-program": "Starts a program: Merlin switches to a filtered sub-list (pick a page, a theme, a block).", "super-daemon-element-click": "Clicks an element.", "insert-tag": "Inserts a block into the page."}
lines = head("Merlin", "merlin", "Merlin", "0,220,460,700", "92,62,56,52", "the option schema every command is defined with, the contexts and events, and who defines commands", "super-daemon.js defineOption() and every defineOption call in the built packages")
lines += ['  subgraph fieldsg ["An option has"]']
for f, d in FIELDS: lines.append(f'    mo_{f}["{f}"]')
lines += ["  end", '  subgraph ctxg ["Contexts"]']
for c, n in mu["ctx"]: lines.append(f'    {cid(c)}["{c}"]')
lines += ["  end", '  subgraph evg ["Events"]']
for e, n in mu["ev"]: lines.append(f'    me_{slug(e)}["{e}"]')
lines += ["  end", '  subgraph who ["Who defines commands"]']
for p, n in mu["calls"]: lines.append(f'    md_{slug(p)}["{p}"]')
lines += ['    tips["tips"]', '    editor["editor"]', "  end", ""]
for f, d in FIELDS: lines.append(f"  merlin -->|option has| mo_{f}")
for c, n in mu["ctx"]: lines.append(f"  mo_context -->|can be| {cid(c)}")
for e, n in mu["ev"]: lines.append(f"  mo_eventName -->|can fire| me_{slug(e)}")
for p, n in mu["calls"]: lines.append(f"  md_{slug(p)} -->|defines {n} options in| merlin")
lines += ["  tips -->|appear in| merlin", "  merlin -->|works inside| editor", "", "  %%@ group hub tier=0", "  %%@ group fieldsg tier=1", "  %%@ group ctxg tier=2", "  %%@ group evg tier=2", "  %%@ group who tier=3", "  %%@ node merlin portal"]
for f, d in FIELDS: lines.append(f"  %%@ node mo_{f} icon=hax:code-json color=athertonViolet motion=nudge")
for c, n in mu["ctx"]: lines.append(f"  %%@ node {cid(c)} mono={(c if len(c) < 5 else c[:4]).upper()} color=wonderPurple motion=nudge")
for e, n in mu["ev"]: lines.append(f"  %%@ node me_{slug(e)} icon=hax:wand color=wonderPurple motion=nudge")
for p, n in mu["calls"]: lines.append(f"  %%@ node md_{slug(p)} portal=elements" if pkid(p) in EL_IDS else f"  %%@ node md_{slug(p)} icon=hax:bricks color=slateGray motion=nudge")
lines += ["  %%@ node tips portal=haxcms", "  %%@ node editor portal"]
nodes = {"merlin": {"always": True}}
for f, d in FIELDS: nodes[f"mo_{f}"] = {"desc": d, "kind": "field", "links": {"code": WC + "super-daemon/super-daemon.js"}}
CTXD = {"*": "Everywhere.", "CMS": "In a HAXcms site.", "HAX": "While editing a page.", "admin": "For admins.", ">": "Slash commands typed in the editor.", "/": "Top-level navigation.", "logged-in": "Only when logged in.", "community": "Community links and help.", "system-settings": "System settings.", "addPage": "While adding a page.", "uploadMedia": "While uploading media."}
for c, n in mu["ctx"]: nodes[f"{cid(c)}"] = {"desc": f"{CTXD.get(c, c)} {n} options use it.", "kind": "context"}
for e, n in mu["ev"]: nodes[f"me_{slug(e)}"] = {"desc": f"{EVENTS.get(e, e)} {n} options fire it.", "kind": "event"}
for p, n in mu["calls"]:
    if pkid(p) not in EL_IDS: nodes[f"md_{slug(p)}"] = {"desc": f"@haxtheweb/{p} defines {n} Merlin options.", "links": {"repo": WC + p}, "kind": "definer"}
tours = [{"id": "merlin", "label": "How Merlin knows what to do", "message": "Every Merlin command is one defineOption call; this is its shape and who defines them.", "scenes": [
    S("Every command is an option with these fields.", *[f"mo_{f}" for f, _ in FIELDS]),
    S("Context decides when an option shows.", "mo_context", *[f"{cid(c)}" for c, _ in mu["ctx"]]),
    S("eventName decides what happens: call a method, run a program, click, insert.", "mo_eventName", *[f"me_{slug(e)}" for e, _ in mu["ev"]]),
    S("HAXcms, the dashboard and the editor define the commands; Tips show up here too.", *[f"md_{slug(p)}" for p, _ in mu["calls"]], "tips"), ]}]
write("merlin", lines, {"name": "Merlin", "parent": "contracts", "noTimeline": True, "sectionLabels": {"field": "option fields", "context": "contexts", "event": "events", "definer": "who defines commands"},
      "about": f"Merlin's option schema, generated from super-daemon's defineOption and the {sum(n for _, n in mu['calls'])} options defined across the built packages: the fields an option has, the contexts it can show in, the events it fires and which packages define them.",
      "kindLabels": {"rel": "field, context, event, definer"}}, nodes, tours)
REPORT["merlin"] = {"options": sum(n for _, n in mu["calls"]), "contexts": [c for c, _ in mu["ctx"]]}

# ================= OER Schema =================
o = json.load(open("ext/oerschema.json")); C = o["classes"]; P = o["properties"]
MIRROR = {"Thing", "Intangible", "Class", "Property", "Enumeration", "DataType", "Person", "Organization", "Place", "StructuredValue", "CreativeWork", "MediaObject", "ImageObject", "Boolean", "Date", "DateTime", "Integer", "Number", "Text", "Time", "URL", "Yes", "No", "True", "False"}
def anc(k, seen=None):
    seen = set() if seen is None else seen
    for s in C.get(k, {}).get("subClassOf", []):
        if s not in seen: seen.add(s); anc(s, seen)
    return seen
GRP = [("og_structure", "Course structure", lambda k: k in ("Resource", "Course", "CourseSection", "CourseSyllabus", "Topic", "LearningObjective", "TableOfContents", "TableOfContentsEntry", "ClassStanding")),
       ("og_patterns", "Instructional patterns", lambda k: k == "LearningComponent" or "InstructionalPattern" in anc(k) or k == "InstructionalPattern"),
       ("og_materials", "Materials", lambda k: k == "AssociatedMaterial" or "AssociatedMaterial" in anc(k)),
       ("og_grading", "Grading and rubrics", lambda k: "GradeFormat" in anc(k) or k == "GradeFormat" or k.startswith("Rubric")),
       ("og_actions", "Learner actions", lambda k: "ActionType" in anc(k) or k == "ActionType"),
       ("og_format", "Formats", lambda k: k == "Format" or "Format" in C.get(k, {}).get("subClassOf", []))]
cls = [k for k in C if k not in MIRROR]
grp_of = {}
for k in cls:
    for gid, lab, f in GRP:
        if f(k): grp_of[k] = gid; break
cls = [k for k in cls if k in grp_of]
SORG = sorted({s.split("/")[-1] for k in cls for s in C[k].get("subClassOf", []) if "schema.org" in s})
lines = head("OER Schema", "oerschema", "OER Schema", "0,200,480,700,900", "92,64,46,44,48", "the vocabulary for open educational resources, how it extends schema.org, and where it shows up in HAX", "oer-schema/lib/oerschema.js (OER Schema " + o.get("version", "") + ")")
lines += ['  subgraph rel ["Builds on"]', '    schemaorg[["schema.org"]]', '    ccrel[["Creative Commons ccREL"]]', "  end", '  subgraph grps ["What it describes"]']
for gid, lab, f in GRP: lines.append(f'    {gid}["{lab}"]')
lines += ["  end", '  subgraph clsg ["Classes"]']
for k in cls: lines.append(f'    oc_{slug(k)}["{k}"]')
lines += ["  end", '  subgraph sorg ["schema.org types it extends"]']
for s in SORG: lines.append(f'    so_{slug(s)}["schema.org/{s}"]')
lines += ["  end", '  subgraph used ["Where it shows up in HAX"]', '    b_oer_schema["b_oer_schema"]', '    course["course"]', '    textbook["textbook"]', '    editor["editor"]', '    oervocab["oervocab"]', '    mcollins(("mcollins"))', "  end", "",
          "  oerschema -.->|extends| schemaorg", "  oerschema -.->|credits works with| ccrel"]
for gid, lab, f in GRP: lines.append(f"  oerschema -->|describes| {gid}")
for k in cls:
    lines.append(f"  {grp_of[k]} -->|includes| oc_{slug(k)}")
    for s in C[k].get("subClassOf", []):
        if "schema.org" in s: lines.append(f"  oc_{slug(k)} -.->|extends| so_{slug(s.split('/')[-1])}")
        elif s in cls and grp_of.get(s) == grp_of[k]: lines.append(f"  oc_{slug(k)} -->|is a kind of| oc_{slug(s)}")
for s in SORG: lines.append(f"  so_{slug(s)} -.->|is part of| schemaorg")
lines += ["  b_oer_schema -->|tags content with| oerschema", "  course -->|is described by| oc_course", "  textbook -->|is described by| oc_learningcomponent", "  editor -->|wraps content in| b_oer_schema", "  mcollins -.->|authored| oerschema", "  oervocab -.->|is| oerschema", "",
          "  %%@ group hub tier=0", "  %%@ group rel tier=1", "  %%@ group grps tier=1", "  %%@ group clsg tier=2", "  %%@ group sorg tier=3", "  %%@ group used tier=4",
          "  %%@ node oerschema portal", "  %%@ node schemaorg mono=SORG color=slateGray motion=lift", "  %%@ node ccrel mono=CC color=slateGray motion=lift"]
GCOL = {"og_structure": "forestGreen", "og_patterns": "creekTeal", "og_materials": "skyBlue", "og_grading": "roarGolden", "og_actions": "athertonViolet", "og_format": "slateGray"}
for gid, lab, f in GRP: lines.append(f"  %%@ node {gid} icon=icons:book color={GCOL[gid]} motion=pop")
for k in cls: lines.append(f"  %%@ node oc_{slug(k)} mono={''.join(ch for ch in k if ch.isupper())[:4] or k[:3].upper()} color={GCOL[grp_of[k]]} motion=nudge")
for s in SORG: lines.append(f"  %%@ node so_{slug(s)} mono=SO color=limestoneGray motion=nudge")
lines += ["  %%@ node b_oer_schema portal=elements" if "b_oer_schema" in EL_IDS else "  %%@ node b_oer_schema icon=hax:bricks color=slateGray motion=nudge", "  %%@ node course portal", "  %%@ node textbook portal", "  %%@ node editor portal", "  %%@ node oervocab portal=contracts", "  %%@ node mcollins portal"]
props_by_dom = collections.defaultdict(list)
for pn, pv in P.items():
    for d in pv.get("domain", []): props_by_dom[d].append(pn)
nodes = {"oerschema": {"always": True},
         "schemaorg": {"desc": "schema.org, the shared vocabulary search engines read. OER Schema extends it: an OER Course is a schema.org Course, a CourseSection a CourseInstance, a LearningComponent a CreativeWork, and an Assessment or Task a schema.org Action.", "links": {"site": "https://schema.org"}},
         "ccrel": {"desc": "Creative Commons Rights Expression Language: every OER Resource is also a cc:Work, so licensing travels with the content.", "links": {"site": "https://creativecommons.org/ns"}}}
GD = {"og_structure": "Courses, sections, syllabi, topics, objectives and tables of contents.", "og_patterns": "How learning is assembled: lessons, units, modules, tasks, activities, projects, practice and assessments.", "og_materials": "Materials attached to instruction: supporting, supplemental and referenced.",
      "og_grading": "How work is graded: point, letter, percent and completion formats, and rubrics with criteria, scales and levels.", "og_actions": "What a learner does: reading, writing, making, researching, listening, watching, reflecting, discussing, observing, presenting, assessing.", "og_format": "Delivery formats, such as face to face."}
for gid, lab, f in GRP: nodes[gid] = {"desc": GD[gid] + f" {sum(1 for k in cls if grp_of[k] == gid)} classes.", "kind": "group"}
for k in cls:
    c = C[k]; pr = c.get("properties", []) or props_by_dom.get(k, [])
    nodes[f"oc_{slug(k)}"] = {"desc": ((c.get("comment") or f"oer:{k}.").strip().rstrip(".") + "." + (f" Properties: {', '.join(pr[:10])}." if pr else "")), "kind": "class", "links": {"term": f"http://oerschema.org/{k}"}}
for s in SORG: nodes[f"so_{slug(s)}"] = {"desc": f"schema.org/{s}, extended by OER Schema.", "links": {"term": f"https://schema.org/{s}"}, "kind": "sorg"}
if "b_oer_schema" not in EL_IDS: nodes["b_oer_schema"] = {"desc": "The oer-schema element: wraps content and marks it up with an OER Schema type and properties.", "links": {"repo": WC + "oer-schema"}}
tours = [{"id": "oerschema", "label": "Describing learning", "message": f"OER Schema {o.get('version', '')}: {len(cls)} classes in six groups, built on schema.org and Creative Commons, authored by Michael Collins.", "scenes": [
    S("OER Schema extends schema.org and Creative Commons, so search engines and licenses understand learning content.", "oerschema", "schemaorg", "ccrel", "mcollins"),
    S("It describes six things.", *[g for g, _, _ in GRP]),
    S("Course structure: courses, sections, syllabi, topics and objectives.", "og_structure", *[f"oc_{slug(k)}" for k in cls if grp_of[k] == "og_structure"]),
    S("Instructional patterns: lessons, units, modules, tasks, activities and assessments.", "og_patterns", *[f"oc_{slug(k)}" for k in cls if grp_of[k] == "og_patterns"]),
    S("Materials, grading and rubrics, learner actions, formats.", "og_materials", "og_grading", "og_actions", "og_format"),
    S("Each one maps onto a schema.org type.", *[f"so_{slug(s)}" for s in SORG]),
    S("In HAX, the oer-schema element tags content in courses and textbooks.", "b_oer_schema", "course", "textbook", "editor"),
    S("All of OER Schema."), ]}]
write("oerschema", lines, {"name": "OER Schema", "parent": "contracts", "noTimeline": True, "sectionLabels": {"group": "what it describes", "class": "classes", "sorg": "schema.org types"},
      "about": f"OER Schema {o.get('version', '')}, generated from the oer-schema element's vocabulary: {len(cls)} classes for describing open educational resources, grouped by what they describe, with every schema.org type they extend and where OER Schema shows up in HAX. schema.org mirror types (Thing, Text, Date and so on) are left out.",
      "kindLabels": {"rel": "group, class, kind of", "schema": "extends schema.org or Creative Commons", "org": "standards it builds on"}}, nodes, tours)
REPORT["oerschema"] = {"classes": cls, "version": o.get("version")}
json.dump(REPORT, open("ext/schemas_report.json", "w"), indent=1)
print({k: {kk: (len(vv) if isinstance(vv, list) else vv) for kk, vv in v.items()} for k, v in REPORT.items()})
