---
name: hax-editor-preview
description: "Build a throwaway page that runs a HAX web component inside the real HAX editor (h-a-x) as static files, to check it is wired into the app store and editable. Use when asked to preview or play with a new or changed element in the HAX editor. Not for writing the element's demoSchema."
version: 1.0.0
license: Apache-2.0
metadata:
  author: haxtheweb
  depends_on: [hax-managed-files, hax-testing]
  tags: [hax, demo, h-a-x, appstore, haxproperties, esbuild, playwright, preview]
---

# HAX editor preview

This is not the element's `demoSchema` (the sample block in `haxProperties` that HAX offers in Blocks). Author that in the
element itself. This skill builds a disposable page that boots the real `<h-a-x>` editor with your element in its app store. It answers: does
the element register, appear in Blocks, open its settings form from `haxProperties`, and write its data to
light DOM. It is a wiring check, not a release step. It never touches the PR, the registry, or the
monorepo build.

"HAXcms housing" means the `<h-a-x>` editor shell and tray, not a full HAXcms site with a backend. Say
which you built; build the full site only if asked (see `hax-site-structure`).

## Output

A `dist/` folder of static files: `index.html`, `appstore.json`, `assets/*.js`, and the runtime-fetched
files under `node_modules/@haxtheweb/...`. Serve it with any static server. A host that only runs your own
files (a sandboxed page, a static host) works because nothing resolves bare imports at runtime.

## Steps

1. **Scratch project, outside the repo.** `npm init -y`, then install the published packages the editor
   loads: `@haxtheweb/h-a-x`, `media-image`, `accent-card`, `grid-plate`, `a11y-collapse`, and anything the
   bundler reports missing. Install clean. Never copy another `node_modules` over it. Copy your element's
   folder to `node_modules/@haxtheweb/<tag>/` from the working branch. npm prunes hand-copied folders, so
   copy again after any install.
2. **`appstore.json`.** Keys `status`, `apps`, `stax`, `autoloader`. Keep it small. `autoloader` maps a tag
   to its module path, and your tag must be in it: `"<tag>": "@haxtheweb/<tag>/<tag>.js"`.
3. **`entry.js`.** Generate it from `autoloader`: one `import` per value, plus
   `@haxtheweb/h-a-x/h-a-x.js`. The HAX store skips dynamic import when a tag is already defined, so
   bundling the element is what makes it available.
4. **Bundle with esbuild.** `bundle`, `format: 'esm'`, `splitting`, `minify`, output to `dist/assets`.
   Add an `onLoad` plugin that rewrites `import.meta.url` per module to
   `new URL("<path relative to dist>", document.baseURI).href`. Without it, runtime fetches of
   `haxProperties` JSON, locales, and SVG icons resolve to the wrong place. Expect about 40 files and 2 MB.
5. **`index.html`.** Inline script: `globalThis.process = { env: { NODE_ENV: 'production' } }` and
   `globalThis.WCGlobalBasePath = new URL('node_modules/', document.baseURI).href`. Then
   `<script type="module" src="assets/entry.js">` and
   `<h-a-x app-store='{"url":"appstore.json"}'>` wrapping sample content that uses your element, with its
   light-DOM data authored the way the element reads it. Give the page a real background for light and
   dark so you can test both.
6. **Find runtime-fetched files.** Serve `dist`, open it in headless Chromium (playwright-core, point
   `executablePath` at the installed browser, pass `--no-sandbox`), and log every response with status 400
   or more plus page errors. Copy each missing path from `node_modules` into `dist` at the same
   `node_modules/...` path. Repeat until there are no 404s and no page errors. It took two passes.
7. **Verify the wiring, then look.** The store instance is `globalThis.HaxStore.instance` (note the casing; `HAXStore` is an
   import name, not a global; `Hax.get('elementList')` also works). It should list your tag in `elementList` and in `gizmoList`. Your array or object properties should be
   populated from light DOM. Take a screenshot, and one in dark mode.
8. **Hand it over.** Say what it is, that edits are not saved, which "housing" you built, and what you did
   not test by hand (opening Edit, using the settings form, saving).

## Gotchas

- Do not `pkill -f <script>`; it can kill your own shell. Use a fresh port and an exact `pgrep` pattern.
- The published hax-body imports `@haxtheweb/image-gallery` without declaring it (fixed upstream in
  haxtheweb/webcomponents#944). On older releases, install it by hand.
- Fonts and most outside hosts may be blocked in a sandbox. The demo needs none.
- A native `legend` straddles its fieldset border and gets clipped on dark pages. Test on dark too.
- Keep the demo separate from the PR. Never merge it, and never run the ubiquity script or a monorepo
  build (`hax-release-prep`).

## Publishing it

Where the harness can host files, publish `dist/` as-is (every file keeps its relative path). Where it
cannot, stop at the folder and tell the person the one-line static-server command to run it.
