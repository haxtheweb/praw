# demo.hax.cloud

The live HAXcms demo from [webcomponents](https://github.com/haxtheweb/webcomponents)
(`elements/haxcms-elements/demo/`), served from the top of its own domain, so pages read
`demo.hax.cloud/<page>` and deep links load directly. The demo at its direct path,
<https://webcomponents.hax.cloud/elements/haxcms-elements/demo/index.html>, keeps working as it is.

It runs its own site, **Try HAX** (`site/`: `site.json` and `pages/`), a short tour a visitor can edit for
five minutes: editing a page, blocks that teach, the outline, themes (`?theme=` previews any theme in
`lib/themes.json`) and how to make your own. Nothing is saved; the demo's save endpoints only pretend.
To change the tour, edit `site/pages/*/index.html` or use the HAX CLI on `site/` (`hax site node:add`).

This folder is its own Vercel project (Root Directory `demo`). Every deploy compiles the demo from
webcomponents `master`, so it always runs the latest code, and every HAX module, style and registry file
is served from demo.hax.cloud itself: nothing loads from cdn.hax.cloud or webcomponents.hax.cloud, and the
browser's network panel shows the whole HAX load on one origin.

- `build/build.sh` runs `build/compile-webcomponents.sh`, which fetches webcomponents at `WC_REF` (default
  `master`), installs it and runs the build half of `ubiquity` in that throwaway checkout: `polymer build`, the xterm and latex2html5 vendor copies,
  CSS template minify, terser, then `wc-autoloader` to regenerate `wc-registry.json` from the compiled
  tree (so elements added on master load before the next ubiquity release) and the third-party license
  file. It never publishes anything. About five minutes; the output is ~250 MB in ~46,000 files.
- the demo folder (`elements/haxcms-elements/demo/`: `theme/`, `custom/`, `dist/dev/` save stubs,
  `wc-registry.json` ...) goes at the top of `_site`, the compiled tree at `_site/node_modules/`, and
  `site/` over both, so this site's `site.json` and pages win.
- `build/top-level.py` changes the demo page's `<base>` from the demo folder to `/`, points
  `../lib/themes.json` at the compiled copy, and adds an import map (built from the compiled tree) for the
  page's own module script and `custom/src/`, the only code that still uses bare imports. The build fails
  if the page no longer has those, or the registry looks incomplete, rather than publishing a demo that
  silently breaks.
- `build/top-level.py` also puts the HAX network bar's demo strip (`<hax-network-bar demo>`) above the demo:
  it says the demo has no backend, so nothing is saved, and links HAXcms in the browser
  (browser.hax.cloud) and Install HAX. The strip sets `--haxcms-top-offset`, so the editor bar, Merlin,
  toasts and the edit tray sit under it. It is left out when the compiled bar has no demo mode.
- hax.cloud (`ecosystem/build/site.sh`) runs the same `build/compile-webcomponents.sh` and ships the
  compiled tree as its own `build/`; the script lives here because this folder is its own Vercel project.
- `vercel.json` serves files first, maps any old `/elements/<name>/...` path to
  `/node_modules/@haxtheweb/<name>/...`, and gives every extension-less path (a page route) the page.

`WC_REPO` / `WC_REF` set as Vercel environment variables point the build at another source, e.g. a
webcomponents pull request branch.
