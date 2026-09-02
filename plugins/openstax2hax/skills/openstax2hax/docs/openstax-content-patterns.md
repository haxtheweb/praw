# OpenStax Content Patterns

This doc describes the recurring content elements in OpenStax books and how to
detect them. Use it during `/openstax2hax:inspect` and `/openstax2hax:prepare`.

OpenStax books share a consistent pedagogical structure. Detect these elements
and record counts and example locations. Cues differ slightly per source format
(HTML/EPUB use classes and tags; CNXML uses semantic tags; PDF/Markdown rely on
text labels).

## Chapters and sections

- Cues: `<h1>`/`<h2>` headings, numbering like `1`, `1.1`, `1.2`, TOC/spine entries.
- CNXML: `collection.xml` `<subcollection>` and module references.
- Record: ordered tree of chapters → sections with titles and slugs.

## Learning objectives

- Cues: headings "Learning Objectives", "By the end of this section, you will be
  able to"; often a bulleted list near the start of a section.
- CNXML: `<note class="learning-objectives">` or abstract.
- Map to: an objectives callout near the top of the HAX page.

## Figures and captions

- Cues: `<figure>` + `<figcaption>`, "Figure 1.2", image `alt` text.
- CNXML: `<figure>` with `<caption>` and `<media>`/`<image>`.
- Record: image path, caption text, alt text, figure number.

## Tables

- Cues: `<table>`, "Table 1.1", a caption row/`<caption>`.
- CNXML: `<table>` with `<title>`.
- Map to: HTML table or a HAX table component; preserve caption and headers.

## Examples (worked examples)

- Cues: "Example 1.1", a problem statement followed by a "Solution".
- CNXML: `<example>`.
- Map to: a worked-example layout (problem + solution sections).

## Notes and callouts

OpenStax uses recurring named callouts. Detect by label/class:

- "Link to Learning"
- "Everyday Connection" / "Everyday Application"
- "Making Connections"
- "Tip" / "Note" / "Warning" / "Important"
- "Career Connection"

CNXML: `<note class="...">`. Map each to an appropriate HAX callout component and
preserve the callout label.

## Key terms

- Cues: bold or emphasized terms defined inline within a section.
- CNXML: `<term>` elements.
- Record: term and inline definition for later glossary cross-linking.

## Glossary terms

- Cues: an end-of-chapter "Glossary" with term/definition pairs (definition list).
- CNXML: `<glossary>` with `<definition>`/`<meaning>`.
- Map to: a glossary section or definition components.

## Summaries

- Cues: "Chapter Summary", "Section Summary", "Key Concepts".
- Map to: a summary section per chapter/section.

## Review questions

- Cues: "Review Questions", "Conceptual Questions", "Critical Thinking".
- Map to: HAX assessment components (e.g. multiple-choice) when answers exist,
  otherwise a questions list.

## Exercises / problems

- Cues: "Problems", "Exercises", numbered problem sets, sometimes with answers.
- CNXML: `<exercise>` with `<problem>`/`<solution>`.
- Map to: problem sets, optionally interactive assessment components.

## Math

- Cues: MathML (`<math>`), LaTeX (`$...$`, `\(...\)`, `\[...\]`), or rendered math
  images with alt text.
- Record: math representation per occurrence and flag conversion risk (MathML vs
  LaTeX vs image). Preserve the original representation for the handoff.

## References

- Cues: "References" lists, citations, footnotes.
- Map to: a references section; preserve citation text and links.

## Links

- Cues: `<a href>` — distinguish internal cross-references (other sections) from
  external links.
- Record: internal links to remap to HAX page slugs; external links to preserve.

## Detecting elements without inline code

Do not write inline Python/Node to count these elements. Use the bundled
inspector, which counts them per page (and aggregates):

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/inspect-openstax.py" --elements <file-or-dir> --json
```

This avoids Claude Code's command-analyzer confirmation prompts (see the **Shell
Safety Rules** in `SKILL.md`). Treat its counts as a first pass and refine by
reading specific pages with your built-in file tools when needed.

## Recording results

For each element type, record in `openstax-elements-found.md`:

- Element type
- Count
- One or two example locations (file + heading/section)
- Any conversion risk or note
