# Sample HAX Handoff Prompt

> Sample only. Fake titles and placeholder content. Contains no real OpenStax
> book content. This is what `/openstax2hax:handoff` produces in
> `conversion/hax-handoff-prompt.md`.

---

## HAX Build Request (paste into a claudehax session)

You are building a HAX site from prepared OpenStax conversion files. Use the HAX
CLI and HAX web components (prefer components over plain HTML). Read the
conversion files in `./conversion/` and build the HAX site into `./hax-site`.

### Rules

- **Build the pilot chapter first** (Chapter 1), then pause for review before
  expanding to the rest of the book.
- **Do NOT flatten the book into one page.** Preserve the book → chapter →
  section hierarchy as a HAX page tree.
- Preserve all attribution and license notices (see Attribution below); they
  must appear in the finished site.
- Preserve figures with captions and alt text, tables with headers, worked
  examples (problem + solution), and the original math representation.
- **Shell safety:** when creating pages, write the page content to a file with a
  single-quoted heredoc and pass the file PATH to the HAX CLI. Never inline
  multiline Markdown/HTML/JSON in a quoted argument, and never use `node -e` or
  `python3 -c` with multiline code (a newline followed by `#` in a quoted
  argument triggers a Claude Code warning).

### Book

- Title: Introduction to Sample Science (sample)
- Edition: 1st edition (sample)
- License: CC BY 4.0 (placeholder)

### Page tree (build as HAX pages)

```text
Chapter 1: Foundations of Sample Science        [PILOT — build first]
  1.1 What Is Sample Science?      -> conversion/pages/ch01-section-01.md
  1.2 Methods and Measurement      -> conversion/pages/ch01-section-02.md
Chapter 2: Applications of Sample Science        [scaffold; build after review]
  2.1 Sample Science in Daily Life -> conversion/pages/ch02-section-01.md
```

### Component hints

- Learning objectives → objectives callout at top of each page.
- Figures → image/figure with caption; keep alt text.
- Tables → table component; keep caption and headers.
- Examples → worked-example layout (problem + solution).
- Notes/callouts ("Link to Learning", "Everyday Connection") → HAX callout
  components with the label preserved.
- Key terms / glossary → defined terms and a glossary section.
- Review questions → multiple-choice / assessment components where answers exist.
- Exercises → problem sets.
- Math → preserve MathML/LaTeX; flag any image-only math.
- References → references section. Internal links → HAX slugs; external links
  preserved.

### Attribution (must appear in the finished site)

This work is a sample adaptation of "Introduction to Sample Science" by Sample
Author A and Sample Author B, published by OpenStax / Rice University
(placeholder), licensed under CC BY 4.0 (placeholder). Source:
https://example.org/sample-book (accessed 2026-06-26).

### Safe page-writing pattern

Write each page to a file first, then pass the file PATH to the HAX CLI:

```bash
cat > /tmp/ch01-section-01.html <<'EOF'
<h1>What Is Sample Science?</h1>
<!-- objectives callout, figures, examples, etc. -->
EOF
# then pass the file path (not the content) to the HAX CLI
hax site node:add --root ./hax-site --title "What Is Sample Science?" --content-file /tmp/ch01-section-01.html
```

(The exact HAX CLI flags are up to `claudehax`; the rule is: content goes in a
file via a single-quoted heredoc, and only the PATH is passed as an argument.)

### Deliverable

A HAX site in `./hax-site` with Chapter 1 (the pilot) fully built (pages 1.1 and
1.2), Chapter 2 scaffolded, navigation reflecting the page tree, and attribution
visible. Write a build report to `conversion/hax-build-report.md` listing the
pages created and the HAX commands/components used, then **stop before converting
the whole book** and wait for review.
