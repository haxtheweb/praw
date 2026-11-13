# Systems

Eight shipped as theme packages in `haxtheweb/webcomponents/elements/`. Use their
`design-system/bridge.json` files as working examples. Re-check licenses from the packed
`package.json` (or the pinned `licenseUrl`) at ingest time. The layout reference page for each
theme is in [demo-sites.md](demo-sites.md).

| System | Theme package | Token sources | License | Fonts | Shell | Notes |
|---|---|---|---|---|---|---|
| PatternFly 6 | `patternfly-theme` | `@patternfly/patternfly` `base/patternfly-variables.css` (css) | MIT | Red Hat Text / Display / Mono (OFL) | Page: masthead, sidebar nav, inset main container; demo is a cluster console dashboard | Reference implementation; density mapped to spacers |
| IBM Carbon | `carbon-theme` | `@carbon/styles` `css/styles.css` (`.cds--white` / `.cds--g100`), `@carbon/colors` and `@carbon/motion` DTCG `tokens/*.tokens.json` | Apache-2.0 | IBM Plex Sans / Mono (OFL) | UI Shell: light header + side nav (3px active accent bar), page header panel with lead text | Spacing vars only exist in a component scope; font stacks and weights only in `@carbon/type` JS |
| Adobe Spectrum | `spectrum-theme` | `@spectrum-css/tokens` `dist/css/index.css` (scopes `.spectrum`, `.spectrum--medium`, `.spectrum--light` / `--dark`) | Apache-2.0 | Source Sans 3 (OFL) | Docs layout: floating rounded nav panel, centered column, "On this page" list | Adobe Clean is proprietary: never ship it. Palette only exists per mode, so named colors use `fromMode: "light"` |
| Material Design 3 | `material-theme` | `@material/web` `tokens/versions/latest/sass/_md-*.scss` (scss-vars: ref-palette, sys-color light/dark, shape, motion, state, typeface) | Apache-2.0 | Roboto / Roboto Flex (OFL) | Navigation rail (page icons, pill indicator) + drawer, 28px rounded surface | Material 3, not MUI's Material 2 look |
| Tailwind | `tailwind-theme` | `tailwindcss` `theme.css` (scope `@theme default`, oklch) | MIT | system stack | Docs layout: eyebrow above the title, "On this page" list | Open-source values only (no Tailwind Plus/UI); no utility classes in authored content |
| shadcn/ui | `shadcn-theme` | `tailwindcss` `theme.css` + the `shadcn init` `globals.css` as a sha-pinned URL source | MIT | Geist (OFL) | Sidebar + inset layout | Shares the Tailwind palette; neutral brand |
| Web Awesome | `webawesome-theme` | `@awesome.me/webawesome` `dist/styles/color/palettes/default.css`, `color/variants/*.css`, `themes/default.css` (css; scopes `:where(:root)` / `.wa-dark` as selector-list members) | MIT (Pro themes, palettes and patterns are commercial: excluded) | system stacks (no web font) | Docs layout: two-row header with section links, sidebar, tag badges and lead under the title, "On this page" | Palettes are lightness-normalized, so every `data-primary` palette passes; its icons are Font Awesome, which can't ship, so HAX icons stay |
| U.S. Web Design System | `uswds-theme` | `@uswds/uswds` color maps `packages/uswds-core/src/styles/tokens/color/_*.scss` (scss-map); theme roles from `settings/_settings-color.scss` | CC0-1.0 (public domain U.S. government work; `SEE LICENSE IN LICENSE.md`) | Source Sans 3, Merriweather (OFL), Roboto Mono (Apache-2.0) | Basic header with primary nav, landing page on the first page, side navigation, footer bands | Never ship the official government banner, seals or identifier; no dark mode of its own |
