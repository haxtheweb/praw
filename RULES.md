# HAX Ecosystem Warp AI Agent Rules

This document contains all comprehensive rules for Warp AI agents working within the HAX ecosystem. These rules are organized by category and precedence to ensure consistent, high-quality development practices.

## Rule Precedence System

**CRITICAL**: Rules are listed in **ASCENDING ORDER OF PRECEDENCE**
- Rules that appear **LATER** in the list take precedence over rules that appear **EARLIER**
- Project-specific rules (with file paths) take precedence over personal rules
- Subdirectory rules override parent directory rules
- When conflicts exist, **ALWAYS** follow the rule that appears **LAST**

### Precedence Hierarchy
1. **Personal Rules** (lowest precedence)
2. **Ecosystem-wide Rules** 
3. **Project Rules** (higher precedence)
4. **Subdirectory Rules** (highest precedence)

## 🏗️ Architecture & File Structure Rules

### HAXcms Site Organization
- **Rule ID**: `ZVEm3yg7jTXBsXBOp3yPzy`
- **Content**: For the HAXcms site, all documentation is located in the `docs` folder. The site structure includes `site.json` for page order in JSON outline schema format, all files are under the `files` folder, and all page HTML content is in the `pages` folder. Documentation should ensure coverage of pillars, pedagogical ontology, and relevant projects referenced in AGENTS.md to maintain comprehensive ecosystem context.

### HAXcms Site Metadata
- **Rule ID**: `rHQ7lLRZmZlnFveLrWslUN`
- **Content**: In a site.json / hax site the metadata.site.name property is used to help establish the correct basePath in some scenarios. This value should not be modified to be anything other than put into alignment with the name of the folder the site is named.

### Reserved Routes
- **Rule ID**: `Q4D9hL9sFNORlMPt1z2ZEb`
- **Content**: The `x/` prefix for routes is reserved for internal HAXcms paths such as `x/search` and `x/tags`.

### Web Component Registry
- **Rule ID**: `69qEidWQwmAfq9eWziwMLn`
- **Content**: wc-registry.json is a file that is built by the ubiquity script and is used for our "magic script". This register contains references to every valid web component that we publish on our CDN and is hydrated based on tag-name being undefined, detected in the DOM, and then imported dynamically at the associated object key.

### Issue Tracking
- **Rule ID**: `tJnuFVxe11BgToleU8oPxK`
- **Content**: For any git repository in or below the current working directory, issues should be checked against the unified issue queue located at `~/Documents/git/haxtheweb/issues`.

### HAXcms Backend Security/Parity
- **Rule ID**: `a8bf4a47-3d4f-4f8e-a356-a04db66ce1ab`
- **Content**: Anytime an audit or security issue is raised for either `haxcms-nodejs` or `haxcms-php`, verify and resolve it in both backends to maintain feature parity and security consistency.

## 🎨 Design System Standards

### DDD Design System (Primary)
- **Rule ID**: `MLhl56jNSqHvnRiAW5A2GR`
- **Content**: The design system called DDD is located under the path `elements/d-d-d` and should be leveraged for fonts, colors, padding, spacing, margins and other consistency in component and site design.

### DDD Usage Audit
- **Rule ID**: `MT6HPJ9BDhA13jwSXjcmeA`
- **Content**: Whenever working on a specific webcomponent, perform a quick audit to ensure proper usage of the DDD design system.

### SimpleColors (Legacy System)
- **Rule ID**: `K0lV6BJOPrqP7iJMZkemUw`
- **Content**: We have an older color based designs system called SimpleColors. We still use this in order to fill in gaps in DDD as far as shades of all colors. SimpleColors creates a base line color spectrum for levels of red, orange, blue, etc. When possible we should be using DDD's colors instead of these, though there are elements that will still leverage it in unique situations.

### DESIGN.md Compliance (PRAW Design Source of Truth)
- **Rule ID**: `c4f0b69d-9ed4-4b6d-bf52-6a3d9937c98f`
- **Content**: For any design-related decisions in this repository, `DESIGN.md` at the repository root is the canonical source of truth. Future design work must conform to its design tokens, CSS variable implementation patterns, component guidance, and Do's/Don'ts.

## 🧩 Web Component Development

### HAX Schema Capability
- **Rule ID**: `rVsCTSDjae8lRmsJmPO3Mk`
- **Content**: Elements with a haxProperties method are HAX capable, leveraging the HAXSchema standard to interface with the HAX editor. The demoSchema part of this standard provides all necessary information to create example elements in HAX. For demos launching in codepen, use demoSchema and HAX helper methods to create valid demos with appropriate tag names, properties, and slotted content for accurate examples.

### Accessibility Audits
- **Rule ID**: `7CPveFErpSF0aZ8tKqxw0Y`
- **Content**: Whenever working on a specific webcomponent, perform a quick audit for potential accessibility enhancements without assuming issues exist, but ensure to look for them.

### JavaScript Standards
- **Rule ID**: `CEHsAztyfB2vTCwtHGGnbk`
- **Content**: When writing global scope referenced JavaScript, use `globalThis` instead of `window` for consistency.

- **Rule ID**: `hKN16ZhzB6OXTED2CkB3yP`
- **Content**: Do not use the optionalChaining syntax because our polymer parser has issues with this syntax

### HAX Content Authoring
- **Rule ID**: `eis0l9w9l2jG1COFySmvdT`
- **Content**: When you write content for hax sites make sure that the webcomponent tags you are using are things that could have been authored and put in the page. This means written using the HAX editor via elements that have HAXSchema. This registry has a list of all valid HAX capable elements and while not always used on every page, it's useful for knowing what is possible. Some times supplying visually interesting content helps with engagement for video, table, and block element data. Also keep in mind the DDD attributes that we support to help make headings and paragraph content offset in a consistent way.

### a11y-collapse heading-button
- **Rule ID**: `a11y-collapse-heading-button`
- **Content**: When using a11y-collapse, ensure that the `heading-button` property is set on the HTML element to make it easier for the end user to click the whole heading to expand the content. Without it, only the small toggle icon is clickable; with it, the entire heading bar becomes a clickable button, which is a better UX.

### Educational Content Standards
- **Rule ID**: `c3XjsqFbCmoA3cxsooNyxG`
- **Content**: When creating educational elements within HAX, attempt to apply the OER Schema metadata parameters to ensure consistent semantic structure and interoperability.

## ⚙️ Build & Development Workflow

### HAX CLI Usage
- **Rule ID**: `ip9IudNwZrZQsyk4ggvCzH`
- **Content**: When running hax commands don't do npx, instead use the local copy that we have as it is always the latest or even experimental as the source starts with this machine.

### Web Component Scaffolding
- **Rule ID**: `hax-webcomponent-scaffold`
- **Content**: When creating new webcomponents in the `webcomponents` monorepo, always use the `hax webcomponent` command to scaffold the element. This ensures the component is generated with the correct structure, HAX compatibility, DDD design system integration, i18n support, and follows the standard monorepo conventions. Do not create webcomponent directories or files manually in the monorepo — always scaffold with the CLI tool first.

### HAX Site Scaffolding
- **Rule ID**: `hax-site-scaffold`
- **Content**: When creating HAXcms sites for testing or any purpose, always use the `hax site` command to generate the site. This ensures the site is created in the standard deployment location with the correct structure, theme configuration, and follows HAXcms conventions. Do not create site directories or files manually — always scaffold with the CLI tool first.

### HAXcms Page Creation via CLI
- **Rule ID**: `hax-page-creation-cli`
- **Content**: Always create HAXcms site pages through the `hax` CLI (`hax site node:add` or `hax site site:items-import`), never by manually creating page directories or hand-editing `site.json`. Manual page creation bypasses the CLI's page-id generation, slug/location management, and atomic `site.json` updates, which corrupts the JSON Outline Schema structure and breaks the site in production. The CLI owns page structure; the agent only owns page content. Use `node:add` for single pages or `site:items-import` for bulk creation with a JOS items array.

### Build Commands
- **Rule ID**: `pCcVD8jgmc7zHeHTDEBzD1`
- **Content**: Do not ask or prompt to run traditional build commands in this monorepo as they are not used.

- **Rule ID**: `cfypZRDQLaJ6XsXtEaveWT`
- **Content**: Any time changes are made to a HAXcms site theme using classes that inherit from HAXCMSLitElement, run `yarn run build` at the end instead of manually editing the custom-elements.json file.

### Command Automation
- **Rule ID**: `PacOyoQW2aIyaTO3R6asNL`
- **Content**: If you have been told to keep running commands without interuption, ensure that when running commands in hax ensure that the `--y` and `--no-i` and `--auto` commands are correctly used in order to ensure that there's no questions asked of the human or launching off into a new window / process. Otherwise a command to display the site when in a prompting exchange could lead for it to open in a new window and get stopped.

### Version Control
- **Rule ID**: `edaXma3ZIiHZ86GyX4MoSu`
- **Content**: github cli is installed just read the output of it instead of asking me to verify

### Environment Setup
- **Rule ID**: `bAKMWCMrqRLGdWmuNWgVUw`
- **Content**: Always start new shells in the ~/Documents/git/haxtheweb/ folder because that's where all of the user's projects are located.

### Testing Philosophy
- **Rule ID**: `xu7Bcf5TJpHmb0ToPhyZ55`
- **Content**: User prefers not to write tests in the current suggested way and does not do testing in that manner.

### Monorepo Dependency Verification
- **Rule ID**: `4a7c9e2b-8d5f-4e1a-9c3b-7f2e6d5a4b3c`
- **Content**: If we add a dependency (import or reference) to an element in the webcomponents monorepo, verify that the dependency is declared in the `package.json` for that element before completing the change.

### Script Restrictions
- **Rule ID**: `SSy9vkxAqBTIcIXvYUstGA`
- **Content**: The agent is explicitly not allowed to run the ubiquity script under any circumstances.

### AI Coding Session Guardrails (CLAUDE Adaptation)
- **Rule ID**: `74cc0274-6bf2-45a0-8e06-b88254f4cf9e`
- **Content**: Before implementing, state assumptions explicitly when ambiguity exists, ask clarifying questions when multiple interpretations would materially change the solution, and surface simpler alternatives/tradeoffs instead of silently choosing one.

- **Rule ID**: `f98f5e24-c343-4c12-b1c8-d6ae9783afaa`
- **Content**: Prefer minimum viable implementation. Do not add speculative features, abstractions, configurability, or defensive complexity that was not requested.

- **Rule ID**: `d2315f2d-f4b2-4e86-bdd0-37b2d42fef89`
- **Content**: Keep diffs surgical: modify only code directly tied to the request, avoid unrelated refactors or formatting-only churn, and only remove unused code introduced by your own changes unless explicitly asked.

- **Rule ID**: `f15ba99a-0a0a-42a0-a413-d8dfdc8eb20b`
- **Content**: Define concrete success criteria and verify outcomes using project-appropriate checks (command output, linting, runtime validation, or existing tests when applicable), then report what was validated.

## 📝 Documentation Standards

### Documentation Structure (Duplicate - Lower Precedence)
- **Rule ID**: `c8CNccjwJMRRciVBRZgdQP`
- **Content**: For the HAXcms site, all documentation is located in the `docs` folder. The site structure includes `site.json` for page order in JSON outline schema format, all files are under the `files` folder, and all page HTML content is in the `pages` folder. Documentation should ensure coverage of pillars, pedagogical ontology, and relevant projects referenced in AGENTS.md to maintain comprehensive ecosystem context.

## 🧠 Instructional Design

### HAX Course Units via Understanding by Design
- **Rule ID**: `a1b2c3d4-e5f6-4789-9abc-def012345678`
- **Content**: When designing or redesigning a HAX course unit (or course/program) whose goal is student understanding, use the Understanding by Design (UbD) backward-design workflow: start from desired results (big ideas, enduring understandings as full-sentence propositions, overarching + topical essential questions, knowledge/skills, and predictable misunderstandings that are pre-assessed and confronted), then determine acceptable evidence (a scrapbook of performance tasks via GRASPS, academic prompts, quiz/test items, and informal checks; a six-facet rubric; the 7-question validity self-test; longitudinal reliability), then plan learning experiences (WHERETO sequence; uncoverage over coverage; feedback/revision cycles). Avoid the two "twin sins": activity-oriented design (fun activities with no aligned understanding target) and coverage (textbook march with no big-idea depth). Use the `hax-ubd-*` skills (`hax-ubd-backward-design` orchestrator, `hax-ubd-stage1/2/3`, `hax-ubd-unit-audit`, and the `hax-ubd-essential-questions` / `hax-ubd-grasps` / `hax-ubd-six-facets` companions); persist each unit's design in a manifest at `files/ubd/<unit-slug>.manifest.json`. Compose with `grad-blooms` (which owns cognitive level/verb — UbD owns goal framing) and `hax-content-chunking-audit` (which owns page-level load — UbD owns unit-level alignment). A single lesson is too short for UbD; design at unit scope or larger. Map every UbD construct to a real, HAX-authorable element (e.g., GRASPS context via `video-player`/`media-playlist`/`audio-player`/`image-compare-slider`; constructed response via `simple-fields`; rubric via `editable-table`; reflection via `stop-note`; retrieval via `self-check`/`flash-card`; selected response via `multiple-choice`/`fill-in-the-blanks`/`matching-question`/`sorting-question`/`tagging-question`) — never invent tag names. See the skill family at `praw/.agents/skills/hax-ubd-*` and the source framework in Wiggins & McTighe (2005), *Understanding by Design* (Expanded 2nd ed.).

## 🗂️ Project-Specific Rules

### HAX Ecosystem Master Rule (HIGHEST PRECEDENCE)
- **Rule ID**: `~/Documents/git/haxtheweb/praw/WARP.md`
- **Content**: [Complete HAX Ecosystem Development Rules - See WARP.md for full content]

This master rule contains comprehensive guidelines for:
- HAX Ecosystem Overview
- Architecture & File Structure
- Design System Standards  
- Web Component Development
- Build System & Development Workflow
- Educational & Pedagogical Context
- HAX Cloud Infrastructure
- Advanced HAX Patterns
- Security Considerations
- Community & Support

## 📋 Rule Management System

### Adding New Rules
1. Add the rule to this RULES.md file under the appropriate category
2. Assign a unique Rule ID (use UUID format for new rules)
3. Document the rule content and context
4. Update precedence order if needed
5. Cross-reference with related WARP.md files

### Updating Existing Rules
1. Locate the rule by Rule ID in this document
2. Update the content while preserving the Rule ID
3. Note any precedence changes needed
4. Update related WARP.md files if necessary

### Rule Categories
- **🏗️ Architecture & File Structure**: Site organization, routing, file systems
- **🎨 Design System Standards**: DDD, SimpleColors, theming guidelines
- **🧩 Web Component Development**: HAX capability, accessibility, JavaScript standards
- **⚙️ Build & Development Workflow**: CLI usage, build commands, version control
- **📝 Documentation Standards**: Content creation, documentation structure
- **🗂️ Project-Specific Rules**: Rules that apply to specific projects or directories

### Cross-References
This RULES.md file works in conjunction with:
- `~/Documents/git/haxtheweb/praw/WARP.md` (Master HAX ecosystem rules)
- `~/Documents/git/haxtheweb/praw/webcomponents/WARP.md` (Web component specific rules)
- `~/Documents/git/haxtheweb/praw/haxcms/WARP.md` (HAXcms specific rules)  
- `~/Documents/git/haxtheweb/praw/design-system/WARP.md` (Design system specific rules)

## 🔄 Future Rule Management

All future RULES work should:
1. **Read from** this repository for existing rules
2. **Write to** this repository for new rules
3. **Update** this RULES.md file as the central registry
4. **Reference** appropriate WARP.md files for detailed context
5. **Maintain** precedence order and rule relationships
6. **Log emergent knowledge** in KNOWLEDGE.md for insights that may become rules

### Knowledge Capture Process

**For emergent insights and learnings:**
- Log decisions, patterns, and discoveries in `KNOWLEDGE.md`
- Use the structured template for consistency
- Mark potential rules with `Candidate: Yes`
- Promote stable knowledge items to formal rules in this file
- Link back to KNOWLEDGE.md entries for context and rationale

---

*This document serves as the authoritative registry for all HAX ecosystem Warp AI agent rules. It should be updated whenever new rules are created or existing rules are modified.*