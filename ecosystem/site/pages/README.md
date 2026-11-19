# Hand-written hax.cloud pages

`ecosystem/build/build_site.py` generates a page for every web, tile and tour. A hand-written page goes above
the generated content of the page with the same slug: name it after the slug with `/` replaced by `__`, for
example `un-sdgs__4-quality-education.html` for hax.cloud/un-sdgs/4-quality-education, or `tours__everyone.html`.

Write it as HAX page HTML (what a HAX page's `index.html` holds: plain HTML and HAX elements). Edit it with the
HAX CLI or editor on a local copy of the site, then open a pull request; the next build publishes it.

A page that is not part of any web (like hax.cloud/magic-script) is listed in `ecosystem/site/extra-pages.json` as
`{slug, title, description, nav}`; its HTML is the hand-written file for that slug. `nav: true` puts it in the top menu.

## Where pages sit in the outline

`ecosystem/site/categories.json` arranges the site outline (the Site view's menu and breadcrumb). The home page holds
the main web's own tiles; every other web is its own page with its tiles under it, filed under a category:

- `categories`: `{id, title, description, parent}`. A category with a `parent` nests under it, so `courses/ist`
  (IST) sits under Courses. Its page is at the id (hax.cloud/courses/ist) and lists what is filed in it.
- `webs`: `{web id: category id}` for each web that opens from the main web, or `"web:<id>"` to file it under that
  web's page (hax.psu.edu and HAX Lab under Penn State). A nested web (JSON Outline Schema under Data contracts)
  stays under its parent web. A web left out stays under the home page, and the build names it.
- `tiles`: `{"<web>:<node id>": "web:<id>"}` files a tile's page under another web, such as Penn State's colleges
  (main-web tiles) under Penn State.

The outline never changes an address: a web's path comes from the web that opens it, and a tile's from its key.
