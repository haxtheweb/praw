# WARP Learning Context - HAX Ecosystem Integration

This document captures learned patterns, discovered workflows, and integration knowledge for how WARP should work effectively across the entire HAX ecosystem.
## Indexed External Worldview Sources
### `btopro/blog` (Bryan Ollendyke long-form corpus)
- Path (local): `~/Documents/git/btopro/blog`
- Path (served): `https://btopro.com`
- Path (source mirror): `https://github.com/btopro/blog`
- Scope: writing across life/work/research/philosophy, indexed for HAX, ELMS:LN, education, edtech, web architecture, open source, building, and community themes
- Exclusion filter for worldview synthesis: hockey and family-centric material unless directly tied to educational technology strategy
- Normalized worldview artifact in this repository: `WORLDVIEW.md`

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

## HAX Conceptual Architecture (Deep Understanding Map)

This section captures the conceptual architecture of HAX as understood through code inspection and direct clarification from the project lead. It is organized to help future agents quickly orient on how concepts relate to each other.

### The HAX Editor Context Spectrum

HAX operates across a spectrum of deployment contexts, and behavior changes based on context:

1. **Standalone HAX editor** (`hax-body` + `hax-tray` + `hax-store`): Fully client-side in-page editing. Works without any backend. Content can be authored and exported as HTML. File upload and app-store integrations (media sources, content services) require a backend.

2. **HAX inside HAXcms** (adds `haxcms-site-store` + `haxcms-site-editor-ui` + admin dialogs + themes): Full CMS experience with page management, site navigation, themes, and backend persistence. The editor is wrapped by site-level concerns.

3. **HAX via HAXiam** (adds multi-tenant auth, per-user directory isolation, SSO): Institutional deployment where HAXcms serves many users, each with their own sites directory. Layers SAML/CAS/OIDC SSO on top of the JWT system.

4. **HAX Desktop** (Electron wrapper): Local development environment providing HAXcms capabilities without a remote server.

The key insight: `hax-body` and `hax-tray` have **zero knowledge of HAXcms**. The CMS layer wraps the editor, not the other way around. This is the "headless authoring" principle in practice.

### State Management Architecture

```
HAXStore (MobX)                    haxcms-site-store (MobX)
├── activeNode                     ├── manifest (site.json)
├── editMode                       ├── activeItem (current page)
├── activeGizmo                    ├── routerManifest
├── globalPreferences              ├── themeData
├── elementAlign                   ├── siteTitle, siteDescription
├── tourOpened                     ├── userData
└── [editor-scoped state]          └── [site/CMS-scoped state]
           \                            /
            \                          /
         haxcms-site-editor-ui (bridge)
              ├── edit/save toggle
              ├── admin dialogs
              ├── Merlin integration
              └── backend API calls
```

### Gizmos, Stax, and Content Architecture

- **Gizmo**: A single web component registered with HAX via `haxProperties`. The gizmo definition describes how it appears in the gizmo browser (icon, title, groups, handles) and how HAX configures it (settings forms).
- **Stax**: Pre-composed multi-element templates (e.g., a hero section = grid-plate + media-image + heading). Currently developer-defined only. User-saveable stax is a desired but not yet implemented feature.
- **haxHooks**: Lifecycle hooks that let elements participate in HAX state changes without importing HAX. Includes: `activeElementChanged`, `editModeChanged`, `inlineContextMenu`, `gizmoRegistration`, `preProcessNodeToContent`, `progressiveEnhancement`, `postProcessNodeToContent`, `preProcessInsertContent`.
- **demoSchema**: Array of demo configurations shipped with each gizmo. Used for drag-and-drop placeholders, CodePen demos, and visual examples in the gizmo browser.

### Admin Dialog System

Dialogs in `haxcms-elements/lib/core/`:
- `haxcms-content-admin-dialog.js` — Page content metadata
- `haxcms-files-admin-dialog.js` — File/media management
- `haxcms-seo-admin-dialog.js` — SEO and metadata
- `haxcms-appearance-admin-dialog.js` — Theme and visual settings
- `haxcms-outline-editor-dialog.js` — Page hierarchy/reordering
- `ui/haxcms-about-dialog-ui.js` — Site information

Access pattern: Merlin program invocation OR admin overview panel. Form data flows: dialog form → backend API endpoint → site.json/page update.

### Theme Lifecycle

1. **Creation**: `hax site --custom-theme-name myTheme` generates a full LitElement class extending `HAXCMSLitElementTheme`.
2. **Template options**: `--custom-theme-template` selects from base, polaris-flex, polaris-sidebar starting points.
3. **Registration**: Theme registers via `HAXCMSThemeWiring` and is discoverable by the theme picker.
4. **Global stylesheet**: Themes can inject global CSS via `HAXCMSGlobalStyleSheetContent()` for styles that must escape shadow DOM (like DDD palette selectors).
5. **Build**: After theme changes, `yarn run build` regenerates `custom-elements.json`.

### Micro-Frontend-Registry

- **Role**: Service discovery layer that connects HAX to external microservices.
- **Primary target**: `open-apis.hax.cloud` (conversion, analysis, processing services).
- **Flexibility**: Can be rerouted to point at alternative service endpoints.
- **Usage pattern**: `import { MicroFrontendRegistry } from "@haxtheweb/micro-frontend-registry/micro-frontend-registry.js"` + `enableServices([...])` to activate specific service integrations.

### Site Creation Flow (app-hax v2)

- Site creation has its own **dedicated UI** in the app-hax dashboard (not a Merlin program).
- **Skeletons** are starting templates that populate new sites with pre-built structure and content.
- Skeleton resolution follows precedence: user-defined → config-level → core-level.
- Skeletons are JSON files containing build instructions and metadata.
- The backend resolves skeletons by machine name matching against filename, meta.machineName, or meta.name.

### Site Insights / Reports Dashboard

- **Current state**: `haxcms-site-insights.js` currently calls open-apis endpoints to assemble and churn site information.
- **Planned migration**: Data source should move from open-apis to **site-local `x/api` endpoints** (planned, not yet implemented). These endpoints would serve structured data about the site under the reserved `x/` route prefix.
- **Vision**: A dashboard providing actionable insights to the site author:
  - Content analysis (what's in the site, content quality metrics)
  - Accessibility auditing results
  - Usage reports
  - Last updated timestamps and change frequency
  - Other site statistics
- **Architecture note**: x/api endpoints should be designed as site-local APIs that the frontend dashboard consumes without external dependencies, improving privacy, reliability, and offline capability.

### Miscellaneous Architecture Notes

- **haxcms-cheat-codes.js**: Easter egg / fun developer features (not functional debug tooling).
- **OpenAPI conformance**: Backend endpoints are annotated with `@OA\Post`/`@OA\Get` annotations. The `openapi()` method generates swagger docs dynamically. Can also output `haxSchema` format for auto-generating forms from API parameters.

## Agent Concept Confidence Map

This map helps future agents understand which areas are well-documented in PRAW vs. which areas still need human guidance for accurate replication. Scores reflect confidence in generating accurate code/content with minimal input.

### Ecosystem Concepts
- **New web component creation**: 85% — Well understood; gap in design judgment for when to create new vs. extend existing
- **Create / CLI tooling**: 70% — Commands and flags known; internal scaffolding mechanics (skeleton resolution, theme template system) less clear
- **Multiple backends relationship**: 75% — Dependency flow clear; request routing/dispatch internals and NodeJS backend architecture less understood
- **Single vs multi-tenant (HAXiam)**: 55% — Auth model now understood; file system layout, SSO configuration, and institutional onboarding flow still need deepening
- **Pillars of development**: 90% — Well documented; gap in instinctive prioritization during real tradeoffs
- **Goals of the project**: 85% — Vision clear; current strategic priorities vs. long-term roadmap unclear

### HAXcms / HAXsite / HAX Editor Concepts
- **hax-body editing**: 65% — ContentStateManager and node operations understood; content insertion lifecycle and undo/redo state management less clear
- **hax-tray management**: 60% — Tab structure and components known; schema-to-form pipeline and tray/body coordination need deeper understanding
- **HAX Schema (haxProperties)**: 90% — Strongest area; HAXWiring.js is excellently documented
- **Merlin / super-daemon programs**: 75% — Can create programs; multi-step program chaining and completion signaling need clarification
- **Admin dialogs**: 55% — Pattern understood (Merlin + panel); form-to-API data flow for specific dialogs needs hands-on experience
- **User scaffolding**: 65% — Architecture and vision now understood; practical consumption patterns need examples
- **Open API / endpoint structure**: 60% — Annotations and swagger generation understood; complete endpoint inventory and form processing pipeline need mapping

### Identified But Underexplored Concepts
- **Dual-store architecture** (HAXStore vs site-store): Now documented in KNOWLEDGE.md
- **Theme system lifecycle**: Now documented above
- **Micro-frontend-registry**: Now documented above
- **haxHooks lifecycle**: Contract known, practical patterns need experience
- **Stax system**: Developer-defined templates; user-saveable stax is a future feature
- **app-hax sites dashboard**: Creation flow documented; deeper UI interaction patterns need exploration

## Open Questions (Remaining)

- **Lightweight analytics**: Privacy-respecting analytics is a desired gap to fill — what form should this take? xAPI? Custom events? Site-local x/api integration?
- **Content versioning**: Does HAX have or plan page-level revision history? (Git provides this at the file level, but is there a user-facing revision UI?)
- **Collaborative editing**: Is real-time multi-user editing on the roadmap or intentionally avoided?
- **Content workflow states**: Draft/review/published states — is this planned or do sites just have "published" and "editing"?

## Strategic Adoption Gap Analysis (Resolved 2026-05-07)

**Critical reframe**: As of 26.0.0+, HAX's feature set is considered to be far beyond anything else that exists. The primary gaps are NOT feature gaps. They are adoption, community, developer experience, and discoverability gaps.

### The Core Communication Challenge
Getting people to understand that "anything can become the web" and that HAX is a radically simple approach to web development and material management. The a11y, UX, publishing, and remixing capabilities all speak for themselves — the challenge is awareness and onboarding.

### Priority Adoption Gaps (Strategic Order)
1. **Documentation and examples** — Comprehensive, discoverable docs with real-world usage examples. This is the highest leverage activity.
2. **User success stories** — Demonstrating real adoption and impact to build credibility and trust.
3. **Community growth and investment** — Growing the contributor and user base through outreach, events, and onboarding.
4. **More themes** — Expanding visual options so new users see HAX as flexible, not locked to one look.
5. **Support for other design systems** — Beyond DDD, enabling organizations to bring their own design tokens and visual identity.
6. **Improved SEO via SSR / hax11ty** — Implementing hax11ty as a Merlin program to ensure published sites are optimized for search engines and deployment.
7. **AI project demonstrations** — Current AI work needs to be shown, presented on, and talked about to build awareness.
8. **Discoverability and adoption curve** — Making it easier to find HAX, understand it, and get started (beyond migration tools, which already exist).
9. **Developer experience (DX)** — Making it easier for the developer community to adopt, understand, and extend HAX.
10. **Extensibility patterns** — Modular extension system similar to Drupal modules, GravCMS plugins, WordPress plugins. People need well-defined patterns and documentation for messing with it and extending it beyond what it does today.

### Agent Implication
When prioritizing work, favor tasks that make HAX more discoverable, documentable, and extensible over adding new capabilities. Documentation, DX improvements, theme creation, and extensibility patterns have higher strategic value than new features.

## CMS Feature Comparison (Secondary Gaps)

These are traditional CMS features that could still add value but are secondary to the adoption gaps above:

1. **Content versioning / revision history** — Git provides file-level versioning; a user-facing revision UI would add CMS parity.
2. **Content scheduling** — Publish pages at future dates. Low complexity, useful for course content.
3. **Workflow states (draft/review/published)** — Valuable for instructional design review workflows.
4. **User-saveable stax** — Already identified as desired; would let faculty build their own reusable content patterns.
5. **Learning analytics** — Lightweight, privacy-respecting engagement metrics via site-local x/api endpoints.

---

*This document evolves with each WARP interaction in the HAX ecosystem. Update it as new patterns emerge or workflows are optimized.*
