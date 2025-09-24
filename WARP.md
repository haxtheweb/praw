# HAX Ecosystem Development Rules

This file contains the comprehensive development guidelines and conventions for the HAX ecosystem. These rules ensure consistency, quality, and proper integration across all HAX projects and web components.

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

### JavaScript Standards
- Use `globalThis` instead of `window` for consistency when writing global scope referenced JavaScript
- Do not use optional chaining syntax (`?.`) because our Polymer parser has issues with this syntax

### Educational Content
- When creating educational elements within HAX, apply OER Schema metadata parameters to ensure consistent semantic structure and interoperability

## Build & Development Workflow

### Command Usage
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

---

*This file serves as the authoritative guide for HAX ecosystem development. All contributors should familiarize themselves with these standards to maintain consistency and quality across the platform.*