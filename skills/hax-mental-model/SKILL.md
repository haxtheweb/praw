---
name: hax-mental-model
description: "Explain how HAX fits together: portable site files, web components, HAXSchema, the editor, optional backends, DDD, and the hax CLI. Load first when someone is new to HAX, asks what HAX is or how the pieces relate, or an agent must decide which HAX skill to use."
version: 1.0.0
license: Apache-2.0
metadata:
  author: haxtheweb
  tags: [hax, onboarding, concepts, architecture, orientation]
---

# HAX Mental Model

Orient a person or agent before they touch anything. HAX (Headless Authoring eXperience) separates
**authoring** from **storage and hosting**: content is plain files and standard web components, so it
works anywhere and stays owned by its author.

## The layers, outside in

1. **Site = portable files.** `site.json` (JSON Outline Schema) is the structure; each page is
   `pages/<id>/index.html`; assets live in `files/`. A site is static output with no required backend.
2. **Content = web components.** Pages are HTML using custom elements. A page full of tags works
   because the autoloader looks each unknown tag up in `wc-registry.json` and imports it.
3. **Authorable = HAXSchema.** A component is editable in the HAX editor only if it exposes
   `haxProperties` (with `demoSchema` for examples). No `haxProperties`, not authorable.
4. **Editor = block-by-block WYSIWYG** that writes clean HTML. People never write the markup by hand.
5. **Backends are optional and swappable.** `haxcms-nodejs` and `haxcms-php` manage sites; the
   authoring experience and the content model do not depend on either.
6. **Look and feel = DDD.** Design tokens (`--ddd-*`) keep components consistent and accessible.
   SimpleColors is the legacy layer.
7. **Interface = the `hax` CLI** (`@haxtheweb/create`). Use the installed `hax` command, not `npx hax`.

## Five rules that prevent most mistakes

- `index.html` is the source of truth for a page; sibling `index.md/json/yaml/xml` are generated.
- Generated files are rebuilt, never hand-edited (see `hax-managed-files`).
- Agents never run the ubiquity script or a top-level monorepo build; the maintainer does.
- Only use tags that exist in the registry and have `haxProperties`. Do not invent tags.
- Accessibility and open standards are defaults, not extras.

## Which skill next?

| You want to... | Use |
|---|---|
| Understand an existing site | `hax-site-structure` |
| Write or edit page content | `hax-content-authoring` |
| Know what is safe to edit or build | `hax-managed-files` |
| Style a component with DDD | `hax-design-system` |
| Build or change a component | `hax-webcomponent-dev` (from `create`) |
| Create a site or run CLI commands | `hax-site-building` (from `create`) |
| Check content quality | `hax-content-audits` plugin |
| Contribute a change | `references/contributing.md` |

Interface skills from `create` install with `hax skills install --all`.

## Going deeper

- `references/glossary.md`: plain-language terms (JOS, HAXsite, HAXcms, magic script, DDD, ...).
- `references/why-hax-works-this-way.md`: the design values behind the rules above.
- `references/contributing.md`: where issues live, how a first change flows, what agents may not do.
