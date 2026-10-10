# Fixing unknown DDD tokens

`ddd-token-lint` (in webcomponents, `scripts/ddd-token-lint.js`) fails CI when a file references a `--ddd-*` custom property that nothing declares. The baseline (`scripts/ddd-token-lint.baseline.json`) is empty, so keep it that way: fix each new finding rather than adding it to the baseline.

## The decision rule

An unknown token fails silently, so start by working out what renders today.

| The reference | What renders today | What to write |
|---|---|---|
| `var(--ddd-typo, <fallback>)` | The fallback | Keep that look. Use a real token with the same or nearest value, or write the fallback as a literal. Expect no visual change. |
| `var(--ddd-typo)`, no fallback | Nothing. The browser drops the declaration, so the property is inherited or unset | Use the token the name was reaching for. This *is* a visual change, so call it out in the PR. |
| A name used as a hook, e.g. `var(--ddd-theme-font-color, …)` | The fallback | If DDD reads it with a fallback on purpose, add it to `HOOK_TOKENS` in the linter with a comment. Otherwise rename it to the element's own namespace (`--simple-blog-font-body`, not `--ddd-font-body`). |

For colour, check dark mode as well:
- **Inside `light-dark()`:** a reference already in the light or dark half takes a plain token.
- **Outside `light-dark()`:** a text or border colour there needs a pair, such as `light-dark(var(--ddd-theme-default-nittanyNavy), var(--ddd-theme-default-linkLight))`, or it will be unreadable on dark surfaces.

## Names people reach for, and the real token

| Unknown | Use | Why |
|---|---|---|
| `--ddd-theme-default-navy` | `--ddd-theme-default-nittanyNavy` | The only navy; `navy40`–`navy80` are translucent steps |
| `--ddd-theme-default-charcoalGray`, `-originalBlack`, `-text` | `--ddd-theme-default-coalyGray` | DDD's ink |
| `--ddd-theme-default-shrineWhite` | `--ddd-theme-default-shrineMaxLight` | |
| `--ddd-theme-default-skyMaxlight` | `--ddd-theme-default-skyMaxLight` | Casing |
| `--ddd-theme-default-<color>-rgb`, `<color>10/30` | `color-mix(in srgb, var(--ddd-theme-default-<color>) N%, transparent)` | DDD only ships `-rgb` channels for primaries |
| `--ddd-font-size-sm` / `-md` / `-2xs` / `-2xl` | `-3xs` (small text) / `-s` / `-xxs` / `-xxl` | DDD's `s` is 24px, larger than the 20px body |
| `--ddd-font-body` | `--ddd-font-primary` | |
| `--ddd-font-monospace` | No token yet. Use a literal stack `ui-monospace, "Courier New", monospace` | |
| `--ddd-line-height-*` | `--ddd-lh-120` / `140` / `150` | |
| `--ddd-icon-l` | `--ddd-icon-lg` (56px) or `--ddd-icon-md` (48px), whichever the fallback was | |
| `--ddd-icon-5xs` | `--ddd-icon-4xs` (16px, the smallest) | |
| `--ddd-boxShadow-xs` | `--ddd-boxShadow-sm` | The smallest |
| `--ddd-radius-pill`, `--ddd-border-radius` | `--ddd-radius-rounded`, `--ddd-radius-sm` | |
| `--ddd-duration-rapid` | `--ddd-duration-fast` (150ms) or `-normal` (300ms), matching the fallback | |
| `--ddd-theme-easing` | `--ddd-timing-ease` | |
| `--ddd-spacing-31+` | A literal (spacing stops at `--ddd-spacing-30` = 120px) | Widths and heights are not spacing |
| `--ddd-opacity-70` / `-90` | The nearest step that keeps text at 4.5:1, usually `--ddd-opacity-80` | The scale is 0, 20, 40, 60, 80, 100 |
| `--ddd-theme-primary-N` | `--ddd-primary-N` | |
| `--ddd-box-shadow-*` | `--ddd-boxShadow-*` | |

## Border shorthands

`--ddd-border-xs`, `-sm`, `-md` and `-lg` are complete shorthands: width, solid and limestoneLight. That causes a common bug:
- **Broken:** `border: var(--ddd-border-xs) solid <colour>` is invalid, and no border renders.
- **Width only:** for a style and colour of your own, use `--ddd-border-size-*`: `border: var(--ddd-border-size-xs) solid <colour>`.
- **Default border:** for the DDD default, use the shorthand alone: `border: var(--ddd-border-sm)`.

The linter fails on the broken form.
