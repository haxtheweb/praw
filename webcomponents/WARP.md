# Web Components Development Rules

Scoped rules for HAX web-component development in the `webcomponents` monorepo (`elements/` directory). This file is read when editing webcomponents-path files. Authoritative rule records (with Rule IDs + Scope) live in `RULES.md`; the triggers below point at them.

## Scoped rules (triggers — full text in RULES.md)
- **Web Component Registry** (`69qEidWQwmAfq9eWziwMLn`) — `wc-registry.json` is built by the ubiquity script and drives the magic-script hydration. (Never run the ubiquity script — see global rule `SSy9vkx…`.)
- **Web Component Scaffolding** (`E9Zioqke3Y0gdnWB08XQn8`) — all new elements must be scaffolded with `hax webcomponent`; never create element dirs/files manually.
- **HAX Schema Capability** (`rVsCTSDjae8lRmsJmPO3Mk`) — elements implement `haxProperties` (HAXSchema); use `demoSchema` for valid demos.
- **DDD Usage Audit** (`MT6HPJ9BDhA13jwSXjcmeA`) — when working on a component, audit DDD token usage. (Token reference: `design-system/WARP.md`.)
- **Accessibility Audits** (`7CPveFErpSF0aZ8tKqxw0Y`) — when working on a component, audit for a11y enhancements without assuming issues exist.
- **JavaScript — globalThis** (`CEHsAztyfB2vTCwtHGGnbk`) — use `globalThis`, not `window`.
- **JavaScript — No optional chaining** (`nJF4SYUGdN5Wr5tEvaDtGY`) — no `?.` syntax (Polymer parser / toolchain issues).
- **HAX Content Authoring** (`eis0l9w9l2jG1COFySmvdT`) — when writing HAX site content, use HAX-capable tags from the registry; leverage DDD attributes for heading/paragraph offset.
- **a11y-collapse heading-button** (`WQoGOB824VGW5HECMh08ew`) — set `heading-button` on `<a11y-collapse>` so the whole heading bar is clickable.
- **SSR Safety & Enhancement Audit** (`1b8b8a93-0458-41f9-85a4-ba8d16923765`) — when creating or working on a component or theme, audit for SSR (Lit SSR + inert shim) and run `hax audit ssr`. The server runs only the constructor, `willUpdate` and `render`: keep them free of `document.body` / storage / `location` / layout, put browser-only work in `connectedCallback` / `firstUpdated`, bind native element state and addresses as attributes (`?checked`, `src=`, `href=`), not properties (`.checked`, `.src`), keep crawler-needed attributes out of `firstUpdated`, make the first render meaningful without JS (a `progressiveEnhancement` hook for property-only content, saved once).
- **Educational Content — OER Schema** (`c3XjsqFbCmoA3cxsooNyxG`) — educational elements should apply OER Schema metadata. Audit with `oerschema-audit`; find missing schema with `oerschema-integration-finder`.
- **Testing — Use the Repo's Own Runner Config** (`646fc5cf-6f1f-47e0-b48c-c54544cda490`) — run tests with the repo's `web-test-runner.config.mjs`, never a stripped-down config.
- **Testing — Poll, Don't Sleep** (`932f6cd4-90a9-451c-98af-4fb577007f9d`) — poll for the condition with a bounded timeout instead of fixed sleeps in tests/e2e.
- **Async Results Must Not Overwrite Newer State** (`35309388-b7be-40ca-88a9-539fe1dd4b0d`) — async lookups must not overwrite a property set while they were pending.
- **Never Rely on querySelectorAll Across Elements That May Stub It** (`896ecfa1-8965-4c06-a3ab-31c7e7eb28bf`) — shared helpers use `Element.prototype.querySelectorAll.call(el, sel)` or walk `children` (elements like `video-player` stub `querySelectorAll`); tests assert the node is actually found/removed.
- **Monorepo Dependency Verification** (`4a7c9e2b-8d5f-4e1a-9c3b-7f2e6d5a4b3c`) — any new import/reference must be declared in the element's `package.json`.

## Component structure & standards
- **DDD integration**: `import "@haxtheweb/d-d-d/d-d-d.js"`; extend `DDD` directly (never `DDD(LitElement)`); with mixins, `DDD` is the base class (`class MyEl extends SomeMixin(DDD) {}`). Use `ddd-` CSS custom properties for spacing, colors, typography. Use DDD icon-sizing variables for icon height/width.
- **SimpleColors**: legacy; use only where DDD lacks a needed color shade. Prefer DDD.
- **JS architecture**: pure JavaScript + LitElement, NO TypeScript. Import pre-compiled `/dist/` for any TS-origin libraries. Single quotes, avoid semicolons, ES modules, `globalThis`, no `?.`.
- **File organization**: `elements/component-name/` with `package.json`, component files, demo. `component-name.js` for the main file. Remove legacy SCSS — use CSS-in-JS.
- **Documentation**: JSDoc all public methods; document CSS custom properties; include a11y/keyboard notes in README. (Use the `hax-webcomponent-documentation-writer` skill to generate/maintain READMEs from `custom-elements.json` + `haxProperties`.)

## Component audits (when working on a component)
1. **DDD Design System**: verify token usage (see `design-system/WARP.md`).
2. **HAX Schema**: complete + accurate `haxProperties` / `demoSchema`.
3. **Accessibility**: ARIA, keyboard nav, semantic markup, focus management.
4. **Dark mode**: verify dark-mode compliance when auditing DDD usage.
5. **Dependencies**: minimal external deps; declared in `package.json`.

## Workflow
- Run `yarn run build` after changes to components inheriting `HAXCMSLitElement` (regenerates `custom-elements.json`; never hand-edit it).
- Do not run a build at the top of the monorepo. Do not prompt for traditional build commands.
- Use the local `hax` CLI checkout, not `npx`.

## Educational components
Apply OER Schema metadata; include pedagogically meaningful defaults; structure content to support learning objectives; consider a11y from an equity perspective.

- **Stores**: `HAXStore` owns editor state, `haxcms-site-store` owns site state; only `haxcms-site-editor-ui` bridges them (rule `d513754d…`).
- **Adaptive state**: remembered/adaptive user state goes through `user-scaffold` (`ltMemory` persistent, `stMemory` session, honor `active`) (rule `01ed665f…`).

---
*Scoped to webcomponents. Full rule registry + IDs: `RULES.md`. Always-on global rules (no ubiquity, no build prompts, AI guardrails, etc.) apply in addition.*
