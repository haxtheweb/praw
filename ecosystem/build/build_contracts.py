"""Data contracts sub-web: the schemas HAX runs on, the files that conform to them, and what reads and writes each.
Portals: ids from hax-ecosystem.mmd and hax-haxcms.mmd. Details in hax-contracts.json."""
import json
GH = "https://github.com/haxtheweb"
WC = GH + "/webcomponents/tree/master/elements/"
NODE = GH + "/haxcms-nodejs/blob/main/"
PHP = GH + "/haxcms-php/blob/master/"
def L(a, b): return {"label": a, "url": b}

SCHEMAS = ["jos", "haxschema", "appstore", "merlin", "oerschema", "xapi", "openapi", "skillsindex", "registry"]  # portals to main
# id, label, which schema, desc, links
FILES = [
 ("sitejson", "site.json", "jos", "One per site: title, metadata, theme and the items tree (id, parent, order, slug, location). The single source of truth for structure and navigation.", {"spec": GH + "/json-outline-schema"}),
 ("josspec", "json-outline-schema-spec", "jos", "The JSON Schema for site.json, shipped as a package so tools can validate a site in process.", {"repo": GH + "/json-outline-schema"}),
 ("haxprops", "<tag>.haxProperties.json", "haxschema", "One per element, in lib/: the gizmo, settings (configure, advanced, developer) and demo an element shows the editor. Referenced from static get haxProperties().", {"example": GH + "/hax-schema/blob/main/example.json"}),
 ("haxpropsschema", "haxProperties.schema.json", "haxschema", "JSON Schema (draft 2020-12) for haxProperties files, in the hax-schema repo, with a validator: npx -p @haxtheweb/hax-schema haxproperties-validate.", {"repo": GH + "/hax-schema", "docs": "https://haxtheweb.github.io/hax-schema/"}),
 ("localeoverlay", "<tag>.<lang>.haxProperties.json", "haxschema", "Translation overlays in locales/: the editor strings of an element in another language, validated by haxProperties.locale.schema.json.", {"schema": GH + "/hax-schema/blob/main/schema/haxProperties.locale.schema.json"}),
 ("appstorejson", "app store manifest", "appstore", "The autoloader's list of blocks a site can place, generated per site so the editor loads only what is needed.", {"code": NODE + "src/lib/HAXAppStoreService.js"}),
 ("sitespec", "site-spec.yaml", "openapi", "The OpenAPI spec for site routes, kept identical in haxcms-nodejs and haxcms-php.", {"nodejs": NODE + "src/openapi/site-spec.yaml", "php": PHP + "system/backend/php/lib/siteRoutes/openapi/site-spec.yaml"}),
 ("systemspec", "system-spec.yaml", "openapi", "The OpenAPI spec for system routes (login, create site, skeletons, app store), kept identical in both backends.", {"nodejs": NODE + "src/openapi/system-spec.yaml", "php": PHP + "system/backend/php/lib/systemRoutes/openapi/system-spec.yaml"}),
 ("xapivocab", "xapi-vocabulary.json", "xapi", "The shared xAPI verbs and objects HAX elements use, with buildStatement to shape a statement the same way everywhere.", {"code": WC + "user-action/lib"}),
 ("merlinoption", "Merlin options", "merlin", "Every Merlin command is one defineOption() call: title, icon, tags, value, eventName, path, context, priority and more. HAXcms, the dashboard and the editor define them.", {"code": WC + "super-daemon/super-daemon.js"}),
 ("skillsjson", ".well-known/agent-skills/index.json", "skillsindex", "The agentskills.io discovery index: which skills a place offers, where to read each and its digest. PRAW keeps the full one; deployments and sites carry a copy of their set.", {"index": GH + "/praw/blob/main/.well-known/agent-skills/index.json"}),
 ("wcregjson", "wc-registry.json", "registry", "Every tag the autoloader can load, mapped to its module. Written by the ubiquity build, copied into each HAXcms build and site.", {"file": GH + "/webcomponents/blob/master/wc-registry.json"}),
 ("cemjson", "custom-elements.json", "registry", "One per package: the Custom Elements Manifest of its elements (properties, attributes, events, slots), written by cem analyze.", {"example": GH + "/webcomponents/blob/master/elements/a11y-collapse/custom-elements.json"}),
 ("translationsjson", "translation-manifest.json", "registry", "Which elements ship which locale files, scanned by the ubiquity build; i18n-manager reads it to load translations.", {"file": GH + "/webcomponents/blob/master/elements/i18n-manager/lib/translation-manifest.json"}),
 ("oervocab", "oerschema.org vocabulary", "oerschema", "The OER Schema terms (course, lesson, learning objective, assessment) as linked data, authored by Michael Collins.", {"site": "https://oerschema.org"}),
]
# readers and writers: portal id -> (web or None for main, [(verb, file)])
RW = {
 "outline": ("haxcms", [("writes", "sitejson")]),
 "haxcms": (None, [("loads elements through", "wcregjson"), ("reads", "sitejson"), ("serves", "appstorejson"), ("implements", "sitespec"), ("implements", "systemspec")]),
 "cli": (None, [("validates", "sitejson"), ("audits against", "haxpropsschema"), ("generates", "appstorejson")]),
 "skeletons": (None, [("bundle a", "sitejson")]),
 "hax11ty": (None, [("reads", "sitejson")]),
 "editor": (None, [("builds forms from", "haxprops"), ("loads blocks from", "appstorejson")]),
 "components": (None, [("describe themselves in", "cemjson"), ("declare", "haxprops"), ("carry", "localeoverlay"), ("emit statements from", "xapivocab"), ("tag content with", "oervocab")]),
 "languages": (None, [("produce", "localeoverlay"), ("are counted in", "translationsjson")]),
 "ubiquity": (None, [("writes", "wcregjson"), ("writes", "translationsjson")]),
 "mcp": (None, [("reads", "sitespec"), ("reads", "systemspec")]),
 "php": (None, [("implements", "sitespec"), ("implements", "systemspec"), ("serves", "skillsjson")]),
 "nodejs": (None, [("implements", "sitespec"), ("implements", "systemspec"), ("serves", "skillsjson")]),
 "praw": (None, [("writes", "skillsjson")]),
 "traveler": (None, [("is found through", "skillsjson")]),
 "insights": ("haxcms", [("consumes", "xapivocab")]),
 "course": (None, [("is described by", "oervocab")]),
 "mcollins": (None, [("authored", "oervocab")]),
}
lines = ["%% Data contracts sub-web: the schemas HAX runs on, the files that conform to them, and what reads and writes each.",
         "%% Portals: ids from hax-ecosystem.mmd and hax-haxcms.mmd. Details in hax-contracts.json.",
         "flowchart TB", "  %%@ layout rings=0,220,470,760 sizes=92,64,58,52",
         '  subgraph hub ["Data contracts"]', '    contracts[("Data contracts")]', "  end", '  subgraph schemas ["Schemas"]']
for s in SCHEMAS: lines.append(f'    {s}[("{s}")]')
lines += ["  end", '  subgraph files ["Files that conform"]']
for id, label, s, *_ in FILES: lines.append(f'    {id}[("{label}")]')
lines += ["  end", '  subgraph rw ["Readers and writers"]']
for p in RW: lines.append(f'    {p}["{p}"]')
lines += ["  end", ""]
for s in SCHEMAS: lines.append(f"  contracts -.->|includes| {s}")
for id, label, s, *_ in FILES: lines.append(f"  {id} -.->|conforms to| {s}")
for p, (web, acts) in RW.items():
    for verb, f in acts: lines.append(f"  {p} -->|{verb}| {f}")
lines += ["", "  %%@ group hub tier=0", "  %%@ group schemas tier=1", "  %%@ group files tier=2", "  %%@ group rw tier=3",
          "  %%@ node contracts icon=hax:code-json color=creekTeal motion=pulse"]
for s in SCHEMAS: lines.append(f"  %%@ node {s} portal")
for id, label, s, *_ in FILES: lines.append(f"  %%@ node {id} icon=hax:code-json color=creekTeal motion=nudge")
for p, (web, acts) in RW.items(): lines.append(f"  %%@ node {p} portal" + (f"={web}" if web else ""))
open("hax-contracts.mmd", "w").write("\n".join(lines) + "\n")

nodes = {"contracts": {"always": True, "desc": f"{len(SCHEMAS)} schemas carry HAX: what a site is, what an element can do, what a site may place, what Merlin can do, what learning content is, what a learner did, what the backends promise, which elements exist and where they load from, and which skills an agent can use. Each has files that conform to it and tools that read or write them."}}
for id, label, s, desc, links in FILES: nodes[id] = {"desc": desc, "links": links}
def S(c, *i): return {"caption": c, "nodes": list(i)}
tours = [{"id": "contracts", "label": "Follow the data", "message": "The schemas HAX runs on, the files that conform to them, and what reads and writes each.", "scenes": [
    S(f"HAX is held together by {len(SCHEMAS)} schemas.", "contracts", *SCHEMAS),
    S("A site is a site.json, validated by the JSON Outline Schema spec.", "jos", "sitejson", "josspec", "outline", "haxcms", "cli", "skeletons", "hax11ty"),
    S("An element describes itself to the editor in haxProperties, with translation overlays.", "haxschema", "haxprops", "haxpropsschema", "localeoverlay", "editor", "components", "languages"),
    S("The app store manifest tells the editor which blocks a site may place.", "appstore", "appstorejson", "editor", "cli"),
    S("Two OpenAPI specs are the promise both backends and the MCP keep.", "openapi", "sitespec", "systemspec", "php", "nodejs", "mcp"),
    S("xAPI and OER Schema describe what learners did and what content is.", "xapi", "xapivocab", "insights", "oerschema", "oervocab", "course", "mcollins"),
    S("The registry and manifests: where every element loads from, what it declares and which languages it speaks.", "registry", "wcregjson", "cemjson", "translationsjson", "ubiquity", "haxcms", "components", "languages"),
    S("The agent skills index tells any agent which skills a place offers.", "skillsindex", "skillsjson", "praw", "php", "nodejs", "traveler"),
    S("All the contracts at once."),
]}]
meta = {"name": "Data contracts", "parent": "main", "noTimeline": True,
        "about": f"The {len(SCHEMAS)} schemas HAX runs on (JSON Outline Schema, HAXSchema, the app store spec, Merlin options, OER Schema, xAPI, OpenAPI, the agent skills index, the element registry and manifests), the files that conform to each, and the tools that read or write them.",
        "kindLabels": {"schema": "conforms to", "rel": "reads or writes"}}
json.dump({"meta": meta, "nodes": nodes, "evidence": {}, "tours": tours}, open("hax-contracts.json", "w"), indent=1, ensure_ascii=False)
print(len(FILES), "files;", len(SCHEMAS) + len(RW), "portals")
