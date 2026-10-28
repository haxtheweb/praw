# HAX Ecosystem Warp AI Agent Rules

This document is the single source of truth for HAX ecosystem Warp AI agent rules. Each rule carries a `Scope:` field that determines how it is delivered as agent context.

## Scope System

Every rule has one of four scopes:
- `global` — universal rules, always-on as Global Rules regardless of working directory. Keep this set small (critical, cross-cutting rules only).
- `webcomponents` — rules that apply only when developing HAX web components. Authoritative copy lives in `webcomponents/WARP.md`; this registry entry is the record.
- `haxcms` — rules that apply only when working on HAXcms sites/backends. Authoritative copy lives in `haxcms/WARP.md`.
- `design-system` — rules that apply only when working on the DDD/SimpleColors design system. Authoritative copy lives in `design-system/WARP.md`.

`scripts/build-rules.js` parses this file, emits `exports/rules-global.json` (the minimal always-on set to sync into Warp's Global Rules store), `exports/rules-by-scope.json` (per-scope groups for regenerating the subdirectory `WARP.md` files), and reports duplicate Rule IDs / duplicate content. `bash scripts/manage-rules.sh validate` runs the same checks.

## Rule Precedence System

**CRITICAL**: Rules are listed in **ASCENDING ORDER OF PRECEDENCE**
- Rules that appear **LATER** in the list take precedence over rules that appear **EARLIER**
- Project-specific rules (with file paths) take precedence over personal rules
- Subdirectory rules override parent directory rules
- When conflicts exist, **ALWAYS** follow the rule that appears **LAST**

### Precedence Hierarchy
1. **Personal Rules** (lowest precedence)
2. **Ecosystem-wide Rules**
3. **Project Rules** (higher precedence)
4. **Subdirectory Rules** (highest precedence)

## 🏗️ Architecture & File Structure Rules

### HAXcms Site Organization
- **Rule ID**: `ZVEm3yg7jTXBsXBOp3yPzy`
- **Scope**: `haxcms`
- **Content**: For the HAXcms site, all documentation is located in the `docs` folder. The site structure includes `site.json` for page order in JSON outline schema format, all files are under the `files` folder, and all page HTML content is in the `pages` folder. Documentation should ensure coverage of pillars, pedagogical ontology, and relevant projects referenced in AGENTS.md to maintain comprehensive ecosystem context.

### HAXcms Site Metadata
- **Rule ID**: `rHQ7lLRZmZlnFveLrWslUN`
- **Scope**: `haxcms`
- **Content**: In a site.json / hax site the metadata.site.name property is used to help establish the correct basePath in some scenarios. This value should not be modified to be anything other than put into alignment with the name of the folder the site is named.

### Reserved Routes
- **Rule ID**: `Q4D9hL9sFNORlMPt1z2ZEb`
- **Scope**: `haxcms`
- **Content**: The `x/` prefix for routes is reserved for internal HAXcms paths such as `x/search` and `x/tags`.

### Web Component Registry
- **Rule ID**: `69qEidWQwmAfq9eWziwMLn`
- **Scope**: `webcomponents`
- **Content**: wc-registry.json is a file that is built by the ubiquity script and is used for our "magic script". This register contains references to every valid web component that we publish on our CDN and is hydrated based on tag-name being undefined, detected in the DOM, and then imported dynamically at the associated object key.

### Issue Tracking
- **Rule ID**: `tJnuFVxe11BgToleU8oPxK`
- **Scope**: `global`
- **Content**: For any git repository in the HAX ecosystem, check issues against the unified issue queue at https://github.com/haxtheweb/issues (for example `gh issue list --repo haxtheweb/issues`).

### HAXcms Backend Security/Parity
- **Rule ID**: `a8bf4a47-3d4f-4f8e-a356-a04db66ce1ab`
- **Scope**: `haxcms`
- **Content**: Anytime an audit or security issue is raised for either `haxcms-nodejs` or `haxcms-php`, verify and resolve it in both backends to maintain feature parity and security consistency.

### MFR Call Namespacing (`@system/` and `@site/`)
- **Rule ID**: `82dc87fd-6bc1-4d20-9d68-5b077bb88b89`
- **Scope**: `haxcms`
- **Content**: System-level calls (site imports, file format conversions, operations not scoped to a single site) must use the MicroFrontendRegistry (MFR) `@system/` namespace, registered from the on-premises OpenAPI spec at `/system/api/v1` (see `app-hax-system-api-registry.js` and `system-spec.yaml`; handlers in `haxcms-nodejs/src/systemRoutes/v1`). Site-scoped calls must use the `@site/` namespace (handlers in `haxcms-nodejs/src/siteRoutes/v1`); v0 site endpoints are removed. Do not add new `@haxcms/`-namespaced registrations or route new work through the retired `open-apis` broker (the legacy v0 import path) — use `@system/` or `@site/` instead. A new site importer is complete only when every layer is wired and each repo has its PR open without being asked: both backends (`haxcms-nodejs` and `haxcms-php`, same behavior), the webcomponents client (MFR service and chooser card), and the `create` CLI, where `IMPORT_STRUCTURE_MAP` must map `<name>ToSite` to the `site/import/:platform` dispatcher (which calls the v1 handlers in-process) and the name must be listed in `--import-structure` help, the man page and the README. Use the `hax-importer-dev` skill. (Full detail lives in `haxcms/WARP.md`.)

### Editor State vs Site State (Dual Store)
- **Rule ID**: `d513754d87c145d6a166ec`
- **Scope**: `webcomponents`
- **Content**: Keep the two MobX stores separate. `HAXStore` (`hax-body/lib/hax-store.js`) owns editor state (active node, edit mode, gizmo, preferences, tour); `haxcms-site-store` (`haxcms-elements/lib/core/haxcms-site-store.js`) owns site/CMS state (manifest, active page/route, site metadata, theme configuration). `haxcms-site-editor-ui` is the only bridge between them and runs the save flow (editor content, then backend API, then manifest update). HAXStore must never know about CMS routing, and the site store must never manipulate page DOM content. Rationale and flow: KNOWLEDGE.md entry "Dual-store architecture".

### HAXiam Multi-Tenant Path/User Alignment
- **Rule ID**: `1286150dc8944178aa82ca`
- **Scope**: `haxcms`
- **Content**: When changing API endpoints or auth code in haxcms-php or haxcms-nodejs, check the HAXiam path (`config->iam`) as well as single-tenant mode. In multi-tenant mode each user has an isolated sites directory, and endpoints such as `connectionSettings` must enforce strict alignment between the authenticated user and the requested path (for example `getIAMTenantUserName()` and `getRequestPathUserName()`). Never weaken that check, and verify the change in both backends. Rationale: KNOWLEDGE.md entry "HAXiam multi-tenant auth model".

### Canonical Repository Directories Are Never Renamed
- **Rule ID**: `7e2c1a94-3b58-4d0f-9c6a-1f8e4d2b5a30`
- **Scope**: `global`
- **Content**: Never rename, move, or delete the canonical repository folders in the local HAX ecosystem working directory (the folder that holds all HAX repo checkouts — for example `create`, `webcomponents`, `haxcms-nodejs`, `haxcms-php`, `praw`, `docs`, `issues`). These folders are the single source of truth for local work; renaming a canonical folder (e.g. to a hidden `.name-<suffix>` copy) makes the work it contains effectively lost. If a repo must be duplicated for isolation (parallel agents, test fixtures), work in a hidden dot-suffixed copy (e.g. `.create-t0D9Xyd1`) and leave the canonical folder in place. When the work is finished, restore relocated checkouts to their canonical names. If a canonical folder is missing or gutted (only `node_modules` / lockfiles remain), recover it from the newest clean git checkout (including hidden copies and `.backup_*` folders) and put it back under its canonical name before doing further work there.

## 🎨 Design System Standards

### DDD Design System (Primary)
- **Rule ID**: `MLhl56jNSqHvnRiAW5A2GR`
- **Scope**: `design-system`
- **Content**: The design system called DDD is located under the path `elements/d-d-d` and should be leveraged for fonts, colors, padding, spacing, margins and other consistency in component and site design.

### DDD Usage Audit
- **Rule ID**: `MT6HPJ9BDhA13jwSXjcmeA`
- **Scope**: `webcomponents`
- **Content**: Whenever working on a specific webcomponent, perform a quick audit to ensure proper usage of the DDD design system. (Design-system detail lives in `design-system/WARP.md`.)

### SimpleColors (Legacy System)
- **Rule ID**: `K0lV6BJOPrqP7iJMZkemUw`
- **Scope**: `design-system`
- **Content**: We have an older color based designs system called SimpleColors. We still use this in order to fill in gaps in DDD as far as shades of all colors. SimpleColors creates a base line color spectrum for levels of red, orange, blue, etc. When possible we should be using DDD's colors instead of these, though there are elements that will still leverage it in unique situations.

### DESIGN.md Compliance (PRAW Design Source of Truth)
- **Rule ID**: `c4f0b69d-9ed4-4b6d-bf52-6a3d9937c98f`
- **Scope**: `design-system`
- **Content**: For any design-related decisions in this repository, `DESIGN.md` at the repository root is the canonical source of truth. Future design work must conform to its design tokens, CSS variable implementation patterns, component guidance, and Do's/Don'ts.

### DDD Palettes vs Single Colors
- **Rule ID**: `447f8d9bc5484749b1188e`
- **Scope**: `design-system`
- **Content**: Use `data-primary` / `data-accent` for a single color on an element (they set `--ddd-theme-primary` / `--ddd-theme-accent`); use `data-palette` for a coordinated multi-color palette across a region or site (`--ddd-palette-color-1` to `-7`, palettes `0` to `7`). `DDDPaletteStyles` selects `[data-palette="N"]`, not `:host([data-palette])`, so those styles must exist where they can match the element: extend `DDDSuper(...)` so DDD registers at the document level, or add `DDDAllStyles` to the global theme stylesheet via `HAXCMSGlobalStyleSheetContent()`. Shadow-scoped inclusion alone can make palette switching silently do nothing. Details: KNOWLEDGE.md entry "DDD data-palette".

### HAX UI: Admin Surfaces Layer of DDD
- **Rule ID**: `1992902d74844c908ab446`
- **Scope**: `design-system`
- **Content**: Admin surfaces (anything only a signed-in editor sees whose job is to change settings or data: site admin and its sections, outline-designer, revisions, reports, system admin, and editor chrome as it is updated) use HAX UI, the admin layer of DDD, not DDD's content scale. HAX UI is deliberately smaller and denser than content; admin UI does not mirror the content font scale (this includes admin fieldsets, `contract-admin-fieldset`). Spread `HaxUiAdminTokens` and `HaxUiAdminPrimitives` from `@haxtheweb/hax-body/lib/hax-ui-styles.js` and style with `--hax-ui-*` only (14px text, 32px rows, one accent; every value maps to a DDD primitive). Site and system admin sections render inside the one admin dialog and never draw their own titlebar or Save button: the shell's action bar stages saves, lights Save when there are changes and asks before leaving with unsaved changes. Authored content, themes and anything a visitor sees stay on DDD. Missing values go into `HaxUiAdminTokens` (mapped to DDD) before use; proposed tokens are documentation until adopted. Guide: `elements/d-d-d/design-system/source/hax-ui-admin.md` in haxtheweb/webcomponents; audit with `hax-pattern-library-audit` (`contract-admin-*`). outline-designer is the reference implementation.

## 🧩 Web Component Development

### HAX Schema Capability
- **Rule ID**: `rVsCTSDjae8lRmsJmPO3Mk`
- **Scope**: `webcomponents`
- **Content**: Elements with a haxProperties method are HAX capable, leveraging the HAXSchema standard to interface with the HAX editor. The demoSchema part provides all necessary information to create example elements in HAX. For demos launching in codepen, use demoSchema and HAX helper methods to create valid demos with appropriate tag names, properties, and slotted content for accurate examples.

### Accessibility Audits
- **Rule ID**: `7CPveFErpSF0aZ8tKqxw0Y`
- **Scope**: `webcomponents`
- **Content**: Whenever working on a specific webcomponent, perform a quick audit for potential accessibility enhancements without assuming issues exist, but ensure to look for them.

### JavaScript Standards — globalThis
- **Rule ID**: `CEHsAztyfB2vTCwtHGGnbk`
- **Scope**: `webcomponents`
- **Content**: When writing global scope referenced JavaScript, use `globalThis` instead of `window` for consistency.

### JavaScript Standards — No optional chaining
- **Rule ID**: `nJF4SYUGdN5Wr5tEvaDtGY`
- **Scope**: `webcomponents`
- **Content**: Do not use the optional chaining syntax (`?.`) because the current toolchain / Polymer parser has issues with this syntax.

### HAX Content Authoring
- **Rule ID**: `eis0l9w9l2jG1COFySmvdT`
- **Scope**: `webcomponents`
- **Content**: When you write content for hax sites make sure that the webcomponent tags you are using are things that could have been authored and put in the page. This means written using the HAX editor via elements that have HAXSchema. This registry has a list of all valid HAX capable elements and while not always used on every page, it's useful for knowing what is possible. Some times supplying visually interesting content helps with engagement for video, table, and block element data. Also keep in mind the DDD attributes that we support to help make headings and paragraph content offset in a consistent way.

### a11y-collapse heading-button
- **Rule ID**: `WQoGOB824VGW5HECMh08ew`
- **Scope**: `webcomponents`
- **Content**: When using a11y-collapse, ensure that the `heading-button` property is set on the HTML element to make it easier for the end user to click the whole heading to expand the content. Without it, only the small toggle icon is clickable; with it, the entire heading bar becomes a clickable button, which is a better UX.

### haxHooks lifecycle integration
- **Rule ID**: `haxhooks-lifecycle-integration`
- **Scope**: `webcomponents`
- **Content**: Elements that need to participate in HAX lifecycle / state changes without importing HAX implement a `haxHooks()` method mapping hook names to element method names. The platform stays type-agnostic by routing through these hooks rather than hard-coding support for specific elements or file types. Use `processFileUpload` (returns `{ fileUuid, operation, valueMapping, fallbackType? }` or `false`) to let an element own its post-upload conversion from the generic tray upload / drag-drop path (`HAXStore.applyFileUploadTransform`), mirroring the per-field schema `uploadTransform`. Use `gizmoRegistration` to extend `validGizmoTypes` or register an app store. Use `mediaSourceUpdated` to refresh an element's live preview when a backing file changes in place. Use `preProcessInsertContent` / `preProcessNodeToContent` / `postProcessNodeToContent` to hook insertion / export serialization. Use `activeElementChanged` / `editModeChanged` to sync edit state. Use `inlineContextMenu` to add context-menu buttons. The authoritative hook list and signatures live in the comment block at the top of `HAXWiring.js` (`elements/hax-body-behaviors/lib/HAXWiring.js`) and are mirrored in `hax-schema/README.md` under `# Hax hooks`.

### Educational Content Standards (OER Schema)
- **Rule ID**: `c3XjsqFbCmoA3cxsooNyxG`
- **Scope**: `webcomponents`
- **Content**: Creating educational elements in HAX? Apply OER Schema metadata for consistent semantic structure and interoperability. Audit authored content with the `oerschema-audit` skill; find components missing schema with the `oerschema-integration-finder` skill. Map to real OER classes (Course/Unit/Module/Lesson/LearningObjective/Assessment/Quiz/Activity/Task/Rubric/SupportingMaterial/TableOfContents) — never invent classes.

### User-Scaffold For Adaptive UX State
- **Rule ID**: `01ed665f326941e9888ab1`
- **Scope**: `webcomponents`
- **Content**: Adaptive and remembered user state goes through the `user-scaffold` singleton (`globalThis.UserScaffold.requestAvailability()`), not ad-hoc localStorage or per-component trackers. Use `ltMemory` for persistent preferences, `stMemory` for session-level behavior, and honor the `active` flag, which pauses tracking when it would conflict with other systems. Treat it as the foundation for system-level adaptive features (welcome messages, adaptive tutorials, save-failure recovery). Rationale: KNOWLEDGE.md entry "User-scaffold".

### SSR Safety & Enhancement Audit
- **Rule ID**: `1b8b8a93-0458-41f9-85a4-ba8d16923765`
- **Scope**: `webcomponents`
- **Content**: When creating a new component or theme, or working in an existing one, audit it for server-side rendering (SSR) without assuming issues exist. HAXcms server-renders elements with Lit SSR (`@lit-labs/ssr`) plus a small inert DOM shim. `hax audit ssr` (report-only, in the `create` repo) shows how an element fares; run it and read the saved HTML (`--save-html`). The server runs only the constructor, `willUpdate` and `render`; `connectedCallback`, `firstUpdated`, `updated` and `disconnectedCallback` do not run. Safety: (1) Keep the constructor, `willUpdate`, `render` and anything they call free of `document.body`, `document.head`, `localStorage` / `sessionStorage`, `location` and layout measurements. The shim supplies an inert `window`, event listeners, `matchMedia`, observers and query / child / class / style APIs, so those do not throw but find nothing, and `getBoundingClientRect` returns zeros. (2) Put browser-only work, including reading storage and measuring layout, in `connectedCallback`, `firstUpdated` or `updated`. (3) Guard any browser API the server can reach with `globalThis` (`typeof globalThis.document !== 'undefined'`, `globalThis.localStorage && ...`) or a try / catch, never a bare `window` / `document` reference, and do not use `?.`. (4) Add listeners and observers in `connectedCallback` and remove them in `disconnectedCallback`, so they keep working if the element is moved. (5) Keep import-time side effects out of helper modules; an element module defining its own tag is expected. (6) Load browser-only dependencies with dynamic `import()` from client-only lifecycle methods. (7) An element that cannot render on the server (WebGL, audio, real layout) sets `static ssr = false`, optionally with `static ssrSkipReason`, instead of throwing. Enhancement (go beyond not breaking): (8) Make the first render useful without JavaScript: default text, slotted content and attribute defaults should produce meaningful HTML on the server, not an empty shell. `radar-chart` is a good model, its server output holds the SVG, a text description and a data table. (9) The shim's `children` is empty, so data the first render needs must arrive through properties or attributes, not be read from light DOM children after upgrade; if an element keeps authored data in light DOM, make sure the render is still meaningful without it. (10) In templates, use attribute bindings instead of property bindings on native elements: `?checked` / `?disabled` rather than `.checked` / `.disabled` (SSR writes `.checked=${false}` out as `checked="false"`, which browsers read as on until hydration), and `src=${v}` / `href=${v}` (with `ifDefined` when it can be undefined) rather than `.src` / `.href` (SSR does not write a property binding at all, so an `<iframe .src=${url}>` reaches the server HTML with no address). `hax audit ssr` flags both. (11) Put attributes that crawlers or styles need (RDFa `typeof`, state that CSS selects on) in the rendered template, a reflected property or authored content, not in `setAttribute` calls inside `firstUpdated`, which the server never runs. (12) Keep `render()` deterministic (no `Math.random()`, `Date.now()` or generated ids) and use `static styles` rather than runtime-injected styles. (13) If the content lives only in a property or in the shadow render (a video address, a number, images), provide a `progressiveEnhancement` hook in `haxHooks()` that returns fallback light DOM markup (a link, text, an `<img>`) for crawlers, RSS, markdown exports and no-JS readers. HAX runs the hook on save and appends its output after the element's existing light DOM children, so make it save once: either set `saveOptions.wipeSlot: true` when the element has no authored slot content to keep, or mark the fallback (`data-prog-fallback`) and remove it in an `editModeChanged` hook when edit mode starts. Put it in a slot the shadow root does not render (the default slot when only named slots are rendered, or `slot="prog-fallback"`) so it is never drawn beside the real element, escape every value and accept only http(s) or relative URLs. (14) For themes, keep the skip link and named regions in the server-rendered template and do not depend on `document.body` or global state at import time. When the audit finds a gap, fix it if it is in scope of the change; otherwise note it so it can be tracked. Rationale and test cases: KNOWLEDGE.md entry "SSR audit of checklist, reflective nudge and radar chart".

## ⚙️ Build & Development Workflow

### Testing — Use the Repo's Own Runner Config
- **Rule ID**: `646fc5cf-6f1f-47e0-b48c-c54544cda490`
- **Scope**: `webcomponents`
- **Content**: When running element tests locally, use the repo's own `web-test-runner.config.mjs` (e.g. `yarn test` from the element directory, or `--config=../../web-test-runner.config.mjs`), not a hand-written or stripped-down config. It supplies the `process` shim the test page needs and the raised per-test timeout; without them healthy suites fail with `process is not defined` or time out, which is easy to misread as an environment limit. If a custom config is unavoidable (for example to point at a different browser binary), spread the repo config and override only the launcher.

### Testing — Poll, Don't Sleep
- **Rule ID**: `932f6cd4-90a9-451c-98af-4fb577007f9d`
- **Scope**: `webcomponents`
- **Content**: Do not wait for asynchronous work in tests (or e2e flows) with a fixed `setTimeout`/sleep. Poll for the condition the test actually needs (a property, attribute, rendered node or dialog) with a bounded timeout, so a slow CI runner passes and a real failure still reports the real assertion. Use fixed waits only to prove that something does not happen.

### Async Results Must Not Overwrite Newer State
- **Rule ID**: `35309388-b7be-40ca-88a9-539fe1dd4b0d`
- **Scope**: `webcomponents`
- **Content**: When an asynchronous lookup (IndexedDB, fetch, storage) assigns to a component property, check that the property has not been set in the meantime before assigning (compare against the value read when the lookup started, or only assign while it is still unset). Otherwise a late result silently clobbers a user or test action, producing intermittent failures that depend on timing.

### Never Rely on querySelectorAll Across Elements That May Stub It
- **Rule ID**: `896ecfa1-8965-4c06-a3ab-31c7e7eb28bf`
- **Scope**: `webcomponents`
- **Content**: Some elements override `querySelectorAll` (for example `video-player`'s SSR stub, which returns `[]`), so shared helpers that call `el.querySelectorAll(...)` on an arbitrary element can silently do nothing. In shared code call the platform method directly (`Element.prototype.querySelectorAll.call(el, selector)`) or walk `el.children`/`el.childNodes`, and keep SSR stubs inert only for the element's own use. Tests for such helpers must assert that the expected node or object is actually found (and, for removals, that it is gone), not merely that the call did not throw; a failed assertion on a DOM node can also hang the test page until the runner's finish timeout.

### HAX CLI Usage
- **Rule ID**: `ip9IudNwZrZQsyk4ggvCzH`
- **Scope**: `global`
- **Content**: When running hax commands don't do npx, instead use the local copy that we have as it is always the latest or even experimental as the source starts with this machine.

### Web Component Scaffolding
- **Rule ID**: `E9Zioqke3Y0gdnWB08XQn8`
- **Scope**: `webcomponents`
- **Content**: All new elements in the monorepo must be created using the `hax webcomponent` CLI command to ensure uniformity, including generation of demo, packaging, and distribution files. Do not create webcomponent directories or files manually in the monorepo — always scaffold with the CLI tool first.

### Element Docs Setup
- **Rule ID**: `f3c7716773784e8f94254a`
- **Scope**: `webcomponents`
- **Content**: Every element in the webcomponents monorepo ships its documentation data. Scaffold with `hax webcomponent <name> --y --no-i` and never pass `--no-docs` there: in the monorepo the scaffold adds `node ../../scripts/extract-element-docs.mjs --write .` to the end of the element's `build` script, which writes `lib/<tag>.docs.json` for `<documentation-player>`. After changing an element's properties, HAX settings, slots or events, run `yarn run build` in its folder and commit the refreshed docs data. Walkthroughs (`lib/<tag>.motion.json`) and video tutorials (`lib/<tag>.video.json`, written by `scripts/link-element-tutorial.mjs`) sit next to it; check walkthroughs with `node scripts/extract-element-docs.mjs --status <element>`.

### HAX Site Scaffolding
- **Rule ID**: `hax-site-scaffold`
- **Scope**: `haxcms`
- **Content**: When creating HAXcms sites for testing or any purpose, always use the `hax site` command to generate the site. This ensures the site is created in the standard deployment location with the correct structure, theme configuration, and follows HAXcms conventions. Do not create site directories or files manually — always scaffold with the CLI tool first.

### HAXcms Page Creation via CLI
- **Rule ID**: `tRwt1R0Bv54nuHgEfl8IWe`
- **Scope**: `haxcms`
- **Content**: Always create HAXcms site pages through the `hax` CLI (`hax site node:add` or `hax site site:items-import`), never by manually creating page directories or hand-editing `site.json`. Manual page creation bypasses the CLI's page-id generation, slug/location management, and atomic `site.json` updates, which corrupts the JSON Outline Schema structure and breaks the site in production. The CLI owns page structure; the agent only owns page content.

### No Traditional Build Prompts
- **Rule ID**: `pCcVD8jgmc7zHeHTDEBzD1`
- **Scope**: `global`
- **Content**: Do not ask or prompt to run traditional build commands in this monorepo as they are not used.

### HAXcms Theme Build
- **Rule ID**: `cfypZRDQLaJ6XsXtEaveWT`
- **Scope**: `haxcms`
- **Content**: Any time changes are made to a HAXcms site theme using classes that inherit from HAXCMSLitElement, run `yarn run build` at the end instead of manually editing the custom-elements.json file.

### Command Automation
- **Rule ID**: `PacOyoQW2aIyaTO3R6asNL`
- **Scope**: `global`
- **Content**: If you have been told to keep running commands without interuption, ensure that when running commands in hax ensure that the `--y` and `--no-i` and `--auto` commands are correctly used in order to ensure that there's no questions asked of the human or launching off into a new window / process. Otherwise a command to display the site when in a prompting exchange could lead for it to open in a new window and get stopped.

### Version Control
- **Rule ID**: `edaXma3ZIiHZ86GyX4MoSu`
- **Scope**: `global`
- **Content**: github cli is installed just read the output of it instead of asking me to verify.

### Cross-Repo References — No Local Paths
- **Rule ID**: `bAKMWCMrqRLGdWmuNWgVUw`
- **Scope**: `global`
- **Content**: When one HAX repo, rule, skill or doc refers to another, use its public URL (`https://github.com/haxtheweb/<repo>`, or `https://raw.githubusercontent.com/haxtheweb/<repo>/<branch>/<path>` for a single file), never a path on someone's machine such as a home-folder checkout. Many agents run in the cloud and cannot see a local checkout. Instructions for a person at a terminal should be relative to their own clone.

### Node.js Version — Latest LTS
- **Rule ID**: `92dfb3b2-1c32-42dc-89c3-0f4ae66f7227`
- **Scope**: `global`
- **Content**: User prefers to always use the latest Node.js LTS release across the ecosystem (currently Node 24). Apply this to `.nvmrc`/`engines` fields, CI workflow `node-version` matrices (e.g. `actions/setup-node`), Docker base images, and local tooling. When a newer LTS supersedes 24, update this rule and all ecosystem workflows/configs in step.

### Monorepo Dependency Verification
- **Rule ID**: `4a7c9e2b-8d5f-4e1a-9c3b-7f2e6d5a4b3c`
- **Scope**: `webcomponents`
- **Content**: If we add a dependency (import or reference) to an element in the webcomponents monorepo, verify that the dependency is declared in the `package.json` for that element before completing the change.

### Script Restrictions
- **Rule ID**: `SSy9vkxAqBTIcIXvYUstGA`
- **Scope**: `global`
- **Content**: The agent is explicitly not allowed to run the ubiquity script under any circumstances.

### AI Guardrails — State Assumptions
- **Rule ID**: `74cc0274-6bf2-45a0-8e06-b88254f4cf9e`
- **Scope**: `global`
- **Content**: Before implementing, state assumptions explicitly when ambiguity exists, ask clarifying questions when multiple interpretations would materially change the solution, and surface simpler alternatives/tradeoffs instead of silently choosing one.

### AI Guardrails — Minimum Viable
- **Rule ID**: `f98f5e24-c343-4c12-b1c8-d6ae9783afaa`
- **Scope**: `global`
- **Content**: Prefer minimum viable implementation. Do not add speculative features, abstractions, configurability, or defensive complexity that was not requested.

### AI Guardrails — Surgical Diffs
- **Rule ID**: `d2315f2d-f4b2-4e86-bdd0-37b2d42fef89`
- **Scope**: `global`
- **Content**: Keep diffs surgical: modify only code directly tied to the request, avoid unrelated refactors or formatting-only churn, and only remove unused code introduced by your own changes unless explicitly asked.

### AI Guardrails — Verify Outcomes
- **Rule ID**: `f15ba99a-0a0a-42a0-a413-d8dfdc8eb20b`
- **Scope**: `global`
- **Content**: Define concrete success criteria and verify outcomes using project-appropriate checks (command output, linting, runtime validation, or existing tests when applicable), then report what was validated.

### AI Guardrails — Pre-Submission Checks
- **Rule ID**: `186fad44-1725-470e-80a7-903ea54fce1a`
- **Scope**: `global`
- **Content**: Before editing in a repo, read its `AGENTS.md` and the `scripts` in its `package.json` to find the lint, format and test commands it expects; do not assume a check you ran elsewhere is the one it uses. Before pushing code or opening a PR, run the repo's `precheck` script (`npm run precheck`; `yarn precheck` in `webcomponents`), fix every failure it reports, and re-run until it passes (`precheck:fix` repairs formatting and fixable lint). Run it again after your last commit, not only after the first. Repos with a `precheck` script (`create`, `haxcms-nodejs`, `webcomponents`) also block `git push` and `gh pr create` via a Claude Code hook, but that hook only fires for those commands, run from inside that repo; a PR opened another way (for example `gh api` where GraphQL is unavailable) or from another working directory is not checked, so run `precheck` yourself first. Do not bypass it by loosening lint or format configs, adding ignore entries, or skipping hooks. ESLint alone is not a substitute: it commonly ignores test files, which Prettier still checks, so a new test file can pass lint and fail format. In a repo without `precheck` (for example `haxcms-php`), run its test suite and any lint or format-check scripts it has on the files you changed, and say in the PR description what you ran. In a sparse or partial checkout where `precheck` or its config is missing, run Prettier and ESLint directly with the repo's own config on the changed files, and say what could not be run. After pushing, check the PR's CI results (`gh pr checks`, or the REST API where GraphQL is unavailable) and, if a check fails, read its logs, fix the cause, and push again.

### HAX Skill Lookup Locations
- **Rule ID**: `c089870b608c482a847ccc`
- **Scope**: `global`
- **Content**: When looking for skills related to HAX itself (HAX-specific workflows, CLI operations, site building, web component development, the DDD design system, onboarding, issue analysis, rule management, UbD/UDL instructional design, etc.), look in the `praw` and `create` repositories rather than searching elsewhere. The canonical HAX skills live under `praw/.agents/skills/` (the authoritative registry) and `create/src/skills/` (a shipped subset that is built into `create/dist/skills/`). Check these locations first before assuming a needed HAX skill does not exist.

## 🧠 Instructional Design

### HAX Course Units via Understanding by Design
- **Rule ID**: `a1b2c3d4-e5f6-4789-9abc-def012345678`
- **Scope**: `haxcms`
- **Content**: Designing a HAX course unit whose goal is student understanding? Use the `hax-ubd-backward-design` skill family (UbD backward design: desired results → acceptable evidence → learning experiences). Design at unit scope or larger; avoid the twin sins of activity-oriented design and coverage. Map every construct to a real, HAX-authorable element — never invent tag names. Persist each unit's design at `files/ubd/<unit-slug>.manifest.json`. Framework: Wiggins & McTighe (2005), *Understanding by Design* (Expanded 2nd ed.).

### Universal Design for Learning (UDL) Audit
- **Rule ID**: `4ab69ab2-d295-4c01-a448-1ce1689c7366`
- **Scope**: `haxcms`
- **Content**: Reviewing whether a HAX site/page reaches all learners? Use the `hax-udl-audit` skill (UDL 3.0: multiple means of Engagement, Representation, Action & Expression). Bias toward flagging Action & Expression gaps — interactive assessment blocks are the empirically-confirmed gap across the HAX training corpus. Map every guideline to a real, HAX-authorable element — never invent tag names. Framework: CAST (2024), *UDL Guidelines 3.0*.

### Learning-Science Design Matched to Learner Proficiency
- **Rule ID**: `fc4153f1-90f0-4d22-a023-fec8f492b408`
- **Scope**: `haxcms`
- **Content**: Designing or reviewing HAX instruction for adults or mixed-experience learners? Profile the learners' stage (novice, advanced beginner, competent, proficient, expert) with the `hax-proficiency-scaffolding` skill before sequencing, and fade support as proficiency rises: heavy guidance helps novices but hurts experts (expertise reversal). Fill question feedback slots at the matching level (`hax-feedback-design`), schedule later retrieval for every key concept (`hax-practice-and-retrieval`), and add stage-matched reflection (`hax-reflection-prompts`). Audit lessons with `hax-instructional-events-audit` and media use with `hax-multimedia-principles-audit`. Map every recommendation to a real, HAX-authorable element — never invent tag names. Framework: Stanney, Skinner & Hughes (2023), *ELEVATE-XR*.


## 🗂️ Project-Specific Rules

### Recurring security-audit playbook for the 5 core repos
- **Rule ID**: `759643a6db03433a9d742f`
- **Content**: Recurring security audits cover create, haxcms-nodejs, webcomponents, haxcms-php, and HAXiam. Start every audit by reading that repo's SECURITY-AUDIT.md (read order, scope, commands, regression guards, reporting convention). The repo's undated security_best_practices_report.md is the canonical current state; dated security_best_practices_report_YYYY-MM-DD.md files are archived rounds. Cite findings with file:line and mark fixes with inline security comments referencing the finding ID. Report vulnerabilities via SECURITY.md private advisories, never public issues. Keep haxcms-php and haxcms-nodejs security/spec fixes mirrored in both backends.

## 📋 Rule Management System

### Adding New Rules
1. Add the rule to this RULES.md file under the appropriate category with a `Scope:` field.
2. Assign a unique Rule ID (UUID format for new rules).
3. Document the rule content and context.
4. Run `node scripts/build-rules.js` to validate (catches duplicate IDs + duplicate content).
5. If the rule is `global`, sync it into Warp's Global Rules store; if scoped, ensure the corresponding subdirectory `WARP.md` carries the prose.

### Updating Existing Rules
1. Locate the rule by Rule ID in this document.
2. Update the content while preserving the Rule ID.
3. Run `node scripts/build-rules.js` to validate.
4. Update the corresponding subdirectory `WARP.md` if it is a scoped rule.

### Rule Categories
- **🏗️ Architecture & File Structure**: Site organization, routing, file systems
- **🎨 Design System Standards**: DDD, SimpleColors, theming guidelines
- **🧩 Web Component Development**: HAX capability, accessibility, JavaScript standards
- **⚙️ Build & Development Workflow**: CLI usage, build commands, version control
- **🧠 Instructional Design**: UbD, UDL pedagogical frameworks

### Validation
- `node scripts/build-rules.js` — parses RULES.md, emits `exports/rules-global.json` + `exports/rules-by-scope.json`, reports duplicate Rule IDs and duplicate normalized content (exit code 2 on warnings).
- `bash scripts/manage-rules.sh validate` — runs the same duplicate checks plus section-header structure checks.

### Cross-References
This RULES.md file is the canonical registry. Scoped prose lives in:
- <https://github.com/haxtheweb/praw/blob/main/webcomponents/WARP.md> (webcomponents scope)
- <https://github.com/haxtheweb/praw/blob/main/haxcms/WARP.md> (haxcms scope)
- <https://github.com/haxtheweb/praw/blob/main/design-system/WARP.md> (design-system scope)
- <https://github.com/haxtheweb/praw/blob/main/WARP.md> (lean ecosystem index, always-on as the praw Project Rule)

## 🔄 Future Rule Management

All future RULES work should:
1. **Read from** this repository for existing rules
2. **Write to** this repository for new rules, including a `Scope:` field
3. **Validate** with `node scripts/build-rules.js` before committing
4. **Reference** the appropriate subdirectory `WARP.md` for scoped prose
5. **Maintain** precedence order and rule relationships
6. **Log emergent knowledge** in KNOWLEDGE.md for insights that may become rules

### Knowledge Capture Process

**For emergent insights and learnings:**
- Log decisions, patterns, and discoveries in `KNOWLEDGE.md`
- Use the structured template for consistency
- Mark potential rules with `Candidate: Yes`
- Promote stable knowledge items to formal rules in this file
- Link back to KNOWLEDGE.md entries for context and rationale

---

*This document serves as the authoritative registry for all HAX ecosystem Warp AI agent rules. It should be updated whenever new rules are created or existing rules are modified. Run `node scripts/build-rules.js` to validate after any change.*
