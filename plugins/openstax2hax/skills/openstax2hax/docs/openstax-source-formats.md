# OpenStax Source Formats

This doc describes the OpenStax source formats this plugin supports and how to
detect each one. Use it during `/openstax2hax:inspect`.

OpenStax books are openly licensed textbooks. Users obtain them in several forms.
Detect the format first, because it drives how you walk the content.

## 1. Downloaded web / HTML folder

A folder of HTML pages plus assets, typically downloaded from the OpenStax web
reader or a site mirror.

Detect when you see:

- Many `.html` / `.xhtml` files, often one per section.
- An `index.html` or a table-of-contents page linking the others.
- A media folder (`images/`, `media/`, `resources/`).

Walk by: parsing the TOC page for chapter/section order, then reading each
section file. Prefer reading order from the TOC over filename sorting.

## 2. EPUB / EPUB export

EPUB is a ZIP archive of XHTML content plus an OPF manifest and spine.

Detect when you see:

- A `.epub` file, or an unzipped folder containing `META-INF/container.xml` and
  a `content.opf` (or similar `.opf`).
- A `toc.ncx` or EPUB 3 nav document.

Walk by: reading `container.xml` → the `.opf` → the `<spine>` for reading order,
then each XHTML item. Do not fully load embedded fonts/media into memory.

## 3. PDF export

A single PDF of the book or a chapter.

Detect when you see:

- A `.pdf` file as the primary source.

Walk by: extracting the text and the PDF outline/bookmarks for structure. PDFs
lose semantic markup, so structure detection relies on headings, numbering, and
the outline. Flag PDFs as higher-risk for math, tables, and figure captions.

## 4. CNXML / collection XML

Legacy OpenStax/Connexions (CNX) format.

Detect when you see:

- `index.cnxml` files and a `collection.xml`.
- A `modules/` directory of CNXML modules.

Walk by: reading `collection.xml` for the chapter/module tree, then each
`index.cnxml`. CNXML carries rich semantics (`<note>`, `<example>`, `<exercise>`,
`<glossary>`, `<figure>`) — prefer these tags for detection.

## 5. HTML bundle (single file)

A single large HTML file containing the whole book.

Detect when you see:

- One very large `.html` file with many `<h1>`/`<h2>` chapter and section headings.

Walk by: splitting on heading levels to reconstruct the chapter/section tree.
**Do not keep this as one page** — split it during preparation.

## 6. Markdown export

Markdown files exported from another tool.

Detect when you see:

- `.md` files organized by chapter/section, possibly with a `SUMMARY.md` or
  `_toc` file.

Walk by: using the TOC/summary file if present, otherwise the heading hierarchy.

## If the format is ambiguous

1. List the directory contents and file extensions.
2. Look for a manifest/TOC/spine/collection file first.
3. Sample a few content files to confirm markup style.
4. Report the detected format (and confidence) in `source-diagnosis.md`.
5. Ask the user only if detection is genuinely ambiguous.

## Things to always capture

Regardless of format, record:

- Book title and edition/version.
- Authors and publisher (OpenStax / Rice University).
- License (e.g. CC BY 4.0) and any license URL.
- Original source URL and access date.
- Asset locations (images, media) for later reference.
