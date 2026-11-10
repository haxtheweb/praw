"""Web component stack sub-web: what a HAX element is built on, from HTML up to the HAX layer, and where people learn it.
Portals: ids from hax-ecosystem.mmd. Details in hax-stack.json."""
import json
GH = "https://github.com/haxtheweb"
WC = GH + "/webcomponents/tree/master/elements/"
NPM = "https://www.npmjs.com/package/"
def L(a, b): return {"label": a, "url": b}
MDN = "https://developer.mozilla.org/en-US/docs/Web/"

# id, label, tier, mono/icon, color, desc, links
LOCAL = [
 ("html", "HTML", 1, "mono=HTML", "inventOrange", "The document: every HAX element is an HTML tag, and its content stays HTML in light DOM so it works without the element.", {"docs": MDN + "HTML"}),
 ("css", "CSS", 1, "mono=CSS", "skyBlue", "Styling, scoped per element by shadow DOM and shared through DDD custom properties.", {"docs": MDN + "CSS"}),
 ("js", "JavaScript", 1, "mono=JS", "keystoneYellow", "Behavior as plain ES2020+ JavaScript; no TypeScript and no optional chaining in the monorepo.", {"docs": MDN + "JavaScript"}),
 ("customel", "Custom Elements", 2, "icon=hax:html-code", "wonderPurple", "customElements.define(tag, class): a new tag the browser treats as a first-class element.", {"docs": MDN + "API/Web_components/Using_custom_elements"}),
 ("shadow", "Shadow DOM", 2, "icon=icons:code", "wonderPurple", "An element's own DOM and styles, isolated from the page; slots let authored light DOM content show through.", {"docs": MDN + "API/Web_components/Using_shadow_DOM"}),
 ("slots", "Templates and slots", 2, "icon=hax:format-textblock", "wonderPurple", "<template> and <slot>: how an element renders authored content in place.", {"docs": MDN + "API/Web_components/Using_templates_and_slots"}),
 ("esm", "ES modules", 2, "icon=hax:code-json", "wonderPurple", "import and export; one module per element, loaded on demand by the autoloader with no bundler.", {"docs": MDN + "JavaScript/Guide/Modules"}),
 ("lit", "Lit", 2, "mono=Lit", "beaverBlue", "The small library HAX elements extend: LitElement, html`` and css`` templates, reactive properties and lifecycle.", {"site": "https://lit.dev", "npm": NPM + "lit"}),
 ("simpleicon", "simple-icon", 3, "icon=hax:hax2022", "creekTeal", "The icon elements and iconsets HAX elements draw from, including the hax: set used in this web.", {"repo": WC + "simple-icon", "npm": NPM + "@haxtheweb/simple-icon"}),
 ("schemabeh", "SchemaBehaviors", 3, "icon=hax:code-json", "athertonViolet", "The mixin that gives an element schema.org metadata so content is machine-readable.", {"repo": WC + "schema-behaviors", "npm": NPM + "@haxtheweb/schema-behaviors"}),
]
PORTALS = {"wcstandard": 0, "ddd": 3, "haxschema": 3, "languages": 3, "components": 3, "cli": 4, "testing": 4, "ubiquity": 4, "ssr": 4, "ist256": 4, "haxcamp": 4, "docs": 4}
PORTAL_WEB = {"docs": "skeletons"}
TIERS = {1: ("web", "The web platform"), 2: ("std", "Web component standards and Lit"), 3: ("hax", "The HAX layer"), 4: ("tools", "Tools that build, test and ship one, and where people learn it")}

lines = ["%% Web component stack sub-web: what a HAX element is built on, from HTML up to the HAX layer, and where people learn it.",
         "%% Portals: ids from hax-ecosystem.mmd. Details in hax-stack.json.",
         "flowchart TB", "  %%@ layout rings=0,220,440,660,880 sizes=92,72,62,58,52",
         '  subgraph hub ["Web component standard"]', '    wcstandard["wcstandard"]', "  end"]
for t, (gid, lab) in TIERS.items():
    lines.append(f'  subgraph {gid} ["{lab}"]')
    for id, label, tier, *_ in LOCAL:
        if tier == t: lines.append(f'    {id}["{label}"]')
    for id, tier in PORTALS.items():
        if tier == t: lines.append(f'    {id}["{id}"]')
    lines.append("  end")
lines += ["",
 "  wcstandard -->|is written in| html", "  wcstandard -->|is written in| css", "  wcstandard -->|is written in| js",
 "  customel -->|builds on| js", "  shadow -->|builds on| html", "  shadow -->|scopes| css", "  slots -->|builds on| html", "  esm -->|builds on| js",
 "  wcstandard -->|defines| customel", "  wcstandard -->|defines| shadow", "  wcstandard -->|defines| slots",
 "  lit -->|builds on| customel", "  lit -->|builds on| shadow", "  lit -->|renders through| slots", "  lit -->|ships as| esm",
 "  components -->|extend| lit", "  components -->|load as| esm",
 "  ddd -->|styles through| css", "  components -->|style with| ddd",
 "  haxschema -.->|describes| components", "  languages -->|translate| components", "  simpleicon -->|draws icons in| components", "  schemabeh -.->|adds metadata to| components",
 "  cli -->|scaffolds| components", "  cli -->|audits against| ddd", "  cli -->|audits against| haxschema",
 "  testing -->|tests| components", "  ubiquity -->|builds and releases| components", "  ssr -->|server-renders| components",
 "  ist256 -->|teaches| wcstandard", "  ist256 -->|teaches| lit", "  haxcamp -->|teaches| wcstandard", "  docs -->|documents| wcstandard",
 "", "  %%@ group hub tier=0"]
for t, (gid, lab) in TIERS.items(): lines.append(f"  %%@ group {gid} tier={t}")
lines.append("  %%@ node wcstandard portal")
for id, label, tier, look, col, *_ in LOCAL: lines.append(f"  %%@ node {id} {look} color={col} motion=lift")
for id in PORTALS:
    if id != "wcstandard": lines.append(f"  %%@ node {id} portal" + (f"={PORTAL_WEB[id]}" if id in PORTAL_WEB else ""))
open("hax-stack.mmd", "w").write("\n".join(lines) + "\n")

nodes = {"wcstandard": {"always": True}}
for id, label, tier, look, col, desc, links in LOCAL: nodes[id] = {"desc": desc, "links": links}
def S(c, *i): return {"caption": c, "nodes": list(i)}
tours = [{"id": "stack", "label": "How a HAX element is built", "message": "From the web platform to the HAX layer: what you need to know to make a web component for HAX.", "scenes": [
    S("Everything starts from the web component standard.", "wcstandard"),
    S("Which is written in the three languages every browser speaks.", "html", "css", "js"),
    S("Four standards make a tag reusable: custom elements, shadow DOM, templates and slots, ES modules.", "customel", "shadow", "slots", "esm"),
    S("Lit is the small library HAX elements extend.", "lit"),
    S("The HAX layer: DDD for style, HAXSchema for editing, i18n for languages, simple-icon and SchemaBehaviors.", "ddd", "haxschema", "languages", "simpleicon", "schemabeh"),
    S("The CLI scaffolds and audits one; tests, Ubiquity and SSR check and ship it.", "cli", "testing", "ubiquity", "ssr", "components"),
    S("IST 256, HAX Camp and the docs are where people learn this.", "ist256", "haxcamp", "docs"),
    S("The whole stack."),
]}]
meta = {"name": "Web component stack", "parent": "main", "noTimeline": True,
        "about": "The standard way a HAX web component is made: HTML, CSS and JavaScript, the four web component standards, Lit, then the HAX layer, with the tools that build and ship one and the places people learn it.",
        "kindLabels": {"rel": "what builds on what", "schema": "contracts an element carries"}}
json.dump({"meta": meta, "nodes": nodes, "evidence": {}, "tours": tours}, open("hax-stack.json", "w"), indent=1, ensure_ascii=False)
print(len(LOCAL), "local;", len(PORTALS), "portals")
