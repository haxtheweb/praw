---
name: hax-rule-management
description: >
  Add, search, validate, and export PRAW (HAX ecosystem) rules stored in RULES.md.
  Use when managing HAX ecosystem development rules, adding new conventions, or updating
  existing rule entries in the PRAW repository.
version: 1.0.0
license: Apache-2.0
metadata:
  author: haxtheweb
  tags: [hax, praw, rules, management, conventions, warp]
---

# HAX Rule Management

Add, search, validate, and export PRAW (HAX ecosystem) rules stored in RULES.md.

## When to Use

- Adding a new rule to the HAX ecosystem rule registry
- Searching existing rules by category or keyword
- Validating RULES.md structure and rule integrity
- Exporting rules to JSON, CSV, or other formats
- Updating existing rule content while preserving Rule IDs
- Reviewing rule precedence and cross-references

## How It Works

1. **Setup**: Run `./scripts/setup.sh` from the PRAW repository root to install aliases and shell integration. Restart the terminal or source the shell config after setup.
2. **Add Rules**: Use `praw-add` interactively, or `praw-add <category> "Title" "Content"` via command line. Categories include architecture, design-system, webcomponent, build-workflow, documentation, and project-specific.
3. **Search Rules**: Use `praw-search <term>` to find rules containing specific keywords. Use `praw-list` to list all rules, or `praw-list <category>` for filtered views.
4. **Show Details**: Use `praw-show <rule-id>` to display a specific rule's full content and metadata.
5. **Validate**: Use `praw-validate` to check RULES.md structure, ensure unique IDs, and verify category integrity.
6. **Export**: Use `praw-export json`, `praw-export csv`, or `praw-export md` to generate distributable rule files.

## Rule Categories

- **architecture** — Site structure, routing, file organization, HAXcms metadata
- **design-system** — DDD, SimpleColors, theming guidelines
- **webcomponent** — HAX capability, accessibility, JavaScript standards
- **build-workflow** — CLI usage, build commands, version control, testing philosophy
- **documentation** — Content creation, documentation structure, standards
- **project-specific** — Rules for specific projects or directories

## Rule Precedence

Rules are listed in **ascending order of precedence** in RULES.md. Rules that appear **later** take precedence over earlier ones. Project-specific rules (with file paths) override personal rules. Subdirectory rules override parent directory rules. When conflicts exist, follow the rule that appears **last**.

## Adding a New Rule

1. Determine the correct category based on the rule's scope
2. Assign a unique Rule ID (UUID format for new rules)
3. Document the rule content and context clearly
4. Check for precedence implications — later rules override earlier ones
5. Cross-reference related WARP.md files if needed
6. Run `praw-validate` before committing
7. Log emergent knowledge in KNOWLEDGE.md if the decision is novel

## Knowledge Capture

For emergent insights that may become rules:
- Log decisions, patterns, and discoveries in `KNOWLEDGE.md`
- Use the structured template for consistency
- Mark potential rules with `Candidate: Yes`
- Promote stable knowledge items to formal rules in RULES.md
- Link back to KNOWLEDGE.md entries for context and rationale

## Scripts

- `scripts/setup.sh` — Initial setup and alias installation
- `scripts/add-rule.sh` — Interactive and CLI rule addition
- `scripts/manage-rules.sh` — Search, list, validate, and export operations

## References

- For rule writing guidelines: `references/rule-writing-guide.md`
- For precedence examples: `references/precedence-examples.md`
