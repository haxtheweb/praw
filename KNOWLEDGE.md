# KNOWLEDGE LOG

This document records emergent knowledge, decisions, conventions, and lessons learned while working across the HAX ecosystem. Use this to capture context that doesn’t fit formal rules yet, or to explain the rationale behind rules.

Structure your entries using the templates below. Keep entries concise and searchable. When a knowledge item stabilizes into a repeatable rule, promote it into RULES.md and link back here.

## How to add a new knowledge entry
- Add a new entry at the top of the relevant section with today’s date.
- Prefer small, atomic entries over long narratives.
- Include links to code, commits, PRs, or files where possible.
- If this entry should likely become a rule, mark it with `Candidate: Yes`.

## Template

- Title: <short, descriptive title>
- Date: YYYY-MM-DD
- Context: <where/why this came up>
- Guidance: <what to do next time>
- Rationale: <why this is the right approach>
- Links: <related files/PRs/issues>
- Candidate: Yes|No

---

## Architecture & State Management

- Title: Dual-store architecture — HAXStore vs haxcms-site-store
- Date: 2026-05-07
- Context: Understanding the MobX state management boundary between the HAX editor and HAXcms site layer
- Guidance:
  - **HAXStore** (in `hax-body/lib/hax-store.js`) owns **editor state**: active node, edit mode, active gizmo, global preferences, element alignment, tour state. It is the single source of truth for anything related to the in-page editing experience.
  - **haxcms-site-store** (in `haxcms-elements/lib/core/haxcms-site-store.js`) owns **site/CMS state**: manifest, active page/route, site metadata, theme configuration, site-level settings. It is the single source of truth for the site as a navigable, publishable entity.
  - **haxcms-site-editor-ui** acts as the **bridge** between these two stores. It orchestrates the transition from CMS context (navigating pages) to editor context (editing a page) and handles the save flow (editor content → backend API → site manifest update).
  - When the user saves a page, the flow is: hax-body produces content → HAXStore holds the state → site-editor-ui reads from HAXStore and calls the backend API via the site-store's connection settings → backend persists to the page HTML file and updates site.json.
- Rationale: Future agents need to understand this boundary to avoid mixing concerns. HAXStore should never directly know about CMS routing, and site-store should never directly manipulate DOM content.
- Links: `webcomponents/elements/hax-body/lib/hax-store.js`, `webcomponents/elements/haxcms-elements/lib/core/haxcms-site-store.js`, `webcomponents/elements/haxcms-elements/lib/core/haxcms-site-editor-ui.js`
- Candidate: No
- Promoted: rule `d513754d87c145d6a166ec` in RULES.md

- Title: Admin dialog system — organic but consistent pattern
- Date: 2026-05-07
- Context: Understanding how admin dialogs (content, files, SEO, appearance, outline-editor, about) are triggered and structured
- Guidance:
  - Admin dialogs evolved organically but follow a consistent pattern: they can be invoked via a **Merlin program** (super-daemon command) or accessed via the **admin overview panel** in the site editor UI.
  - Each dialog is a separate web component in `haxcms-elements/lib/core/` (e.g., `haxcms-content-admin-dialog.js`, `haxcms-files-admin-dialog.js`, `haxcms-seo-admin-dialog.js`, `haxcms-appearance-admin-dialog.js`, `haxcms-outline-editor-dialog.js`).
  - Dialogs aim to be form-based and consistent in their data flow: render form → user submits → call backend API endpoint → update site state.
  - This is an area identified for potential future refactoring to standardize the triggering mechanism and form-to-API pipeline even further.
- Rationale: When creating or modifying admin dialogs, follow the existing organic pattern (Merlin-invokable + panel-accessible) while keeping form structure consistent. Future standardization efforts should aim to make all dialogs follow an identical event-driven pattern.
- Links: `webcomponents/elements/haxcms-elements/lib/core/haxcms-*-admin-dialog.js`, `webcomponents/elements/haxcms-elements/lib/core/haxcms-site-editor-ui.js`
- Candidate: No
- Decision: kept as a guide, not a rule (2026-10-20)

- Title: User-scaffold — foundational adaptive UX infrastructure
- Date: 2026-05-07
- Context: Understanding the current state and future vision of user-scaffold
- Guidance:
  - **Current usage**: Primarily for recalling prior user interactions and preferences. Used in a few places today (e.g., `HAXCMSSitePalette` persistence in themes like `clean-portfolio-theme` and `journey-theme`).
  - **Foundation being built**: The interaction tracking (short-term memory: delays, interaction counts; long-term memory: localStorage-persisted preferences) is infrastructure for future adaptive UX.
  - **Planned capabilities** (not yet implemented):
    - Hiding welcome messages after the user has seen them
    - Tutorial systems that adapt to user experience level
    - Recalling the state of a failed page save and offering to restore it on next reload
    - Adapting UI complexity based on user's demonstrated proficiency
  - **Architecture**: Singleton pattern via `globalThis.UserScaffold.requestAvailability()`. Uses MobX observables for `stMemory` (short-term, session-scoped), `ltMemory` (long-term, localStorage), `action` (current user action type/architype), and `data` (current action data/value).
  - **Action architypes**: mouse clicks, paste (text/html/base64/url/file), drop, drag, keyboard input. Each action is classified into a type and architype for pattern recognition.
- Rationale: When consuming user-scaffold state in components, use `ltMemory` for persistent user preferences and `stMemory` for session-level behavior tracking. The `active` flag exists to pause tracking when scaffold behavior would conflict with other systems.
- Links: `webcomponents/elements/user-scaffold/user-scaffold.js`
- Candidate: No
- Promoted: rule `01ed665f326941e9888ab1` in RULES.md

- Title: HAXiam multi-tenant auth model
- Date: 2026-05-07
- Context: Understanding how HAXiam layers institutional SSO on top of the base JWT system
- Guidance:
  - **Single-tenant**: Simple username/password authentication generating JWT tokens. One user, one installation, full admin access.
  - **HAXiam (multi-tenant)**: Layers institutional SSO (SAML/CAS/OIDC) on top of the JWT system. Enabled via `config->iam = true`.
  - **Key differences in multi-tenant mode**:
    - Per-user directory isolation (each user gets their own sites directory)
    - Symlink-based site sharing between users (`haxiamAddUserAccess` endpoint creates symlinks between user directories)
    - Path-based user validation (`getIAMTenantUserName()`, `getRequestPathUserName()`) ensuring the authenticated user matches the path being accessed
    - `connectionSettings` endpoint enforces path/user alignment in IAM mode
    - Skeleton directories can be extended via hooks (`haxcms-skeleton-dirs` event) for institutional customization
  - **API impact**: Some endpoints are only available when HAXiam is enabled (e.g., `haxiamAddUserAccess`). The frontend conditionally renders UI based on endpoint presence in `appSettings`.
- Rationale: When modifying API endpoints or auth-related code, always check for the `config->iam` conditional path. HAXiam security requires strict path/user alignment validation.
- Links: `haxcms-php/system/backend/php/lib/Operations.php` (connectionSettings, haxiamAddUserAccess), `haxcms-php/build/es6/node_modules/@haxtheweb/app-hax/lib/v2/HAXIAM_API_SPEC.md`
- Candidate: No
- Promoted: rule `1286150dc8944178aa82ca` in RULES.md

## Site Insights & Reporting

- Title: Site Insights — reports come from site-local x/api
- Date: 2026-10-20
- Context: An entry from 2026-05-07 planned a move from open-apis to site-local `x/api` endpoints. That move has landed.
- Guidance:
  - `haxcms-site-insights.js` loads reports through the `@site/listReports` and `@site/getReportByName` MFR calls, backed by `/x/api/v1/reports` in both `haxcms-nodejs` and `haxcms-php` (reports: overview, content, links, media).
  - Add a new report as a `/x/api/v1/reports/{report}` entry, mirrored in both backends and both specs (see `haxcms/WARP.md`).
  - Reports still missing from the original dashboard plan are tracked in https://github.com/haxtheweb/issues/issues/3167.
- Rationale: Site-local APIs keep insights working without an external service, keep data on-site, and work for static or offline sites.
- Links: `webcomponents/elements/haxcms-elements/lib/core/haxcms-site-insights.js`, `haxcms-nodejs/src/siteRoutes/v1/reports.js`, `haxcms-php/system/backend/php/lib/siteRoutes/v1/reports.php`
- Candidate: No

## Strategic Direction & Adoption

- Title: HAX adoption gaps — strategy lives in the issue queue
- Date: 2026-10-20
- Context: A 2026-05-07 entry ranked ten adoption, community and developer-experience gaps. That is roadmap, not a technical decision, so it moved to the issue queue.
- Guidance: Favor work that makes HAX more discoverable, documentable and extensible over adding new capabilities. The ranked gap list is tracked in https://github.com/haxtheweb/issues/issues/3166.
- Rationale: Strategy changes faster than the technical decisions recorded here, and an issue can be split, assigned and closed.
- Links: https://github.com/haxtheweb/issues/issues/3166, WORLDVIEW.md
- Candidate: No

## Web Components

- Title: Example – Prefer globalThis over window
- Date: 2025-09-25
- Context: Align with cross-environment JS standards and our ecosystem rule
- Guidance: Use `globalThis` whenever referencing global scope in components or utilities
- Rationale: Works in Node, browsers, and workers; matches existing rule CEHsAztyfB2vTCwtHGGnbk
- Links: RULES.md (JavaScript Standards)
- Candidate: No

- Title: SSR audit of checklist, reflective nudge and radar chart
- Date: 2026-10-20
- Context: First test cases for the SSR rule. Ran `hax audit ssr` and read the saved server HTML for `bullet-check-list`, `self-reflective-nudge` and `radar-chart` (webcomponents main, using the monorepo `d-d-d`). All three render. Verified in the output: (1) the checklist and the nudge write every checkbox / radio as `checked="false"`, because `.checked=${...}` on a native input is serialized as an attribute and browsers read its presence as on; (2) the checklist's `typeof="oer:LearningComponent"`, set in `firstUpdated`, is missing from the server HTML; (3) the nudge's text comes from light DOM children read in `firstUpdated`, so the server output has an empty nudge region; (4) `radar-chart` has no lifecycle code and its server output holds the full SVG, a text description and a data table. Also verified: published `@haxtheweb/d-d-d` 26.8.0 throws under SSR (`DesignSystemManager` undefined without `document.body`); monorepo main already guards it, so audits need the monorepo copy until it is released. Read from the code, not tested: the nudge creates its `MutationObserver` in `firstUpdated` and disconnects it in `disconnectedCallback`, so it probably stops observing after the element is moved; the checklist reads storage in `willUpdate`, which does run on the server (guarded by `isConnected` and try / catch), so its client first render can differ from the server's.
- Guidance: Fix the checklist and nudge with `?checked` bindings, and move the checklist's `typeof` into the template or authored content. Treat `radar-chart` as the model for a render-derived element. Re-run `hax audit ssr` after each fix.
- Rationale: The first draft of the SSR rule was written from general SSR practice and was wrong in places: the HAXcms shim already supplies `window`, `matchMedia` and observers, and the real hazards are the lifecycle split (only constructor, `willUpdate` and `render` run) and what the shim does not supply (`document.body`, storage, `location`). The bound-attribute bug could only be found by reading actual server output.
- Links: RULES.md (SSR Safety & Enhancement Audit), https://github.com/haxtheweb/create/pull/85, https://github.com/haxtheweb/haxcms-nodejs/tree/main/src/lib/ssr
- Candidate: Yes

- Title: Registry-wide SSR audit and light DOM fallbacks
- Date: 2026-10-21
- Context: Ran `hax audit ssr` over all 595 `wc-registry.json` elements of webcomponents, then fixed what it showed. First pass: 220 rendered, 118 shell, 21 empty, 36 no shadow root, 200 threw. All 200 throws were packages missing from the sandbox (185 of them `mobx`), not element bugs; after installing the pinned versions (and not the latest: `mobx` 7 gives a false "Cannot annotate" error on code written for the pinned 6.13.7) 7 still threw, all from missing packages or registry entries whose packages are legacy `9.0.1` npm dependencies rather than monorepo folders. Final: 345 rendered, 164 shell, 33 empty, 46 no shadow root. Most empty / no-shadow-root elements are utilities (stores, routers, managers). Of the elements an author can place in a page, almost all keep content in slotted light DOM already; `music-player` and `web-baseline-status` held content only in a property and got `progressiveEnhancement` hooks. 18 OER elements set `typeof` in `firstUpdated` and now reflect it. I first reported `video-player`, `a11y-media-player` and `editable-table` as throwing; that was my own render script without the shim, and with the real audit they render fine. What was missing was a link to the video, and the iframe address (`.src` property binding). Reading `nodeToContent` showed the hook output is appended after existing light DOM children, so `count-up` and `image-compare-slider` would stack another copy on each save.
- Guidance: (1) Before calling a throw an element bug, re-run it in the real audit and with the pinned dependency versions; most throws in a bare sandbox are missing packages. (2) On native elements bind attributes, not properties (`?checked`, `src=`, `href=`). (3) For property-only content add a `progressiveEnhancement` hook; make it save once with `saveOptions.wipeSlot` or a `data-prog-fallback` marker removed in `editModeChanged`; keep it out of the rendered slot. (4) Elements that already author their content as light DOM (`editable-table` writes a `<table>` on save) need nothing.
- Rationale: The audit measures server output, so it is accurate about what crawlers and exports get, but it cannot say whether a missing piece matters; reading the element and its HAX save path does. Two of the mistakes made while doing this (installing `mobx` 7, and judging three elements from a script that did not set up the shim) came from not checking the environment before trusting a result.
- Links: RULES.md (SSR Safety & Enhancement Audit), https://github.com/haxtheweb/webcomponents/pull/965, https://github.com/haxtheweb/webcomponents/pull/966, https://github.com/haxtheweb/webcomponents/pull/968, https://github.com/haxtheweb/webcomponents/pull/972, https://github.com/haxtheweb/create/pull/87
- Candidate: Yes

## HAXcms

- Title: Example – Keep metadata.site.name aligned
- Date: 2025-09-25
- Context: BasePath and routing inconsistencies traced to incorrect site name
- Guidance: Ensure metadata.site.name exactly matches the site folder name
- Rationale: Prevents basePath issues in some deployment scenarios
- Links: RULES.md (HAXcms Site Metadata)
- Candidate: No

## Design System (DDD & SimpleColors)

- Title: DDD `data-palette` (site palettes) vs `data-primary` / `data-accent` (single colors)
- Date: 2026-02-17
- Context: Theme development for HAXcms themes (`clean-portfolio-theme`, `journey-theme`) uses `data-palette` to switch multi-color palettes. Initial analysis focused on `data-primary` / `data-accent`, which control only `--ddd-theme-primary` / `--ddd-theme-accent` (single-color theming), not full palettes.
- Guidance:
  - Use `data-primary` / `data-accent` when you need a single primary/accent color for an element (sets `--ddd-theme-primary` / `--ddd-theme-accent`).
  - Use `data-palette` when you need a coordinated multi-color palette for a whole region/site.
  - Ensure the CSS that defines palette variables is applied in a scope that can match the element carrying the `data-palette` attribute.
    - `DDDPaletteStyles` uses selectors like `[data-palette="3"] { ... }` (NOT `:host([data-palette="3"])`). This means it must exist in a stylesheet that can match the actual DOM element with `data-palette` (typically the global document stylesheet), otherwise palette switching may appear to do nothing.
  - If a theme wants deterministic palette switching, prefer one of:
    - Extend `DDDSuper(...)` so DDD (including palettes) is registered via `DesignSystemManager` at the document level.
    - Or inject the palette styles into the global theme stylesheet (via `HAXCMSGlobalStyleSheetContent()`), rather than relying on shadow-scoped styles.
- Rationale:
  - In DDD, `DDDPaletteStyles` defines `--ddd-palette-color-1` through `--ddd-palette-color-7` and changes them based on `[data-palette]`.
  - Palettes currently defined in `DDDPaletteStyles` (name / number):
    - `wisdom-walk-green` / `0` (default)
    - `very-violent-red` / `1`
    - `beetles-yellow` / `2`
    - `offbrand-nittany-blue` / `3`
    - `boring-blue-gray` / `4`
    - `monotone` / `5`
    - `salmon-season` / `6`
    - `tweedle-dee` / `7`
  - Application notes (as of 2026-02-17):
    - `clean-portfolio-theme`
      - Reflects `dataPalette` to `data-palette`, persists `HAXCMSSitePalette` via `user-scaffold`.
      - Extends `DDDSuper(HAXCMSLitElementTheme)` and includes `DDDAllStyles` in global theme stylesheet; palette selectors match and update `--ddd-palette-color-*`.
      - Maps `--ddd-palette-color-*` → `--ddd-palette-*` and then defines `--ddd-lightDark-*` helper vars used throughout its CSS.
      - Cycles palettes `0..6` (does not reach palette `7`).
    - `journey-theme`
      - Reflects `dataPalette` to `data-palette`, persists `HAXCMSSitePalette` via `user-scaffold`.
      - Includes `DDDAllStyles` in `static styles` (shadow scope). Because `DDDPaletteStyles` is written as `[data-palette="..."]` selectors, shadow-scoped inclusion alone does not guarantee it can match the host element; palettes may only work if DDD palette styles are also present globally.
      - Only maps two variables: `--ddd-palette-1` from `--ddd-palette-color-1` and `--ddd-palette-2` from `--ddd-palette-color-6`.
      - Cycles palettes `0..5` (does not reach palettes `6` or `7`).
- Links:
  - `webcomponents/elements/d-d-d/lib/DDDStyles.js` (`DDDPaletteStyles`)
  - `webcomponents/elements/clean-portfolio-theme/clean-portfolio-theme.js` (`dataPalette`, `togglePalette`, palette var mapping)
  - `webcomponents/elements/journey-theme/journey-theme.js` (`dataPalette`, `togglePalette`, palette var mapping)
  - `webcomponents/elements/haxcms-elements/lib/core/HAXCMSLitElementTheme.js` (global theme stylesheet injection via `HAXCMSGlobalStyleSheetContent()`)
- Candidate: No
- Promoted: rule `447f8d9bc5484749b1188e` in RULES.md

- Title: Example – Prefer DDD tokens; use SimpleColors sparingly
- Date: 2025-09-25
- Context: Migrating components to DDD while retaining shade coverage
- Guidance: Use DDD tokens for spacing/typography/colors; use SimpleColors only when DDD lacks required shade
- Rationale: Aligns with primary design system while acknowledging gaps
- Links: RULES.md (Design System Standards)
- Candidate: No

## Build & Workflow

- Title: Example – Avoid optional chaining
- Date: 2025-09-25
- Context: Polymer parser incompatibilities
- Guidance: Don’t use `?.`; refactor to safe checks compatible with our tooling
- Rationale: Avoids build breaks and runtime surprises
- Links: RULES.md (JavaScript Standards)
- Candidate: No

## Documentation & Authoring

- Title: Example – Author with HAX-capable elements
- Date: 2025-09-25
- Context: Ensuring content can be edited with HAX and demoed consistently
- Guidance: Use elements with HAXSchema; consider demoSchema for demos and examples
- Rationale: Guarantees editor compatibility and consistent UX
- Links: RULES.md (HAX Content Authoring)
- Candidate: No
