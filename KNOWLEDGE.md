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
- Candidate: Yes

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
- Candidate: Yes

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
- Candidate: Yes

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
- Candidate: Yes

## Site Insights & Reporting

- Title: Site Insights — current architecture and planned evolution
- Date: 2026-05-07
- Context: Understanding what haxcms-site-insights.js does today and where it is heading
- Guidance:
  - **Current state**: Insights currently hits open-apis endpoints to assemble information about the site. The data is churned and presented via the `haxcms-site-insights.js` component (renamed internally as "Reports UI").
  - **Planned evolution**:
    - Data source should move from open-apis to **`x/api` endpoints served by the site itself**. These x/api endpoints are planned but not yet implemented.
    - Envisioned as a **dashboard** providing the site author with:
      - Content insights (what's in the site, content quality)
      - Accessibility auditing results
      - Usage reports
      - Last updated timestamps and change history
      - Other site statistics
    - The goal is to give users actionable insights into the site they are creating, not just raw data.
  - **Architecture implication**: When building x/api endpoints for insights, they should be designed as site-local APIs (served under the reserved `x/` route prefix) that return structured data the frontend dashboard can consume without relying on external services.
- Rationale: Moving insights to site-local x/api endpoints improves reliability (no external dependency), privacy (data stays on-site), and performance (no network round-trips to open-apis). This also makes insights available for static/offline sites.
- Links: `webcomponents/elements/haxcms-elements/lib/core/haxcms-site-insights.js`
- Candidate: Yes

## Strategic Direction & Adoption

- Title: HAX adoption gaps — not features, but community and discoverability
- Date: 2026-05-07
- Context: Assessing what HAX needs most to grow adoption, comparing against WordPress/Drupal/Canvas/Notion
- Guidance:
  - **Critical reframe**: As of 26.0.0+, HAX's feature set is considered to be **far beyond anything else that exists**. The gaps are NOT feature gaps. They are adoption, community, and developer experience gaps.
  - **Highest priority gaps** (in order of strategic importance):
    1. **Documentation and examples** — Comprehensive, discoverable docs with real-world usage examples
    2. **User success stories** — Demonstrating real adoption and impact to build credibility
    3. **Community growth and investment** — Growing the contributor and user base
    4. **More themes** — Expanding visual options to appeal to broader audiences
    5. **Support for other design systems** — Beyond DDD, enabling organizations to bring their own design tokens
    6. **Improved SEO via SSR / hax11ty** — Implementing hax11ty as a program to ensure published sites are optimized for search engines and deployment
    7. **AI project demonstrations** — Showing, presenting on, and talking about current AI work to build awareness
    8. **Discoverability and adoption curve** — Making it easier for people to find HAX, understand it, and get started beyond just migration tools (which already exist)
    9. **Developer experience (DX)** — Making it easier for the developer community to adopt and extend HAX
    10. **Extensibility patterns** — Modular extension system similar to Drupal modules, GravCMS plugins, WordPress plugins. People need to be able to mess with it, extend it beyond what it does, with well-defined patterns and documentation
  - **The core communication challenge**: Getting people to understand that "anything can become the web" and that HAX is a radically simple approach to web development and material management.
  - **What already works well**: Accessibility, UX, publishing workflow, and remixing capabilities all speak for themselves. The product is strong; the challenge is awareness and onboarding.
- Rationale: Agents working on HAX should understand that the primary strategic need is not building more features but rather improving documentation, DX, community infrastructure, and extensibility. When prioritizing work, favor tasks that make HAX more discoverable, documentable, and extensible over adding new capabilities.
- Links: WORLDVIEW.md (pillars), WARP.md (ecosystem overview)
- Candidate: Yes

## Web Components

- Title: Example – Prefer globalThis over window
- Date: 2025-09-25
- Context: Align with cross-environment JS standards and our ecosystem rule
- Guidance: Use `globalThis` whenever referencing global scope in components or utilities
- Rationale: Works in Node, browsers, and workers; matches existing rule CEHsAztyfB2vTCwtHGGnbk
- Links: RULES.md (JavaScript Standards)
- Candidate: No

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
- Candidate: Yes

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
