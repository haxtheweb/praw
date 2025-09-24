# WARP Learning Context - HAX Ecosystem Integration

This document captures learned patterns, discovered workflows, and integration knowledge for how WARP should work effectively across the entire HAX ecosystem.

## Ecosystem Integration Patterns

### Repository Interaction Map

The HAX ecosystem requires WARP to understand cross-repository dependencies and interaction patterns:

```
webcomponents/ (Core Components & DDD)
    ↓ provides components to
haxcms-php/ & haxcms-nodejs/ (Backends)
    ↓ serves content from  
HAXsites (docs/, various ai-sites/)
    ↑ developed with
create/ (HAX CLI)
    ↓ generates scaffolding for
desktop/ (Local Development)
    ↓ facilitates
open-apis/ (Microservices)
    ↓ supports conversion/analysis for
All HAX Projects
```

### Cross-Repository Workflows

#### When working in `webcomponents/`:
- **Impact Assessment**: Changes affect all HAXcms backends and sites
- **Testing Strategy**: Must verify components work in HAX editor context
- **Build Coordination**: `yarn run build` affects `custom-elements.json` across ecosystem
- **Registry Updates**: Component changes potentially affect `wc-registry.json` (but never run ubiquity script)

#### When working in `haxcms-php/` or `haxcms-nodejs/`:
- **Component Dependencies**: Must understand available webcomponents and their schemas
- **API Compatibility**: Changes affect all HAXsites using the backend
- **Theme System**: Backend changes may impact theme rendering across sites

#### When working in `create/` (HAX CLI):
- **Template Coordination**: Templates must align with current webcomponents and backends
- **Scaffolding Accuracy**: Generated code must match ecosystem standards
- **Cross-platform Testing**: CLI changes affect developers across all HAX projects

#### When working in `docs/` or HAXsites:
- **Component Usage**: Must use HAX-capable components from webcomponents registry
- **Backend Alignment**: Site structure must align with chosen backend capabilities
- **Content Standards**: Educational content should leverage OER Schema patterns

### Learned Integration Challenges

#### Component Registry Synchronization
- **Issue**: Components exist in webcomponents/ but may not be available in specific site contexts
- **WARP Response**: Always check `wc-registry.json` or HAX schema before suggesting components
- **Verification**: Test component availability in target environment

#### Build System Coordination
- **Issue**: Changes in one repo may require builds in dependent repos
- **WARP Response**: When modifying webcomponents, consider downstream build impacts
- **Pattern**: `webcomponents/` changes → `haxcms-*` updates → `docs/` rebuild

#### Version Alignment
- **Issue**: CLI, backends, and components may have version mismatches
- **WARP Response**: Use local tooling (`hax` command) rather than global npm packages
- **Verification**: Check package.json versions across repositories for compatibility

## Discovered Workflow Patterns

### Effective Development Sequences

#### New Component Development:
1. **Research Phase**: Check `issues/` for related requests or bugs
2. **Scaffold Phase**: Use `hax webcomponent` with proper flags (`--y`, `--writeHaxProperties`)
3. **Development Phase**: Implement with DDD tokens, accessibility standards
4. **Integration Phase**: Test in HAX editor, verify HAX schema
5. **Documentation Phase**: Update demos, documentation, examples
6. **Ecosystem Phase**: Test in HAXcms context, verify theme compatibility

#### Site Content Creation:
1. **Component Assessment**: Verify available components for content needs
2. **Content Planning**: Structure content using JSON Outline Schema patterns
3. **Authoring Phase**: Use HAX editor interface for content creation
4. **Enhancement Phase**: Add educational metadata (OER Schema where applicable)
5. **Quality Phase**: Test accessibility, performance, cross-device compatibility
6. **Integration Phase**: Verify content works with selected backend

#### Cross-Repository Bug Fixes:
1. **Issue Location**: Check unified `issues/` repository first
2. **Impact Assessment**: Identify which repositories are affected
3. **Fix Coordination**: Address root cause in primary repository
4. **Propagation**: Update dependent repositories as needed
5. **Testing**: Verify fix works across affected repositories
6. **Documentation**: Update relevant WARP.md files with learned patterns

### Command Coordination Patterns

#### Development Server Management:
- Use `hax serve` from appropriate directory based on project type
- For HAXsites: Run from site root directory
- For webcomponents: Use monorepo development server
- Always use `--y --no-i --auto` flags to prevent interactive interruptions

#### Build Coordination:
- **webcomponents/**: `yarn run build` affects entire ecosystem
- **HAXsites with themes**: `yarn run build` required after HAXCMSLitElement changes
- **Never manually edit**: `custom-elements.json`, manifest files, `wc-registry.json`

#### Version Control Coordination:
- Check `issues/` repository for existing related issues
- Use GitHub CLI (`gh`) for cross-repository issue management
- Coordinate commits across repositories when changes span multiple repos

## Educational Context Integration

### OER Schema Application
- **Content Creation**: Apply OER metadata to educational components and content
- **Pedagogical Patterns**: Leverage HAX's educational component library
- **Learning Objectives**: Structure content to support measurable learning outcomes
- **Accessibility**: Apply Universal Design for Learning principles

### Instructional Design Patterns
- **Progressive Disclosure**: Use HAX components that support chunked content delivery
- **Interactive Elements**: Leverage question components, self-check activities
- **Assessment Integration**: Use formative assessment patterns with immediate feedback
- **Multimedia Support**: Properly implement video, audio, and interactive media

## Troubleshooting Patterns

### Common Cross-Repository Issues

#### Component Not Available in HAX Editor:
1. **Check**: Component exists in `webcomponents/elements/`
2. **Verify**: `haxProperties` method is properly implemented
3. **Confirm**: Component is built and published to registry
4. **Test**: Component loads properly in development environment

#### Site Build Failures:
1. **Check**: Backend compatibility with site structure
2. **Verify**: All referenced components are available
3. **Confirm**: `site.json` follows JSON Outline Schema
4. **Test**: Theme compatibility with content structure

#### CLI Command Failures:
1. **Use Local**: Use local `hax` command, not `npx` version
2. **Check Flags**: Include `--y --no-i --auto` for non-interactive execution
3. **Verify Environment**: Ensure proper directory context for command
4. **Update Tools**: Use `hax update` to ensure latest CLI version

### Performance Optimization Patterns

#### Component Bundle Size:
- **Analyze**: Use DDD tokens instead of custom CSS
- **Minimize**: Reduce external dependencies
- **Optimize**: Use lazy loading for heavy components
- **Test**: Verify load times in various network conditions

#### Site Performance:
- **Assets**: Optimize images and media in `files/` directory
- **Caching**: Leverage HAXcms built-in caching strategies
- **Components**: Use efficient component loading patterns
- **Monitoring**: Test performance across device types

## Future Learning Areas

### Emerging Patterns to Document:
- **AI Integration**: How WARP learns from HAX ecosystem usage patterns
- **Component Evolution**: Tracking component migration from SimpleColors to DDD
- **Educational Effectiveness**: Measuring impact of OER Schema implementation
- **Developer Experience**: Optimizing WARP assistance for HAX workflows

### Knowledge Gaps to Address:
- **Advanced Theme Development**: Complex theme inheritance patterns
- **Microservice Integration**: Deep integration with open-apis services
- **Multi-language Support**: Internationalization across ecosystem
- **Enterprise Integration**: HAX in larger institutional contexts

---

*This document evolves with each WARP interaction in the HAX ecosystem. Update it as new patterns emerge or workflows are optimized.*