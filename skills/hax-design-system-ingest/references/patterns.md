# Patterns to learn from each system

Every system brought into HAX is a chance to make the DDD contract and the bridge generator more
accurate. While reading a system's tokens, look for these patterns, map what the contract already
covers, and record anything new in the PR (and as an issue in
<https://github.com/haxtheweb/issues> when it should change DDD itself).

## Seen so far

| Pattern | Where | What it means for HAX |
|---|---|---|
| Paired "on" colors | Web Awesome `--wa-color-<hue>-on`, `fill-quiet/normal/loud` with `on-quiet/normal/loud`; Material `on-primary`, `on-surface` | Adopted: each `data-primary` palette has a `--ddd-primary-N-on` text color, and the generator flips it when a remapped palette needs the other one. Map a system's own `on` color there when it has one. |
| Lightness-normalized palettes | Web Awesome (a step number is the same lightness in every hue); Tailwind and Radix are close | Contrast is predictable by step: light steps take dark text and dark steps take white. Map DDD colors by step and every palette passes. |
| Scale knobs | Web Awesome `--wa-space-scale`, `--wa-border-radius-scale`, `--wa-shadow-blur-scale`, `--wa-font-size-scale` | One number rescales a family. The generator resolves knobs to values; DDD's density tier could take a scale the same way. |
| Semantic surface tiers | Web Awesome `surface-lowered/default/raised`; Carbon `layer-01/02`; Material `surface-container-*` | Use them for the theme chrome (bars, panels, sidebars); DDD blocks keep their own background tokens. |
| Component-level tokens | Web Awesome `--wa-panel-*`, `--wa-form-control-*`; Carbon component scopes | Adopted as the contract's component tier (card, control, tag). Map them from the system's own card, button and tag, in px. |
| Shared vocabulary | Web Awesome `variant` / `appearance` / `size`; Spectrum `variant` / `treatment`; Material filled / tonal / outlined / text | DDD blocks answer the same three words through the `DDDVocabulary` mixin, translated from their existing attributes. Record the system's names for each value; they don't change the bridge. |
| rem sized for a 16px root | Carbon, PatternFly, shadcn, Web Awesome | HAX's root is 20px, so rem values come out 25% larger than designed. Component values go in as px; the existing rem density mappings are a known gap (haxtheweb/issues#3339). |
| Theme variants in one package | Web Awesome default / awesome / shoelace; Spectrum light / dark / wireframe | Pick one, say which in `bridge.json`'s `$comment`, and leave the others for a later variant. |
| Free and commercial editions | Web Awesome Free vs Pro; Tailwind vs Tailwind Plus | Read only the open-source package; never copy values shown only in paid themes or docs. |
| Icon sets | Carbon, Material Symbols, Spectrum 2 workflow, Lucide (shadcn), Heroicons (Tailwind) | Adopted: a bridge's `icons` block maps HAX icon names to the system's set (`icon-maps.json`, one column per set). Check the icons' own license: PatternFly's (Font Awesome, Red Hat Design System) are Creative Commons and are not used. |

## What to record for a new system

- Any token family the contract has no slot for, and whether it belongs in DDD (issue) or only in
  the theme chrome (note in `bridge.json`).
- Any value the generator can't read or resolve (a new color syntax, a computed value, a file
  layout), and the generator change or workaround used.
- The system's layout primitives (page regions such as Web Awesome's `wa-page` slots: header,
  subheader, navigation, main-header, aside, footer) and how they map to HAXcms regions.
