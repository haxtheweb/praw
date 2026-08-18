---
name: hax-theme-builder
description: >
  Turn a screenshot (plus a short Q&A loop) into a real HAXcms theme that extends
  HAXCMSLitElementTheme correctly — accessible, dark-mode-compliant, responsive, with a
  skip-link, site-menu/site-menu-button/site-breadcrumb wiring, and named regions. Use when
  the user says "make a theme from this screenshot", "build a HAXcms theme", "run the hax
  theme skill", "theme skill", "remake <name> using the theme skill", or attaches an image
  of a site layout and asks for a matching theme — even if they don't say "skill". Offers to
  add the result either as a custom theme on an existing HAXsite or as a new bundled theme
  package in the webcomponents monorepo (haxtheweb/issues#2963, haxtheweb/issues#2962).
version: 1.0.0
license: Apache-2.0
metadata:
  author: haxtheweb
  tags: [hax, haxcms, theme, screenshot, ddd, accessibility, dark-mode, site-menu, regions, monorepo, custom-theme]
---

# HAXcms Theme Builder

Analyze a screenshot of a site layout, ask only what can't be inferred, then generate a real
HAXcms theme built on `HAXCMSLitElementTheme` — accessible, dark-mode compliant, responsive,
and wired into the site-menu/breadcrumb/region ecosystem instead of reinventing plumbing.
Trigger: **"make a theme from this screenshot"** / **"run the hax theme skill"** (see
haxtheweb/issues#2963).

## Inputs

- **A screenshot** (image path) of the target layout — required. Read it with a
  vision-capable file read, not OCR/CV; the analysis in step 2 is done by looking at it.
- **Theme name** (optional) — if omitted, ask. Must resolve to a valid tag name
  (`<name>-theme` for a monorepo package, `custom-<name>-theme` for a site custom theme).
- **Description** (optional) — one sentence for `package.json`/`@title` JSDoc; ask if omitted.
- **Target site** (optional) — an existing HAXsite directory, needed only for the custom-theme
  path. Not needed for the monorepo path.

## Prerequisites

- `hax` CLI (local copy — never `npx`). Always pass `--y --no-i --auto --skip --quiet` when
  scripting so no prompts or sub-processes launch.
- Working from `~/Documents/git/haxtheweb/`. The monorepo path scaffolds under
  `webcomponents/elements/`; the custom-theme path scaffolds under `<site>/custom/src/`.
- Read `references/haxcms-theme-architecture.md` before writing the theme component — it is
  the cheat sheet for the base class, mixins, region components, palette registry, and the
  JSDoc tags theme-discovery.js parses. Do not guess these from memory.

## Modes

- **Monorepo (bundled theme)** — a new bundled theme package the whole ecosystem ships,
  discoverable via `webcomponents/scripts/theme-discovery.js`. Default when the user does not
  name an existing site, or explicitly says "bundle this" / "add it to the monorepo" / "make
  it a real theme option".
- **Custom site theme** — a one-off theme added to a single HAXsite's `custom/` folder.
  Default when the user names/points at an existing HAXsite, or says "just for this site" /
  "custom theme".
- If genuinely ambiguous, ask as part of the Q&A loop (step 3) rather than guessing silently
  — this choice determines the whole scaffold path.

## Execution style

Do the screenshot analysis and Q&A up front, confirm the plan once, then run the rest of the
workflow straight through with minimal narration. Report once at the end: what was built,
where, and the build/audit results.

## Workflow

1. **Read the screenshot.** Load it as an image (vision), not as a file to grep. Identify:
   header/banner presence and whether it looks like a manifest-driven image vs. solid color,
   nav position (top bar vs. left column vs. sidebar) and whether it looks collapsible/mobile,
   content area shape and any distinctive geometry (e.g. a corner notch/chamfer, rounded
   panels, a hard border), fixed-width vs. fluid container, footer structure (single band vs.
   primary/secondary bands), any visible palette/accent colors, and typography weight/scale
   cues. Note explicitly that font/color inconsistencies in a screenshot may be incidental —
   don't over-fit to exact pixel colors unless the user says the palette matters.
2. **Ask only what the screenshot can't answer.** Use `ask_user_question`-style questions (or
   inline questions if not available) for, at minimum, whatever of these remain undetermined
   after step 1 and aren't already given in the request:
   - Theme name + one-line description.
   - Target: monorepo bundled theme vs. custom theme on an existing site (see Modes). If
     custom, get the site directory.
   - Base strategy: bespoke (extend `HAXCMSLitElementTheme` directly — right choice for a
     genuinely novel layout like a notched/chamfered panel) vs. extend `PolarisFlexTheme`
     (right choice when the screenshot is essentially a flex/sidebar variant).
   - Palette support: none, DDD `--ddd-palette-color-N` (see
     `references/haxcms-theme-architecture.md` for the registry and `dataPalette` pattern), or
     another explicit system. If DDD palette, ask where it applies (host background, header
     band, accents/borders).
   - Site-manifest-driven data: should the banner image come from
     `metadata.theme.variables.image/imageAlt/imageLink` (site-wide, like `polaris-theme.js`)
     or from `metadata.image` on the active page (per-page, via
     `site-active-media-banner`)? Should author details render from `metadata.author` (like
     `journey-theme.js`)?
   - Regions: confirm which named `site-region` slots are needed (e.g. banner, content-top,
     below-menu, footer-primary, footer-secondary) based on what step 1 saw plus any the user
     mentions explicitly.
   - Any additional structural components to engineer (per issue #2963: "any additional
     components to engineer from it").
   Do not ask about things the screenshot already makes obvious (e.g. don't ask "is there a
   header" if there clearly is one) — only ask for the gaps.
3. **Confirm the plan in one short summary** (name, target, base strategy, palette, regions)
   before scaffolding. If the user skips/doesn't respond, proceed with the most reasonable
   defaults implied by the screenshot and state the assumption in the final report.
4. **Scaffold**, per the chosen target:
   - **Monorepo:** run
     `hax webcomponent <name>-theme --template monorepo --y --no-i --org haxtheweb --author "<author>"`
     from `webcomponents/elements/`. This generates a standard Lit component scaffold (NOT a
     theme) — you must hand-adapt it in step 5, per rule E9Zioqke3Y0gdnWB08XQn8 (always
     scaffold via the CLI, never create files manually; adapting the generated file afterward
     is expected and is not the same as manual creation).
   - **Custom site theme:** run
     `hax site --custom-theme-name <name> --custom-theme-template base --y --no-i --auto --skip --quiet`
     from the target site directory (use `polaris-flex`/`polaris-sidebar` templates instead of
     `base` only if the user chose the extend-PolarisFlexTheme strategy in step 2). This
     scaffolds `custom/src/<name>.js`, appends the import to `custom/src/custom.js`, and sets
     `manifest.metadata.theme` in `site.json` automatically — do not hand-edit `site.json` for
     this.
5. **Write the theme component**, replacing the generated placeholder body. Consult
   `references/haxcms-theme-architecture.md` for exact import paths and patterns. Required
   elements regardless of target:
   - Extends `HAXCMSLitElementTheme` (directly, or via `PolarisFlexTheme` per the chosen
     strategy). If mixins are used, `HAXCMSLitElementTheme` (or `DDDSuper(...)`) must be the
     innermost/base class — mixins wrap it, they don't replace it.
   - `static get tag()` returning the theme's element name; `globalThis.customElements.define`.
   - A JSDoc block above the class with `@title <Display Name>`, `@element <tag-name>`, and
     (monorepo target only) `@haxcms-theme-category`, `@haxcms-theme-priority`, and
     `@haxcms-theme-palettes` if applicable — these feed `theme-discovery.js`.
   - A skip-link as the first thing in `render()`: `<a class="skip-link" href="#contentcontainer">Skip to content</a>`.
   - The content contract HAX requires: an element with `id="contentcontainer"` wrapping
     `id="slot"` wrapping `<slot></slot>` (see any reference theme).
   - `site-menu` (via `HAXCMSMobileMenuMixin`'s `HAXCMSMobileMenu()`/`HAXCMSFlexMenu()` helper,
     or a direct `<site-menu>` for a fixed left column) for navigation, `site-menu-button` for
     forward/back where the screenshot shows pager controls, `site-breadcrumb` if the layout
     has room for one.
   - `site-region` elements for every region confirmed in step 2/3 (e.g.
     `<site-region name="banner">`, `<site-region name="belowMenu">`,
     `<site-region name="footerPrimary">`).
   - DDD tokens exclusively for spacing/color/typography/icon-sizing (`--ddd-spacing-*`,
     `--ddd-font-*`, `--ddd-radius-*`, `--ddd-theme-default-*`) — no hardcoded hex unless
     wrapped in a fallback per `light-dark()`. Dark mode via `light-dark()` pairs and/or
     `:host([dark-mode])` (from `HAXCMSThemeParts`).
   - Responsive `@media` breakpoints so the layout collapses sensibly on mobile (matching the
     `900px`/`800px` conventions used in sibling themes) — a fixed-width layout still needs a
     narrow-viewport fallback.
   - Any bespoke geometry called out in the screenshot (e.g. a corner notch/chamfer): implement
     with `clip-path` or a pseudo-element on the content container, using DDD radius/spacing
     tokens for the cut dimensions rather than magic numbers where reasonable.
   - `globalThis`, not `window`; no optional chaining (`?.`); single quotes/no semicolons where
     practical, matching repo JS style.
6. **Monorepo target only — package metadata.** Model `package.json` on
   `elements/example-haxcms-theme/package.json`: `name: "@haxtheweb/<name>-theme"`,
   dependencies on `@haxtheweb/d-d-d`, `@haxtheweb/haxcms-elements`, `lit`, `mobx`; scripts
   `build: "npm run analyze"`, `analyze: "cem analyze --litelement --exclude public"`,
   `dddaudit: "hax audit"`; `hax: { cli: true }`; `customElements: "custom-elements.json"`. Add
   a `demo/index.html` (no inline styles per rule UFDnZ9G3sRwCDltjckOT13 — use classes/tokens).
7. **Build and audit.**
   - Monorepo target: from the new package directory, run `npm install` then
     `npm run build` (never the monorepo-wide `yarn run build`/ubiquity script — those are
     forbidden). Then run `hax audit` for DDD compliance.
   - Custom-theme target: the `hax site --custom-theme-name` command already ran
     `npm install && npm run build && npm run analyze` inside `<site>/custom/` — just confirm
     it succeeded; re-run only on failure. Run `hax audit` from the site root afterward.
   - Fix any audit findings (missing tokens, contrast, dark-mode gaps) before reporting done.
8. **Report back once**, concisely: theme name/tag, target (monorepo path or site path), base
   strategy used, palette/region decisions, build + audit result, and the exact file path(s)
   to review. Invite feedback — this skill is expected to be iterated on a11y/design accuracy.

## Command reference

- Monorepo scaffold: `hax webcomponent <name>-theme --template monorepo --y --no-i --org haxtheweb --author "<author>"`
- Custom-theme scaffold: `hax site --custom-theme-name <name> --custom-theme-template <base|polaris-flex|polaris-sidebar> --y --no-i --auto --skip --quiet`
- Monorepo build/audit: `cd elements/<name>-theme && npm install && npm run build && hax audit`
- Custom-theme audit: `cd <site> && hax audit`

## Guardrails (ecosystem rules)

- Always scaffold via the `hax` CLI (`hax webcomponent` / `hax site --custom-theme-name`) —
  never hand-create the package/theme files from scratch. Hand-adapting the generated
  placeholder file's contents afterward is expected and required (steps 5-6).
- Use the local `hax` command, never `npx`.
- Always pass `--y --no-i --auto --skip --quiet` when scripting `hax`.
- Never run the top-level monorepo build or the ubiquity script. Component-local
  `npm run build` (which just runs `cem analyze`) is fine and expected.
- Never hand-edit `custom-elements.json` or `site.json` for theme registration — the CLI
  writes both.
- Use `globalThis`, not `window`. Avoid optional chaining (`?.`).
- Prefer `simple-icon-button-lite` for icon buttons; use DDD design tokens for all
  spacing/color/typography/icon-sizing; check dark-mode compliance explicitly (this is a
  standing audit expectation for any HAX component work, not unique to this skill).
- Avoid inline styles in any `demo/index.html`.
- `metadata.site.name` in any site.json must stay equal to the site's folder name — do not
  touch it even indirectly.

## Gotchas

- `hax webcomponent` scaffolds a generic Lit component (`DDDSuper(I18NMixin(LitElement))`),
  not a theme — there's no separate "theme" template. You must replace the base class and
  render body per step 5; that's expected, not a workaround.
- Themes are discovered by regex over the source file (`theme-discovery.js` looks for
  `static get tag()`, `customElements.define`, and specific `@`-prefixed JSDoc tags) — the
  JSDoc tags in step 5 aren't decorative, they are what makes a bundled theme show up
  correctly categorized in the theme picker.
- `site-region` fetches rendered HTML for content IDs assigned to that named region via the
  site's region editor — it renders nothing until the user assigns content to that region in
  the running site. Empty regions in a fresh theme are expected, not a bug.
- A "fixed-width" layout still needs a mobile fallback — don't skip the responsive breakpoint
  just because the screenshot shows a wide desktop capture.
- Screenshot font/color inconsistencies may be incidental capture artifacts — confirm with the
  user in the Q&A step before treating every screenshot color as a hard requirement.

## References

- `references/haxcms-theme-architecture.md` — cheat sheet: `HAXCMSLitElementTheme` base class
  contract (contentcontainer/slot, skip-link CSS already built in, `HAXCMSGlobalStyleSheetContent()`),
  mixins (`HAXCMSThemeParts`, `HAXCMSMobileMenuMixin`, DDD via `DDDSuper`), navigation/region
  components (`site-menu`, `site-menu-button`, `site-breadcrumb`, `site-region`,
  `site-active-media-banner`), the DDD palette registry + `dataPalette` persistence pattern,
  manifest metadata paths (`metadata.theme.variables`, `metadata.author`), the
  `theme-discovery.js` JSDoc tags, and monorepo `package.json` conventions.
