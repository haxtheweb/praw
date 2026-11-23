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

MWG is folded into the existing Claude review pass on webcomponents PRs; there is no separate bot. The instructions live in [`REVIEW.md`](https://github.com/haxtheweb/webcomponents/blob/master/REVIEW.md) at the root of webcomponents, the file Claude Code Review reads from the default branch. A review reads the diff and the code around it and runs nothing, so the instructions state the checks themselves instead of calling the CLI:

> For changed files under `elements/`, also review against Modern Web Guidance: accessibility, HTML semantics, forms and platform API use. Comment only when you find something, and only on lines the PR changed. Drop any finding that conflicts with praw rule `f54de8cb-0b65-4f50-98e6-43e8c2ebc4c7` or the browser support policy `4e0800ef-32ff-42dc-83f0-bbb953d97554`. Start each finding with "MWG (advisory)" and name the guide id. Nit at most; never a reason to hold a merge.

An agent reviewing in a session that can run commands may also `retrieve` the guide at the pinned version to quote it accurately.

MetaMask runs the same pattern: in its first five weeks the bot reviewed about 480 PRs, commented on 64, and engineers fixed 43 findings, mostly accessibility, semantics and forms.

## Weekly `legacy-scan` (Sunday)

[`legacy-scan.yml`](https://github.com/haxtheweb/webcomponents/blob/master/.github/workflows/legacy-scan.yml) in webcomponents runs [`scripts/legacy-scan.mjs`](https://github.com/haxtheweb/webcomponents/blob/master/scripts/legacy-scan.mjs) on Sunday evening and on demand (`yarn legacy-scan [element ...]` locally). Same shape as the other Sunday reports: plain scripting, results ready for Monday.

- It runs `legacy-scan elements --json` at the pinned version, after checking the tarball's sha512 against the pin, with `DISABLE_TELEMETRY=1`.
- It leaves out third-party and generated files, plus anything listed with a reason in `scripts/legacy-scan.set-aside.json` (a guide, or one guide in one file, that HAX has decided not to follow), then groups the rest by element.
- The report goes to the job summary and nowhere else. The job has a read-only token and never opens an issue or a PR, comments, labels, merges or deploys.
- Each guide is listed with the Baseline status of the features it names, so the browser support policy can be applied at a glance.
- It is a hint list, not a to-do list: `legacy-scan` only covers the guides with deterministic rules (33 of them at 1.0.0, about 20% of the corpus), and a match can be a deliberate fallback. A fix that would change an authorable element's front-end API is out.
- A version bump changes `skills-lock.json` here and `MWG_VERSION` / `MWG_INTEGRITY` in the script, each in its own PR.

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

MWG takes outside guides, but not in the repository the npm package is published from: [`GoogleChrome/modern-web-guidance`](https://github.com/GoogleChrome/modern-web-guidance) is a publish target, and its `CONTRIBUTING.md` sends issues and pull requests to the source repository, <https://github.com/GoogleChrome/modern-web-guidance-src>. Open a proposal issue there first, one candidate at a time, and record each submission on the tracking issue. Before filing, read that repository's contributing guide for the guide file format, its eval requirements and its contributor agreement.

Published guides are single markdown files at `skills/modern-web-guidance/guides/<category>/<guide-id>.md`: a title, a short statement of the problem, numbered or bulleted rules with small code samples, and a `Baseline status for <feature>: ...` line for each platform feature the guide leans on. The drafts below follow that shape and are written for any web component library, with Lit named only where the behavior is Lit's. They are HAX's own words (Apache-2.0), so they can be offered under MWG's terms.

Suggested order: RTL first (smallest, and it comes with a deterministic check), then meaning channels, then server rendering.

### 1. RTL and text-expansion checks for component UIs

- **Proposed guide id and place:** `rtl-and-text-expansion-checks`, under `guides/accessibility/` or `guides/css/`.
- **Gap in MWG 1.0.0:** several guides say to use logical properties, but none says how to check a UI in a right-to-left or longer language before a translation exists.
- **Where HAX's version lives:** the `i18n-layout` check in webcomponents, <https://github.com/haxtheweb/webcomponents/blob/master/scripts/i18n-layout-check.mjs>.
- **Evals to offer:** a component with `margin-left`, `text-align: left` and a fixed-width button; expected output moves to logical properties and reports the clipped label under the pseudo-locale. Without the guide an agent fixes the properties it notices and never runs the UI in `dir="rtl"`.

Draft text:

> **RTL and text-expansion checks.** A layout that only ever ran in English and left-to-right hides two classes of bug: physical-side CSS that does not mirror, and containers sized to the English string.
>
> 1. Write spacing, borders, positioning and alignment with logical properties and values: `margin-inline`, `padding-inline-start`, `border-inline-end`, `inset-inline-start`, `text-align: start`. Reserve `left` / `right` for things that are physically sided (a video scrubber, a chart axis).
> 2. Do not hard-code direction. Let `dir` inherit from the document, and inside shadow DOM select on it with `:dir(rtl)`, which sees the inherited direction; `[dir="rtl"]` only matches an attribute on that same element.
> 3. Mirror directional icons (back, forward, disclosure arrows) and leave non-directional ones (search, clock, media play) alone.
> 4. Check before translating: render the component with `dir="rtl"` on an ancestor and with a pseudo-locale that pads every string by 30 to 40% and adds accented characters. Fail on horizontal overflow of the component, clipped or ellipsized labels on controls, and overlapping siblings.
> 5. Run the same check at a phone width; expansion and a narrow viewport fail together.
>
> Baseline status lines to carry: CSS logical properties and values; the `:dir()` pseudo-class.

### 2. Meaning channels: state and consequential actions in more than color

- **Proposed guide id and place:** `meaning-channels`, under `guides/accessibility/`.
- **Gap in MWG 1.0.0:** "do not use color alone" appears as a one-line DON'T in `color`, `tabs`, `copy-button` and several form guides. No guide says which other channels to use, or when the full set is required.
- **Where HAX's version lives:** rule `8d0c033b-7c96-4c6e-aafc-7dfff8ad9123`, with the color vision rule `13a03330-483e-404e-9e48-b0d9f16432d3` behind it, in <https://github.com/haxtheweb/praw/blob/main/RULES.md>.
- **Evals to offer:** "show which quiz answers were right and wrong" and "add a permanent delete button next to Save". Without the guide an agent uses green and red backgrounds and a red button; with it, each state also has a label, a distinct icon, a pattern that survives grayscale and a visible focus state.

Draft text:

> **Meaning channels.** When a user has to interpret a state (correct or incorrect, draft or published, valid or invalid) or make a choice with consequences (delete permanently, confirm or cancel), carry the meaning in every channel, so losing one loses nothing:
>
> 1. **Label:** text that names the state or action, visible or shown on hover and on focus, and present in the accessible name.
> 2. **Color:** hues that stay distinguishable with common color vision differences. Check the pair in a color vision simulator; green against red is the pair most often lost.
> 3. **Focus:** a visible focus state that does not reuse the state color.
> 4. **Texture:** a pattern, border style or shape that still separates the states in grayscale and in forced-colors mode.
> 5. **Icon:** one icon per meaning, not one icon recolored.
>
> Use all five for assessment feedback, destructive and irreversible actions, form validation, status chips, diffs and chart series. Ordinary navigation, toolbar buttons and easily undone edits need a clear label, a focus state and contrast; a selected tab or toggle still needs more than color.
>
> Baseline status lines to carry: `forced-colors` media query; `prefers-contrast`.

### 3. Server rendering a web component so the first response is useful

- **Proposed guide id and place:** an addition to the existing `guides/html/prerendering-custom-elements.md`, or a companion `server-rendering-web-components` next to it.
- **Gap in MWG 1.0.0:** `prerendering-custom-elements` covers declarative shadow DOM, hydration timing, FOUC and fallbacks. It does not cover what a component author must do so a server renderer can run the component at all, which bindings reach the server HTML, or what the no-JavaScript reader gets.
- **Where HAX's version lives:** rule `1b8b8a93-0458-41f9-85a4-ba8d16923765` in <https://github.com/haxtheweb/praw/blob/main/RULES.md>; the report-only `hax audit ssr` in <https://github.com/haxtheweb/create>.
- **Evals to offer:** a component that reads `localStorage` in its constructor and renders `<input type="checkbox" .checked=${this.done}>` and `<iframe .src=${this.url}>`. Without the guide an agent guards the storage call at most; with it, the storage read moves to a client-only lifecycle method and both bindings become attribute bindings.

Draft text:

> **Server rendering a web component.** A server renderer runs a component's constructor and its render path and nothing else; the callbacks that fire on connection to a document never run there (in Lit SSR: the constructor, `willUpdate` and `render` run; `connectedCallback`, `firstUpdated` and `updated` do not).
>
> 1. Keep the constructor and render path free of `document`, storage, `location`, layout measurement and observers. Do that work in the connected or first-update callbacks.
> 2. Guard any browser API the server can reach with a `typeof globalThis.document !== "undefined"` style check, not a bare `window` or `document` reference.
> 3. Keep rendering deterministic: no random ids, clocks or locale-dependent formatting that differs between server and client, or hydration will mismatch.
> 4. On native elements, bind attributes, not properties. A property binding is not serialized: Lit SSR writes `.checked=${false}` as `checked="false"`, which browsers read as checked until hydration, and writes nothing at all for `.src` or `.href`, so an iframe or link reaches the browser with no address. Use boolean attribute bindings (`?checked`) and plain attribute bindings (`src=${url}`).
> 5. Attributes that crawlers or CSS depend on belong in the rendered template or a reflected property, not in a `setAttribute` call that only runs on the client.
> 6. Make the first render carry the content: default text, slotted light DOM and attribute defaults should produce meaningful HTML, not an empty shell. For content that exists only as a property (a video address, a data series), keep a light DOM fallback (a link, a table, an image) in a slot the shadow root does not draw, so feeds, exports and readers without JavaScript still get it.
> 7. A component that cannot render on a server (WebGL, audio, real layout) should say so through an opt-out its renderer understands, and render its fallback instead of throwing.
>
> Baseline status line to carry: declarative shadow DOM.
