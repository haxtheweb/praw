# `design-system/bridge.json`

Read by `elements/d-d-d/design-system/bridge/build-bridge.js`
(<https://github.com/haxtheweb/webcomponents/tree/master/elements/d-d-d/design-system/bridge>).
Working example: `elements/patternfly-theme/design-system/bridge.json`.

```jsonc
{
  "system": "patternfly",          // design system name in DesignSystemManager; also <system>.ddd-map.json
  "title": "PatternFly",           // display name in generated headers
  "prefix": "Patternfly",          // export prefix: PatternflyTokens, PatternflyDDDMap, PatternflyFonts
  "upstream": {
    "package": "@patternfly/patternfly",
    "version": "6.7.0",            // exact; fetched with npm pack, never added as a dependency
    "license": "MIT",              // must match the packed package.json, and be shippable
    "homepage": "https://www.patternfly.org",
    "repository": "https://github.com/patternfly/patternfly",
    "file": "base/patternfly-variables.css"   // CSS with the custom properties, inside the package
  },
  "scopes": {                      // selectors merged in order to resolve each mode
    "light": [":root"],
    "dark": [":root", ":root:where(.pf-v6-theme-dark)"]
  },
  "fonts": [{ "family": "Red Hat Text", "license": "OFL-1.1", "url": "https://fonts.googleapis.com/css2?..." }],
  "ddd": {                         // DDD token → upstream token
    "--ddd-theme-default-beaverBlue": { "token": "--pf-t--color--blue--50", "note": "primary brand blue" },
    "--ddd-font-primary": { "token": "--pf-t--global--font--family--body" },
    "--ddd-focus-ring": { "value": "2px solid var(--pf-t--global--focus-ring--color--default)" },
    "--ddd-theme-default-link": { "token": "--some--semantic--link", "modeAware": true }
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

## What the generator does with it

- Resolves every exported token through `var()` chains in each scope; values that differ between
  modes become `light-dark()` on the color parts only (shadows keep their geometry).
- Derives `--ddd-primary-N-rgb` triplets from wherever their named color now points.
- Reports coverage for the DDD surface a system is expected to answer: named colors
  (`--ddd-theme-default-*`), `--ddd-font-{primary,secondary,navigation,mono}`,
  `--ddd-radius-{xs..xl}`, `--ddd-boxShadow-{sm..xl}`, `--ddd-focus-ring`.
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
