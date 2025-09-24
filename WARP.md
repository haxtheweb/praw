# HAX Ecosystem Development Rules

This file contains the comprehensive development guidelines and conventions for the HAX ecosystem. HAX (Headless Authoring eXperience) is a comprehensive web development ecosystem that enables rapid creation of accessible, performant web components and static sites. These rules ensure consistency, quality, and proper integration across all HAX projects and web components.

## HAX Ecosystem Overview

The HAX ecosystem consists of multiple interconnected repositories serving specific purposes:

### Core Repositories
- **`webcomponents`** - The heart of HAX: a monorepo containing 250+ LitElement-based web components, themes, and the DDD design system
- **`create` (@haxtheweb/create)** - The HAX CLI tool for scaffolding new web components, HAXsites, and managing development workflow
- **`haxcms-php`** - PHP backend implementation providing content management, API endpoints, and server-side rendering
- **`haxcms-nodejs`** - Node.js backend implementation offering same capabilities as PHP version
- **`desktop`** - Electron-based desktop application providing local development environment

### Supporting Repositories
- **`hax11ty`** - Integration layer bridging HAX components with Eleventy (11ty) static site generator
- **`json-outline-schema`** - Defines JSON schema used by HAXcms for content structure and navigation
- **`hax-schema`** - Contains HAX property schemas defining web component integration with HAX authoring interface
- **`open-apis`** - Microservice APIs and shared infrastructure deployed at https://open-apis.hax.cloud/
- **`docs`** - Official HAX documentation site built as HAXcms site with comprehensive ecosystem documentation
- **`issues`** - Unified issue tracking repository for entire HAX ecosystem

### Development Philosophy & Community Pillars

HAX is built on community pillars that guide all development decisions and community interactions:

#### Core Pillars
- **Accessible**: Maximizes accessibility while removing knowledge required to maintain accessibility standards (WCAG 2.0 AA)
- **Extensible**: Built for sustainable extension through web standards, microservices, and modular architecture
- **Free and Open**: Open community embracing 5Rs of OER (Retain, Reuse, Revise, Remix, Redistribute)
- **Efficient**: Optimized for performance through web standards over heavy libraries, lazy loading, offline capability
- **Platform Agnostic**: Works anywhere - standalone HAXsites, integrated HAXcms, static pages, existing CMS platforms
- **Remixable**: Maximizes remix-ability through modular design, open licensing, semantic content structures
- **Sustainable**: Environmental, technological, and community sustainability

#### Technical Emphasis
- **Rapid Development**: Scaffolding tools and design systems accelerate creation
- **Unbundled Delivery**: Pure JavaScript, HTML, CSS approach without compilation steps
- **Modularity**: Components work independently and compose together seamlessly
- **Ubiquitous Web**: Content should "just work" regardless of how it was built

## Architecture & File Structure

### HAXcms Site Structure
- All documentation is located in the `docs` folder
- Site structure uses `site.json` for page order in JSON outline schema format
- All files are stored under the `files` folder
- All page HTML content is in the `pages` folder
- Documentation should ensure coverage of pillars, pedagogical ontology, and relevant projects referenced in AGENTS.md to maintain comprehensive ecosystem context
- The `x/` prefix for routes is reserved for internal HAXcms paths such as `x/search` and `x/tags`
- In `site.json` / HAX site, the `metadata.site.name` property should align with the folder name and should not be modified to be anything else

### Web Component Registry
- `wc-registry.json` is built by the ubiquity script and used for our "magic script"
- Contains references to every valid web component published on our CDN
- Hydrated based on tag-name being undefined, detected in the DOM, then imported dynamically
- **CRITICAL**: The agent is explicitly not allowed to run the ubiquity script under any circumstances

## Design System Standards

### DDD Design System (Primary)
- Located under `elements/d-d-d` path
- Should be leveraged for fonts, colors, padding, spacing, margins and other consistency in component and site design
- Always perform a quick audit to ensure proper usage of the DDD design system when working on web components
- DDD should be used instead of SimpleColors when possible

### SimpleColors (Legacy/Supplementary)
- Older color-based design system still used to fill gaps in DDD
- Creates baseline color spectrum for levels of red, orange, blue, etc.
- Use only when DDD doesn't provide the required color variations

## Web Component Development

### HAX Capability & Schema
- Elements with a `haxProperties` method are HAX capable, leveraging the HAXSchema standard
- The `demoSchema` part provides all necessary information to create example elements in HAX
- For demos launching in CodePen, use `demoSchema` and HAX helper methods to create valid demos with appropriate tag names, properties, and slotted content
- When writing content for HAX sites, ensure webcomponent tags are authored elements that could be put in pages via the HAX editor
- Supply visually interesting content for engagement (video, table, block element data)
- Keep in mind DDD attributes for consistent heading and paragraph content offset

### Accessibility Standards
- Always perform a quick audit for potential accessibility enhancements when working on web components
- Don't assume issues exist, but ensure to look for them systematically

### JavaScript-Only Architecture
- **Language**: Pure JavaScript with LitElement for web components
- **NO TypeScript**: HAX strictly avoids TypeScript to eliminate compilation requirements
- **Unbundled Approach**: Components ship as native JS/HTML/CSS for maximum compatibility
- **Third-party Libraries**: When using libraries written in TypeScript, always import the pre-compiled JavaScript distribution
- **External Dependencies**: Leverage libraries like `vaadin-upload`, `shoelace-carousel`, etc. but always use their JS builds

### JavaScript Standards
- **Global References**: Use `globalThis` instead of `window` for consistency across environments
- **Formatting**:
  - Use single quotes (`'`)
  - Avoid semicolons where possible
  - Prefer functional programming patterns
  - Use Prettier for consistent formatting
- **ES Modules**: Use standard ES6 import/export syntax
- **Modern JavaScript**: Leverage ES2018+ features while maintaining browser compatibility
- **Optional Chaining**: Do not use optional chaining syntax (`?.`) because our Polymer parser has issues with this syntax

### Educational Content
- When creating educational elements within HAX, apply OER Schema metadata parameters to ensure consistent semantic structure and interoperability

## Setup Commands & HAX CLI Usage

### Installation
- **Install HAX CLI globally**: `npm install @haxtheweb/create --global`
- **Alternative usage**: `npx @haxtheweb/create` or `npm init @haxtheweb`
- **Update HAX CLI**: `hax update`

### Core Commands
- **Start interactive CLI**: `hax start` (launches interactive CLI with ASCII art via Clack)
- **Start development server**: `hax serve` (launches site at http://localhost)
- **Create web component**: `hax webcomponent my-element --y` (creates LitElement with DDD and i18n)
- **Create HAXsite**: `hax site mysite --y` (generates HAXcms-based static site)
- **DDD compliance audit**: `hax audit` (checks CSS against DDD design system standards)

### CLI Command Options
- `--v`: Verbose output
- `--debug`: Developer-focused output
- `--y` or `--auto`: Auto-accept all prompts
- `--no-i`: Prevent interactive sub-processes (ideal for scripting)
- `--skip`: Skip animations for faster execution
- `--quiet`: Suppress console logging
- `--writeHaxProperties`: Write haxProperties for web components
- `--custom-theme-name <name>`: Custom theme name for HAXsites
- `--custom-theme-template <template>`: Theme template (base, polaris-flex, polaris-sidebar)
- `--import-site <url>`: URL of site to import
- `--import-structure <method>`: Import method (pressbooksToSite, htmlToSite, etc.)

## Build System & Development Workflow

### Build Process Understanding
HAX uses a sophisticated build pipeline optimized for unbundled JavaScript delivery:
1. **Gulp**: Handles asset compilation and processing
2. **Prettier**: Ensures consistent code formatting
3. **CEM (Custom Elements Manifest)**: Generates `custom-elements.json` for component metadata
4. **Lerna**: Manages monorepo dependencies and publishing
5. **No TypeScript Compilation**: Pure JavaScript workflow eliminates build complexity

### Build Commands
- **Standard build**: `yarn run build` (from component root)
  - Compiles assets, formats code, generates custom-elements.json
  - **CRITICAL**: Always run after changes to HAXCMSLitElement themes
  - Do NOT manually edit `custom-elements.json` - it's auto-generated
- **Development build**: `yarn run dev` (with watching)
- **Monorepo build**: `yarn run build` (from webcomponents root)

### Command Usage Standards
- When running HAX commands, don't use `npx` - instead use the local copy as it's always the latest or experimental
- For HAXcms site theme changes using classes that inherit from HAXCMSLitElement, run `yarn run build` at the end instead of manually editing `custom-elements.json`
- Do not ask or prompt to run traditional build commands in this monorepo as they are not used
- When running commands in HAX, ensure `--y`, `--no-i`, and `--auto` flags are used to prevent interruptions and avoid launching new windows/processes

### Version Control
- For any git repository in or below the current working directory, check issues against the unified issue queue at `~/Documents/git/haxtheweb/issues`
- GitHub CLI is installed and available for use

### Testing Philosophy
- User prefers not to write tests in the current suggested way and does not do testing in the traditional manner

## Environment Setup

### Directory Structure
- Always start new shells in the `~/Documents/git/haxtheweb/` folder where all projects are located
- Project structure follows monorepo patterns with specialized subdirectories

### Tool Configuration  
- Local HAX tooling should be used instead of global installations
- Avoid interactive or fullscreen commands that could interrupt workflow

## Content Creation Guidelines

### HAX Site Content
- Use web component tags that are HAX-capable and available in the registry
- Leverage DDD attributes for consistent styling
- Provide engaging visual content (videos, tables, block elements) when appropriate
- Ensure all content can be authored through the HAX editor interface

### Documentation Standards
- Maintain comprehensive ecosystem context in all documentation
- Reference pillars and pedagogical ontology where relevant
- Ensure coverage aligns with projects mentioned in AGENTS.md

## Quality Assurance

### Component Audits
When working on web components, perform these audits:
1. **Design System Compliance**: Verify proper DDD usage
2. **Accessibility**: Check for enhancement opportunities  
3. **HAX Schema**: Ensure proper HAX capability implementation
4. **Code Standards**: Verify JavaScript best practices

### Consistency Checks
- Verify naming conventions align with folder structures
- Ensure metadata properties match expected values
- Check that routing doesn't conflict with reserved `x/` prefix

## Educational & Pedagogical Context

HAX has deep roots in educational technology, evolving from over a decade of work in online learning:

### Educational Heritage
- **ELMS:LN Legacy**: HAX evolved from ELMS Learning Network (2012-2022), a Next Generation Digital Learning Environment (NGDLE)
- **OER Commitment**: Embraces the 5Rs of Open Educational Resources (Retain, Reuse, Revise, Remix, Redistribute)
- **Instructional Design Focus**: Built-in support for pedagogical patterns through specialized components

### Educational Components
HAX includes purpose-built components for learning:
- **Question Types**: Multiple choice, fill-in-blanks, drag-and-drop, true/false, short answer, sorting, tagging
- **Instructional Tools**: Self-check activities, stop notes, timelines, math notation (MathML/LaTeX)
- **Assessment Features**: Immediate feedback, progressive disclosure, formative assessment patterns
- **Accessibility in Learning**: Screen reader compatibility, keyboard navigation, high contrast support

### Pedagogical Patterns
- **Chunked Content**: Break complex topics into digestible components
- **Active Learning**: Interactive elements encourage engagement over passive consumption
- **Universal Design for Learning**: Multiple means of representation, engagement, and expression
- **Evidence-Based Design**: Components based on learning science research

## HAX Cloud Infrastructure

### HAX.cloud Services
HAX leverages cloud infrastructure at https://hax.cloud for:
- **CDN**: Content delivery network for component libraries
- **AI Services**: Content analysis and processing capabilities
- **Documentation**: Centralized documentation and community resources
- **Open Infrastructure**: Publicly available APIs and services

### Microservice Architecture
- **open-apis.hax.cloud**: Conversion, analysis, and processing services
- **Stateless Design**: Services designed for scalability and reliability
- **REST APIs**: Standard HTTP interfaces for integration
- **Vercel Deployment**: Serverless functions for optimal performance

## Advanced HAX Patterns

### Content Import & Migration
Supported import methods:
- `pressbooksToSite` - Academic textbook platform
- `elmslnToSite` - ELMS Learning Network
- `haxcmsToSite` - Between HAXcms instances
- `notionToSite` - Notion workspace
- `gitbookToSite` - GitBook documentation
- `evolutionToSite` - Evolution CMS
- `htmlToSite` - Generic HTML import
- `docxToSite` - Microsoft Word documents

### External Library Integration
- **Vaadin Components**: Import from `@vaadin/[component]/[component].js`
- **Shoelace Components**: Import from `@shoelace-style/shoelace/dist/components/[component]/[component].js`
- **Other Libraries**: Always use the `/dist/` or compiled JavaScript version
- **Open APIs**: Leverage https://open-apis.hax.cloud/ for conversion, analysis, and processing services
- **Avoid**: Direct TypeScript imports or source files requiring compilation

### Repository Structure
```
~/Documents/git/haxtheweb/
├── webcomponents/           # Component library & themes
│   └── elements/           # Individual components
│       ├── d-d-d/         # Design system
│       └── [250+ more]/   # All other components
├── create/                 # HAX CLI tool
├── haxcms-php/            # PHP backend
├── haxcms-nodejs/         # Node.js backend
├── desktop/               # Electron app
├── hax11ty/              # 11ty integration
├── json-outline-schema/   # Content schemas
├── hax-schema/           # HAX property schemas
├── open-apis/            # Microservice APIs
├── docs/                 # Official HAX documentation
└── issues/               # Unified issue tracking
```

### Security Considerations
- Keep dependencies updated before running `npm install`
- Avoid committing API keys or sensitive data to `package.json`, `site.json`, or public files
- Validate source URLs when using `--import-site` to prevent malicious content
- Sanitize user inputs in custom components
- Only import from trusted, well-maintained JavaScript distributions

### Community & Support
- **HAX Community**: Run `hax party` for involvement opportunities
- **Discord**: https://bit.ly/hax-discord
- **Issue Reporting**: Use `haxtheweb/issues` or GitHub interface
- **Documentation**: Run `man hax` (Linux/macOS) for comprehensive CLI docs
- **Educational Resources**: Complete documentation at https://haxtheweb.org/

---

*This file serves as the authoritative guide for HAX ecosystem development. All contributors should familiarize themselves with these standards to maintain consistency and quality across the platform.*
