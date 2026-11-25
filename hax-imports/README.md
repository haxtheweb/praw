# File based imports
Copies of file based importers are included here as import-example.{format}, one for every file type the Import cards accept
- [DOCX](import-example.docx)
- [ODT](import-example.odt)
- [PDF](import-example.pdf)
- [PPTX](import-example.pptx)
- [ODP](import-example.odp)
- [XLSX](import-example.xlsx)
- [ODS](import-example.ods)
- [Markdown](import-example.md)
- [TXT](import-example.txt) (read as Markdown, so `#` headings become pages)
- [HTML](import-example.html): every page of [Learn HAX](https://learn.hax.cloud) as one site export (top-level pages are `h1`, the pages under them `h2`), loading its blocks from the HAX CDN so it also opens on its own. Rebuild it from a Learn checkout with `node scripts/build-import-example-html.js <learn checkout>` so it keeps up with the docs.

The ODT, ODP and ODS files are the DOCX, PPTX and XLSX examples saved in their OpenDocument formats, so each pair should import to the same pages.

# File uploads
Formats that upload into a page as a file and its block rather than importing as pages
- [ICS](import-example.ics) (calendar)
- [VCF](import-example.vcf) (contact card)

# URL based imports
These are URLs that are valid for importing into HAXcms
- [Gitbook](https://github.com/haxtheweb/gitbook-v1-example)
- [HAXcms](https://btopro.com)
- [Notion](https://github.com/BenFictional/dart-100-notion)
- [HTML URL](https://courses.ems.psu.edu/geog486/book/export/html/847)
- [Pressbooks](https://psu.pb.unizin.org/psuoerqsg/)
- [WordPress Pages](https://sites.psu.edu/)
- Drupal Book - Enable menu link JSON exposure (for example `menu_link_content`)
- Plone - Enable `plone.restapi: Use REST API` permission for authenticated/anonymous access




