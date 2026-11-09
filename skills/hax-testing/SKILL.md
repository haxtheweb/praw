---
name: hax-testing
description: "Find and run the right tests per HAX repo, write the test for a new endpoint, and write or replay fuzz (fast-check property) tests. Use before opening any PR in haxcms-nodejs, haxcms-php, webcomponents or create, when asked how to test a backend or element change, or when fuzzing, property-based testing, seeds or test:fuzz come up."
version: 1.1.0
license: Apache-2.0
metadata:
  author: haxtheweb
  depends_on: [hax-managed-files]
  tags: [hax, testing, haxcms, nodejs, php, phpunit, conformance, e2e, ci, fuzzing, fast-check, property-based]
---

# HAX testing

Tests are how you verify an outcome before reporting it (the "AI Guardrails — Verify Outcomes" rule in
https://github.com/haxtheweb/praw/blob/main/RULES.md). Run the tier that matches what you changed, and
add a test whenever you add an endpoint or change behavior.

## haxcms-nodejs

Repo: https://github.com/haxtheweb/haxcms-nodejs. Tests use `node:test` and live in `test/`.

| Command | What it covers |
|---|---|
| `npm test` | Unit plus API conformance |
| `npm run test:unit` | `test/unit/*.test.cjs` |
| `npm run test:api-conformance` | v1 site and system routes checked against `src/openapi/*-spec.yaml` |
| `npm run test:e2e` | Headless-browser UI workflows; needs Chrome or Chromium (`PUPPETEER_EXECUTABLE_PATH` overrides detection) |
| `npm run test:e2e:update` | Regenerate screenshot baselines after an intentional UI change |
| `npm run test:coverage` | c8 coverage over lib, routes and entry files |
| `npm run precheck` | Prettier and ESLint on the files you changed (`precheck:fix` auto-fixes) |

## haxcms-php

Repo: https://github.com/haxtheweb/haxcms-php.

| Command | What it covers |
|---|---|
| `composer install` in `system/backend/php`, then `yarn test` | PHPUnit (`tests/Unit` and route tests) |
| `npm run test:e2e` | Browser workflows in `test/e2e/` (runs with `--test-concurrency=1`) |

CI (`.github/workflows/tests.yml`) runs PHPUnit on PHP 8.3 from `system/backend/php`. A cloud agent needs
the same PHP extensions the workflow installs (mbstring, xml, dom, simplexml, gd, zip, curl, intl,
fileinfo, iconv, xmlreader, xmlwriter, zlib) before `composer install` will work.

## webcomponents

Repo: https://github.com/haxtheweb/webcomponents. Run tests from that repo with the filter form its
`AGENTS.md` documents (`npm run test --filter <component_name>`). Never run a build at the monorepo top
level; use the component's own `yarn run build` after changes that affect generated metadata.

## Before you push or open a PR

Run these in the repo you changed, after your last edit, and again if you commit more. Read that repo's
`AGENTS.md` and `package.json` scripts first; each repo names its own checks.

| Repo | Run before pushing |
|---|---|
| haxcms-nodejs, create | `npm run precheck` (Prettier and ESLint on changed files), then the test tier above |
| webcomponents | `yarn precheck`, then `yarn test` in the element's folder |
| haxcms-php | PHPUnit from `system/backend/php`; it has no `precheck`, so also run the node-side `precheck` for the mirrored change |

- ESLint is not enough. It usually ignores test files, which Prettier still checks, so a new test file can
  pass lint and fail format. `precheck` runs both.
- The Claude Code hook that blocks `git push` and `gh pr create` until `precheck` passes does not fire for a
  PR opened with `gh api` or from another working directory. Run `precheck` yourself first.
- In a sparse or partial checkout `precheck` may be missing. Run Prettier and ESLint with the repo's own
  config on the changed files and note in the PR description what could not be run.
- After pushing, read the PR's CI results (`gh pr checks`, or the REST API) and fix failures. State in the PR
  description which checks you ran.

## Recipe: test a new or changed endpoint

1. Add or update the route's entry in `site-spec.yaml` or `system-spec.yaml` first. Conformance tests read
   the spec, so a missing entry fails them.
2. Add a unit test in `test/unit/` (Node) covering success, validation failure and auth failure.
3. Run `npm run test:api-conformance` to confirm the live route matches the spec.
4. Mirror the endpoint in haxcms-php (see `hax-backend-dev`) and add a PHPUnit test under
   `system/backend/php/tests/`.
5. Run `yarn test` in the PHP repo, then each repo's pre-submission check.
6. Put the commands you ran and their results in the PR description.

## Fuzz / property-based tests

HAX uses [fast-check](https://fast-check.dev/) for property-based fuzzing in create, haxcms-nodejs and
webcomponents, with one convention across all three (https://github.com/haxtheweb/issues/issues/3272).

**When to write one.** Code that sanitizes, validates, parses or bulk-saves untrusted input: HTML and URL
sanitizers, path and name validators, importers, `saveOutline`-style writes. State what must *always*
hold, not one expected output: "never throws", "never lets a `javascript:` URL through", "the rewrite
returns the same output as the old regex" (differential). Bias generators toward the dangerous shapes
(`..`, `%2e`, `\0`, event-handler attributes, mixed-case protocols) instead of only `fc.string()`.

**Where the parameters come from.** Never hardcode `{ numRuns }` without a seed; that draws a new random
seed on every CI run, so a red build can't be reproduced. Use the repo's helper:

| Repo | Helper | Example |
|---|---|---|
| create, haxcms-nodejs | `test/_helpers/fuzz-config.cjs` | `const RUNS = fuzzConfig({ defaultSeed: 20261109 });` |
| webcomponents | `scripts/test-setup/fuzz-config.mjs` | `import { fuzzConfig } from "../../../scripts/test-setup/fuzz-config.mjs";` |

Pass `RUNS` as the last argument to every `fc.assert`. Pick a new integer `defaultSeed` per file (today's
date works). In webcomponents the test runner copies `HAX_FUZZ_*` into the browser page, so the same
variables work for element tests.

**Running.**

| Goal | Command |
|---|---|
| Normal run (fixed seed, same inputs every time) | `npm test` / `yarn test` |
| Hunt for new bugs (random seed, thousands of runs) | `npm run test:fuzz` (create, haxcms-nodejs); `yarn test:fuzz` at the webcomponents root |
| Replay a reported failure | `HAX_FUZZ_SEED=<seed> HAX_FUZZ_PATH=<path> npm run test:unit` |
| More depth on the fixed seed | `HAX_FUZZ_RUNS=5000 npm test` |

A fast-check failure prints `{ seed, path }` and the shrunk counterexample; those two values are the replay.
Bad values (`HAX_FUZZ_SEED=abc`) throw rather than silently changing the run. haxcms-nodejs still accepts
the older `HAXCMS_FUZZ_*` names.

**Naming.** End the file in `-fuzz.test.js` so `test:fuzz` picks it up. Prefer `.js` over `.cjs` where the
repo's lint config allows it: the OpenSSF Scorecard Fuzzing check only scans `.js`/`.jsx` for fast-check.

**When a hunt finds something.** Fix the code, then pin the counterexample: add it to that property's
`examples` option or write a plain example-based test beside it, so the fixed-seed run guards it from
then on. Say in the PR which seed found it.

## Rules of thumb

- Run the smallest tier that proves the change, then the full unit and conformance run before the PR.
- Visual e2e diffs warn rather than fail; read the warnings.
- If a test cannot run in your environment (no Chrome, no PHP), say which and why in the PR. Do not
  claim it passed.
- Do not edit generated files or `build/` to make a test pass. Fix the source.
