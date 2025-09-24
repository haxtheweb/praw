# Design System Rules

These rules apply specifically when working with HAX design systems, primarily DDD (Design, Develop, Deliver) and legacy SimpleColors.

## DDD Design System (Primary)

### Implementation Requirements
- Always import DDD: `import "@haxtheweb/d-d-d/d-d-d.js"`
- Use DDD CSS custom properties for all styling needs
- Apply `ddd-` prefixed custom properties consistently
- Prioritize DDD tokens over hardcoded values

### Core Design Tokens

#### Typography
- `--ddd-font-primary` - Primary font family
- `--ddd-font-secondary` - Secondary font family
- `--ddd-font-size-*` - Standardized font sizes (xs, s, ms, m, ml, l, xl, xxl)
- `--ddd-font-weight-*` - Font weights (light, regular, medium, bold)
- `--ddd-line-height-*` - Line height values

#### Spacing
- `--ddd-spacing-*` - Consistent spacing scale (0-32)
- `--ddd-radius-*` - Border radius values (xs, s, m, l, xl)
- Apply spacing tokens for margins, padding, and gaps
- Use spacing scale consistently across components

#### Colors
- `--ddd-primary-*` - Primary brand colors (0-25 scale)
- `--ddd-accent-*` - Accent color variations
- `--ddd-text-*` - Text color variations
- `--ddd-border-*` - Border color options
- Prefer DDD colors over SimpleColors when available

#### Layout
- `--ddd-breakpoint-*` - Responsive breakpoints
- Use CSS Grid and Flexbox with DDD spacing tokens
- Implement consistent container and wrapper patterns

### Implementation Patterns

#### Component Styling
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

#### Responsive Design
```css
@media (max-width: 768px) {
  :host {
    margin: var(--ddd-spacing-2);
  }
  
  .component-header {
    font-size: var(--ddd-font-size-m);
  }
}
```

### Design System Audits
When working with DDD, verify:
1. **Token Usage**: All spacing, colors, and typography use DDD tokens
2. **Consistency**: Visual elements align with established patterns
3. **Responsiveness**: Design adapts properly across breakpoints
4. **Accessibility**: Color contrast meets accessibility standards
5. **Performance**: Minimal custom CSS beyond token usage

## SimpleColors (Legacy System)

### When to Use SimpleColors
- Filling gaps where DDD doesn't provide needed color variations
- Working with legacy components that haven't migrated to DDD
- Creating complex color schemes requiring extended color palettes
- Supporting existing themes that rely on SimpleColors

### SimpleColors Structure
- Provides 12 base colors with 25 shades each (0-24)
- Colors: red, pink, purple, indigo, blue, cyan, teal, green, lime, yellow, amber, orange
- Each color includes light/dark theme variations
- Accessible contrast ratios built into the color scale

### Implementation Guidelines
```css
/* Use SimpleColors only when DDD is insufficient */
.legacy-component {
  background-color: var(--simple-colors-default-theme-blue-7);
  color: var(--simple-colors-default-theme-blue-1);
  border: 1px solid var(--simple-colors-default-theme-blue-4);
}
```

### Migration Strategy
- Audit existing SimpleColors usage in components
- Replace with DDD equivalents where possible
- Document remaining SimpleColors dependencies
- Plan gradual migration to DDD tokens

## Design System Integration

### Component Development
- Start with DDD tokens for all new components
- Use SimpleColors only for specific color needs not covered by DDD
- Document design decisions and token choices
- Test components across different themes and contexts

### Theme Development
- Build themes using DDD as the foundation
- Extend with SimpleColors for specialized color needs
- Ensure consistent application of design tokens
- Test theme variations for accessibility compliance

### Quality Standards
- Maintain consistent visual hierarchy
- Use proper contrast ratios for accessibility
- Implement responsive design patterns
- Follow established spacing and typography scales

## Best Practices

### Performance
- Minimize custom CSS beyond design system tokens
- Use CSS custom properties efficiently
- Avoid redundant style declarations
- Optimize for CSS payload size

### Maintainability
- Document design system usage patterns
- Create reusable style mixins where appropriate
- Maintain consistency across component library
- Plan for design system evolution and updates

### Accessibility
- Use design system color combinations with proper contrast
- Implement focus states using design system tokens
- Ensure typography scales remain readable
- Test with assistive technologies

### Developer Experience
- Provide clear documentation for design system usage
- Include examples and code snippets
- Maintain up-to-date design system documentation
- Create tooling to validate design system compliance

---

*These rules ensure consistent, accessible, and maintainable design implementations across the HAX ecosystem using established design system patterns.*