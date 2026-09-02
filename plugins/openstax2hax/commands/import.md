---
description: One-command import of an OpenStax book from its URL into local conversion files.
argument-hint: <openstax-url>
---

# /openstax2hax:import

Import the OpenStax book at the URL `$ARGUMENTS`, download it locally, and produce
all HAX-ready conversion files — without building the final HAX site.

Use the `openstax2hax` skill as the source of truth, especially the
"Import from OpenStax URL" section.

## Goal

Give the user a single command that turns an OpenStax book URL into a complete
set of conversion files plus a HAX handoff prompt. The actual HAX site is built
later by the [`hax-site-ops`](https://github.com/haxtheweb/praw) plugin.

## Steps

1. **Validate the URL.** Confirm `$ARGUMENTS` is a single URL on the
   `openstax.org` domain (scheme `https://`, host `openstax.org` or
   `www.openstax.org`). If it is missing or not an OpenStax URL, stop and tell
   the user the command only accepts `https://openstax.org/...` URLs.
2. **Download/mirror the book.** Run the plugin's bundled import script with the
   URL. The script ships inside the plugin, so resolve it via
   `${CLAUDE_PLUGIN_ROOT}`:

   ```bash
   bash "${CLAUDE_PLUGIN_ROOT}/scripts/openstax-import.sh" "$ARGUMENTS"
   ```

   The script validates the URL again, creates `source/`, `conversion/`, and
   `hax-site/` in the current project, resolves OpenStax `details` URLs to a
   readable starting page, mirrors the book with `wget` into `source/`, and
   writes `conversion/source-url.txt`, `conversion/download.log`, and
   `conversion/import-report.md`. If `wget` is not installed, relay the install
   instructions the script prints and stop.
3. **Inspect the downloaded source** under `./source/openstax.org` using the
   skill's inspection and detection guidance. Do not convert directly from the
   live URL — always inspect the local mirror.
4. **Create or update the conversion files** (in `conversion/`):
   - `conversion/source-diagnosis.md`
   - `conversion/book-structure.json`
   - `conversion/openstax-elements-found.md`
   - `conversion/asset-inventory.json`
   - `conversion/attribution.md`
   - `conversion/hax-mapping-plan.md`
   - `conversion/pilot-chapter-plan.md`
   - `conversion/qa-checklist.md`
   - `conversion/hax-handoff-prompt.md`
5. **Stop before building the HAX site.** Do not run the HAX CLI, do not create
   `site.json`, and do not generate HAX pages. Leave `hax-site/` empty for
   `hax-site-ops`.

When creating the conversion files in step 4 from the shell, follow the **Shell
Safety Rules** in the `openstax2hax` skill: write each file with a single-quoted
heredoc (`cat > conversion/source-diagnosis.md <<'EOF' ... EOF`) and never pass
the file's Markdown/JSON content inside a quoted CLI argument.

## Conversion file notes

- `book-structure.json` — normalized book → chapter → section tree with stable
  slugs, a designated pilot chapter, and per-section element counts.
- `asset-inventory.json` — images and media found in the mirror, with their
  local paths and any captions/alt text.
- `pilot-chapter-plan.md` — the concrete plan for the single pilot chapter to
  build first.
- `hax-handoff-prompt.md` — must follow `/openstax2hax:handoff`: tell `hax-site-ops`
  to build into `./hax-site`, pilot chapter first, preserving structure,
  figures, captions, tables, learning objectives, review questions, exercises,
  glossary terms, math, and attribution, and to write
  `conversion/hax-build-report.md`.

## After import

Tell the user the exact next steps to build the site with `hax-site-ops`:

```text
/plugin marketplace add haxtheweb/praw
/plugin install hax-site-ops@haxtheweb
/hax Read conversion/hax-handoff-prompt.md and build only the pilot chapter in ./hax-site.
```

Remind them: `openstax2hax` grabbed and prepared the book; `hax-site-ops` builds the
HAX site, and the first build should be a single pilot chapter, not the whole
book.
