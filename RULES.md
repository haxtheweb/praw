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

### Educational Content Standards
- **Rule ID**: `c3XjsqFbCmoA3cxsooNyxG`
- **Content**: When creating educational elements within HAX, attempt to apply the OER Schema metadata parameters to ensure consistent semantic structure and interoperability.

## ⚙️ Build & Development Workflow

### HAX CLI Usage
- **Rule ID**: `ip9IudNwZrZQsyk4ggvCzH`
- **Content**: When running hax commands don't do npx, instead use the local copy that we have as it is always the latest or even experimental as the source starts with this machine.

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

### Script Restrictions
- **Rule ID**: `SSy9vkxAqBTIcIXvYUstGA`
- **Content**: The agent is explicitly not allowed to run the ubiquity script under any circumstances.

## 📝 Documentation Standards

### Documentation Structure (Duplicate - Lower Precedence)
- **Rule ID**: `c8CNccjwJMRRciVBRZgdQP`
- **Content**: For the HAXcms site, all documentation is located in the `docs` folder. The site structure includes `site.json` for page order in JSON outline schema format, all files are under the `files` folder, and all page HTML content is in the `pages` folder. Documentation should ensure coverage of pillars, pedagogical ontology, and relevant projects referenced in AGENTS.md to maintain comprehensive ecosystem context.

## 🗂️ Project-Specific Rules

### HAX Ecosystem Master Rule (HIGHEST PRECEDENCE)
- **Rule ID**: `/home/bto108a/Documents/git/haxtheweb/praw/WARP.md`
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
- `/home/bto108a/Documents/git/haxtheweb/praw/WARP.md` (Master HAX ecosystem rules)
- `/home/bto108a/Documents/git/haxtheweb/praw/webcomponents/WARP.md` (Web component specific rules)
- `/home/bto108a/Documents/git/haxtheweb/praw/haxcms/WARP.md` (HAXcms specific rules)  
- `/home/bto108a/Documents/git/haxtheweb/praw/design-system/WARP.md` (Design system specific rules)

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