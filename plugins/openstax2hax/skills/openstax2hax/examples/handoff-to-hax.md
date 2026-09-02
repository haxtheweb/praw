# Example: Hand off to the hax-site-ops plugin

This example shows the final handoff step. All names and content are **fake
placeholders**.

## Prerequisite

You have already run `/openstax2hax:prepare`, so `conversion/` contains
`book-structure.json`, `content-map.md`, `attribution.md`, `pages/`, and
`qa-report.md`.

## Step 1 — Generate the handoff prompt

```text
/openstax2hax:handoff
```

Expected behavior:

1. Confirms the conversion files exist.
2. Reads the structure, content map, and attribution.
3. Writes `conversion/hax-handoff-prompt.md` — a paste-ready prompt that:
   - Instructs `hax-site-ops` to build a HAX site using the HAX CLI and components.
   - Recommends building the pilot chapter first.
   - Forbids flattening the book into one page.
   - Includes the page tree, per-page references, and component hints.
   - Carries the attribution/license text into the site.

This command does **not** build the HAX site.

## Step 2 — Build the site with hax-site-ops

1. Open a new Claude Code session that has the
   [`hax-site-ops`](https://github.com/haxtheweb/praw) plugin installed.
2. Paste the contents of `conversion/hax-handoff-prompt.md` (typically after
   `/hax`).
3. Let `hax-site-ops` build the pilot chapter, review it, then expand to the full
   book.

See `examples/sample-hax-handoff-prompt.md` (at the repo root) for what the
generated prompt looks like.
