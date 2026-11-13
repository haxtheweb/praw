# `design-system/bridge.json`

Read by `elements/d-d-d/design-system/bridge/build-bridge.js`
(<https://github.com/haxtheweb/webcomponents/tree/master/elements/d-d-d/design-system/bridge>).
Working examples in `elements/`: `patternfly-theme` (one CSS source), `carbon-theme` (CSS plus
two DTCG sources), `spectrum-theme` (CSS scopes, `fromMode`), `tailwind-theme` (nested
`@theme`, oklch), `shadcn-theme` (Tailwind palette plus a sha-pinned URL source) and
`material-theme` (`scss-vars` with per-mode files) and `uswds-theme` (`scss-map` palette files,
CC0 with `SEE LICENSE IN`, literal Sass-computed values). `webawesome-theme` reads several CSS files from one package (palette, color variants, theme) with selector-list scopes. Every mapping is
checked against the shared tier contract in `contract.json` next to the generator.

```jsonc
{
  "system": "patternfly",          // design system name in DesignSystemManager; also <system>.ddd-map.json
  "title": "PatternFly",           // display name in generated headers
  "prefix": "Patternfly",          // export prefix: PatternflyTokens, PatternflyDDDMap, PatternflyFonts
  "homepage": "https://www.patternfly.org",
  "sources": [                     // one or more; later sources win on name clashes
    {
      "package": "@patternfly/patternfly",
      "version": "6.7.0",          // exact; fetched with npm pack, never added as a dependency
      "license": "MIT",            // must match the packed package.json, and be shippable
      "copyright": "Copyright (c) 2019 Red Hat, Inc.",
      "repository": "https://github.com/patternfly/patternfly",
      "format": "css",
      "file": "base/patternfly-variables.css",
      "scopes": {                  // selectors merged in order to resolve each mode
        "light": [":root"],
        "dark": [":root", ":root:where(.pf-v6-theme-dark)"]
      }
    }
    // a DTCG source (Carbon): { "package": "@carbon/colors", "version": "11.62.0",
    //   "license": "Apache-2.0", "format": "dtcg", "file": "tokens/colors.tokens.json",
    //   "prefix": "--carbon-" }  → blue.60 becomes --carbon-blue-60
    // a Sass source (Material): { "package": "@material/web", "version": "2.5.0",
    //   "license": "Apache-2.0", "format": "scss-vars", "prefix": "--md-sys-color-",
    //   "files": { "light": "tokens/versions/latest/sass/_md-sys-color.scss", "dark": "..." } }
    // a Sass map source (USWDS): { "package": "@uswds/uswds", "version": "3.14.0",
    //   "license": "CC0-1.0", "format": "scss-map", "prefix": "--usa-",
    //   "files": ["packages/uswds-core/src/styles/tokens/color/_blue.scss", "..."] }
    // a URL source (shadcn/ui, not on npm): { "url": "https://raw.githubusercontent.com/shadcn-ui/ui/<full sha>/.../globals.css",
    //   "sha256": "<hash of the file>", "licenseUrl": "https://raw.githubusercontent.com/shadcn-ui/ui/<same sha>/LICENSE.md",
    //   "package": "shadcn-ui/ui (label for the report)", "version": "<same sha>", "license": "MIT",
    //   "format": "css", "scopes": { "light": [":root", "@theme inline"], "dark": [":root", ".dark", "@theme inline"] } }
  ],
  "fonts": [{ "family": "Red Hat Text", "license": "OFL-1.1", "url": "https://fonts.googleapis.com/css2?..." }],
  "ddd": {                         // DDD token → upstream token
    "--ddd-theme-default-beaverBlue": { "token": "--pf-t--color--blue--50", "note": "primary brand blue" },
    "--ddd-font-primary": { "token": "--pf-t--global--font--family--body" },
    "--ddd-focus-ring": { "value": "2px solid var(--pf-t--global--focus-ring--color--default)" },
    "--ddd-theme-default-link": { "token": "--some--semantic--link", "modeAware": true },
    "--ddd-theme-default-beaverBlue": { "token": "--spectrum-blue-900", "fromMode": "light" },  // Spectrum
    "--ddd-surface-padding": { "token": "--pf-t--global--spacer--lg", "note": "24px" }
  },
  "extraTokens": ["--pf-t--global--background--color--primary--default"]  // also exported, for the theme chrome
}
```

## Entries

- `{ "token": "--x" }` — the DDD token becomes `var(--x)`; `--x` is exported.
- `{ "value": "... var(--x) ..." }` — a literal; every `var(--x)` inside it is exported and
  resolved per mode for the report.
- `"note"` — why; shows in the map JSON. Required in practice for anything surprising.
- `"modeAware": true` — only for a named DDD color that deliberately follows the mode. Almost
  never right: blocks already wrap named colors in `light-dark()`.
- `"fromMode": "light"` (or `"dark"`) — write that mode's resolved value as a constant. For named
  colors when the palette only exists per mode.

## What the generator does with it

- Resolves every exported token through `var()` chains in each scope; values that differ between
  modes become `light-dark()` on the color parts only (shadows keep their geometry).
- Derives `--ddd-primary-N-rgb` triplets from wherever their named color now points.
- Classifies every mapped DDD token by contract tier. It fails on a locked (structure) token, a
  token the contract doesn't list, or a broken guard (body text under 16px, headings under body
  or growing as the level goes down, control heights under 24px, a density token under its
  `densityMinPx` floor).
- Reports coverage per tier and family (identity: color, font, weight, radius, shadow, focus;
  feel: motion, state, control, border; semantic: type, density).
- Re-checks DDD's key contrast pairs (ink on white, link on white, white on the brand blues,
  status ink on status surface, ...) with the mapped values; below 4.5:1 fails.
- Writes outputs through Prettier so the element build doesn't make `--check` stale.

## Mapping by role

| DDD token(s) | Role | Look for upstream |
|---|---|---|
| beaverBlue, nittanyNavy, potentialMidnight | brand, dark brand, darkest brand surface | brand/primary palette steps |
| pughBlue, accent, sky* | light brand / accents | lighter brand steps |
| coalyGray, black, white | ink, black, white | darkest neutral (body text), black, white |
| limestone*, slate*, background, disabled | neutrals and surfaces | neutral/gray steps |
| link, linkLight | link on light, link on dark | brand/link palette steps |
| error/warning/info/success (+Light) | status ink on status surface | status palette, dark step + light step |
| opportunityGreen, futureLime | correct (light, dark) | greens |
| wonderPurple, athertonViolet | incorrect (light, dark) | purples |
| other hues (teal, orange, yellow, pink, coral, brown, tan, gold) | DDD palettes 0–15 | closest hue so palettes stay distinct |
