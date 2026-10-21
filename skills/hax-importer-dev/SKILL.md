---
name: hax-importer-dev
description: "Build a new site importer (a platform-to-HAXcms converter such as Quarto, VitePress, GitBook or OpenStax) end to end: Node and PHP converters, dispatcher, OpenAPI spec, API error codes, client service and chooser card, i18n, and tests. Use when asked to add or change an importer, or to support migrating a new format or CMS into HAX."
version: 1.0.0
license: Apache-2.0
metadata:
  author: haxtheweb
  depends_on: [hax-backend-dev, hax-testing, hax-managed-files, hax-i18n-translate]
  tags: [hax, haxcms, importer, migration, convert, nodejs, php, openapi, mfr, app-hax]
---

# HAX importer development

An importer turns an outside source (a git repo, a site URL, an uploaded file) into HAXcms JSON Outline
Schema items plus a map of files to download. HAX ships many of them, and each new one touches the same
places in four repos. This skill is the checklist, the contract, and the security posture, so an agent
spends its effort on parsing the source format and not on rediscovering the wiring.

Everything resolves through public URLs, so it works from a local clone or a cloud agent:

- Node backend: https://github.com/haxtheweb/haxcms-nodejs
- PHP backend: https://github.com/haxtheweb/haxcms-php
- Client (app-hax, micro-frontend-registry): https://github.com/haxtheweb/webcomponents
- Rules: https://github.com/haxtheweb/praw/blob/main/RULES.md
- Work queue: https://github.com/haxtheweb/issues

## When to use

- Adding an importer for a new platform or format.
- Extending an existing importer (new source shape, new content transforms).
- Reviewing an importer plan someone drafted. Check it against the contract below first.

For backend parity in general, load `hax-backend-dev`. For test commands, load `hax-testing`. This skill only
covers what is specific to importers.

## Read the current code before you design

Layouts and conventions move, and plans drift. Before writing a plan or code, read, from `main`:

1. The reference converter closest to your source (below), in **both** backends.
2. `siteImport` in each backend (the dispatcher).
3. The matching entries for that reference in the OpenAPI spec, the API-code file, the client registry, the
   chooser card, and the tests.

Pick the reference by source shape, not by familiarity:

| Source shape | Reference | Why |
|---|---|---|
| Git repo with a config file declaring the outline plus markdown pages | `convertVitepressToSite` (Node `src/systemRoutes/v1/routes/imports/`, PHP `system/backend/php/lib/systemRoutes/v1/imports/`) | Current best practice: config read as data, safe fetch and YAML, limits, asset map, license attribution, fixture-based tests, exact Node/PHP parity |
| Markdown repo with an index file (SUMMARY.md style) | `convertGitbookToSite` | Simple, but older: it predates several of the hardening conventions below. Do not copy its fetch or error handling |
| Structured book with parts and chapters from an API | `convertOpenstaxToSite` | Hierarchy built from a remote table of contents |
| CMS or site URL | `convertWordpressToSite`, `convertDrupalToSite`, `convertPloneToSite` | Discovery, pagination, metadata |
| Single uploaded file | `importDocx`, `importPdf`, and similar | File inputs go through a different route family |

If an issue plan says to mirror an older converter, compare it with the VitePress reference and say where
the plan is out of date.

## The output contract

A converter returns `{ status: 200, data: { items, filename, files, ... } }`:

- `items`: `JSONOutlineSchemaItem` objects with `title`, `slug`, `order`, `indent`, `parent` (the parent
  item's `id`, or null for top level), `contents` (sanitized HTML), and `metadata`. Set
  `metadata.sourceType` to the platform and keep source details (repo, branch, path, license, author,
  accessed date) under a namespaced key. Set `metadata.source` to the page's public URL when it is known.
- `files`: a map of `files/<name>` to the source URL. `files/` is flat, so keep basenames unique.
  Only extensions `createSite` accepts are importable; anything else keeps its source URL in the content.
  The file map carries URLs, and `createSite` downloads them behind its own SSRF guard. The converter never
  downloads assets itself.
- `filename`: the site name.
- Optional: `site: { license }`, `truncated`, and a list of unmapped source components, so the client can
  tell the user what did not convert.
- Errors use `{ status, data: { error, items: [], filename: null, files: {} } }`.
  400 for a bad request, 422 when the source is readable but is not what the importer expects or has no
  pages, 403 for authorization.

Each page: split front matter, render markdown with `markdown-it`, map source-specific syntax to HAX
elements where one exists (`media-image`, `video-player`, `license-element`, `oer-schema`), unwrap what has no
equivalent, and report it. Rewrite in-book links to the imported slugs, and rewrite image and file
references into the file map. A page that cannot be read gets a link back to the source, never an empty
page that looks successful.

Titles resolve in this order: an explicit outline label from the source's own navigation, then front matter
title, then the first heading, then file name. The outline label wins because it is what the author chose to show
in the table of contents, and it keeps slugs stable. Slugs derive from the outline
path (parent slug plus title slug), never from file basenames alone, because `ch1/index` and `ch2/index`
collide.

## Security posture (non-negotiable)

`repoUrl` and every file the converter reads are caller-controlled. These apply to both backends:

- **Never execute the source's code.** Do not `require`, `eval`, or run a repo's config. Read configuration as
  data. If it cannot be read as plain data, fall back to the file tree, the way VitePress does.
- **Network only through the safe fetchers**: `safeFetch` in Node and `SsrfGuard` in PHP. No bare `fetch`,
  `curl`, or `file_get_contents` on caller-influenced URLs. Send `User-Agent: HAXcms-Import/1.0` to GitHub;
  without it every call 403s and a swallowed error looks like an empty repo.
- **Parse YAML with `loadYamlSafely`** (Node `src/lib/safeYaml.js`), which caps size and rejects anchors
  and aliases. Do not call `js-yaml` directly. Front matter that fails to parse falls back to `{}`.
- **Escape everything written into HTML**: `escapeHTMLAttribute` for attributes, and sanitize rendered
  content. Content from the source is untrusted.
- **Bound the work.** Define a `LIMITS` object (max pages, max files, total fetch budget in seconds, delay
  between requests, and for formats with includes or transclusion a max include count and depth), mark the
  result `truncated` when a limit hits, and export `LIMITS` so tests can lower them. Keep the PHP values
  identical.
- **Return client-safe errors** with `clientSafeErrorDetail`. No paths or stack traces reach the response.
- **GitHub limits apply.** Unauthenticated API calls are rate-limited. Fetch the tree once and read file
  contents from `raw.githubusercontent.com`.

## Wiring checklist

Nothing is discovered automatically. Miss one of these and the importer is unreachable or untested.
(OpenStax shipped unreachable once for exactly that reason; see haxtheweb/issues#2912.)

### haxcms-nodejs

1. New converter `src/systemRoutes/v1/routes/imports/convert<Name>ToSite.js`. CommonJS, `async function
   convert<Name>ToSite(req, res)`, exports the function and `LIMITS`. **No optional chaining** (`?.`)
   anywhere; the toolchain does not allow it.
2. Dispatcher `src/systemRoutes/v1/routes/siteImport.js`: `require`, a `case '<platform>'`, and the
   supported-platforms doc comment.
3. Spec `src/openapi/system-spec.yaml`: a `/system/api/v1/site/import/<platform>` path with
   `operationId: <platform>ToSite` (that id becomes the `@system/<platform>ToSite` service name),
   request schema (`repoUrl`), and 200/400/403/422 responses. Also update the platform list in the generic
   `{platform}` description and the importer list in the `ImportData` schema description.
4. API codes `src/lib/haxcmsApiCodes.json`: add regexes for the converter's error strings to the right
   code (`IMPORT_EMPTY`, `IMPORT_SOURCE_INVALID`, `IMPORT_FETCH_FAILED`, `IMPORT_FAILED`). An uncoded
   error reaches the client as raw English. Add one example per new message to the `EXAMPLES` list in
   `test/unit/api-message-codes.test.cjs`.
5. Test `test/unit/convert<Name>ToSite.test.cjs`.

### haxcms-php

Same contract, same outline, slugs, file map, status codes and error strings.

1. `system/backend/php/lib/systemRoutes/v1/imports/convert<Name>ToSite.php`, wrapped in
   `function_exists` guards, with limits overridable through a `$GLOBALS` hook for tests.
2. `system/backend/php/lib/systemRoutes/v1/siteImport.php`: `include_once` and a `case`.
3. `system/backend/php/lib/systemRoutes/openapi/system-spec.yaml`: the same spec edits.
4. `system/backend/php/lib/haxcms-api-codes.json`: the same code edits.
5. `system/backend/php/tests/run.php`: add the platform to the platform list and the file map.
6. `system/backend/php/tests/Unit/Convert<Name>ToSiteTest.php`.

### webcomponents

1. `elements/micro-frontend-registry/lib/microServices.js`: a `MicroFrontendRegistry.add` entry with
   `endpoint`, `name: "@system/<platform>ToSite"`, `title`, `description`, `params`.
2. `elements/micro-frontend-registry/test/micro-frontend-registry.test.js`: add the pair to the importer list.
3. `elements/app-hax/lib/v2/app-hax-use-case-filter.js`: strings in the `this.t` block
   (`<platform>ImportDescription`, `<platform>ImportPrompt`, and a tooltip if the icon needs one) and a card
   in `getImportItems()` with `importKind: "url"`, `importType`, `callback`, `param: "repoUrl"`, `prompt`,
   `useCaseTitle`, `useCaseDescription`, `useCaseIcon`, `useCaseTag: ["Import", "<Name>"]`.
4. `elements/app-hax/locales/app-hax-use-case-filter.<lang>.json`: the new keys in every locale file. Use
   the `hax-i18n-translate` skill. Do not hand-edit around it.
5. `elements/app-hax/test/app-hax-use-case-filter.test.js`: a card test next to the existing ones.
6. `elements/haxcms-elements/lib/haxcms-api-codes.json`: the bundled copy of the API-code catalog (it is the
   stated source of truth; the backends mirror it). Apply the same regex additions as in the backends. The
   per-language `haxcms-api.<lang>.json` files key on the existing codes, so they need no change.

In a blobless or sparse clone of webcomponents, never `git grep` across history: it fetches blobs one at a
time. List paths with `git ls-tree -r HEAD --name-only`, read one file with `git show HEAD:<path>`, and add
only the directory you need with `git sparse-checkout add`. Also check that your prettier version matches the
repo's before running `--write`; a different major version reformats unrelated lines.

Do not run the ubiquity script or a top-level monorepo build. After the PR merges, a maintainer runs it
(see `hax-release-prep`).

## Testing

- The network is stubbed at `safeFetch`; the suite never leaves the machine. Build a small **synthetic
  fixture repository** in memory (an object of path to contents, plus a tree listing) that carries every
  shape the importer handles. Do not commit third-party content as a fixture.
- Cover: outline from config, nested groups, the file-tree fallback, each page transform, front matter
  title override, asset registration and unique names, link rewriting, unmapped components, each limit, and
  each error path (missing `repoUrl`, bad host, no config, no pages, unreadable page).
- Run the tier from `hax-testing`: `npm run test:unit`, `npm run test:api-conformance`, and `precheck` in
  Node; PHPUnit and `yarn test` in PHP; the registry and app-hax tests in webcomponents. If a tier cannot
  run in your environment, say which and why in the PR.

## Trying it on a real source

A real repository is good for finding gaps, and only for that.

- Run the converter **locally** and inspect the output. Do not publish, deploy, or commit converted
  content, and do not put it in a PR, a test fixture or a demo site.
- Many sources are not openly licensed or restrict derivatives. A test run is not permission to
  redistribute, so check the repo's license before using it for anything beyond a local check.
- Prefer sources whose license allows derivatives when choosing a demo target.
- Record what the real run revealed (shapes the fixture missed) by adding a **synthetic** case to the
  fixture, not the real content.
- If the sandbox cannot reach the GitHub API (HTTP 403), clone the repo read-only into a scratch directory
  and run the converter with `safeFetch` replaced by a stub that serves the tree and raw files from disk.
  Keep the script and its output outside the repository.
- A first real run typically reveals syntax that straddles another construct, for example a figure caption
  that contains inline code and so splits across the code-span pass. Run inline rewrites that can contain
  code spans before the code-span protection pass, and guard against matches that start inside a code span.
- Check the converted output with counts, not eyeballs: leftover fences, attribute blocks, shortcodes,
  cross-reference keys and broken links across every page.

## Workflow

1. Read the issue in https://github.com/haxtheweb/issues and any plan comment. Check the plan against
   the reference converter; flag anything stale.
2. Inventory the source format: where the outline lives, page file types, front matter, special syntax,
   asset conventions, and the license signals it carries.
3. Write the Node converter and its tests against the synthetic fixture.
4. Wire the dispatcher, spec, API codes.
5. Port to PHP, structure for structure, then mirror the tests.
6. Wire the client: registry service, chooser card, strings, locales.
7. Run each repo's tests and pre-submission check.
8. Open **one PR per repo**, cross-linked and referencing the issue. Each description says what the PR
   touches and which commands you ran with their results. Do not merge; maintainers review.

## Guardrails

- Link between repos by public URL, never by a local filesystem path.
- Do not add `@haxcms/` registrations or touch the CLI's legacy `--import-structure` path.
- Do not hand-edit generated files, `build/`, or `node_modules/`; load `hax-managed-files` first.
- A change that lands in only one backend is a bug in the other.

## Checklist before opening the PRs

- [ ] Converter follows the output contract and security posture, in Node and PHP.
- [ ] Dispatcher, spec (path, platform list, `ImportData` note), and API codes updated in both backends.
- [ ] Client service, chooser card, strings, and every locale updated.
- [ ] Tests added in all three repos and passing, or the gap stated in the PR.
- [ ] No optional chaining in Node; no direct network calls; no code from the source executed.
- [ ] No third-party content committed or published.
- [ ] PRs cross-link and reference the issue; nothing merged.
