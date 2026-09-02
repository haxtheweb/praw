# Example: Prepare an OpenStax EPUB export

This example covers inspecting and preparing a book delivered as an EPUB. All
names and content are **fake placeholders**.

## Scenario

The user has `~/books/sample-world-history.epub`.

## Step 1 — Inspect

```text
/openstax2hax:inspect ~/books/sample-world-history.epub
```

Expected behavior:

1. Detects the **EPUB** format (a `.epub`, or an unzipped folder with
   `META-INF/container.xml` + a `.opf`).
2. Reads `container.xml` → the `.opf` → the `<spine>` for reading order.
3. Walks each XHTML item in spine order to enumerate chapters and sections.
4. Detects content elements and writes `source-diagnosis.md` and
   `openstax-elements-found.md` only.

If only a `.epub` archive is present, note in `source-diagnosis.md` whether it
must be unzipped first, and prefer reading the spine rather than guessing order
from filenames.

## Step 2 — Prepare

```text
/openstax2hax:prepare ~/books/sample-world-history.epub
```

Expected behavior:

1. Normalizes the spine into `conversion/book-structure.json`.
2. Fully prepares the pilot chapter; scaffolds the remaining chapters.
3. Preserves figure captions, tables, callouts, and math representation.
4. Captures attribution (title, authors, publisher, license, source URL).
5. Does **not** build a HAX site.

### Safe file writing

Follow the **Shell Safety Rules** in `SKILL.md`. Write each generated file with a
single-quoted heredoc, then (later, in `claudehax`) pass file PATHs to the HAX
CLI — never inline multiline content in a quoted argument:

```bash
cat > conversion/attribution.md <<'EOF'
# Attribution

Title: Sample World History (sample)
License: CC BY 4.0 (placeholder)
EOF
```

## Notes

- EPUB XHTML is usually well structured, so element detection is reliable.
- Watch for image-only math and large embedded media; flag these in the QA report.
