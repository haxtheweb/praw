# Design System Rules

Scoped rules for the HAX design systems: DDD (Design, Develop, Deliver — primary) and SimpleColors (legacy/supplementary). This file is read when editing design-system-path files. Authoritative rule records (Rule IDs + Scope) live in `RULES.md`. `DESIGN.md` at the repository root is the canonical design guidance for this repo; conform future design work to its tokens, CSS variable patterns, component conventions, and Do's/Don'ts.

## Scoped rules (triggers — full text in RULES.md)
- **DDD Design System (Primary)** (`MLhl56jNSqHvnRiAW5A2GR`) — DDD lives at `elements/d-d-d`; use it for fonts, colors, padding, spacing, margins, consistency.
- **SimpleColors (Legacy)** (`K0lV6BJOPrqP7iJMZkemUw`) — use only to fill DDD gaps in color shades; prefer DDD colors otherwise.
- **DESIGN.md Compliance** (`c4f0b69d-9ed4-4b6d-bf52-6a3d9937c98f`) — `DESIGN.md` is the canonical source of truth for design decisions in this repo.
- *(When auditing a specific component for DDD usage, see webcomponents-scoped rule `MT6HPJ9BDhA13jwSXjcmeA`.)*

## DDD implementation
- Always import DDD: `import "@haxtheweb/d-d-d/d-d-d.js"`. Extend `DDD` directly (never `DDD(LitElement)`); with mixins, `DDD` is the base class.
- Use `ddd-`-prefixed CSS custom properties consistently; prioritize DDD tokens over hardcoded values.
- Use DDD icon-sizing variables for icon height/width (not spacing variables).

### Core tokens (reference)
- **Typography**: `--ddd-font-primary`, `--ddd-font-secondary`, `--ddd-font-size-*` (xs,s,ms,m,ml,l,xl,xxl), `--ddd-font-weight-*` (light,regular,medium,bold), `--ddd-line-height-*`.
- **Spacing**: `--ddd-spacing-*` (0-32) for margin/padding/gaps; `--ddd-radius-*` (xs,s,m,l,xl).
- **Colors**: `--ddd-primary-*` (0-25), `--ddd-accent-*`, `--ddd-text-*`, `--ddd-border-*`. Prefer DDD over SimpleColors.
- **Layout**: `--ddd-breakpoint-*`; CSS Grid/Flexbox with DDD spacing tokens.

### Component styling pattern
```css
:host {
  display: block;
  font-family: var(--ddd-font-primary);
  color: var(--ddd-text-primary);
  margin: var(--ddd-spacing-4);
}
.component-header {
  font-size: var(--ddd-font-size-l);
  font-weight: var(--ddd-font-weight-medium);
  margin-bottom: var(--ddd-spacing-3);
}
```

## Transitions & animations (standards)
- Minimal interactions: `.3s ease-in-out` (hover, focus, color, small changes).
- Extended interactions: `.6s ease-in-out` (panel slides, expand/collapse, fades, layout shifts).
- Default to `ease-in-out`; avoid one-off durations; respect `prefers-reduced-motion`.

## SimpleColors (when DDD is insufficient)
12 base colors × 25 shades (0-24): red, pink, purple, indigo, blue, cyan, teal, green, lime, yellow, amber, orange. Light/dark theme variations; accessible contrast built in. Example: `var(--simple-colors-default-theme-blue-7)`. Migrate to DDD equivalents where possible; document remaining SimpleColors dependencies.

## Design system audits (when working on DDD)
1. **Token usage**: spacing, colors, typography use DDD tokens.
2. **Consistency**: visual elements align with established patterns.
3. **Responsiveness**: adapts across breakpoints.
4. **Accessibility**: color contrast meets standards; dark-mode compliance.
5. **Performance**: minimal custom CSS beyond tokens.

---
*Scoped to design-system. Full rule registry + IDs: `RULES.md`. Always-on global rules apply in addition.*
