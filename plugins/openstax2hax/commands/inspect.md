---
description: Inspect an OpenStax source and report what was found, without changing anything.
argument-hint: <source-path>
---

# /openstax2hax:inspect

Read-only diagnosis of an OpenStax book source located at `$ARGUMENTS`.

Use the `openstax2hax` skill as the source of truth for detecting OpenStax
source formats and content patterns. Follow its **Shell Safety Rules**: prefer
your built-in file tools, and never inline `python3 -c` / `node -e` / interpreter
heredocs (they cause Claude Code confirmation prompts).

For a downloaded web/HTML mirror, get the chapter/section structure from the
bundled inspector instead of writing inline code:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/inspect-openstax.py" <source-path>
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/inspect-openstax.py" <source-path> --json
```

## Goal

Inspect the OpenStax source and report what it contains. **Do not modify the
source, do not create conversion files, and do not build a HAX site.** This
command only produces two diagnostic files.

## Steps

1. Resolve the source path from `$ARGUMENTS`. If no path is provided, ask the
   user for one (or default to `.` only if it clearly looks like an OpenStax
   source).
2. Determine the source format (downloaded web folder, EPUB/EPUB export, PDF
   export, CNXML/collection XML, HTML bundle, or Markdown export). See
   `skills/openstax2hax/docs/openstax-source-formats.md`.
3. Walk the directory tree and identify the book title, chapters, and sections.
4. Detect OpenStax content patterns: learning objectives, figures, captions,
   tables, examples, notes/callouts, key terms, glossary terms, chapter
   summaries, review questions, exercises, math, references, and links. See
   `skills/openstax2hax/docs/openstax-content-patterns.md`.
5. Note attribution, license, and edition/version metadata.
6. Flag anything that may be hard to convert (complex math, interactive
   simulations, large media, inconsistent markup).

## Output (create these two files ONLY)

Write both files to the current working directory (or a `conversion/` folder if
one already exists):

- `source-diagnosis.md` — source format, detected book title, chapter/section
  counts, license/attribution metadata, overall structure quality, and
  conversion risks/recommendations.
- `openstax-elements-found.md` — an itemized inventory of every OpenStax element
  type detected (learning objectives, figures, captions, tables, examples,
  notes, key terms, glossary terms, summaries, review questions, exercises,
  math, references, links), with counts and example locations.

Do **not** create any other files. When finished, summarize the findings and
recommend running `/openstax2hax:prepare <source-path>` next.
