# Planned systems

Licenses checked from npm on 2026-11-11; re-check from the packed `package.json` at ingest time.

| System | Theme package | Token source (npm) | License | Fonts | Shell to follow | Notes |
|---|---|---|---|---|---|---|
| PatternFly 6 | `patternfly-theme` (done) | `@patternfly/patternfly` → `base/patternfly-variables.css` | MIT | Red Hat Text / Display / Mono (OFL) | Page: masthead, sidebar nav, inset main container | Reference implementation |
| Adobe Spectrum | `spectrum-theme` | `@adobe/spectrum-tokens` or `@spectrum-css/tokens` | Apache-2.0 | Source Sans 3 (OFL) | Spectrum app frame: top bar + side nav | Adobe Clean is proprietary: never ship it |
| IBM Carbon | `carbon-theme` | `@carbon/themes` / `@carbon/styles` (theme classes white, g10, g90, g100) | Apache-2.0 | IBM Plex Sans / Serif / Mono (OFL) | UI Shell: header + side nav | Light = white or g10, dark = g100 |
| Material Design 3 | `material-theme` | `@material/web` tokens (`--md-sys-*`), color from `@material/material-color-utilities` | Apache-2.0 | Roboto / Roboto Flex (OFL) | Top app bar + navigation drawer/rail | Material 3, not MUI's Material 2 look |
| Tailwind | `tailwind-theme` | `tailwindcss` default theme (`theme.css` `--color-*`, `--spacing`, `--radius-*`) | MIT | Inter (OFL) or system stack | Neutral docs layout | Open-source values only (no Tailwind Plus/UI); no utility classes in authored content |
| shadcn/ui | `shadcn-theme` | `shadcn` registry base colors (`--background`, `--foreground`, `--primary`, `--radius`, ...) | MIT | Geist / Inter (OFL) | Sidebar + inset layout | Shares the Tailwind palette: layer on `tailwind-theme`'s tokens |
