# KNOWLEDGE LOG

This document records emergent knowledge, decisions, conventions, and lessons learned while working across the HAX ecosystem. Use this to capture context that doesn’t fit formal rules yet, or to explain the rationale behind rules.

Structure your entries using the templates below. Keep entries concise and searchable. When a knowledge item stabilizes into a repeatable rule, promote it into RULES.md and link back here.

## How to add a new knowledge entry
- Add a new entry at the top of the relevant section with today’s date.
- Prefer small, atomic entries over long narratives.
- Include links to code, commits, PRs, or files where possible.
- If this entry should likely become a rule, mark it with `Candidate: Yes`.

## Template

- Title: <short, descriptive title>
- Date: YYYY-MM-DD
- Context: <where/why this came up>
- Guidance: <what to do next time>
- Rationale: <why this is the right approach>
- Links: <related files/PRs/issues>
- Candidate: Yes|No

---

## Web Components

- Title: Example – Prefer globalThis over window
- Date: 2025-09-25
- Context: Align with cross-environment JS standards and our ecosystem rule
- Guidance: Use `globalThis` whenever referencing global scope in components or utilities
- Rationale: Works in Node, browsers, and workers; matches existing rule CEHsAztyfB2vTCwtHGGnbk
- Links: RULES.md (JavaScript Standards)
- Candidate: No

## HAXcms

- Title: Example – Keep metadata.site.name aligned
- Date: 2025-09-25
- Context: BasePath and routing inconsistencies traced to incorrect site name
- Guidance: Ensure metadata.site.name exactly matches the site folder name
- Rationale: Prevents basePath issues in some deployment scenarios
- Links: RULES.md (HAXcms Site Metadata)
- Candidate: No

## Design System (DDD & SimpleColors)

- Title: Example – Prefer DDD tokens; use SimpleColors sparingly
- Date: 2025-09-25
- Context: Migrating components to DDD while retaining shade coverage
- Guidance: Use DDD tokens for spacing/typography/colors; use SimpleColors only when DDD lacks required shade
- Rationale: Aligns with primary design system while acknowledging gaps
- Links: RULES.md (Design System Standards)
- Candidate: No

## Build & Workflow

- Title: Example – Avoid optional chaining
- Date: 2025-09-25
- Context: Polymer parser incompatibilities
- Guidance: Don’t use `?.`; refactor to safe checks compatible with our tooling
- Rationale: Avoids build breaks and runtime surprises
- Links: RULES.md (JavaScript Standards)
- Candidate: No

## Documentation & Authoring

- Title: Example – Author with HAX-capable elements
- Date: 2025-09-25
- Context: Ensuring content can be edited with HAX and demoed consistently
- Guidance: Use elements with HAXSchema; consider demoSchema for demos and examples
- Rationale: Guarantees editor compatibility and consistent UX
- Links: RULES.md (HAX Content Authoring)
- Candidate: No
