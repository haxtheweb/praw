# Example: Prepare a downloaded OpenStax web/HTML folder

This example walks through inspecting and preparing a book that was downloaded as
a folder of HTML pages. All names and content below are **fake placeholders**.

## Scenario

The user has a folder at `~/books/intro-to-sample-science/` containing:

```text
intro-to-sample-science/
  index.html            # table of contents
  ch01-01.html
  ch01-02.html
  ch02-01.html
  images/
```

## Step 1 — Inspect

```text
/openstax2hax:inspect ~/books/intro-to-sample-science
```

Expected behavior:

1. Detects the **downloaded web/HTML folder** format (many `.html` files +
   `index.html` TOC + `images/`).
2. Parses `index.html` for chapter/section order.
3. Detects elements per section (objectives, figures, tables, examples, notes,
   key terms, summaries, review questions, math, references, links).
4. Writes `source-diagnosis.md` and `openstax-elements-found.md` only.

Example `openstax-elements-found.md` excerpt (placeholder counts):

```text
Learning objectives: 6 (e.g. ch01-01.html "Learning Objectives")
Figures:            12 (e.g. ch01-02.html "Figure 1.3")
Tables:              3 (e.g. ch02-01.html "Table 2.1")
Examples:            5 (e.g. ch01-02.html "Example 1.2")
Notes/callouts:      8 (Link to Learning, Everyday Connection)
Math:                4 (MathML)
```

## Step 2 — Prepare (pilot chapter first)

```text
/openstax2hax:prepare ~/books/intro-to-sample-science
```

Expected behavior:

1. Builds `conversion/book-structure.json` for the whole book, but fully prepares
   only the pilot chapter (`ch01`) and scaffolds the rest.
2. Writes cleaned pages to `conversion/pages/ch01-section-01.md`, etc.
3. Writes `conversion/content-map.md`, `conversion/attribution.md`, and
   `conversion/qa-report.md`.
4. Does **not** build a HAX site or create `site.json`.

### Safe file writing

Follow the **Shell Safety Rules** in `SKILL.md`. Write each generated file with a
single-quoted heredoc — never inline the Markdown/JSON in a quoted argument:

```bash
mkdir -p conversion/pages
cat > conversion/pages/ch01-section-01.md <<'EOF'
# What Is Sample Science?

<!-- learning objectives callout -->
...cleaned page content...
EOF
```

## Step 3 — Review

Review `conversion/qa-report.md` and the pilot pages before expanding to the full
book or running `/openstax2hax:handoff`.
