# Systems

All six shipped as theme packages in `haxtheweb/webcomponents/elements/`. Use their
`design-system/bridge.json` files as working examples. Re-check licenses from the packed
`package.json` (or the pinned `licenseUrl`) at ingest time.

| System | Theme package | Token sources | License | Fonts | Shell | Notes |
|---|---|---|---|---|---|---|
| PatternFly 6 | `patternfly-theme` | `@patternfly/patternfly` `base/patternfly-variables.css` (css) | MIT | Red Hat Text / Display / Mono (OFL) | Page: masthead, sidebar nav, inset main container | Reference implementation; density mapped to spacers |
| IBM Carbon | `carbon-theme` | `@carbon/styles` `css/styles.css` (`.cds--white` / `.cds--g100`), `@carbon/colors` and `@carbon/motion` DTCG `tokens/*.tokens.json` | Apache-2.0 | IBM Plex Sans / Mono (OFL) | UI Shell: dark header + side nav (3px active accent bar) | Spacing vars only exist in a component scope; font stacks and weights only in `@carbon/type` JS |
| Adobe Spectrum | `spectrum-theme` | `@spectrum-css/tokens` `dist/css/index.css` (scopes `.spectrum`, `.spectrum--medium`, `.spectrum--light` / `--dark`) | Apache-2.0 | Source Sans 3 (OFL) | App frame: top bar + side nav | Adobe Clean is proprietary: never ship it. Palette only exists per mode, so named colors use `fromMode: "light"` |
| Material Design 3 | `material-theme` | `@material/web` `tokens/versions/latest/sass/_md-*.scss` (scss-vars: ref-palette, sys-color light/dark, shape, motion, state, typeface) | Apache-2.0 | Roboto / Roboto Flex (OFL) | Top app bar + navigation drawer | Material 3, not MUI's Material 2 look |
| Tailwind | `tailwind-theme` | `tailwindcss` `theme.css` (scope `@theme default`, oklch) | MIT | system stack | Neutral docs layout | Open-source values only (no Tailwind Plus/UI); no utility classes in authored content |
| shadcn/ui | `shadcn-theme` | `tailwindcss` `theme.css` + the `shadcn init` `globals.css` as a sha-pinned URL source | MIT | Geist (OFL) | Sidebar + inset layout | Shares the Tailwind palette; neutral brand |
