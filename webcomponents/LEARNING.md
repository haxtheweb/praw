# Webcomponents LEARNING Context

Learned patterns and integration knowledge for WARP when working specifically with HAX webcomponents.

## Component Development Integration Patterns

### HAX Schema Integration Learning

#### Discovered Patterns:
- **haxProperties Method**: Must return object with `canScale`, `canPosition`, `canEditSource`, `gizmo`, `settings`, `configure`, `advanced`
- **demoSchema Usage**: Provides realistic examples that render properly in HAX editor
- **Property Configuration**: Complex properties need proper `inputMethod` specification (textfield, select, boolean, etc.)

#### Common Implementation Issues:
- **Missing demoSchema**: Components without proper demos are hard to discover in HAX editor
- **Invalid Property Types**: HAX schema expects specific property types that must align with component properties
- **Slot Content**: demoSchema must include realistic slot content for components that accept children

### DDD Integration Learning

#### Effective DDD Usage Patterns:
- **Token Hierarchy**: Use DDD tokens in order: theme → semantic → raw values as fallback
- **Spacing Consistency**: Always use `--ddd-spacing-*` tokens instead of hardcoded margins/padding
- **Color Application**: Prefer `--ddd-primary-*` and `--ddd-accent-*` over SimpleColors when possible
- **Typography Scale**: Use `--ddd-font-size-*` with corresponding `--ddd-line-height-*` values

#### Migration Patterns from SimpleColors:
```css
/* Legacy SimpleColors */
.old-component {
  color: var(--simple-colors-default-theme-blue-7);
  background: var(--simple-colors-default-theme-blue-1);
}

/* Migrated to DDD */
.new-component {
  color: var(--ddd-primary-15);
  background: var(--ddd-accent-1);
}
```

### Component Architecture Learning

#### LitElement Best Practices Discovered:
- **Property Declaration**: Always use proper TypeScript-style property declarations even in JS
- **Lifecycle Management**: Use `updated()` for DOM-dependent operations, not `firstUpdated()`
- **Event Handling**: Prefer `@click=${this.handleClick}` over `addEventListener` for better performance
- **CSS-in-JS**: Use `static styles` instead of external CSS files for better bundling

#### Accessibility Integration Patterns:
- **Focus Management**: Components with complex interactions need proper focus trapping
- **ARIA Implementation**: Use `role`, `aria-label`, `aria-describedby` consistently
- **Keyboard Navigation**: Implement arrow key navigation for composite components
- **Screen Reader**: Test with actual screen readers, not just automated tools

## Cross-Repository Dependencies

### Impact Assessment Learning

#### Webcomponents → HAXcms Sites:
- **Component Changes**: Any component API change affects all sites using that component
- **HAX Schema Updates**: Changes to haxProperties affect HAX editor behavior across ecosystem
- **Build Dependencies**: Component builds trigger downstream site updates

#### Webcomponents → Create (CLI):
- **Scaffolding Templates**: CLI templates must stay synchronized with component patterns
- **Default Properties**: CLI-generated components should include current DDD patterns
- **HAX Integration**: Generated components should include proper HAX schema by default

### Registry Integration Learning

#### wc-registry.json Dependencies:
- **Component Discovery**: Registry determines which components are available in HAX editor
- **Version Management**: Registry must stay synchronized with published component versions
- **CDN Coordination**: Registry URLs must align with actual CDN component locations

#### Build System Coordination:
- **custom-elements.json**: Generated file affects IDE support and documentation
- **Storybook Integration**: Component stories depend on proper metadata generation
- **Testing Dependencies**: Test files must stay synchronized with component APIs

## Educational Component Patterns

### OER Schema Integration Learning

#### Effective Educational Metadata:
```javascript
// Educational component example
static get haxProperties() {
  return {
    gizmo: {
      title: 'Learning Objective',
      description: 'Component for structured learning outcomes',
      icon: 'av:library-books',
      color: 'blue',
      groups: ['Education', 'Content'],
      handles: [
        {
          type: 'inline',
          text: 'objective'
        }
      ],
      meta: {
        author: 'HAX Educational Components',
        owner: 'HAX Community',
        learningObjective: true,
        educationalUse: 'instruction'
      }
    }
  };
}
```

#### Pedagogical Component Patterns:
- **Question Components**: Need immediate feedback mechanisms
- **Assessment Tools**: Must track completion states without external dependencies
- **Interactive Media**: Should degrade gracefully for accessibility
- **Progress Tracking**: Use local storage for persistence across sessions

### Content Structure Learning

#### Effective Educational Content:
- **Chunked Learning**: Break complex concepts into digestible component pieces
- **Progressive Disclosure**: Use collapsible sections and stepped content
- **Multiple Modalities**: Include text, visual, and interactive elements
- **Assessment Integration**: Embed formative assessment throughout content

## Performance Optimization Learning

### Bundle Size Management

#### Discovered Optimization Patterns:
- **Lazy Loading**: Import heavy dependencies only when component becomes visible
- **Code Splitting**: Separate complex functionality into optional modules
- **CSS Optimization**: Use DDD tokens to reduce custom CSS payload
- **Dependency Analysis**: Regularly audit component dependencies for bloat

#### Build Performance Learning:
- **Incremental Builds**: Component builds should only rebuild changed dependencies
- **Cache Management**: Leverage build caches for faster development iterations
- **Parallel Processing**: Multiple components can build simultaneously in monorepo

### Runtime Performance Patterns:

#### Efficient Component Patterns:
```javascript
// Efficient property handling
static get properties() {
  return {
    // Use appropriate types to prevent unnecessary re-renders
    title: { type: String },
    items: { type: Array },
    selected: { type: Boolean, reflect: true }
  };
}

// Efficient rendering with guards
render() {
  return html`
    ${this.items?.length ? html`
      <ul>
        ${this.items.map(item => html`<li>${item.title}</li>`)}
      </ul>
    ` : html`<p>No items available</p>`}
  `;
}
```

## Troubleshooting Patterns

### Common Component Issues

#### HAX Editor Integration Problems:
1. **Component Not Appearing**: Check haxProperties method implementation
2. **Properties Not Editable**: Verify settings/configure schema alignment with actual properties
3. **Demo Content Issues**: Ensure demoSchema provides valid, engaging examples
4. **Rendering Problems**: Test component both in HAX editor and live site contexts

#### DDD Integration Issues:
1. **Token Not Available**: Check if using correct DDD version and token exists
2. **Styling Conflicts**: Verify component doesn't override DDD tokens inappropriately  
3. **Theme Incompatibility**: Test component across different HAXcms themes
4. **Responsive Problems**: Ensure component uses DDD breakpoint tokens properly

#### Build System Issues:
1. **custom-elements.json Errors**: Usually indicates JSDoc or property declaration problems
2. **Import Failures**: Check for circular dependencies or missing exports
3. **Bundle Problems**: Verify component exports and dependency declarations
4. **Registry Sync**: Ensure component is properly published and registered

### Performance Debugging Patterns:

#### Memory Leaks:
- **Event Listeners**: Always remove listeners in `disconnectedCallback()`
- **Observers**: Clean up IntersectionObserver, ResizeObserver, etc.
- **Timers**: Clear intervals and timeouts on component destruction

#### Render Performance:
- **Expensive Operations**: Move costly computations to `willUpdate()` or use `@state()`
- **DOM Updates**: Minimize direct DOM manipulation, use LitElement's rendering system
- **CSS Performance**: Avoid complex selectors, use CSS custom properties efficiently

## Future Learning Areas

### Emerging Component Patterns:
- **Web Components v2**: Preparing for upcoming web standards changes
- **AI Integration**: Components that leverage HAX's AI capabilities
- **Advanced Accessibility**: Beyond WCAG 2.1 AA to more inclusive design
- **Performance Monitoring**: Built-in performance tracking for components

### Integration Evolution:
- **Micro-Frontend Patterns**: Components as standalone applications
- **Edge Computing**: Components optimized for edge deployment
- **Progressive Enhancement**: Better fallback strategies for older browsers
- **Developer Experience**: Enhanced tooling for component development

---

*This document captures component-specific learning from WARP interactions. Update as new patterns emerge in webcomponent development.*