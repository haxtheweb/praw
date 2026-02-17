# KNOWLEDGE LOG

This document records emergent knowledge, decisions, conventions, and lessons learned while working across the HAX ecosystem. Use this to capture context that doesn’t fit formal rules yet, or to explain the rationale behind rules.

Structure your entries using the templates below. Keep entries concise and searchable. When a knowledge item stabilizes into a repeatable rule, promote it into RULES.md and link back here.

## How to add a new knowledge entry
- Add a new entry at the top of the relevant section with today’s date.
- Prefer small, atomic entries over long narratives.
- Include links to code, commits, PRs, or files where possible.
- If this entry should likely become a rule, mark it with `Candidate: Yes`.

## Template

- Title: <short, descriptive title>
- Date: YYYY-MM-DD
- Context: <where/why this came up>
- Guidance: <what to do next time>
- Rationale: <why this is the right approach>
- Links: <related files/PRs/issues>
- Candidate: Yes|No

---

## Web Components

- Title: Example – Prefer globalThis over window
- Date: 2025-09-25
- Context: Align with cross-environment JS standards and our ecosystem rule
- Guidance: Use `globalThis` whenever referencing global scope in components or utilities
- Rationale: Works in Node, browsers, and workers; matches existing rule CEHsAztyfB2vTCwtHGGnbk
- Links: RULES.md (JavaScript Standards)
- Candidate: No

## HAXcms

- Title: Example – Keep metadata.site.name aligned
- Date: 2025-09-25
- Context: BasePath and routing inconsistencies traced to incorrect site name
- Guidance: Ensure metadata.site.name exactly matches the site folder name
- Rationale: Prevents basePath issues in some deployment scenarios
- Links: RULES.md (HAXcms Site Metadata)
- Candidate: No

## Design System (DDD & SimpleColors)

- Title: DDD `data-palette` (site palettes) vs `data-primary` / `data-accent` (single colors)
- Date: 2026-02-17
- Context: Theme development for HAXcms themes (`clean-portfolio-theme`, `journey-theme`) uses `data-palette` to switch multi-color palettes. Initial analysis focused on `data-primary` / `data-accent`, which control only `--ddd-theme-primary` / `--ddd-theme-accent` (single-color theming), not full palettes.
- Guidance:
  - Use `data-primary` / `data-accent` when you need a single primary/accent color for an element (sets `--ddd-theme-primary` / `--ddd-theme-accent`).
  - Use `data-palette` when you need a coordinated multi-color palette for a whole region/site.
  - Ensure the CSS that defines palette variables is applied in a scope that can match the element carrying the `data-palette` attribute.
    - `DDDPaletteStyles` uses selectors like `[data-palette="3"] { ... }` (NOT `:host([data-palette="3"])`). This means it must exist in a stylesheet that can match the actual DOM element with `data-palette` (typically the global document stylesheet), otherwise palette switching may appear to do nothing.
  - If a theme wants deterministic palette switching, prefer one of:
    - Extend `DDDSuper(...)` so DDD (including palettes) is registered via `DesignSystemManager` at the document level.
    - Or inject the palette styles into the global theme stylesheet (via `HAXCMSGlobalStyleSheetContent()`), rather than relying on shadow-scoped styles.
- Rationale:
  - In DDD, `DDDPaletteStyles` defines `--ddd-palette-color-1` through `--ddd-palette-color-7` and changes them based on `[data-palette]`.
  - Palettes currently defined in `DDDPaletteStyles` (name / number):
    - `wisdom-walk-green` / `0` (default)
    - `very-violent-red` / `1`
    - `beetles-yellow` / `2`
    - `offbrand-nittany-blue` / `3`
    - `boring-blue-gray` / `4`
    - `monotone` / `5`
    - `salmon-season` / `6`
    - `tweedle-dee` / `7`
  - Application notes (as of 2026-02-17):
    - `clean-portfolio-theme`
      - Reflects `dataPalette` to `data-palette`, persists `HAXCMSSitePalette` via `user-scaffold`.
      - Extends `DDDSuper(HAXCMSLitElementTheme)` and includes `DDDAllStyles` in global theme stylesheet; palette selectors match and update `--ddd-palette-color-*`.
      - Maps `--ddd-palette-color-*` → `--ddd-palette-*` and then defines `--ddd-lightDark-*` helper vars used throughout its CSS.
      - Cycles palettes `0..6` (does not reach palette `7`).
    - `journey-theme`
      - Reflects `dataPalette` to `data-palette`, persists `HAXCMSSitePalette` via `user-scaffold`.
      - Includes `DDDAllStyles` in `static styles` (shadow scope). Because `DDDPaletteStyles` is written as `[data-palette="..."]` selectors, shadow-scoped inclusion alone does not guarantee it can match the host element; palettes may only work if DDD palette styles are also present globally.
      - Only maps two variables: `--ddd-palette-1` from `--ddd-palette-color-1` and `--ddd-palette-2` from `--ddd-palette-color-6`.
      - Cycles palettes `0..5` (does not reach palettes `6` or `7`).
- Links:
  - `webcomponents/elements/d-d-d/lib/DDDStyles.js` (`DDDPaletteStyles`)
  - `webcomponents/elements/clean-portfolio-theme/clean-portfolio-theme.js` (`dataPalette`, `togglePalette`, palette var mapping)
  - `webcomponents/elements/journey-theme/journey-theme.js` (`dataPalette`, `togglePalette`, palette var mapping)
  - `webcomponents/elements/haxcms-elements/lib/core/HAXCMSLitElementTheme.js` (global theme stylesheet injection via `HAXCMSGlobalStyleSheetContent()`)
- Candidate: Yes

- Title: Example – Prefer DDD tokens; use SimpleColors sparingly
- Date: 2025-09-25
- Context: Migrating components to DDD while retaining shade coverage
- Guidance: Use DDD tokens for spacing/typography/colors; use SimpleColors only when DDD lacks required shade
- Rationale: Aligns with primary design system while acknowledging gaps
- Links: RULES.md (Design System Standards)
- Candidate: No

## Build & Workflow

- Title: Example – Avoid optional chaining
- Date: 2025-09-25
- Context: Polymer parser incompatibilities
- Guidance: Don’t use `?.`; refactor to safe checks compatible with our tooling
- Rationale: Avoids build breaks and runtime surprises
- Links: RULES.md (JavaScript Standards)
- Candidate: No

## Documentation & Authoring

- Title: Example – Author with HAX-capable elements
- Date: 2025-09-25
- Context: Ensuring content can be edited with HAX and demoed consistently
- Guidance: Use elements with HAXSchema; consider demoSchema for demos and examples
- Rationale: Guarantees editor compatibility and consistent UX
- Links: RULES.md (HAX Content Authoring)
- Candidate: No
