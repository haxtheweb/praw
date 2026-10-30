# HAX Ecosystem Development Rules (Lean Index)

This file is the always-on Project Rule for the `praw` repo — a lean index to the HAX ecosystem. It intentionally does **not** restate the individual rules; those live in `RULES.md` (the canonical registry) and are delivered as Global Rules (always-on) or via the scoped subdirectory files below (conditional, agent-mediated on path ancestry). Keep this file short so always-on context stays small.

## Where things live
- **`RULES.md`** — canonical registry of every rule, each tagged with a `Scope:` (`global` | `webcomponents` | `haxcms` | `design-system`). Run `node scripts/build-rules.js` to validate and emit `exports/rules-global.json` (the minimal always-on set).
- **`webcomponents/WARP.md`** — scoped rules for web-component development (read when editing webcomponents-path files).
- **`haxcms/WARP.md`** — scoped rules for HAXcms sites/backends (read when editing haxcms-path files).
- **`design-system/WARP.md`** — scoped rules for the DDD/SimpleColors design system (read when editing design-system-path files).
- **`WHY.md` · `WORLDVIEW.md` · `VOICE.md` · `WINS.md`** — purpose, beliefs and pillar checks, voice, and sourced wins. Read `VOICE.md` and `WINS.md` before writing public copy (posts, release notes, READMEs, proposals); data behind the wins is in `impact/` (`node scripts/impact-stats.mjs`).
- **Skills** — canonical HAX skills live under `praw/.agents/skills/` (authoritative registry) and `create/src/skills/` (shipped subset built into `create/dist/skills/`). Check there first before assuming a HAX skill does not exist.

## Ecosystem map
- **`webcomponents`** — monorepo of 250+ LitElement components, themes, and the DDD design system.
- **`create` (`@haxtheweb/create`)** — the `hax` CLI: scaffolds components/sites, manages dev workflow.
- **`haxcms-php`** / **`haxcms-nodejs`** — HAXcms backends (content management, APIs, SSR). Keep feature/security parity between them.
- **`desktop`** — Electron local dev environment.
- **`hax11ty`** — HAX + Eleventy static-site integration.
- **`open-apis`** — legacy microservice (open-apis.hax.cloud), phased out; route new work through on-premises `@system/`/`@site/` MFR namespaces (see `haxcms/WARP.md`).
- **`docs`** — official HAX docs (a HAXcms site).
- **`issues`** — unified issue tracker for the whole ecosystem.

## Schema repos (documentation-only, not runtime code)
Each documents the contract/data-shape for one HAX subsystem; the runtime that consumes it lives in `webcomponents` (mostly `elements/hax-body*`, `elements/haxcms-elements`, `elements/super-daemon`) unless noted.
- **`json-outline-schema`** — `site.json`'s shape: the flat `items` list (`id`/`parent`/`order`/`indent`/`location`/`slug`) that forms a HAXsite's navigation tree, plus the Skeleton API that layers starter-site templates on top of it. Consumed by both HAXcms backends and `haxcms-site-store`.
- **`hax-schema`** — `haxProperties` / HAXSchema: the contract that makes a web component editable in the HAX editor (gizmo metadata, `settings` form fields, `haxHooks` lifecycle integration, `demoSchema`). Read before adding or auditing HAX capability on an element.
- **`hax-element-schema`** — `HAXElementSchema`, the lightweight `{tag, properties, content, eventName}` virtual-DOM object HAX passes around for insertion, duplication, and DOM↔schema conversion (`haxElementToNode`/`nodeToHaxElement`). Companion to `hax-schema`; `demoSchema` entries are `HAXElementSchema` objects.
- **`merlin-schema`** — the Option/Program contract for Merlin, the universal command-palette and voice assistant (`<super-daemon>`, `Alt+Shift`) shared by HAXcms, the HAX body editor, and app-hax. Use when registering new palette commands.
- **`appstore-spec`** — the schema for HAX's media/app browser: external media provider definitions (`apps`), reusable content stacks (`stax`), and preloaded custom elements (`autoloader`). Backs the `generateAppStore`-style endpoints that feed the HAX editor's media tray.

## Pillars (one-liners)
Accessible (WCAG 2.0 AA, minimal knowledge to maintain) · Extensible (web standards + microservices) · Free & Open (5Rs of OER) · Efficient (web standards over heavy libs, lazy loading, offline) · Platform Agnostic · Remixable (modular, semantic content) · Sustainable (environmental, technical, community).

## HAX CLI quick reference
Install/update: `npm install @haxtheweb/create --global` · `hax update` · `hax start` (interactive) · `hax serve` (dev server at http://localhost).
Scaffold: `hax webcomponent my-element --y` · `hax site mysite --y` · `hax audit` (DDD compliance).
Common flags: `--v` verbose · `--debug` · `--y`/`--auto` accept prompts · `--no-i` no interactive sub-processes · `--skip` skip animations · `--quiet` · `--writeHaxProperties` · `--custom-theme-name <n>` · `--custom-theme-template base|polaris-flex|polaris-sidebar` · `--import-site <url>` · `--import-structure <method>`.
Use the local CLI checkout (not `npx`) — it is always latest/experimental on this machine.

## Import methods (`--import-structure` values)
`pressbooksToSite` · `elmslnToSite` · `haxcmsToSite` · `notionToSite` · `gitbookToSite` · `evolutionToSite` · `ploneToSite` · `wordpressPagesToSite` · `drupalToSite` · `openstaxToSite` · `vitepressToSite` · `quartoToSite` · `htmlToSite` · `docxToSite` · `xlsxToSite`. A new importer adds its name here too (see rule `82dc87fd…`). Example import files live in `hax-imports/`.

## Critical always-on rules (see RULES.md for full text)
These are `global`-scope and always loaded: no ubiquity script (`SSy9vkx…`), no traditional build prompts (`pCcVD8j…`), use local `hax` CLI not npx (`ip9IudN…`), issue queue at <https://github.com/haxtheweb/issues> (`tJnuFVx…`), cross-repo references use public URLs, never local paths (`bAKMWCM…`), always use the latest Node.js LTS (currently 24) across configs/CI/tooling (`92dfb3b2…`), gh CLI is installed — read its output (`edaXma3Z…`), plus the five AI coding guardrails (state assumptions, minimum viable, surgical diffs, verify outcomes, pre-submission checks: run `precheck` before pushing or opening a PR). Full registry: `RULES.md`.

## Community
Discord: https://discord.gg/aCGxmRHEJP · Docs: https://haxtheweb.org/ · `man hax` for CLI docs.

---
*Lean index. Add new rules to `RULES.md` with a `Scope:` field, then run `node scripts/build-rules.js`.*
