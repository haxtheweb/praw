# demo.hax.cloud

The live HAXcms demo from [webcomponents](https://github.com/haxtheweb/webcomponents)
(`elements/haxcms-elements/demo/`), served from the top of its own domain, so pages read
`demo.hax.cloud/<page>` and deep links load directly. The demo at its direct path,
<https://webcomponents.hax.cloud/elements/haxcms-elements/demo/index.html>, keeps working as it is.

It runs its own site, **Try HAX** (`site/`: `site.json` and `pages/`), a short tour a visitor can edit for
five minutes: editing a page, blocks that teach, the outline, themes (`?theme=` previews any theme in
`lib/themes.json`) and how to make your own. Nothing is saved; the demo's save endpoints only pretend.
To change the tour, edit `site/pages/*/index.html` or use the HAX CLI on `site/` (`hax site node:add`).

This folder is its own Vercel project (Root Directory `demo`). It builds:

- `build/build.sh` fetches the deployed demo page and `build/top-level.py` changes its `<base>` from the
  demo folder to `/` (and makes the one folder-relative path, `../lib/themes.json`, absolute). The build fails
  if the page no longer has those, rather than publishing a demo that silently breaks.
- the build copies `site/` beside it, and Vercel serves those files before any rewrite, so this site's
  `site.json` and pages win over the demo folder's.
- `vercel.json` proxies everything else back to webcomponents.hax.cloud: `/elements/*` and `/node_modules/*`
  as they are, any other path with a file extension (`theme/…`, `custom/…`, `assets/…`,
  `dist/dev/…`) from the demo folder, and every other path (a page route) gets the page.

Asset requests always reach the latest webcomponents deploy. The page itself (import map, app settings)
updates when this project redeploys; `DEMO_SOURCE` points the build at another deploy, e.g. a webcomponents
preview.
