# Hand-written hax.cloud pages

`ecosystem/build/build_site.py` generates a page for every web, tile and tour. A hand-written page goes above
the generated content of the page with the same slug: name it after the slug with `/` replaced by `__`, for
example `un-sdgs__4-quality-education.html` for hax.cloud/un-sdgs/4-quality-education, or `tours__everyone.html`.

Write it as HAX page HTML (what a HAX page's `index.html` holds: plain HTML and HAX elements). Edit it with the
HAX CLI or editor on a local copy of the site, then open a pull request; the next build publishes it.
