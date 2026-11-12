# demo.hax.cloud

The live HAXcms demo from [webcomponents](https://github.com/haxtheweb/webcomponents)
(`elements/haxcms-elements/demo/`), served from the top of its own domain, so pages read
`demo.hax.cloud/<page>` and deep links load directly. The demo at its direct path,
<https://webcomponents.hax.cloud/elements/haxcms-elements/demo/index.html>, keeps working as it is.

This folder is its own Vercel project (Root Directory `demo`). It holds one built file:

- `build/build.sh` fetches the deployed demo page and `build/top-level.py` changes its `<base>` from the
  demo folder to `/` (and makes the one folder-relative path, `../lib/themes.json`, absolute). The build fails
  if the page no longer has those, rather than publishing a demo that silently breaks.
- `vercel.json` proxies everything else back to webcomponents.hax.cloud: `/elements/*` and `/node_modules/*`
  as they are, any other path with a file extension (`site.json`, `pages/…`, `theme/…`, `custom/…`,
  `dist/dev/…`) from the demo folder, and every other path (a page route) gets the page.

Asset requests always reach the latest webcomponents deploy. The page itself (import map, app settings)
updates when this project redeploys; `DEMO_SOURCE` points the build at another deploy, e.g. a webcomponents
preview.
