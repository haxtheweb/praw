# Design System Rules

Scoped rules for the HAX design systems: DDD (Design, Develop, Deliver — primary) and SimpleColors (legacy/supplementary). This file is read when editing design-system-path files. Authoritative rule records (Rule IDs + Scope) live in `RULES.md`. `DESIGN.md` at the repository root is the canonical design guidance for this repo; conform future design work to its tokens, CSS variable patterns, component conventions, and Do's/Don'ts.

## Scoped rules (triggers — full text in RULES.md)
- **DDD Design System (Primary)** (`MLhl56jNSqHvnRiAW5A2GR`) — DDD lives at `elements/d-d-d`; use it for fonts, colors, padding, spacing, margins, consistency.
- **SimpleColors (Legacy)** (`K0lV6BJOPrqP7iJMZkemUw`) — use only to fill DDD gaps in color shades; prefer DDD colors otherwise.
- **DESIGN.md Compliance** (`c4f0b69d-9ed4-4b6d-bf52-6a3d9937c98f`) — `DESIGN.md` is the canonical source of truth for design decisions in this repo.
- **HAX UI: Admin Surfaces Layer of DDD** (`1992902d74844c908ab446`) — admin chrome (site admin, outline-designer, system admin, editor chrome) uses `--hax-ui-*` from `HaxUiAdminTokens`, not DDD content sizes. See "HAX UI (admin surfaces)" below.
- **Admin Fields Are simple-fields** (`956c54783626475ea901a6`) — every input, select, textarea and checkbox in admin chrome is a `simple-fields-field` styled by `HaxUiAdminSimpleFields` (`class="hax-ui-simple-field"`); never a hand-drawn `<input>`, `<select>` or `<textarea>` (hidden and file inputs excepted). The webcomponents HAX UI admin contract check reports them as `raw-field`.
- **HAXcms Prototypes Are Built On The Real System** (`ccca6768-05e0-4d4d-b3a1-4b9895531558`) — any prototype of HAXcms itself (whole site, top bar, edit mode, menus, admin, multipage flows) uses the `haxcms-prototype` skill: brief first, base from a real branch or the haxcms-nodejs UI inventory, only the proposal hand-authored and marked, values from the inventory's `tokens.css`, provenance stamped, fidelity check passed before review.
- **Every Area Has an Icon, a DDD Color and a Motion on Record** (`411423ec-d922-4bd4-8c45-3d8c65b9fbfa`) — a project area, surface or network site gets one icon, one DDD named color and one DDD icon motion, recorded in the ecosystem web (`ecosystem/web/*.mmd` `%%@ node` lines) or `ecosystem/network.json` before it ships; everything that shows the area reads them from there. See "Area icons, colors and motion" below.
- *(When auditing a specific component for DDD usage, see webcomponents-scoped rule `MT6HPJ9BDhA13jwSXjcmeA`.)*
- *(Choosing colors for opposing actions or on/off states? They must read apart without color: webcomponents-scoped rule `13a03330-483e-404e-9e48-b0d9f16432d3`.)*

## DDD implementation
- Always import DDD: `import "@haxtheweb/d-d-d/d-d-d.js"`. Extend `DDD` directly (never `DDD(LitElement)`); with mixins, `DDD` is the base class.
- Use `ddd-`-prefixed CSS custom properties consistently; prioritize DDD tokens over hardcoded values.
- Use DDD icon-sizing variables for icon height/width (not spacing variables).

### Core tokens (reference)
- **Typography**: `--ddd-font-primary`, `--ddd-font-secondary`, `--ddd-font-navigation`, `--ddd-font-size-*` (6xs-4xl, type1-s/m/l), `--ddd-font-weight-*` (light,regular,medium,bold,black), `--ddd-lh-*` (120,140,150), `--ddd-ls-*`.
- **Spacing**: `--ddd-spacing-*` (0-30, 4px steps) for margin/padding/gaps; `--ddd-radius-*` (0,xs,sm,md,lg,xl,rounded,circle).
- **Colors**: `--ddd-primary-*` (0-25), `--ddd-accent-*` (0-14), `--ddd-theme-default-*`, `--ddd-border-*` (xs-lg). DDD has no `--ddd-text-*` tokens; use `--ddd-theme-default-coalyGray` (or `--ddd-theme-primary` in themed regions) for text. Prefer DDD over SimpleColors.
- **Layout**: `--ddd-breakpoint-*` (write the px value literally in `@media`); CSS Grid/Flexbox with DDD spacing tokens.

### Component styling pattern
```css
:host {
  display: block;
  font-family: var(--ddd-font-primary);
  color: var(--ddd-theme-default-coalyGray);
  margin: var(--ddd-spacing-4);
}
.component-header {
  font-size: var(--ddd-font-size-l);
  font-weight: var(--ddd-font-weight-medium);
  margin-bottom: var(--ddd-spacing-3);
}
```

## HAX UI (admin surfaces)
HAX UI is the admin layer of DDD: denser and quieter than content (14px text, 32px rows and controls, one accent) so long lists and many settings fit. Every value maps to a DDD primitive. Full guide: [`hax-ui-admin.md`](https://github.com/haxtheweb/webcomponents/blob/master/elements/d-d-d/design-system/source/hax-ui-admin.md) (also the HAX UI section of the DDD Design System artifact).

- **When**: if a site visitor can see it, use DDD content. If only a signed-in editor sees it and it changes settings or data, use HAX UI: site admin and every section in it, outline-designer, revisions, reports, system admin (next), and editor chrome (top bar, tray, element settings panel) as it is updated. Content previews inside admin keep DDD.
- **How**: `import { HaxUiAdminTokens, HaxUiAdminPrimitives } from "@haxtheweb/hax-body/lib/hax-ui-styles.js"`, spread both into `static get styles()`, style with `--hax-ui-*` only. No raw hex, no `--ddd-font-size-*` content sizes, no SimpleColors in admin chrome. A missing value is added to `HaxUiAdminTokens` (mapped to DDD) before an element uses it.
- **One admin dialog**: site (then system) admin sections render inside one shell: titlebar with breadcrumb, section rail, page header, optional toolbar, body, and an action bar the shell owns. A section never draws its own titlebar or Save button.
- **Staged save**: edits wait for Save; Save is quiet until something changes, then becomes the primary fill with a count and changed-field dots; leaving with unsaved changes asks first (Stay / Discard and leave / Save and leave). Auto-save is later work.
- **Patterns**: 32px buttons with words beside icons (one primary per bar; danger outline for a step, danger fill only for the final commit), segmented controls, filter chips, switches, `.hax-ui-pill`, `.hax-ui-kbd`, outline-designer's row states, field rows (label + help left, 40px control right), one-line callouts, empty states.
- **Proposed tokens** (titlebar, sunken, primary, warning, info, field/titlebar/action-bar heights, rail width) are documentation until the editing update and the element settings panel adopt them; write the DDD value and name the proposed token in a comment.
- **Audit**: `hax-pattern-library-audit` grades admin elements against `contract-admin-surface-tokens`, `contract-admin-action-bar` and `contract-admin-row-states`.

## Transitions & animations (standards)
- Minimal interactions: `.3s ease-in-out` (hover, focus, color, small changes).
- Extended interactions: `.6s ease-in-out` (panel slides, expand/collapse, fades, layout shifts).
- Default to `ease-in-out`; avoid one-off durations; respect `prefers-reduced-motion`.

- Icon motion comes from the DDD motion library ([`DDDMotion.js`](https://github.com/haxtheweb/webcomponents/blob/master/elements/d-d-d/lib/DDDMotion.js)), not from keyframes an element writes itself: `motion="<name>"` on `simple-icon` / `simple-icon-lite`, or `ddd-motion-<name>` with `ddd-motion-trigger` on the card or link around it. Nine names: `pop`, `wiggle`, `tilt`, `beat`, `lift`, `spin`, `nudge`, `strike`, `glow`. `beat` is the scale motion; `pulse` (`data-pulse`) is the ring that asks for attention. Each plays once on hover or keyboard focus, lasts under a second, never carries meaning alone, and does not exist under `prefers-reduced-motion: reduce`.

## Area icons, colors and motion
Every part of HAX that people are shown has one icon, one DDD named color and one icon motion (rule `411423ec…`).
- **Record**: the `%%@ node <id> icon=… color=… motion=…` line in the ecosystem web that draws it (`ecosystem/web/hax-ecosystem.mmd` for an area, its sub-web for a part), and `ecosystem/network.json` for a site in the network. No other copy; change the record first.
- **Guide**: [`ecosystem/README.md`, "Area icons, colors and motion"](../ecosystem/README.md#area-icons-colors-and-motion): how to add one, the icon grid and one-ink rule, how a color is chosen, which motion means what, dark mode and reduced motion.
- **Icons are HAX's own marks**: 24 grid, one filled path in one ink, in `@haxtheweb/hax-iconset` (`hax:php`, `hax:nodejs` are the examples). Never another project's logo, mascot or wordmark.

## SimpleColors (when DDD is insufficient)
12 base colors × 25 shades (0-24): red, pink, purple, indigo, blue, cyan, teal, green, lime, yellow, amber, orange. Light/dark theme variations; accessible contrast built in. Example: `var(--simple-colors-default-theme-blue-7)`. Migrate to DDD equivalents where possible; document remaining SimpleColors dependencies.

## Design system audits (when working on DDD)
1. **Token usage**: spacing, colors, typography use DDD tokens.
2. **Consistency**: visual elements align with established patterns.
3. **Responsiveness**: adapts across breakpoints.
4. **Accessibility**: color contrast meets standards; dark-mode compliance.
5. **Performance**: minimal custom CSS beyond tokens.

## Palettes
`data-primary`/`data-accent` = one color; `data-palette` = multi-color palette. `DDDPaletteStyles` uses `[data-palette="N"]` selectors, so it must be in document-level styles (`DDDSuper` or the global theme stylesheet), not shadow-only (rule `447f8d9b…`).

---
*Scoped to design-system. Full rule registry + IDs: `RULES.md`. Always-on global rules apply in addition.*
