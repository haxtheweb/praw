# Theme layouts and demo sites

A bridged theme is judged by whether a site built on it reads like that design system's own
work. The block list matters less than the shape: the theme should take the layout of the
system's own documentation or reference pages, and the demo should be a believable site in
that system's voice, built only from HAX blocks.

## Pick a reference page

Before writing the theme, pick one public page from the system's own site as the layout
reference, and name it in the PR. Read it from the live page (a browser or the docs), not from
memory. Good references are pages that show the system's page shell with real content:

| System | Reference used | What the theme took from it |
|---|---|---|
| USWDS | Storybook "Landing page" template | Basic header, hero, full-bleed bands, centered column, return-to-top + footer bands |
| Carbon | carbondesignsystem.com docs pages | Light UI shell, side nav, page header panel with lead text, content on layer 01 |
| PatternFly | patternfly.org dashboard design guidelines | Masthead, sidebar, card dashboard in the inset main container |
| Spectrum | spectrum.adobe.com docs pages | Floating rounded nav panel, centered column, big title, "On this page" list |
| Material 3 | m3.material.io | Navigation rail with icon + label and pill indicator, drawer, 28px rounded surface |
| Tailwind | tailwindcss.com docs | Eyebrow above the title, "On this page" list, sticky sidebar |
| Web Awesome | webawesome.com component docs pages | Two-row header (site bar, section links), sidebar, tag badges and lead text under the title, "On this page" |
| shadcn/ui | ui.shadcn.com dashboard example | Sidebar + inset layout, stat cards, chart card |

For a new system, look for: a landing page or page template in its Storybook, its docs site, or
a dashboard example. Pick the one closest to how HAX sites are used (courses, docs, sites).

## Theme patterns that recur

All of these are in shipped themes; copy from the named one.

- **"On this page" list**: `<site-menu-content label="${this.t.onThisPage}">` in an `<aside>`,
  sticky, shown from 1280px, next to a content column with `flex: 1 1 auto; min-width: 0`
  (without `min-width: 0` long code lines widen the page). Import
  `site-menu-content.js` in the theme: the registry only autoloads tags found in page content,
  never pieces a theme renders in its own shadow DOM. (`tailwind-theme`, `spectrum-theme`)
- **Navigation rail / top links from the outline**: an autorun over `store.manifest` keeps the
  top-level items (no `parent`, not `hideInMenu`, published), and `store.ancestorItem` gives the
  current section. Set `aria-current="page"` on the active page and `"true"` on its section.
  Page icons come from `metadata.icon`. (`material-theme`, `uswds-theme`)
- **Landing page on the first page**: reflect a `landing` attribute when the active item is the
  first item; center the column and let `page-section` / `full-width-image` bleed with
  `margin-inline: calc(50% - 50vw)` and `overflow-x: clip` on `main`. DDD's light-DOM global
  styles beat `::slotted()` rules, so use selectors that win on their own, not `::slotted`.
  (`uswds-theme`)
- **Lead text under the title** from the active item's `description`. (`carbon-theme`)
- **Title font**: `font-family: var(--ddd-font-heading, var(--ddd-font-secondary))` so the
  bridge's heading face applies.
- **Images**: add `<theme-tag> img { max-width: 100%; height: auto; }` in
  `HAXCMSGlobalStyleSheetContent()`; DDD's `data-width` only applies from 600px, so a plain
  `<img>` overflows on phones otherwise.
- **Page icons in titles**: if the theme shows icons in a rail, hide
  `site-active-title .site-active-title-icon` so they don't repeat in the title.

## Write the demo as a site

Write the pages as a spec file and generate the demo with `scripts/build-demo.py` (it replaces
`demo/site.json` items and `demo/pages/`), so the demo can be regenerated after each fix. Give
the site a name and a subject that fit the system (a federal-style course commons for USWDS, a
design-guidance site for Spectrum, a cluster console for PatternFly, a course design kit for
Material). Six to nine pages, one or two levels deep.

Use a range of blocks the way that system's own pages would:

- Hero: `page-section` (USWDS-style bands, `data-primary="3" data-design-treatment="bg"` for a
  dark band) or a rounded `<img data-border-radius="lg" data-width="100">`.
- Cards: `ddd-card` always draws its image area, so give it a `src` (an SVG in `demo/files`);
  for text-only cards use a bordered div:
  `<div data-border="xs" data-border-radius="lg" data-primary="5">`.
- Layout: `grid-plate` (`1-1`, `1-2`, `1-1-1`, `1-1-1-1`); avoid four text columns on narrow
  content, they break words.
- Guidance: `ddd-steps-list`, `stop-note` (info / warning / success), `a11y-collapse-group`,
  `bullet-check-list` (`items` JSON, `storage-id`), `a11y-tabs` / `a11y-tab label="..."`.
- Data: `editable-table bordered striped` with a `<caption>`, `count-up`, `progress-donut`,
  `code-sample` with `<template preserve-content="preserve-content">`.
- Actions: `simple-cta` (`data-primary="1"` filled, `data-primary="4"` dark).
- Answer states: `multiple-choice question="..."` with `<input data-correct="true" value="..."/>`.
- Palettes: swatches as `<div data-primary="N" data-design-treatment="bg" data-padding="m">`.
  Run `scripts/primary-contrast.py` first and leave out any palette it marks FAIL: those are
  bridge-level contrast gaps (haxtheweb/issues#3338), not something to hide in the demo
  without saying so in the PR.

Artwork in `demo/files` must be original (generated SVG shapes or gradients in the system's
palette). Never copy the system's own illustrations, photos, logos or icons.

## Check the demo

A brand-new theme package isn't linked into `node_modules/@haxtheweb/` until the workspace is
installed (`yarn install`, or link it by hand for a local check), and until then the theme module
fails to load and the page is empty. `check-demo.cjs` reports that as NOT RENDERED instead of
passing the empty page.

Start one dev server per theme from the monorepo root, then run `scripts/check-demo.cjs` over
every slug. It screenshots light and dark at 1280px and light at 390px, runs axe WCAG 2.1 A/AA,
reports horizontal overflow on phones, and counts blocks still "Loading...". Look at the
screenshots, not just the axe result: cramped cards, huge images and mid-word breaks pass axe.

Fix a finding in the element that causes it when the element is wrong (a11y-tabs ids, code-sample
keyboard scrolling and the replace-tag prefix bug were all found this way), and say so in the PR.
