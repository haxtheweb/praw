# HAX glossary

Plain-language terms, each tied to where it shows up. Source details live in the named skills.

| Term | Meaning |
|---|---|
| **HAX** | Headless Authoring eXperience: an open platform for authoring and owning web content. "Headless" means the authoring experience is not tied to one backend. |
| **HAXsite** | A site made of portable files (`site.json`, `pages/`, `files/`, theme). Can be hosted anywhere static files can be served. |
| **HAXcms** | The content management backends (`haxcms-nodejs`, `haxcms-php`) that create and manage HAXsites. Optional for reading or hosting a finished site. |
| **HAX editor** | The block-by-block WYSIWYG editor. Writes standards-based HTML built from web components. |
| **JOS (JSON Outline Schema)** | The format of `site.json`: a flat list of items with `parent`, `order`, `indent`, `location`, and `slug` that forms the navigation tree. https://github.com/haxtheweb/json-outline-schema |
| **Web component** | A custom HTML element built on browser standards. In HAX most are LitElement-based and live in the `webcomponents` monorepo. |
| **HAXSchema / `haxProperties`** | The description that makes a component editable in the HAX editor: its settings, inputs, and sample content (`demoSchema`). |
| **`wc-registry.json`** | A built map from every valid component tag to its module path. Read it to know which tags exist. Generated; never hand-edit. |
| **Magic script / autoloader** | The page script that finds undefined custom elements, looks them up in the registry, and imports them on demand. |
| **DDD** | The primary HAX design system (tokens such as `--ddd-*`). The repo's `hax-design-system` skill spells out the acronym. SimpleColors is the older layer it replaces. |
| **`hax` CLI** | `@haxtheweb/create`. Scaffolds sites and components, audits DDD compliance, serves and publishes. |
| **Interface skill** | A skill that documents CLI commands and flags. Owned by the `create` repo and version-locked to the CLI. |
| **Workflow skill** | A higher-order pattern that composes the CLI (audits, course design, publishing). Owned by PRAW. |
| **Managed file** | A generated file (`llms.txt`, `sitemap.xml`, `wc-registry.json`, ...). Rebuilt by tooling, never hand-edited. |
| **Ubiquity script** | The build that produces the CDN registry and distribution. Run by the maintainer, never by an agent. |
| **PRAW** | This repo: rules, knowledge, workflow skills, and the plugin marketplace for working with HAX. |
| **OER Schema** | A vocabulary for describing open educational resources (courses, lessons, assessments) in page markup. |
