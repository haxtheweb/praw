# HAX Ecosystem Warp AI Agent Rules

This document is the single source of truth for HAX ecosystem Warp AI agent rules. Each rule carries a `Scope:` field that determines how it is delivered as agent context.

## Scope System

Every rule has one of four scopes:
- `global` — universal rules, always-on as Global Rules regardless of working directory. Keep this set small (critical, cross-cutting rules only).
- `webcomponents` — rules that apply only when developing HAX web components. Authoritative copy lives in `webcomponents/WARP.md`; this registry entry is the record.
- `haxcms` — rules that apply only when working on HAXcms sites/backends. Authoritative copy lives in `haxcms/WARP.md`.
- `design-system` — rules that apply only when working on the DDD/SimpleColors design system. Authoritative copy lives in `design-system/WARP.md`.

`scripts/build-rules.js` parses this file, emits `exports/rules-global.json` (the minimal always-on set to sync into Warp's Global Rules store), `exports/rules-by-scope.json` (per-scope groups for regenerating the subdirectory `WARP.md` files), and reports duplicate Rule IDs / duplicate content. `bash scripts/manage-rules.sh validate` runs the same checks.

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
- **Scope**: `haxcms`
- **Content**: For the HAXcms site, all documentation is located in the `docs` folder. The site structure includes `site.json` for page order in JSON outline schema format, all files are under the `files` folder, and all page HTML content is in the `pages` folder. Documentation should ensure coverage of pillars, pedagogical ontology, and relevant projects referenced in AGENTS.md to maintain comprehensive ecosystem context.

### HAXcms Site Metadata
- **Rule ID**: `rHQ7lLRZmZlnFveLrWslUN`
- **Scope**: `haxcms`
- **Content**: In a site.json / hax site the metadata.site.name property is used to help establish the correct basePath in some scenarios. This value should not be modified to be anything other than put into alignment with the name of the folder the site is named.

### Reserved Routes
- **Rule ID**: `Q4D9hL9sFNORlMPt1z2ZEb`
- **Scope**: `haxcms`
- **Content**: The `x/` prefix for routes is reserved for internal HAXcms paths such as `x/search` and `x/tags`.

### Web Component Registry
- **Rule ID**: `69qEidWQwmAfq9eWziwMLn`
- **Scope**: `webcomponents`
- **Content**: wc-registry.json is a file that is built by the ubiquity script and is used for our "magic script". This register contains references to every valid web component that we publish on our CDN and is hydrated based on tag-name being undefined, detected in the DOM, and then imported dynamically at the associated object key.

### Issue Tracking
- **Rule ID**: `tJnuFVxe11BgToleU8oPxK`
- **Scope**: `global`
- **Content**: For any git repository in or below the current working directory, issues should be checked against the unified issue queue located at `~/Documents/git/haxtheweb/issues`.

### HAXcms Backend Security/Parity
- **Rule ID**: `a8bf4a47-3d4f-4f8e-a356-a04db66ce1ab`
- **Scope**: `haxcms`
- **Content**: Anytime an audit or security issue is raised for either `haxcms-nodejs` or `haxcms-php`, verify and resolve it in both backends to maintain feature parity and security consistency.

### MFR Call Namespacing (`@system/` and `@site/`)
- **Rule ID**: `82dc87fd-6bc1-4d20-9d68-5b077bb88b89`
- **Scope**: `haxcms`
- **Content**: System-level calls (site imports, file format conversions, operations not scoped to a single site) must use the MicroFrontendRegistry (MFR) `@system/` namespace, registered from the on-premises OpenAPI spec at `/system/api/v1` (see `app-hax-system-api-registry.js` and `system-spec.yaml`; handlers in `haxcms-nodejs/src/systemRoutes/v1`). Site-scoped calls must use the `@site/` namespace (handlers in `haxcms-nodejs/src/siteRoutes/v1`); v0 site endpoints are removed. Do not add new `@haxcms/`-namespaced registrations or route new work through the legacy `create` CLI `--import-structure` v0 path — use `@system/` or `@site/` instead. (Full detail lives in `haxcms/WARP.md`.)

## 🎨 Design System Standards

### DDD Design System (Primary)
- **Rule ID**: `MLhl56jNSqHvnRiAW5A2GR`
- **Scope**: `design-system`
- **Content**: The design system called DDD is located under the path `elements/d-d-d` and should be leveraged for fonts, colors, padding, spacing, margins and other consistency in component and site design.

### DDD Usage Audit
- **Rule ID**: `MT6HPJ9BDhA13jwSXjcmeA`
- **Scope**: `webcomponents`
- **Content**: Whenever working on a specific webcomponent, perform a quick audit to ensure proper usage of the DDD design system. (Design-system detail lives in `design-system/WARP.md`.)

### SimpleColors (Legacy System)
- **Rule ID**: `K0lV6BJOPrqP7iJMZkemUw`
- **Scope**: `design-system`
- **Content**: We have an older color based designs system called SimpleColors. We still use this in order to fill in gaps in DDD as far as shades of all colors. SimpleColors creates a base line color spectrum for levels of red, orange, blue, etc. When possible we should be using DDD's colors instead of these, though there are elements that will still leverage it in unique situations.

### DESIGN.md Compliance (PRAW Design Source of Truth)
- **Rule ID**: `c4f0b69d-9ed4-4b6d-bf52-6a3d9937c98f`
- **Scope**: `design-system`
- **Content**: For any design-related decisions in this repository, `DESIGN.md` at the repository root is the canonical source of truth. Future design work must conform to its design tokens, CSS variable implementation patterns, component guidance, and Do's/Don'ts.

## 🧩 Web Component Development

### HAX Schema Capability
- **Rule ID**: `rVsCTSDjae8lRmsJmPO3Mk`
- **Scope**: `webcomponents`
- **Content**: Elements with a haxProperties method are HAX capable, leveraging the HAXSchema standard to interface with the HAX editor. The demoSchema part provides all necessary information to create example elements in HAX. For demos launching in codepen, use demoSchema and HAX helper methods to create valid demos with appropriate tag names, properties, and slotted content for accurate examples.

### Accessibility Audits
- **Rule ID**: `7CPveFErpSF0aZ8tKqxw0Y`
- **Scope**: `webcomponents`
- **Content**: Whenever working on a specific webcomponent, perform a quick audit for potential accessibility enhancements without assuming issues exist, but ensure to look for them.

### JavaScript Standards — globalThis
- **Rule ID**: `CEHsAztyfB2vTCwtHGGnbk`
- **Scope**: `webcomponents`
- **Content**: When writing global scope referenced JavaScript, use `globalThis` instead of `window` for consistency.

### JavaScript Standards — No optional chaining
- **Rule ID**: `nJF4SYUGdN5Wr5tEvaDtGY`
- **Scope**: `webcomponents`
- **Content**: Do not use the optional chaining syntax (`?.`) because the current toolchain / Polymer parser has issues with this syntax.

### HAX Content Authoring
- **Rule ID**: `eis0l9w9l2jG1COFySmvdT`
- **Scope**: `webcomponents`
- **Content**: When you write content for hax sites make sure that the webcomponent tags you are using are things that could have been authored and put in the page. This means written using the HAX editor via elements that have HAXSchema. This registry has a list of all valid HAX capable elements and while not always used on every page, it's useful for knowing what is possible. Some times supplying visually interesting content helps with engagement for video, table, and block element data. Also keep in mind the DDD attributes that we support to help make headings and paragraph content offset in a consistent way.

### a11y-collapse heading-button
- **Rule ID**: `WQoGOB824VGW5HECMh08ew`
- **Scope**: `webcomponents`
- **Content**: When using a11y-collapse, ensure that the `heading-button` property is set on the HTML element to make it easier for the end user to click the whole heading to expand the content. Without it, only the small toggle icon is clickable; with it, the entire heading bar becomes a clickable button, which is a better UX.

### haxHooks lifecycle integration
- **Rule ID**: `haxhooks-lifecycle-integration`
- **Scope**: `webcomponents`
- **Content**: Elements that need to participate in HAX lifecycle / state changes without importing HAX implement a `haxHooks()` method mapping hook names to element method names. The platform stays type-agnostic by routing through these hooks rather than hard-coding support for specific elements or file types. Use `processFileUpload` (returns `{ fileUuid, operation, valueMapping, fallbackType? }` or `false`) to let an element own its post-upload conversion from the generic tray upload / drag-drop path (`HAXStore.applyFileUploadTransform`), mirroring the per-field schema `uploadTransform`. Use `gizmoRegistration` to extend `validGizmoTypes` or register an app store. Use `mediaSourceUpdated` to refresh an element's live preview when a backing file changes in place. Use `preProcessInsertContent` / `preProcessNodeToContent` / `postProcessNodeToContent` to hook insertion / export serialization. Use `activeElementChanged` / `editModeChanged` to sync edit state. Use `inlineContextMenu` to add context-menu buttons. The authoritative hook list and signatures live in the comment block at the top of `HAXWiring.js` (`elements/hax-body-behaviors/lib/HAXWiring.js`) and are mirrored in `hax-schema/README.md` under `# Hax hooks`.

### Educational Content Standards (OER Schema)
- **Rule ID**: `c3XjsqFbCmoA3cxsooNyxG`
- **Scope**: `webcomponents`
- **Content**: Creating educational elements in HAX? Apply OER Schema metadata for consistent semantic structure and interoperability. Audit authored content with the `oerschema-audit` skill; find components missing schema with the `oerschema-integration-finder` skill. Map to real OER classes (Course/Unit/Module/Lesson/LearningObjective/Assessment/Quiz/Activity/Task/Rubric/SupportingMaterial/TableOfContents) — never invent classes.

## ⚙️ Build & Development Workflow

### HAX CLI Usage
- **Rule ID**: `ip9IudNwZrZQsyk4ggvCzH`
- **Scope**: `global`
- **Content**: When running hax commands don't do npx, instead use the local copy that we have as it is always the latest or even experimental as the source starts with this machine.

### Web Component Scaffolding
- **Rule ID**: `E9Zioqke3Y0gdnWB08XQn8`
- **Scope**: `webcomponents`
- **Content**: All new elements in the monorepo must be created using the `hax webcomponent` CLI command to ensure uniformity, including generation of demo, packaging, and distribution files. Do not create webcomponent directories or files manually in the monorepo — always scaffold with the CLI tool first.

### HAX Site Scaffolding
- **Rule ID**: `hax-site-scaffold`
- **Scope**: `haxcms`
- **Content**: When creating HAXcms sites for testing or any purpose, always use the `hax site` command to generate the site. This ensures the site is created in the standard deployment location with the correct structure, theme configuration, and follows HAXcms conventions. Do not create site directories or files manually — always scaffold with the CLI tool first.

### HAXcms Page Creation via CLI
- **Rule ID**: `tRwt1R0Bv54nuHgEfl8IWe`
- **Scope**: `haxcms`
- **Content**: Always create HAXcms site pages through the `hax` CLI (`hax site node:add` or `hax site site:items-import`), never by manually creating page directories or hand-editing `site.json`. Manual page creation bypasses the CLI's page-id generation, slug/location management, and atomic `site.json` updates, which corrupts the JSON Outline Schema structure and breaks the site in production. The CLI owns page structure; the agent only owns page content.

### No Traditional Build Prompts
- **Rule ID**: `pCcVD8jgmc7zHeHTDEBzD1`
- **Scope**: `global`
- **Content**: Do not ask or prompt to run traditional build commands in this monorepo as they are not used.

### HAXcms Theme Build
- **Rule ID**: `cfypZRDQLaJ6XsXtEaveWT`
- **Scope**: `haxcms`
- **Content**: Any time changes are made to a HAXcms site theme using classes that inherit from HAXCMSLitElement, run `yarn run build` at the end instead of manually editing the custom-elements.json file.

### Command Automation
- **Rule ID**: `PacOyoQW2aIyaTO3R6asNL`
- **Scope**: `global`
- **Content**: If you have been told to keep running commands without interuption, ensure that when running commands in hax ensure that the `--y` and `--no-i` and `--auto` commands are correctly used in order to ensure that there's no questions asked of the human or launching off into a new window / process. Otherwise a command to display the site when in a prompting exchange could lead for it to open in a new window and get stopped.

### Version Control
- **Rule ID**: `edaXma3ZIiHZ86GyX4MoSu`
- **Scope**: `global`
- **Content**: github cli is installed just read the output of it instead of asking me to verify.

### Environment Setup
- **Rule ID**: `bAKMWCMrqRLGdWmuNWgVUw`
- **Scope**: `global`
- **Content**: Always start new shells in the ~/Documents/git/haxtheweb/ folder because that's where all of the user's projects are located.

### Monorepo Dependency Verification
- **Rule ID**: `4a7c9e2b-8d5f-4e1a-9c3b-7f2e6d5a4b3c`
- **Scope**: `webcomponents`
- **Content**: If we add a dependency (import or reference) to an element in the webcomponents monorepo, verify that the dependency is declared in the `package.json` for that element before completing the change.

### Script Restrictions
- **Rule ID**: `SSy9vkxAqBTIcIXvYUstGA`
- **Scope**: `global`
- **Content**: The agent is explicitly not allowed to run the ubiquity script under any circumstances.

### AI Guardrails — State Assumptions
- **Rule ID**: `74cc0274-6bf2-45a0-8e06-b88254f4cf9e`
- **Scope**: `global`
- **Content**: Before implementing, state assumptions explicitly when ambiguity exists, ask clarifying questions when multiple interpretations would materially change the solution, and surface simpler alternatives/tradeoffs instead of silently choosing one.

### AI Guardrails — Minimum Viable
- **Rule ID**: `f98f5e24-c343-4c12-b1c8-d6ae9783afaa`
- **Scope**: `global`
- **Content**: Prefer minimum viable implementation. Do not add speculative features, abstractions, configurability, or defensive complexity that was not requested.

### AI Guardrails — Surgical Diffs
- **Rule ID**: `d2315f2d-f4b2-4e86-bdd0-37b2d42fef89`
- **Scope**: `global`
- **Content**: Keep diffs surgical: modify only code directly tied to the request, avoid unrelated refactors or formatting-only churn, and only remove unused code introduced by your own changes unless explicitly asked.

### AI Guardrails — Verify Outcomes
- **Rule ID**: `f15ba99a-0a0a-42a0-a413-d8dfdc8eb20b`
- **Scope**: `global`
- **Content**: Define concrete success criteria and verify outcomes using project-appropriate checks (command output, linting, runtime validation, or existing tests when applicable), then report what was validated.

### HAX Skill Lookup Locations
- **Rule ID**: `c089870b608c482a847ccc`
- **Scope**: `global`
- **Content**: When looking for skills related to HAX itself (HAX-specific workflows, CLI operations, site building, web component development, the DDD design system, onboarding, issue analysis, rule management, UbD/UDL instructional design, etc.), look in the `praw` and `create` repositories rather than searching elsewhere. The canonical HAX skills live under `praw/.agents/skills/` (the authoritative registry) and `create/src/skills/` (a shipped subset that is built into `create/dist/skills/`). Check these locations first before assuming a needed HAX skill does not exist.

## 🧠 Instructional Design

### HAX Course Units via Understanding by Design
- **Rule ID**: `a1b2c3d4-e5f6-4789-9abc-def012345678`
- **Scope**: `haxcms`
- **Content**: Designing a HAX course unit whose goal is student understanding? Use the `hax-ubd-backward-design` skill family (UbD backward design: desired results → acceptable evidence → learning experiences). Design at unit scope or larger; avoid the twin sins of activity-oriented design and coverage. Map every construct to a real, HAX-authorable element — never invent tag names. Persist each unit's design at `files/ubd/<unit-slug>.manifest.json`. Framework: Wiggins & McTighe (2005), *Understanding by Design* (Expanded 2nd ed.).

### Universal Design for Learning (UDL) Audit
- **Rule ID**: `4ab69ab2-d295-4c01-a448-1ce1689c7366`
- **Scope**: `haxcms`
- **Content**: Reviewing whether a HAX site/page reaches all learners? Use the `hax-udl-audit` skill (UDL 3.0: multiple means of Engagement, Representation, Action & Expression). Bias toward flagging Action & Expression gaps — interactive assessment blocks are the empirically-confirmed gap across the HAX training corpus. Map every guideline to a real, HAX-authorable element — never invent tag names. Framework: CAST (2024), *UDL Guidelines 3.0*.

## 📋 Rule Management System

### Adding New Rules
1. Add the rule to this RULES.md file under the appropriate category with a `Scope:` field.
2. Assign a unique Rule ID (UUID format for new rules).
3. Document the rule content and context.
4. Run `node scripts/build-rules.js` to validate (catches duplicate IDs + duplicate content).
5. If the rule is `global`, sync it into Warp's Global Rules store; if scoped, ensure the corresponding subdirectory `WARP.md` carries the prose.

### Updating Existing Rules
1. Locate the rule by Rule ID in this document.
2. Update the content while preserving the Rule ID.
3. Run `node scripts/build-rules.js` to validate.
4. Update the corresponding subdirectory `WARP.md` if it is a scoped rule.

### Rule Categories
- **🏗️ Architecture & File Structure**: Site organization, routing, file systems
- **🎨 Design System Standards**: DDD, SimpleColors, theming guidelines
- **🧩 Web Component Development**: HAX capability, accessibility, JavaScript standards
- **⚙️ Build & Development Workflow**: CLI usage, build commands, version control
- **🧠 Instructional Design**: UbD, UDL pedagogical frameworks

### Validation
- `node scripts/build-rules.js` — parses RULES.md, emits `exports/rules-global.json` + `exports/rules-by-scope.json`, reports duplicate Rule IDs and duplicate normalized content (exit code 2 on warnings).
- `bash scripts/manage-rules.sh validate` — runs the same duplicate checks plus section-header structure checks.

### Cross-References
This RULES.md file is the canonical registry. Scoped prose lives in:
- `~/Documents/git/haxtheweb/praw/webcomponents/WARP.md` (webcomponents scope)
- `~/Documents/git/haxtheweb/praw/haxcms/WARP.md` (haxcms scope)
- `~/Documents/git/haxtheweb/praw/design-system/WARP.md` (design-system scope)
- `~/Documents/git/haxtheweb/praw/WARP.md` (lean ecosystem index, always-on as the praw Project Rule)

## 🔄 Future Rule Management

All future RULES work should:
1. **Read from** this repository for existing rules
2. **Write to** this repository for new rules, including a `Scope:` field
3. **Validate** with `node scripts/build-rules.js` before committing
4. **Reference** the appropriate subdirectory `WARP.md` for scoped prose
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

*This document serves as the authoritative registry for all HAX ecosystem Warp AI agent rules. It should be updated whenever new rules are created or existing rules are modified. Run `node scripts/build-rules.js` to validate after any change.*
