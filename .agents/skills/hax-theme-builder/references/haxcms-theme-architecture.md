# HAXcms Theme Architecture Cheat Sheet

All paths below are relative to `webcomponents/elements/haxcms-elements/lib/` unless noted.

## Base class: `HAXCMSLitElementTheme`

`core/HAXCMSLitElementTheme.js`, extends `HAXCMSTheme(ResponsiveUtilityBehaviors(LitElement))`.

```js
import { HAXCMSLitElementTheme, css, html, store, autorun, toJS } from "@haxtheweb/haxcms-elements/lib/core/HAXCMSLitElementTheme.js";
```

Provides for free:
- Reactive props: `editMode`, `trayStatus`, `isLoggedIn`, `emptyContent`, `color`, `hexColor`,
  `contentContainer`, `_location`, `responsiveSize`.
- `HAXCMSThemeSettings` (autoScroll, scrollTarget, scrollSettings, etc).
- `HAXCMSGlobalStyleSheetContent()` — override and call `super.HAXCMSGlobalStyleSheetContent()`
  first (spread the array) to add global `body`/`:root` rules injected into the page's global
  style element. Use this for `body` background/margin resets, not `:host`.
- Skip-link CSS already defined (`.skip-link` / `.skip-link:focus`) — you only need to render
  the anchor tag, not restyle it, unless you have a specific reason to.
- Heading copy-link behavior (click a heading to copy an anchor link) — automatic once
  headings render inside the slot.
- The base `render()` is just the contentcontainer/slot wrapper — **always override render()**
  in a real theme, but preserve the exact structure:
  ```html
  <div id="contentcontainer"><div id="slot"><slot></slot></div></div>
  ```
  This exact id nesting is required for the HAX editor to attach correctly. Never rename these
  ids or drop a level.
- Default `#slot` min-heights and edit-mode hide-on-edit CSS already baked in via `styles()` —
  call `super.styles` in your `static get styles()` array.

## Mixins (compose around the base, never replace it)

- **`utils/HAXCMSThemeParts.js`** → `HAXCMSThemeParts(SuperClass)`. Adds `editMode`/`darkMode`
  reactive props reflecting MobX store state, plus `[part="edit-mode-active"]` dimming/blur
  CSS. Use `:host([dark-mode])` for dark-mode-specific overrides once this mixin is applied.
- **`core/utils/HAXCMSMobileMenu.js`** → `HAXCMSMobileMenuMixin(SuperClass)`. Adds
  `menuOpen`/`isFlex`/`isHorizontal`, persists menu-open state to localStorage, auto-closes on
  mobile navigation. Exposes `HAXCMSMobileMenuButton(position)` (a `simple-icon-button-lite`
  toggle), `HAXCMSMobileMenu()` (fixed/stacked nav wrapping `<site-menu>` via `<replace-tag>`),
  and `HAXCMSFlexMenu(maxDepth)` (flex/horizontal variant). Prefer these helpers over a raw
  `<site-menu>` when you want built-in mobile collapse behavior; for a genuinely fixed
  always-visible left column (e.g. a notched/chamfer layout with a persistent left nav), a
  direct `<site-menu>` is fine — just make sure it collapses/hides at your mobile breakpoint.
- **DDD** → `import { DDDSuper } from "@haxtheweb/d-d-d/d-d-d.js"` and wrap:
  `class MyTheme extends DDDSuper(HAXCMSLitElementTheme) {}`, or with other mixins:
  `HAXCMSThemeParts(HAXCMSMobileMenuMixin(DDDSuper(HAXCMSLitElementTheme)))`. DDD must be the
  innermost wrap around the HAXCMS base, matching `polaris-theme.js`'s composition order:
  `HAXCMSOperationButtons(PDFPageMixin(PrintBranchMixin(QRCodeMixin(HAXCMSThemeParts(HAXCMSMobileMenuMixin(DDDSuper(HAXCMSLitElementTheme)))))))`.
  Only add `PrintBranchMixin`/`PDFPageMixin`/`QRCodeMixin`/`HAXCMSOperationButtons` if the
  screenshot/user actually calls for print/PDF/QR/operation-button affordances — don't cargo
  cult the full Polaris stack for a simple theme.

## Navigation & layout components (import as side-effect, then use the tag)

- **`ui-components/navigation/site-menu.js`** (`<site-menu>`) — wraps `<map-menu>`, reactive to
  `store.routerManifest`/`store.activeId`. Attributes: `is-flex`, `is-horizontal`, `max-depth`.
  Use directly for a persistent sidebar/left-column nav.
- **`ui-components/navigation/site-menu-button.js`** (`<site-menu-button type="prev|next">`) —
  forward/back pager button, wired to `store.activeRouterManifestIndex`/`routerManifest`.
- **`ui-components/navigation/site-breadcrumb.js`** (`<site-breadcrumb>`) — renders
  `store`-driven breadcrumb trail; extends DDD directly, ships its own DDD-token styles.
- **`ui-components/layout/site-region.js`** (`<site-region name="...">`) — fetches HTML for
  content item IDs assigned to that named region (`store.regionData[name]`) and injects it
  into light DOM with `part="site-region-wrapper-<name>"`. Empty until content is assigned in
  the running site — that's expected, not a bug. Common region names seen in shipped themes:
  `header`, `footerSecondary`, `footerPrimary` (see `polaris-theme.js`); pick names that match
  the layout's actual sections (e.g. `banner`, `belowMenu`, `contentTop`).
- **`ui-components/active-item/site-active-title.js`** (`<site-active-title>`) — renders the
  active page's `<h1>` title.
- **`ui-components/active-item/site-active-media-banner.js`**
  (`<site-active-media-banner>`) — reads `store.activeItem.metadata.image` (per-page banner,
  not site-wide) and renders an image/video/gif banner with the page title overlaid for gifs.
- **`ui-components/site/site-title.js`** (`<site-title>`) — site-wide title from manifest.

## Site-wide vs. per-page banner image — the two real patterns

- **Site-wide (from `site.json` `metadata.theme.variables`)** — pattern used by
  `polaris-theme.js`: autorun on `store.themeData.variables`, assign `this.image`/`imageAlt`/
  `imageLink`, render a plain `<img src="${this.image}" alt="${this.imageAlt}">` linked via
  `imageLink`. Use when the screenshot shows one consistent banner image across every page.
- **Per-page (from each page's own `metadata.image`)** — use
  `<site-active-media-banner>` directly; it already reads `store.activeItem.metadata.image`
  internally. Use when the screenshot/description implies the banner changes per page (the
  Chamfer brief said "banner image should come from the site manifest" — confirm with the user
  whether they mean site-wide `metadata.theme.variables.image` or per-page
  `metadata.image`; don't assume).

## Author details

`journey-theme.js` pattern: autorun on `store.manifest`, read
`this.manifest.metadata.author` (name/image/email/etc.) once available. Guard every access
(`this.manifest && this.manifest.metadata && this.manifest.metadata.author`) since it may be
empty `{}` on a fresh site.

## DDD palette pattern (`dataPalette`)

`d-d-d/lib/DDDPaletteRegistry.js` exports `DDDPaletteRegistry` (16 named palettes, numbered
`0`-`15`, e.g. `wisdom-walk-green` = 0, `very-violent-red` = 1, `boldly-lion` = 11) and helpers
`getDDDPaletteOptionByValue`/`getDDDPaletteAttributeValue`/`getDDDPaletteKey`. Shipped pattern
(`journey-theme.js`):
```js
import { UserScaffoldInstance } from "@haxtheweb/user-scaffold/user-scaffold.js";
// constructor:
const stored = UserScaffoldInstance.readMemory("HAXCMSSitePalette");
this.dataPalette = stored === "" || stored === null ? 11 : stored;
// updated():
if (changedProperties.has("dataPalette")) {
  UserScaffoldInstance.writeMemory("HAXCMSSitePalette", this.dataPalette, "long");
}
// properties: dataPalette: { type: Number, reflect: true, attribute: "data-palette" }
// styles: --ddd-palette-1: var(--ddd-palette-color-1, default); (map raw palette-color-N
// tokens to semantic --ddd-palette-N custom props scoped to :host, so palette swaps are one
// property update, not a full re-render)
```
Use `DDDVariables, DDDPaletteStyles` from `@haxtheweb/d-d-d/lib/DDDStyles.js` in
`static get styles()` (spread before `super.styles`) if you want the raw `--ddd-palette-color-N`
custom properties available at all.

## Manifest / JSON Outline Schema metadata paths

From `json-outline-schema/example.json` and shipped theme usage:
- `metadata.site.name` — must equal the site's folder name. Never touch.
- `metadata.theme.element` / `.path` / `.name` / `.variables.{hexCode,cssVariable,icon,image,
  imageAlt,imageLink}` — theme registration + site-wide banner/palette variables, read via
  `store.themeData`.
- `metadata.author` — `{name, image, email, phone, location, website, ...}`, read via
  `store.manifest.metadata.author`.
- Per-item `metadata.image` — per-page banner, read via `store.activeItem.metadata.image`.

## `theme-discovery.js` JSDoc tags (monorepo target only)

`webcomponents/scripts/theme-discovery.js` regex-parses each theme source file (only run via
`yarn run theme-discovery`/ubiquity — you never run this yourself, it runs on the ecosystem
build). Still, write these tags correctly so the theme is categorized right once discovered:
- `@title <Display Name>` — shown in the theme picker.
- `@element <tag-name>` — fallback if `static get tag()` isn't matched (write both regardless).
- `@haxcms-theme-category <comma, separated>` — defaults to `Website` if omitted. Never emit
  `Blank`, `Personal`, or `Module` (banned tags, silently filtered).
- `@haxcms-theme-priority <number>` — sort weight, default `0`. Negative numbers sort earlier
  (`journey-theme.js` uses `-1`).
- `@haxcms-theme-palettes <comma-separated palette numbers>` — which DDD palette numbers this
  theme supports, if any.
- `@haxcms-theme-hidden` / `@haxcms-theme-internal` (boolean, bare tag or `true`/`false`) —
  keeps the theme in `themes.json` but out of the user-facing picker (used for system/dev
  themes like `haxcms-blank-theme`).
- Thumbnails are auto-generated later by a separate Puppeteer automation step
  (`theme-<element>-thumb.jpg`) — do not attempt to produce one yourself.

## Monorepo package conventions

Model on `elements/example-haxcms-theme/`:
- `package.json`: `name: "@haxtheweb/<name>"`, `type: "module"`, `main`/`module` point at the
  theme's own `.js` file, `customElements: "custom-elements.json"`, `hax: { cli: true }`.
  Scripts: `build: "npm run analyze"`, `analyze: "cem analyze --litelement --exclude public"`,
  `dddaudit: "hax audit"`, `test: "web-test-runner test/**/*.test.js --coverage --node-resolve"`.
  Dependencies: `@haxtheweb/d-d-d`, `@haxtheweb/haxcms-elements`, `lit`, `mobx` (pin to the
  monorepo's current versions — check a sibling package.json rather than guessing).
- `demo/index.html`: imports `@haxtheweb/deduping-fix/deduping-fix.js` and
  `@haxtheweb/demo-snippet/demo-snippet.js`, wraps a `<demo-snippet><template>` around a sample
  usage of the tag. No inline styles.
- `rollup.config.js`: copy verbatim from a sibling theme package (standard open-wc rollup
  config, no per-theme customization needed).
- `test/<name>.test.js`: minimal `@open-wc/testing` fixture + accessibility assertion
  (`expect(element).shadowDom.to.be.accessible()`), modeled on
  `example-haxcms-theme/test/example-haxcms-theme.test.js`.

## Custom-theme-on-a-site CLI mechanics (for reference, not to hand-replicate)

`create/src/lib/programs/site.js`'s `customSiteTheme()` (invoked by
`hax site --custom-theme-name ...` / interactively via `hax site` → `site:theme` →
`custom-theme`):
1. Normalizes the name to `custom-<name>-theme`.
2. Copies one of `create/src/templates/sitetheme/{base-theme.js,flex-theme.js,sidebar-theme.js}`
   into `<site>/custom/src/<name>.js` and EJS-renders `className`/`customThemeName`/`year`/
   `author`.
3. Appends `import "./<name>.js";` to `custom/src/custom.js`.
4. Sets `manifest.metadata.theme = {element, path: "./custom/build/custom.es6.js", name}` in
   `site.json` and saves.
5. Runs `npm install && npm run build && npm run analyze` inside `<site>/custom/`.

`base-theme.js` is a **bespoke** template (extends `HAXCMSLitElementTheme` directly, minimal
pager nav). `flex-theme.js`/`sidebar-theme.js` both extend `PolarisFlexTheme` from
`@haxtheweb/polaris-theme/lib/polaris-flex-theme.js` and override slot-render methods to blank
out unwanted default sections — use these two only when the chosen base strategy is "extend
PolarisFlexTheme".
