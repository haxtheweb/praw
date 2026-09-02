# HAX Handoff Format

This doc defines the conversion files produced by `/openstax2hax:prepare` and the
handoff prompt produced by `/openstax2hax:handoff`. These artifacts are what the
[`hax-site-ops`](https://github.com/haxtheweb/praw) plugin consumes to build
the HAX site. This plugin never builds the site itself.

## Conversion files overview

All conversion artifacts live under `conversion/` in the user's working
directory (never committed to this plugin repo):

```text
conversion/
  book-structure.json      # normalized page tree + element references
  content-map.md           # OpenStax element → HAX component mapping
  attribution.md           # license + attribution to carry into the site
  pages/                   # cleaned per-page Markdown (pilot chapter first)
    ch01-section-01.md
    ...
  qa-report.md             # QA checklist results
  hax-handoff-prompt.md    # written by /openstax2hax:handoff (last)
```

## book-structure.json

A normalized book → chapter → section tree. Keep it stable and slug-based so the
handoff and the eventual HAX page tree line up. See
`examples/sample-book-structure.json` for a complete placeholder example.

Required shape (abbreviated):

```json
{
  "book": {
    "title": "string",
    "edition": "string",
    "license": "string",
    "attribution": { "authors": "string", "publisher": "string", "sourceUrl": "string", "accessed": "YYYY-MM-DD" }
  },
  "pilotChapter": "ch01",
  "chapters": [
    {
      "id": "ch01",
      "title": "string",
      "slug": "chapter-1-...",
      "order": 1,
      "sections": [
        {
          "id": "ch01-sec01",
          "title": "string",
          "slug": "...",
          "order": 1,
          "page": "pages/ch01-section-01.md",
          "elements": {
            "learningObjectives": 0,
            "figures": 0,
            "tables": 0,
            "examples": 0,
            "notes": 0,
            "keyTerms": 0,
            "glossaryTerms": 0,
            "summary": false,
            "reviewQuestions": 0,
            "exercises": 0,
            "math": 0,
            "references": 0,
            "links": 0
          }
        }
      ]
    }
  ]
}
```

## content-map.md

A human-readable mapping from each detected OpenStax element to the HAX
representation. Recommended default mappings:

- Learning objectives → callout/objectives block at top of page.
- Figure + caption → `<figure>`/image with caption; preserve alt text.
- Table → HTML table or HAX table component; preserve caption + headers.
- Example → worked-example layout (problem + solution).
- Note / callout → HAX callout component, label preserved (e.g. "Link to Learning").
- Key term → inline defined term, optionally linked to glossary.
- Glossary → glossary section or definition components.
- Summary → summary section.
- Review questions → assessment component (e.g. multiple-choice) when answers
  exist; otherwise a questions list.
- Exercises / problems → problem sets, optionally interactive.
- Math → preserve MathML/LaTeX; note any image-only math.
- References → references section.
- Links → internal links remapped to HAX slugs; external links preserved.

These are recommendations; `hax-site-ops` chooses the actual HAX components.

## pages/

One Markdown file per page, starting with the pilot chapter. Each page contains
cleaned content with lightweight HAX component hints (HTML comments or labeled
sections), plus a footer line referencing attribution. Do not embed the full
book; reference assets by path.

When writing these page files from the shell, use a single-quoted heredoc
(`cat > conversion/pages/ch01-section-01.md <<'EOF' ... EOF`). Never place the
page's Markdown/HTML inside a quoted CLI argument — see the **Shell Safety
Rules** in `SKILL.md`.

## attribution.md

Carries the license and attribution that must appear in the finished HAX site:
title, authors, publisher (OpenStax / Rice University), license + version,
source URL, and access date.

## hax-handoff-prompt.md

The paste-ready prompt for a `hax-site-ops` session. It must:

1. State the goal: build a HAX site from these conversion files.
2. Tell `hax-site-ops` to prefer the HAX CLI and HAX web components.
3. Recommend building the **pilot chapter first**, then expanding.
4. **Forbid flattening the book into one page** — preserve the page tree.
5. Include the page tree (from `book-structure.json`) and per-page content
   references (from `pages/`).
6. Include component hints (from `content-map.md`).
7. Include the attribution/license text that must appear in the site.
8. Include a **Shell safety** rule for `hax-site-ops`: when creating HAX pages,
   write the page content (Markdown/HTML/JSON) to a file with a single-quoted
   heredoc (`cat > page.html <<'EOF' ... EOF`) and pass the file PATH to the HAX
   CLI. Never inline multiline content in a quoted argument, and never use
   `node -e "..."` or `python3 -c "..."` with multiline code.

See `examples/sample-hax-handoff-prompt.md` for the target shape. The example
uses fake placeholder content only.
