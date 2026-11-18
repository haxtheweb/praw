# Homage themes from static site generator themes

How to turn a well known Hugo, Jekyll, Astro or Docusaurus theme into a HAXcms theme that pays
homage to it. Written from building the first seventeen
(https://github.com/haxtheweb/issues/issues/3365,
https://github.com/haxtheweb/webcomponents/pull/1468). Paths are in
https://github.com/haxtheweb/webcomponents unless noted.

An homage is an ordinary HAXcms theme whose layout a reader of the original would recognize. It
is not a port: nothing from the original ships.

## 1. License gate (before any code)

Read the original's repository, not a list that summarizes it. Record what you find in the
tracking issue.

| Check | Where | What it decides |
|---|---|---|
| Code license | `LICENSE` at the pinned commit | MIT, Apache-2.0, BSD are fine to honor. Anything else: stop and ask. |
| Extra clauses | file headers, README "License" section | "Attribution required", "powered by" footers, paid keys: treat that code as not permissive. |
| Trademark | README, `TRADEMARK*`, Apache-2.0 section 6, who owns the project | A company or project brand name does not come with the license. |
| Bundled assets | fonts, icon sets, vendored JS, each with its own license | None of these ship anyway; note them so nobody copies them later. |
| Demo content | photos, sample posts, docs (often CC BY) | Never reused. |

Then sort the theme into one of three:

- **Named homage**: permissive code license and no trademark claim. The HAX theme may carry the
  name (`papermod-theme`) with a credit.
- **Neutral name**: permissive code, but the name is a company's or project's brand (a
  documentation theme owned by a large project, for example). Name the HAX theme for what it is
  (`handbook-theme`), and say which layout it honors only in the description, source comment
  and `NOTICE`.
- **Concept only**: trademark stated, attribution-required code, or paid features. Take the
  idea of the layout and nothing else; no named theme.

This is a read of the files, not legal advice. When in doubt, pick the more careful category
and tell the user why.

## 2. Rules every homage follows

- No upstream code, CSS, templates, fonts, icons, logos, mascots or demo content.
- A layout over the theme parts HAXcms ships, styled with DDD tokens only. It adds no design
  system: it sits on the theme side of the theme / design system split.
- Because the chrome reads only `--ddd-*` tokens, the theme says so:
  `static get acceptsDesignSystems() { return true; }` (the family bases below already do).
- Credit in three places: the class JSDoc, the package `README.md`, and `NOTICE` (name,
  generator, license, repository URL, the copyright line from the original's `LICENSE`, and a
  sentence that nothing of it is used and there is no affiliation).

## 3. Pick a family, then write a variant

Most themes are one of three layouts. Extend the family base and set tokens; write a new base
only when none fits.

| Family | Looks like | Extend | Lives in |
|---|---|---|---|
| Docs | site menu, page, on this page | `BookTheme` (`@haxtheweb/book-theme/book-theme.js`) | `elements/book-theme/lib/<tag>.js` |
| Single column | header with top level pages, one centered column | `HomageColumnTheme` (`@haxtheweb/papermod-theme/lib/HomageColumnTheme.js`) | `elements/papermod-theme/lib/<tag>.js` |
| Sidebar | fixed identity column with the site menu, page beside it | `HomageSidebarTheme` (`@haxtheweb/papermod-theme/lib/HomageSidebarTheme.js`) | `elements/papermod-theme/lib/<tag>.js` |

What a variant sets:

| Family | Constructor options | Custom properties |
|---|---|---|
| Docs | `bookLayout = "topbar"` (header on every size, tools in it), `tocFold = true` (on this page stays in its button) | `--book-theme-menu-width`, `--book-theme-toc-width`, `--book-theme-container-width`, `--book-theme-header-height`, `--book-theme-link`, `--book-theme-rule`, `--book-theme-surface`, `--book-theme-menu-surface`, `--book-theme-header-surface`, `--book-theme-header-color` |
| Single column | `headerLayout = "split" \| "stack"`, `stickyHeader`, `listVariant`, `darkModeSwitch` | `--homage-column-width`, `--homage-header-bg`, `--homage-header-text`, plus the shared ones |
| Sidebar | `withToc`, `masthead`, `listVariant`, `darkModeSwitch` | `--homage-sidebar-width`, `--homage-sidebar-bg`, `--homage-sidebar-text`, `--homage-sidebar-accent`, `--homage-column-width`, `--homage-toc-width`, plus the shared ones |

Shared by the single column and sidebar families: `--homage-text`, `--homage-bg`,
`--homage-surface`, `--homage-accent`, `--homage-muted`, `--homage-rule`,
`--homage-font-body`, `--homage-font-heading`, `--homage-radius`.

`listVariant` is how `homage-page-list` draws the pages under the active page (the post index):
`cards`, `rows`, `plain`, `compact` or `grid`.

A variant is short: imports the base, a JSDoc block, `static get tag()`, a constructor that sets
options, and `static get styles()` returning `[super.styles, css\`...\`]`. Copy the nearest
existing one.

Give the variant its character with DDD's named colors and fonts (`--ddd-theme-default-*`,
`--ddd-font-mono`), always as `light-dark(<light>, <dark>)` pairs. A theme that is dark by
design sets `color-scheme: dark` on `:host` and `darkModeSwitch = false`.

## 4. Things that are easy to get wrong

- **Discovery needs the base class name in the file.** `scripts/theme-discovery.mjs` treats a
  file as a theme when its text contains `HAXCMSLitElementTheme`. A variant that only imports a
  family base must still say it in its JSDoc ("A HAXCMSLitElementTheme built on ...").
- **The scaffold starts a dev server.** `hax webcomponent <name> --y --no-i` does not exit;
  stop it once the files exist. Then delete what a theme does not have: `.vscode/`,
  `lib/<tag>.haxProperties.json`, and every non-English file in `locales/`.
- **Sticky parts sit under the top bar.** Logged in, the HAXcms bar is fixed over the page:
  offset `top` by `calc(64px + var(--haxcms-top-offset, 0px))` under `:host([is-logged-in])`.
- **Edit mode needs room for the tray.** `:host([edit-mode]) { margin: var(--hax-tray-element-align-margin, ...) }`
  with the collapsed-tray and small-screen resets, as `polaris-flex-theme` does. Without it,
  content slides under the tray on any window narrower than the layout.
- **Body text size is DDD's.** The reading size is a locked structure token; a theme does not
  shrink it to match the original.
- **No bare text in the theme's own shadow root without a site.** The theme fades in; an axe
  run in a test fixture sees half-faded text as a contrast failure. Render dates and similar
  only when there is a value ("Last updated" with no date is wrong anyway).
- **Dark mode gate.** Anything that sets a color of its own must change under dark mode: use
  `light-dark()` tokens, including on `option` elements inside a `select`.
- **Reserved content height.** A page that only introduces a list should not hold the default
  minimum height: set `--haxcms-theme-content-min-height: 0px` (and `-mobile`) for that state.

## 5. Register and picture it

1. `yarn theme-discovery` writes `elements/haxcms-elements/lib/themes.json`; run Prettier on
   the file so only the new entry differs. Check no base class was registered as a theme.
2. Add one line for the tag to the three registries that are regenerated at release
   (`wc-registry.json`, `elements/haxcms-elements/demo/wc-registry.json`,
   `elements/replace-tag/demo/wc-registry.json`), so the editor demo can load the theme with
   `?theme=<tag>` on a preview before then.
3. Screenshots in `elements/haxcms-elements/lib/theme-screenshots/`: `theme-<tag>.jpg`
   (1440x900 of the editor demo with `?theme=<tag>`, published view, light) and
   `theme-<tag>-thumb.jpg` (145x204, a 640x900 crop that shows the layout's character).

## 6. Demo

- The lead theme of a package uses `demo/index.html` + `demo/site.json`. Every other theme gets
  its own folder: `demo/<tag>/index.html` and `demo/<tag>/site.json`. A second `.html` file in
  `demo/` does not work: the HAXcms router reads any file name but `index.html` as a page slug.
- In a folder demo, anchor the page's `<base>` to `/demo/<tag>/`, point item `location`s at
  the shared pages one folder up (`../pages/...`), and add one `../` to the registry and
  deduping-fix paths.
- Import `@haxtheweb/wc-autoload/wc-autoload.js` in the demo page. A real site always carries
  the autoloader; a bare demo page only gets it by accident, and without it blocks in the
  content never upgrade.
- Model the demo on how the original presents itself (a blog for a blog theme, versioned docs
  for a docs theme), written from scratch with HAX blocks. No hotlinked media.
- Set the `@demo` JSDoc tag to the theme's own demo.

## 7. Tests and gates

One test file per package covers every tag in it: defined with its tag, the content contract
and skip link, anything the variant's options change, and the axe audit
(`ignoredRules: ["skip-link", "empty-heading"]`, both only true of a fixture with no site).
Then, from the monorepo root: `yarn precheck` (includes CodeQL), and the gates CI runs on
changed demos, which can be run locally:

```bash
node scripts/dark-motion-check.mjs --base origin/master
node scripts/without-hax-check.mjs --base origin/master
```

Look at every theme in the editor demo (`elements/haxcms-elements/demo/index.html?theme=<tag>`)
in light and dark, logged in and scrolled, in edit mode, and at phone width. The demo's strip
has a live theme, palette and design system switcher for this.

## 8. When the original is as much content as layout

Academic and landing page themes are recognizable by their pages, not their chrome. Pair the
theme with a skeleton (starter site):

- The same JSON file in both backends:
  https://github.com/haxtheweb/haxcms-nodejs `src/coreConfig/skeletons/` and
  https://github.com/haxtheweb/haxcms-php `system/coreConfig/skeletons/`, with the theme
  registered in each `coreConfig/themes.json` and a test in each (twins).
- Mirror it in the app-hax demo (`elements/app-hax/demo/skeletons/` and `skeletons.json`).
- No images (none are bundled with skeletons), h2s with the Headline style preset, sample
  content that says it is a sample.
- The skeleton only works once the theme's code is in the backend's build, so its pull
  requests wait on the webcomponents release. Say so in them.
- Use the skeleton's content as the theme's demo site so the two stay the same.

## 9. Versions (docs themes)

Docs themes carry `site-version-switcher`. A version is a top level page tagged `version`; the
pages under it are that version's docs; the first in the outline is the current one. The
switcher keeps the reader on the same page when the other version has one at the same path. A
versioned demo needs two version pages with at least one shared path and one page only the
newer version has.
