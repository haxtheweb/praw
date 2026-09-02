---
description: Prepare conversion files from an OpenStax source (everything except the final HAX site).
argument-hint: <source-path>
---

# /openstax2hax:prepare

Generate the full set of conversion files for the OpenStax book at `$ARGUMENTS`.

Use the `openstax2hax` skill as the source of truth, including its **Shell
Safety Rules**: prefer built-in file tools, never inline `python3 -c` / `node -e`
/ interpreter heredocs, and get the page structure from the bundled inspector
(`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/inspect-openstax.py" <source> --json`)
rather than ad-hoc inline code.

This command works with any local source, including one created by
`/openstax2hax:import`. After an import, the source lives at
`./source/openstax.org`, so a typical call is:

```text
/openstax2hax:prepare ./source/openstax.org
```

## Goal

Transform the inspected OpenStax source into a clean, structured set of
conversion files that the `claudehax` plugin can later use to build a HAX site.

**This command creates every conversion file EXCEPT the final HAX site.** Do not
run the HAX CLI, do not create `site.json`, and do not generate HAX pages here.

## Steps

1. Resolve the source path from `$ARGUMENTS`. If none is given but an imported
   mirror exists at `./source/openstax.org`, use that. If `source-diagnosis.md`
   and `openstax-elements-found.md` do not exist yet, run the inspection logic
   first (or ask the user to run `/openstax2hax:inspect`).
2. Build a normalized book structure (book → chapters → sections) and map every
   detected OpenStax element to a HAX-friendly representation. See
   `skills/openstax2hax/docs/hax-handoff-format.md`.
3. **Recommend a pilot chapter first.** Default to fully preparing ONE chapter
   and scaffolding the rest, rather than flattening the whole book. Never collapse
   a whole book into a single page.
4. Preserve attribution, license, edition, and source URLs for every page.
5. Run the QA checklist in `skills/openstax2hax/docs/qa-checklist.md`.

## Output (create these conversion files)

Create a `conversion/` directory and write:

- `conversion/book-structure.json` — normalized book → chapter → section tree
  with stable slugs, ordering, and per-page element references.
- `conversion/content-map.md` — human-readable mapping of OpenStax elements to
  HAX components/page sections.
- `conversion/attribution.md` — book title, authors, publisher, license,
  edition/version, access date, and source URLs.
- `conversion/pages/` — one Markdown file per prepared page (start with the
  pilot chapter), containing cleaned content and HAX component hints.
- `conversion/qa-report.md` — results of the QA checklist, including any
  unresolved risks.

Then generate or refresh `conversion/hax-handoff-prompt.md` following
`/openstax2hax:handoff` (see `skills/openstax2hax/docs/hax-handoff-format.md`) so
the source is fully handoff-ready. Do **not** build the HAX site, run the HAX
CLI, or create `site.json` — the site is built later by `claudehax` into
`./hax-site`.

When creating these files from the shell, follow the **Shell Safety Rules** in
the `openstax2hax` skill: write each file with a single-quoted heredoc
(`cat > conversion/pages/ch01-section-01.md <<'EOF' ... EOF`) and never pass the
file's Markdown/JSON content inside a quoted CLI argument.

When finished, summarize what was prepared and tell the user they can refine the
handoff with `/openstax2hax:handoff` or proceed to build with `claudehax`.
