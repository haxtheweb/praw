# HAXcms Site & Backend Rules

Scoped rules for HAXcms sites and backends (`haxcms-nodejs`, `haxcms-php`, and any HAXcms site checkout with `site.json`/`pages/`/`files/`). This file is read when editing haxcms-path files. Authoritative rule records (Rule IDs + Scope) live in `RULES.md`.

## Scoped rules (triggers — full text in RULES.md)
- **HAXcms Site Organization** (`ZVEm3yg7jTXBsXBOp3yPzy`) — docs in `docs/`, page order in `site.json` (JSON Outline Schema), files in `files/`, page HTML in `pages/`. Cover pillars, pedagogical ontology, AGENTS.md projects.
- **HAXcms Site Metadata** (`rHQ7lLRZmZlnFveLrWslUN`) — `metadata.site.name` must align with the site folder name; do not change it otherwise (it establishes basePath).
- **Reserved Routes** (`Q4D9hL9sFNORlMPt1z2ZEb`) — `x/` prefix is reserved (`x/search`, `x/tags`, `x/manifest`); do not create conflicting routes.
- **HAXcms Page Creation via CLI** (`tRwt1R0Bv54nuHgEfl8IWe`) — create pages via `hax site node:add` / `hax site site:items-import`, never by hand-editing `site.json` or creating page dirs manually. CLI owns page structure; agent owns page content.
- **HAX Site Scaffolding** (`hax-site-scaffold`) — create HAXcms sites with `hax site`, not manually.
- **HAXcms Theme Build** (`cfypZRDQLaJ6XsXtEaveWT`) — after theme changes to `HAXCMSLitElement` subclasses, run `yarn run build`; never hand-edit `custom-elements.json`.
- **HAXcms Backend Security/Parity** (`a8bf4a47-3d4f-4f8e-a356-a04db66ce1ab`) — any audit/security issue must be resolved in BOTH `haxcms-nodejs` and `haxcms-php` for parity.
- **MFR Call Namespacing** (`82dc87fd-6bc1-4d20-9d68-5b077bb88b89`) — see full detail below.
- **UbD course design** (`a1b2c3d4-e5f6-4789-9abc-def012345678`) — designing a unit for understanding → use `hax-ubd-backward-design` skill family; unit scope or larger; map constructs to real HAX elements.
- **UDL audit** (`4ab69ab2-d295-4c01-a448-1ce1689c7366`) — reviewing site reach for all learners → use `hax-udl-audit` skill (UDL 3.0); bias toward Action & Expression gaps.

## MFR Call Namespacing (full detail) — rule `82dc87fd…`
System-level calls (site imports, file-format conversions, operations not scoped to a single site) must use the MicroFrontendRegistry (MFR) `@system/` namespace, registered from the on-premises OpenAPI spec at `/system/api/v1` (see `app-hax-system-api-registry.js` and `system-spec.yaml`; server handlers live in `haxcms-nodejs/src/systemRoutes/v1`). Site-scoped calls (actions scoped to a specific site) must use the `@site/` namespace (handlers in `haxcms-nodejs/src/siteRoutes/v1`); the v0→v1 siteRoutes migration is complete and legacy v0 site endpoints are removed — all site-scoped work goes through `siteRoutes/v1`. We moved off the legacy `@haxcms/` MFR registrations (e.g. `@haxcms/wordpressToSite`, `@haxcms/htmlToSite`) because they resolved to external endpoints on `open-apis.hax.cloud`, which have been phased out in favor of on-premises calls. Do not add new `@haxcms/`-namespaced registrations or wire new import/conversion flows through the `create` CLI's `--import-structure` legacy v0 path; route new work through the v1 `@system/` (system-wide) or `@site/` (site-scoped) namespaces instead. All API calls must originate on-premises (do not route through open-api.hax.cloud).

## Site architecture
- `docs/` documentation · `files/` static assets · `pages/` page HTML · `site.json` structure (JSON Outline Schema) · `manifest.json` PWA manifest.
- `metadata.site.name` aligns with folder name; `metadata.theme` holds theme config; `items` is the page hierarchy.
- Use HAXcms theme inheritance (`HAXCMSLitElement`); apply DDD tokens; ensure responsive + skip-link + site-menu/breadcrumb wiring.

## Content creation
- Use HAX-capable web components for rich content; apply DDD attributes for spacing/typography; include engaging/interactive elements; ensure content is editable via the HAX editor.
- Apply OER Schema metadata where applicable; support pedagogical objectives.
- Store media in `files/`; include alt text/captions; prefer `media-playlist` + `audio-player` for media presentation and direct audio playback.

## Workflow
- Edit content through the HAX editor when possible; keep JSON Outline Schema compliance; kebab-case slugs.
- `yarn run build` after theme modifications; never hand-edit generated manifests.
- Do not work with `v1/` assets in app-hax / sites dashboard (not used).
- Use the local `hax` CLI checkout, not `npx`; use `--y`/`--no-i`/`--auto` to avoid interactive prompts when running uninterrupted.

## Integration
- Follow HAXcms API conventions; proper error handling; maintain API versioning.
- For audit/security issues, verify + resolve in BOTH backends (see rule `a8bf4a47…`).
- Repurpose core code for loading data-model aspects rather than writing new abstractions; prefer reusing existing methods for file-path resolution and similar tasks.
- Any modification to site-spec or system-spec in one system must be mirrored in both systems.

## Site quality
Performance (lazy loading, caching, minimal deps) · Accessibility (heading hierarchy, skip links, screen-reader/keyboard, contrast) · SEO (meta descriptions, semantic structure, structured data, sitemap).

---
*Scoped to haxcms. Full rule registry + IDs: `RULES.md`. Always-on global rules apply in addition.*
