---
name: hax-openstax2hax
description: >
  Convert OpenStax books into HAX sites using the openstax2hax plugin.
  Use when the user wants to import, inspect, or prepare an OpenStax book for
  conversion into a HAX site, or when working with OpenStax source files and
  HAX handoff prompts.
version: 1.0.0
license: Apache-2.0
metadata:
  author: haxtheweb
  tags: [hax, openstax, claudehax, plugin, import, conversion, oer]
---

# HAX OpenStax2HAX Plugin

Convert OpenStax books into HAX sites using the openstax2hax plugin and HAX CLI.

## When to Use

- The user wants to turn an OpenStax book or chapter into a HAX site
- Inspecting or preparing downloaded OpenStax source files (HTML, EPUB, PDF, CNXML, Markdown)
- Generating HAX handoff prompts for the hax-site-ops plugin
- Working with OpenStax URL imports and conversion files
- Preserving OpenStax attribution and licensing in HAX sites

## Prerequisites

Before using openstax2hax, verify the environment:

1. **Claude Code** installed: `claude --version`
2. **wget** installed (macOS: `brew install wget`; Ubuntu: `sudo apt-get install wget`)
3. **Node.js 22+**: `node -v`
4. **HAX CLI** installed globally: `npm install -g @haxtheweb/create`, verify with `hax --help`

## Plugin Installation

Inside Claude Code:

1. Add the marketplace:
   ```
   /plugin marketplace add haxtheweb/praw
   ```
2. Install the plugin:
   ```
   /plugin install openstax2hax@haxtheweb
   ```
3. Verify:
   ```
   /plugin list
   ```
   Should show `openstax2hax` and its commands:
   ```
   /openstax2hax:import
   /openstax2hax:inspect
   /openstax2hax:prepare
   /openstax2hax:handoff
   ```

## Workflow

The fastest path is a one-command import from an OpenStax URL:

```
/openstax2hax:import https://openstax.org/details/books/principles-finance
```

This validates the URL, downloads the book into `./source`, creates `./conversion` and `./hax-site`, and generates `conversion/hax-handoff-prompt.md`.

### Step-by-step workflow

1. **Import** (recommended when you have a URL):
   ```
   /openstax2hax:import <openstax-url>
   ```

2. **Inspect** a local source:
   ```
   /openstax2hax:inspect <source-path>
   ```

3. **Prepare** conversion files (pilot chapter first):
   ```
   /openstax2hax:prepare <source-path>
   ```

4. **Hand off** to HAX:
   ```
   /openstax2hax:handoff
   ```

5. **Build** the HAX site with hax-site-ops in a separate session:
   ```
   /plugin marketplace add haxtheweb/praw
   /plugin install hax-site-ops@haxtheweb
   /hax Read conversion/hax-handoff-prompt.md and build only the pilot chapter in ./hax-site.
   ```

## Relationship to hax-site-ops

- **openstax2hax** prepares the conversion and writes `conversion/hax-handoff-prompt.md`
- **hax-site-ops** consumes that prompt and builds the actual HAX site using the HAX CLI

Always keep source analysis separate from site building. openstax2hax does NOT run the HAX CLI or create `site.json`.

## Output Files

`import` creates:
- `source/` — downloaded OpenStax book files
- `conversion/book-structure.json` — normalized book → chapter → section tree
- `conversion/content-map.md` — OpenStax element → HAX component mapping
- `conversion/attribution.md` — license and attribution metadata
- `conversion/pages/` — cleaned per-page Markdown (pilot chapter first)
- `conversion/qa-report.md` — QA checklist results
- `conversion/hax-handoff-prompt.md` — paste-ready prompt for hax-site-ops

## Key Guidelines

- **Pilot chapter first**: Always build one pilot chapter, review it, then expand to the full book.
- **Preserve hierarchy**: Never flatten an entire book into a single HAX page. Maintain book → chapter → section structure.
- **Preserve attribution**: OpenStax content is openly licensed (typically CC BY). Always capture and carry title, authors, publisher, license, source URL, and access date into the finished HAX site.
- **No copyrighted content in repos**: Do not commit OpenStax book content into git repositories. Conversion files live in the user's working directory.
- **Shell safety**: When writing page content from the shell, use single-quoted heredocs (`cat > file <<'EOF' ... EOF`) and pass file paths to the HAX CLI — never inline multiline content into quoted arguments.

## References

- openstax2hax plugin (PRAW): `https://github.com/haxtheweb/praw`
- hax-site-ops plugin (PRAW): `https://github.com/haxtheweb/praw`
- HAX CLI: `https://www.npmjs.com/package/@haxtheweb/create`
- HAX Documentation: `https://haxtheweb.org/`
