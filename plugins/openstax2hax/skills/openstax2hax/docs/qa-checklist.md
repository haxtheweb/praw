# QA Checklist

Run this checklist during `/openstax2hax:prepare` and record the results in
`conversion/qa-report.md` before generating the handoff prompt.

## Structure

- [ ] Source format was detected and recorded.
- [ ] Book title, edition/version captured.
- [ ] Chapters and sections enumerated in correct reading order.
- [ ] Stable, unique slugs assigned to every chapter and section.
- [ ] A pilot chapter is identified and fully prepared.
- [ ] The book is NOT flattened into a single page.

## Content elements

- [ ] Learning objectives detected and mapped.
- [ ] Figures preserved with captions and alt text.
- [ ] Tables preserved with captions and headers.
- [ ] Examples preserved with problem + solution structure.
- [ ] Notes/callouts preserved with their labels.
- [ ] Key terms recorded.
- [ ] Glossary terms recorded.
- [ ] Summaries preserved.
- [ ] Review questions preserved (and mapped to assessments where answers exist).
- [ ] Exercises/problems preserved.
- [ ] Math representation preserved; image-only math flagged.
- [ ] References preserved.
- [ ] Internal links remapped to slugs; external links preserved.

## Attribution and licensing

- [ ] License captured (e.g. CC BY 4.0) with version and URL.
- [ ] Authors and publisher (OpenStax / Rice University) captured.
- [ ] Source URL and access date captured.
- [ ] Attribution carried into `conversion/attribution.md`.
- [ ] Handoff prompt includes attribution to appear in the finished site.
- [ ] No copyrighted OpenStax content committed to the plugin repo.

## Accessibility

- [ ] All images have meaningful alt text (or are flagged for review).
- [ ] Tables have headers; data tables are not used purely for layout.
- [ ] Heading levels are consistent and hierarchical.

## Conversion files

- [ ] `conversion/book-structure.json` is valid JSON and matches the schema.
- [ ] `conversion/content-map.md` covers every detected element type.
- [ ] `conversion/pages/` contains the prepared pages (pilot chapter at minimum).
- [ ] `conversion/qa-report.md` lists unresolved risks.

## Risks

Record any of the following in `qa-report.md`:

- Complex or image-only math.
- Interactive simulations or embeds with no clear HAX equivalent.
- Very large media that may need optimization.
- Inconsistent or missing markup that required guessing.
