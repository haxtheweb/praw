# HAX Ecosystem Development Rules (Lean Index)

This file is the always-on Project Rule for the `praw` repo — a lean index to the HAX ecosystem. It intentionally does **not** restate the individual rules; those live in `RULES.md` (the canonical registry) and are delivered as Global Rules (always-on) or via the scoped subdirectory files below (conditional, agent-mediated on path ancestry). Keep this file short so always-on context stays small.

## Where things live
- **`RULES.md`** — canonical registry of every rule, each tagged with a `Scope:` (`global` | `webcomponents` | `haxcms` | `design-system`). Run `node scripts/build-rules.js` to validate and emit `exports/rules-global.json` (the minimal always-on set).
- **`webcomponents/WARP.md`** — scoped rules for web-component development (read when editing webcomponents-path files).
- **`haxcms/WARP.md`** — scoped rules for HAXcms sites/backends (read when editing haxcms-path files).
- **`design-system/WARP.md`** — scoped rules for the DDD/SimpleColors design system (read when editing design-system-path files).
- **Skills** — canonical HAX skills live under `praw/.agents/skills/` (authoritative registry) and `create/src/skills/` (shipped subset built into `create/dist/skills/`). Check there first before assuming a HAX skill does not exist.

## Ecosystem map
- **`webcomponents`** — monorepo of 250+ LitElement components, themes, and the DDD design system.
- **`create` (`@haxtheweb/create`)** — the `hax` CLI: scaffolds components/sites, manages dev workflow.
- **`haxcms-php`** / **`haxcms-nodejs`** — HAXcms backends (content management, APIs, SSR). Keep feature/security parity between them.
- **`desktop`** — Electron local dev environment.
- **`hax11ty`** — HAX + Eleventy static-site integration.
- **`json-outline-schema`** — JSON schema for HAXcms content structure/navigation.
- **`hax-schema`** — HAX property schemas (HAXSchema) for editor integration.
- **`open-apis`** — legacy microservice (open-apis.hax.cloud), phased out; route new work through on-premises `@system/`/`@site/` MFR namespaces (see `haxcms/WARP.md`).
- **`docs`** — official HAX docs (a HAXcms site).
- **`issues`** — unified issue tracker for the whole ecosystem.

## Pillars (one-liners)
Accessible (WCAG 2.0 AA, minimal knowledge to maintain) · Extensible (web standards + microservices) · Free & Open (5Rs of OER) · Efficient (web standards over heavy libs, lazy loading, offline) · Platform Agnostic · Remixable (modular, semantic content) · Sustainable (environmental, technical, community).

## HAX CLI quick reference
Install/update: `npm install @haxtheweb/create --global` · `hax update` · `hax start` (interactive) · `hax serve` (dev server at http://localhost).
Scaffold: `hax webcomponent my-element --y` · `hax site mysite --y` · `hax audit` (DDD compliance).
Common flags: `--v` verbose · `--debug` · `--y`/`--auto` accept prompts · `--no-i` no interactive sub-processes · `--skip` skip animations · `--quiet` · `--writeHaxProperties` · `--custom-theme-name <n>` · `--custom-theme-template base|polaris-flex|polaris-sidebar` · `--import-site <url>` · `--import-structure <method>`.
Use the local CLI checkout (not `npx`) — it is always latest/experimental on this machine.

## Import methods (`--import-structure` values)
`pressbooksToSite` · `elmslnToSite` · `haxcmsToSite` · `notionToSite` · `gitbookToSite` · `evolutionToSite` · `htmlToSite` · `docxToSite`. Example import files live in `hax-imports/`.

## Critical always-on rules (see RULES.md for full text)
These are `global`-scope and always loaded: no ubiquity script (`SSy9vkx…`), no traditional build prompts (`pCcVD8j…`), use local `hax` CLI not npx (`ip9IudN…`), issue queue at `~/Documents/git/haxtheweb/issues` (`tJnuFVx…`), start shells in `~/Documents/git/haxtheweb/` (`bAKMWCM…`), gh CLI is installed — read its output (`edaXma3Z…`), plus the four AI coding guardrails (state assumptions, minimum viable, surgical diffs, verify outcomes). Full registry: `RULES.md`.

## Community
Discord: https://discord.gg/aCGxmRHEJP · Docs: https://haxtheweb.org/ · `man hax` for CLI docs.

---
*Lean index. Add new rules to `RULES.md` with a `Scope:` field, then run `node scripts/build-rules.js`.*
