# Web Components Development Rules

These rules apply specifically when working with HAX web components in the elements/ directory structure.

## Component Structure & Standards

### HAX Capability Requirements
- All components should implement `haxProperties` method for HAX editor integration
- Use `demoSchema` to provide comprehensive examples for HAX editor
- Ensure proper tag naming follows HAX conventions (kebab-case)
- Include appropriate slot content examples in demoSchema

### Design System Integration
- Always import and use DDD design tokens: `import "@haxtheweb/d-d-d/d-d-d.js"`
- Apply DDD CSS custom properties for spacing, colors, and typography
- Use `ddd-` prefixed CSS custom properties for consistent theming
- Audit components for proper DDD compliance during development

### Accessibility Standards
- Include proper ARIA labels and roles where needed
- Ensure keyboard navigation support for interactive components
- Test with screen readers when applicable
- Use semantic HTML elements as base structure
- Include focus management for complex components

### JavaScript Best Practices
- Use `globalThis` instead of `window` for global references
- Avoid optional chaining syntax (`?.`) due to Polymer parser limitations
- Implement proper event handling with `addEventListener`
- Use LitElement lifecycle methods appropriately
- Handle null/undefined states gracefully

### File Organization
- Follow monorepo element structure: `elements/component-name/`
- Include package.json, component files, and demo files
- Maintain consistent naming: `component-name.js` for the main component file
- Include proper exports in index.js files
- Remove any legacy SCSS files when encountered - we use CSS-in-JS patterns

### Documentation Requirements
- Include comprehensive JSDoc comments for all public methods
- Document all CSS custom properties with descriptions
- Provide usage examples in component README
- Include accessibility notes and keyboard interaction documentation

### Development Workflow
- Run `yarn run build` after making changes to components that inherit from HAXCMSLitElement
- Do not manually edit custom-elements.json - it's auto-generated
- Use local HAX tooling instead of npx versions
- Test components in HAX editor environment before release

## Component Audits

When working on components, perform these checks:

### Technical Audit
1. **DDD Design System**: Verify proper usage of design tokens
2. **HAX Schema**: Ensure complete and accurate haxProperties implementation
3. **Accessibility**: Check ARIA attributes, keyboard navigation, semantic markup
4. **Performance**: Review bundle size, lazy loading opportunities
5. **Browser Compatibility**: Test across supported browser versions

### Content Audit  
1. **Demo Quality**: Ensure demoSchema provides realistic, engaging examples
2. **Documentation**: Verify all properties and methods are documented
3. **Examples**: Include diverse use cases in demo content
4. **Visual Design**: Confirm component follows HAX visual standards

### Integration Audit
1. **HAX Editor**: Test component creation and editing in HAX
2. **Theme Compatibility**: Verify component works with different HAX themes
3. **Responsive Design**: Ensure proper behavior across device sizes
4. **Dependencies**: Check for minimal external dependencies

## Educational Component Guidelines

For educational web components:
- Apply OER Schema metadata parameters where applicable
- Include pedagogically meaningful default content
- Provide content structure that supports learning objectives
- Consider accessibility from an educational equity perspective
- Include examples relevant to educational contexts

---

*These rules ensure HAX web components maintain high quality and consistent behavior across the ecosystem.*