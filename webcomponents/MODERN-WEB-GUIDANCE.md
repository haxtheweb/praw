# Modern Web Guidance in HAX

[Modern Web Guidance](https://github.com/GoogleChrome/modern-web-guidance) (MWG) is a set of agent skills from the Chrome team (with Firefox and Edge contributing) that carry web platform best practices and Baseline data. HAX uses it as **advice**: it reviews and hints, it never blocks, and HAX rules win where they disagree.

Tracking: <https://github.com/haxtheweb/issues/issues/3298>

## Rules that govern it

| Rule | ID | What it settles |
| --- | --- | --- |
| Browser Support Policy — Baseline | `4e0800ef-32ff-42dc-83f0-bbb953d97554` | Replaces MWG's "only Widely available is safe" default |
| HAX Rules Win Over Modern Web Guidance | `f54de8cb-0b65-4f50-98e6-43e8c2ebc4c7` | The conflict list |
| Outside Skills Are Version-Pinned | `d2a1207c-b6d1-4cd6-9930-bd21b29a516c` | Exact version, no telemetry in CI |
| Shadow-Boundary ARIA References | `410c4334-a186-4356-9584-0796e5d2bc2d` | The web component lessons taken from MWG |

Full text: <https://github.com/haxtheweb/praw/blob/main/RULES.md>

## Running it

Always run the version pinned in [`skills-lock.json`](https://github.com/haxtheweb/praw/blob/main/skills-lock.json), never `@latest`:

```sh
DISABLE_TELEMETRY=1 npx -y modern-web-guidance@1.0.0 search "light dismiss dialog"
DISABLE_TELEMETRY=1 npx -y modern-web-guidance@1.0.0 retrieve "<guide-id>"
DISABLE_TELEMETRY=1 npx -y modern-web-guidance@1.0.0 legacy-scan elements/<element> --json
```

- The guide corpus ships inside the npm package, so the npm version is the pin. `--skill-version` only tags telemetry and update notices; it does not pin.
- The CLI sends usage telemetry to Google unless `DISABLE_TELEMETRY=1` is set. Set it in every CI and scheduled job.
- License: code Apache-2.0, guide content CC BY 4.0. Quoting a guide in HAX docs needs attribution.

## Advisory PR review (webcomponents)

Fold MWG into the existing Claude review pass on webcomponents PRs; do not add a separate bot. The added review instructions:

> For changed files under `elements/`, use Modern Web Guidance (pinned version, `DISABLE_TELEMETRY=1`) to check accessibility, HTML semantics, forms and platform API use. Comment only when you find something, and only on lines the PR changed. Drop any finding that conflicts with praw rule `f54de8cb-0b65-4f50-98e6-43e8c2ebc4c7` or the browser support policy `4e0800ef-32ff-42dc-83f0-bbb953d97554`. Label each finding "MWG (advisory)" and name the guide id. Never request changes or block.

MetaMask runs the same pattern: in its first five weeks the bot reviewed about 480 PRs, commented on 64, and engineers fixed 43 findings, mostly accessibility, semantics and forms.

## Weekly `legacy-scan` (Sunday)

Same shape as the other Sunday jobs: results ready for Monday review, one rolling output, nothing auto-merged.

- Run `legacy-scan elements --json` at the pinned version against latest `master`.
- Skip generated and third-party files (`node_modules`, `dist`, `locales`, `custom-elements.json`, vendored libraries).
- Filter out findings the HAX conflict list rejects, then group the rest by element.
- Update one rolling report or PR; open nothing when the filtered list is empty.
- It is a hint list, not a to-do list: `legacy-scan` only covers the guides with deterministic rules (about 20% of the corpus), and a match can be a deliberate fallback. A fix that would change an authorable element's front-end API is out.

## Triage cheat sheet

| MWG tends to suggest | HAX position |
| --- | --- |
| Optional chaining, `window` globals | `?.` banned in webcomponents; use `globalThis` |
| Extensionless or bare imports | HAX's own modules use explicit `.js` paths; third-party bare is fine |
| `confirm()` / `prompt()` for quick confirmations | HAX UI dialogs only |
| Strict CSP, upgrade `http:` resources, restrict outbound connections | Authored `http` links and resources stay working |
| `frame-ancestors` / `X-Frame-Options` | Site pages stay embeddable (Canvas and other LMSs iframe them) |
| Raw color/spacing values in examples | DDD tokens (`--ddd-*`, HAX UI tokens) |
| Rename or restructure attributes while modernizing | Not on authorable elements; all content ever made must keep working |
| Fallbacks for anything not Widely available | Newly available is fine behind feature detection; no polyfills |

## Contributing back

MWG accepts outside guides through its `CONTRIBUTING.md`. Things HAX knows that MWG does not cover yet:

- **Lit SSR of web components**: what runs on the server, attribute vs property bindings, meaningful first render, progressive-enhancement fallbacks (from rule `1b8b8a93-0458-41f9-85a4-ba8d16923765`).
- **Meaning channels**: conveying correct/incorrect and consequential decisions through label, color, focus, texture and icon (rule `8d0c033b-7c96-4c6e-aafc-7dfff8ad9123`).
- **RTL layout checks**: logical properties, pseudo-locale and RTL testing of component UIs.

Propose one at a time, starting with whichever has the clearest evals, and record each submission on the tracking issue.
