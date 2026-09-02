---
description: Generate a HAX handoff prompt that the claudehax plugin can consume.
---

# /openstax2hax:handoff

Generate `conversion/hax-handoff-prompt.md` from the conversion files produced by
`/openstax2hax:prepare`.

Use the `openstax2hax` skill, especially
`skills/openstax2hax/docs/hax-handoff-format.md`, as the source of truth.

## Goal

Produce a single, self-contained prompt that a user can paste into a Claude Code
session running the [`claudehax`](https://github.com/haxtheweb/claudehax) plugin
to build the actual HAX site.

**This command does NOT build the HAX site.** It only writes the handoff prompt.

## Steps

1. Confirm the conversion files exist (`conversion/book-structure.json`,
   `conversion/content-map.md`, `conversion/attribution.md`, and
   `conversion/pages/`). If they do not, tell the user to run
   `/openstax2hax:prepare` first.
2. Read the normalized structure, content map, and attribution metadata.
3. Assemble the handoff prompt following the HAX handoff format. It must tell
   the `claudehax` plugin to:
   - Read the conversion files in `./conversion` (book structure, content map,
     attribution, and any pages/plans).
   - Build the HAX site in `./hax-site` (preferring the HAX CLI and HAX web
     components).
   - Build **only the pilot chapter first**, then stop for review.
   - Preserve the chapter/section structure as the HAX page tree.
   - Preserve figures, captions, tables, learning objectives, review questions,
     exercises, glossary terms, math, and attribution.
   - Write a build report to `conversion/hax-build-report.md`.
   - **Stop before converting the whole book** — do not flatten the book into one
     page and do not build remaining chapters until the user approves the pilot.
   - **Shell safety:** write each page's content to a file with a single-quoted
     heredoc (`cat > page.html <<'EOF' ... EOF`) and pass the file PATH to the
     HAX CLI. Never inline multiline Markdown/HTML/JSON in a quoted argument, and
     never use `node -e "..."` or `python3 -c "..."` with multiline code.

When you write `conversion/hax-handoff-prompt.md` yourself, follow the **Shell
Safety Rules** in the `openstax2hax` skill: use a single-quoted heredoc rather
than placing the prompt's Markdown inside a quoted argument.

## Output (create this file ONLY)

- `conversion/hax-handoff-prompt.md` — the complete, paste-ready HAX handoff
  prompt.

When finished, tell the user to open a `claudehax`-enabled session and paste the
contents of `conversion/hax-handoff-prompt.md` (typically with `/hax`).
