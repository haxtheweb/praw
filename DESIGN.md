---
version: alpha
name: HAX DDD Baseline for PRAW
description: Canonical design-system guidance for LLMs working across HAX repositories using the PRAW rule set.
colors:
  primary: "#1E407C"
  secondary: "#001E44"
  tertiary: "#009CDE"
  accent: "#96BEE6"
  neutral: "#E4E5E7"
  surface: "#FFFFFF"
  surfaceAlt: "#F2F2F4"
  text: "#262626"
  textInverse: "#FFFFFF"
  link: "#005FA9"
  background: "#EFF2F5"
  success: "#1E4620"
  warning: "#663C00"
  error: "#5F2120"
  info: "#014361"
typography:
  headline-lg:
    fontFamily: "Roboto Slab, serif"
    fontSize: 40px
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: 0.2px
  headline-md:
    fontFamily: "Roboto Slab, serif"
    fontSize: 32px
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: 0.16px
  body-md:
    fontFamily: "Roboto, Franklin Gothic Medium, Tahoma, sans-serif"
    fontSize: 20px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0.1px
  body-sm:
    fontFamily: "Roboto, Franklin Gothic Medium, Tahoma, sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0.08px
  label-md:
    fontFamily: "Roboto Condensed, sans-serif"
    fontSize: 16px
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: 0.24px
rounded:
  none: 0px
  xs: 4px
  sm: 8px
  md: 12px
  lg: 16px
  xl: 20px
  full: 100px
spacing:
  none: 0px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  3xl: 64px
  gutter: 24px
components:
  button-primary:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.textInverse}"
    typography: "{typography.label-md}"
    rounded: "{rounded.sm}"
    padding: "12px"
  button-primary-hover:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.textInverse}"
  icon-button:
    backgroundColor: "{colors.surfaceAlt}"
    textColor: "{colors.text}"
    rounded: "{rounded.full}"
    size: "40px"
    padding: "0px"
  card-default:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.xl}"
    padding: "{spacing.md}"
  instructional-callout:
    backgroundColor: "{colors.surfaceAlt}"
    textColor: "{colors.text}"
    rounded: "{rounded.sm}"
    padding: "{spacing.lg}"
---
# HAX Design Guidance for PRAW
## Overview
PRAW is a rule and guidance repository, not a standalone product UI. This DESIGN.md defines the visual system LLMs should follow when generating examples, component updates, and design decisions for HAX ecosystem work.
Use DDD as the primary system for color, typography, spacing, icon size, and shape. Use SimpleColors only as a fallback when DDD does not provide a needed shade or palette behavior.
The intended style is clear, academic-professional, high-contrast, and accessible in both light and dark mode contexts.
## Colors
The base palette follows DDD theme defaults:
- Primary and secondary tones are deep blues for structure and action hierarchy.
- Tertiary and link colors provide interactive emphasis.
- Neutral, surface, and surfaceAlt colors provide readable backgrounds and containers.
- Semantic state colors (success, warning, error, info) should be used consistently for feedback.

For theming mechanics:
- Use `data-primary` and `data-accent` when you need single-color theming hooks.
- Use `data-palette` when you need coordinated multi-color palettes across a region/site.
- Treat `data-primary`/`data-accent` and `data-palette` as different tools, not substitutes.
## Typography
Typography follows DDD defaults:
- **Headlines**: Roboto Slab, bold weight, strong hierarchy.
- **Body copy**: Roboto at readable sizes and generous line-height.
- **Labels/navigation**: Roboto Condensed with moderate letter spacing for utility text.

Use DDD typography tokens first, and avoid introducing ad-hoc font stacks or custom type ramps unless a project explicitly requires them.
## Layout
Layout uses DDD’s 4px-based spacing rhythm (`4, 8, 12, 16, 24, 32...`) to maintain consistency.
Use spacing tokens for margins, padding, and gaps; keep gutters near 24px for common container patterns.
For responsive design, align to DDD breakpoints (360, 768, 1080, 1440).
Use DDD icon sizing tokens (`--ddd-icon-*`) for icon dimensions rather than spacing tokens.
## Elevation & Depth
Depth should be subtle and functional:
- Prefer border contrast and tonal separation first.
- Use DDD box-shadow levels (`sm`, `md`, `lg`) only when needed for hierarchy.
- In dark mode, ensure shadows and borders still preserve clear separation.

Use `light-dark(...)` patterns where available so surfaces and text maintain legibility across schemes.
## Shapes
Shape language is softly geometric:
- Small controls: `xs`/`sm` radius.
- Containers and cards: `md`/`lg`/`xl` radius.
- Icon buttons and pill UI: `full` radius.

Do not mix sharply different corner treatments within the same component unless there is a deliberate semantic reason.
## Components
Use these component-level defaults:
- **Buttons**: Primary actions use dark navy backgrounds with light text; hover may shift toward primary blue.
- **Icon buttons**: Prefer `simple-icon-button-lite` for icon-only actions.
- **Icons**: Prefer `simple-icon-lite` so icon color can follow light DOM CSS `color`.
- **Cards**: Follow the `ddd-card` pattern (surface background, strong title hierarchy, moderate shadow, larger radius).
- **Instructional callouts**: Use semantic instructional treatments and keep contrast compliant.
### CSS variable implementation pattern
- Treat CSS custom properties as the primary implementation contract for styling.
- Use DDD token families consistently:
  - Colors: `--ddd-primary-*`, `--ddd-accent-*`, `--ddd-theme-default-*`
  - Typography: `--ddd-font-*`, `--ddd-lh-*`, `--ddd-ls-*`
  - Spacing: `--ddd-spacing-*`
  - Shape: `--ddd-radius-*`
  - Borders: `--ddd-border-*`
  - Elevation: `--ddd-boxShadow-*`
  - Icons: `--ddd-icon-*`
- Prefer `var(--ddd-token)` usage over hardcoded values.
- Use local component aliases only when needed for clarity or theming boundaries (for example `--my-el-card-bg: var(--ddd-accent-2)`).
- Use `light-dark(...)` patterns where available for dark mode compatibility.
- Use `data-palette` for coordinated palette themes; use `data-primary` and `data-accent` for single-color theming hooks.

When implementing DDD in web components, import DDD from `@haxtheweb/d-d-d/d-d-d.js` and use DDD as the base class (or base in mixin chains).
## Do's and Don'ts
- Do use DDD tokens for fonts, colors, spacing, radii, and icon sizes.
- Do run quick accessibility and dark mode compliance audits when updating a component.
- Do prefer `simple-icon-button-lite` and `simple-icon-lite` for icon interaction patterns.
- Do use SimpleColors only where DDD does not provide the required shade/palette behavior.
- Do keep demos and examples token-driven (classes/variables), not inline style driven.
- Don't hardcode spacing, colors, radii, or typography where DDD tokens exist.
- Don't use deprecated `<style is="custom-style" include="demo-pages-shared-styles">`.
- Don't treat `data-primary`/`data-accent` as a replacement for `data-palette`.
- Don't choose `simple-icon` when `simple-icon-lite` satisfies the requirement.