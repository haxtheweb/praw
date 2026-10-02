---
name: hax-pattern-library-audit
description: >
  READ-ONLY diagnostic: analyze a single HAX web component in the webcomponents
  monorepo against the DDD Atomic Design pattern library and emit a report with
  three sections — (a) Composition conformance (does the element appear in any
  registry composition, and do authored usages match the canonical recipe for
  slots, spacing tokens, data-attributes), (b) Internal-contract conformance
  (for each internal surface the element exposes — title/caption, callout,
  collapsible heading, click-to-reveal trigger, iframe/embed wrapper, admin
  fieldset — does it use the contracted DDD tokens/classes/structure, or does
  it hardcode/deviate), and (c) Library-ingest candidates (custom patterns the
  element implements that are reusable and should be promoted into the registry
  as new molecules/organisms/contracts). Use when the user says "audit this
  element against the pattern library", "does this element conform to DDD
  patterns", "what patterns should this element be part of", "check this
  element's internal consistency", "find ingest candidates in this element", or
  "grade this element against the pattern library" — even if they don't say
  "pattern library" or "audit". Diagnoses only; hands off to hax-webcomponent-dev
  / hax-design-system for remediation and to the DDDPatternLibrary registry for
  ingest.
version: 1.0.0
license: Apache-2.0
metadata:
  author: PRAW
  tags: [hax, ddd, atomic-design, pattern-library, audit, diagnostic, design-system, consistency, conformance]
  requirements: "A single element source tree in the webcomponents monorepo (elements/<tag>/). Reads DDDPatternLibrary.js from elements/d-d-d/lib/. Emits a report; does NOT edit element source, the registry, or site.json."
---

# HAX Pattern Library Audit (Read-Only Diagnostic)

Analyze a single HAX web component against the **DDD Atomic Design pattern
library** (the registry at `elements/d-d-d/lib/DDDPatternLibrary.js`) and emit a
diagnostic + remediation report with three sections. This skill **diagnoses and
recommends only** — it does not edit element source, mutate the registry, or
change `site.json`. It mirrors the `hax-a11y-audit` read-only pattern but
operates through the **pattern-conformance** lens: does this element's authored
usage and its internal styling match the canonical recipes and internal
contracts the library defines?

## The worldview in one paragraph

The DDD pattern library is a single-source registry of atoms, molecules,
organisms, templates, and cross-cutting internal contracts (titles, callouts,
collapsibles, embeds, admin fieldsets). It exists so that AI-generated HAX HTML
is uniform and so the ecosystem's element internals feel cohesive. This skill
grades one element at a time against that registry: (a) is the element part of
any documented composition, and when authors use it do they match the canonical
recipe (correct slots, spacing tokens, data-attributes); (b) for each internal
surface the element exposes, does it honor the contracted DDD tokens/classes or
does it hardcode values / deviate; (c) does the element implement a reusable
custom pattern worth promoting into the registry. This is distinct from
**token-usage compliance** (did a token get used at all — `hax-design-system`'s
job), from **component-internal accessibility** (shadow-DOM ARIA/keyboard —
`hax-webcomponent-dev`'s job), and from **authored-page a11y** (`hax-a11y-audit`).
This skill reports conformance gaps and ingest opportunities; it never invents a
tag, never edits source, and never auto-ingests.

## When to Use

**Trigger conditions:**
- "Audit this element against the pattern library" / "grade this element against DDD patterns"
- "Does this element conform to DDD patterns" / "check this element's internal consistency"
- "What patterns should this element be part of" / "find ingest candidates in this element"
- "Why does this element's title not match the others" / "make this element feel cohesive"
- "Does this element's callout match the callout contract"
- even when the user does not say "pattern library" — if the question is about an
  element's conformance to documented DDD compositions or internal styling
  consistency, this is the skill

**When NOT to use (with redirect):**
- Pure token-usage compliance (was a DDD token used at all, SimpleColors migration) → `hax-design-system`
- Component-INTERNAL accessibility (shadow-DOM ARIA/keyboard/tabindex) → `hax-webcomponent-dev`
- Authored-page WCAG compliance (alt text, headings, landmarks on a HAX site page) → `hax-a11y-audit`
- Pedagogical inclusivity / UDL → `hax-udl-audit`
- Page-scope cognitive load / chunking → `hax-content-chunking-audit`
- Applying fixes to the element source → `hax-webcomponent-dev` (this skill only reports)

## Scope: this skill is READ-ONLY

This skill **diagnoses and recommends only**. It produces a report. To apply
remediation, hand off to `hax-webcomponent-dev` (element source edits) and
`hax-design-system` (token/class swaps). To ingest a discovered custom pattern,
the human approves a registry update to `elements/d-d-d/lib/DDDPatternLibrary.js`.
Never edit element source, the registry, or `site.json` from within this skill.

## Inputs

- A single element source tree: `elements/<tag>/` (the `<tag>.js`, `lib/*.js`,
  `src/*.js`, `*.css`, demo HTML, and `lib/<tag>.haxProperties.json` if present).
- The registry: `elements/d-d-d/lib/DDDPatternLibrary.js` (read for
  `DDDPATTERNS`, `INTERNAL_CONTRACTS`, `HAX_CAPABILITY`, and the helper getters
  `getPatternsUsingComponent(tag)`, `getContractsForElement(tag)`,
  `resolveHaxCapabilityReport()`).
- Optional: the element's `README.md` and demo for authored-usage examples.

## Methodology

1. **Ingest the element.** Read the element's main `<tag>.js` and any `lib/*.js`
   it pulls in. Identify: the class, the base class (does it extend `DDD` /
   `DDDSuper` / `SimpleColors`), the `render()` template, the `static get styles()`
   block, the `static get haxProperties()` (external JSON ref or inline), the
   slots it exposes, and the properties it reflects. Note whether it ships
   `haxProperties` at all (the gate cares about this).
2. **Composition conformance.** Call `getPatternsUsingComponent(tag)` from the
   registry. For each pattern that includes this element:
   - Does the canonical recipe use slots/attributes this element actually
     supports? (Flag any recipe referencing a non-existent slot or property —
     that is a registry bug, not an element bug.)
   - Does the element's own demo / README usage match the canonical recipe's
     spacing tokens and data-attributes, or does the demo improvise?
   - If the element is NOT in any pattern, note it as an uncovered element (a
     candidate for future composition coverage, not a failure).
3. **Internal-contract conformance.** Call `getContractsForElement(tag)`. For
   each contract that targets this element, read the element's `styles` and
   `render()` and check whether the contracted surface uses the contracted
   DDD tokens/classes/structure or hardcodes values:
   - **Element title/caption:** does the titled surface use
     `--ddd-theme-h*-font-size` + `--ddd-font-weight-bold` + the contracted
     margins, or a hardcoded font-size / margin?
   - **Callout/status box:** radius `--ddd-radius-md`, padding
     `--ddd-spacing-4`, border `--ddd-border-xs`, icon `--ddd-icon-*`, accent
     via `data-accent` — or hardcoded equivalents?
   - **Collapsible heading:** `heading-button` set, `--ddd-font-weight-bold`,
     `--ddd-spacing-4` padding — or missing `heading-button` / hardcoded?
   - **Click-to-reveal trigger:** `simple-cta` / `simple-icon-button-lite`
     with `--ddd-icon-xs` and `--ddd-spacing-2` gap — or a raw `<button>` with
     hardcoded styles?
   - **Iframe/embed wrapper:** `--ddd-spacing-4` padding, `--ddd-border-xs`,
     `--ddd-radius-md`, caption slot — or hardcoded?
   - **Admin fieldset:** mirrors public `a11y-collapse`/`multiple-choice`
     spacing — or diverges?
   Each deviation is a finding: cite the exact hardcoded value and the
   contracted token it should use.
4. **Library-ingest candidates.** Look for reusable structure the element
   implements that is NOT yet in the registry: a novel composed block in its
   demo, a reusable internal layout, a status/treatment variant that other
   elements could share. For each, propose a registry entry (level, title,
   components, tokens, a draft `html` recipe) so the human can ingest it.
   Only propose genuinely reusable patterns — not one-off styling.
5. **Apply the overlap / defer rules:**
   - **Token-usage compliance (SYMMETRIC with `hax-design-system`):** if the only
     issue is "a hex color was used instead of a DDD token," defer to
     `hax-design-system`. This skill checks conformance to *named contracts and
     recipes*, not raw token usage. State the split in the finding.
   - **Component-internal a11y:** if the failure is shadow-DOM ARIA/keyboard,
     defer to `hax-webcomponent-dev`.
   - **HAX-capability:** if the element lacks `haxProperties`, flag it as a gate
     gap (it cannot be referenced by any published pattern until wiring exists).
6. **Determine the overall rating:**
   - **Conforming:** the element honors every contract that targets it and its
     demoed usage matches canonical recipes. Ingest candidates may be noted but
     do not affect the rating.
   - **Partial:** one or more contract deviations or recipe mismatches, but the
     element is fundamentally in the DDD family (extends DDD, uses mostly
     tokens). Remediation is surgical (swap hardcoded values for tokens).
   - **Non-conforming:** the element does not extend DDD / uses SimpleColors-only
     internals / hardcodes multiple contracted surfaces — a structural
     mismatch needing real remediation, or a candidate to mark
     `designSystem: false` if it genuinely is outside DDD.
7. **Emit the report** (format below), then an "Implementation handoff" block.

## Expected Output Format

Format findings exactly like this structure (mirrors `hax-a11y-audit`):

```
### 📊 DDD Pattern Library Diagnostics
* **Conformance Rating:** [Conforming / Partial / Non-conforming]
* **Primary Gap:** [the worst offender — one sentence, e.g. "video-player's
  .video-caption hardcodes 16px margin instead of the title contract's
  --ddd-spacing-2 / --ddd-font-weight-bold pairing."]

### 🔍 Findings & Remediation

* **{element tag} — Composition conformance**
  * **Status:** [Conforming / Partial / Not-covered / Registry-bug]
  * **Issue:** [the exact mismatch, e.g. "Element is in pattern org-hero but
    its demo uses accent-color='blue' while the recipe uses data-primary='2'."]
  * **Contract/Recipe:** [cite the pattern id + the canonical recipe snippet]
  * **Remediation:** [concrete tweak, e.g. "Swap the demo's accent-color for
    data-primary='2' to match org-hero, OR update the registry recipe if the
    demo form is preferred."] OR "Hand off to hax-webcomponent-dev."

* **{element tag} — Internal contract: {contract id}**
  * **Status:** [Conforming / Deviation]
  * **Issue:** [the exact hardcoded value vs the contracted token]
  * **Contract:** [cite the contract id + the contracted token]
  * **Remediation:** [the token swap, e.g. "Replace font-size: 16px with
    var(--ddd-theme-h5-font-size) and add font-weight: var(--ddd-font-weight-bold)."]

* **{element tag} — Library-ingest candidate**
  * **Candidate:** [proposed pattern id, level, title]
  * **Why:** [reusable structure found, where]
  * **Draft recipe:** [a short html snippet following registry conventions]

### 🛠 Implementation handoff
* [one-line action per fix → skill/owner, e.g. "Swap hardcoded caption margin in
  video-player.js:150 for --ddd-spacing-2 via hax-webcomponent-dev."]
* [ingest: "Add mol-foo candidate to DDDPatternLibrary.js (human-approved)."]
```

## Worked example

**Input** — `elements/video-player/video-player.js`:
- `.video-caption` div renders `mediaTitle` (line ~150); styles hardcode
  `font-size: 16px; margin: 8px 0;` rather than DDD tokens.
- Extends `LitElement` (not `DDD`), ships inline `haxProperties` (gate-passing).
- `getContractsForElement("video-player")` returns `contract-element-title` and
  `contract-iframe-embed-wrapper`.
- `getPatternsUsingComponent("video-player")` returns none currently (the
  org-media-playlist pattern uses `media-playlist` + `audio-player`, not
  video-player directly).

**Output:**
```
### 📊 DDD Pattern Library Diagnostics
* **Conformance Rating:** Partial
* **Primary Gap:** video-player's .video-caption hardcodes 16px font-size and
  8px margin instead of the element-title contract's --ddd-theme-h5-font-size +
  --ddd-font-weight-bold + --ddd-spacing-2 pairing.

### 🔍 Findings & Remediation

* **video-player — Internal contract: contract-element-title**
  * **Status:** Deviation
  * **Issue:** `.video-caption` uses `font-size: 16px; margin: 8px 0;` while
    the contract specifies `--ddd-theme-h5-font-size` (h5 maps to the caption
    tier) + `--ddd-font-weight-bold` + margin top 0 / bottom
    var(--ddd-spacing-2).
  * **Contract:** contract-element-title — "Use the DDD heading font-size scale
    + bold weight; margin top 0, bottom var(--ddd-spacing-2)."
  * **Remediation:** In video-player.js styles, replace the hardcoded caption
    font-size/margin with `font-size: var(--ddd-theme-h5-font-size);
    font-weight: var(--ddd-font-weight-bold); margin: 0 0 var(--ddd-spacing-2);`
    Hand off to hax-webcomponent-dev.

* **video-player — Internal contract: contract-iframe-embed-wrapper**
  * **Status:** Partial
  * **Issue:** The iframe path wraps in `.responsive-video-container` with no
    contracted border/radius/padding; the contract asks for wrapper
    --ddd-spacing-4 / --ddd-border-xs / --ddd-radius-md + a caption slot. The
    slotted `caption` exists but the wrapper styling is unstyled.
  * **Contract:** contract-iframe-embed-wrapper.
  * **Remediation:** Add wrapper tokens or document that video-player
    intentionally omits the border (acceptable if deliberate; flag for human
    decision). Defer raw-token choice to hax-design-system.

* **video-player — Composition conformance**
  * **Status:** Not-covered
  * **Issue:** video-player is not currently referenced by any registry
    pattern (org-media-playlist uses media-playlist + audio-player).
  * **Remediation:** None required. See ingest candidate below.

* **video-player — Library-ingest candidate**
  * **Candidate:** `org-video-feature` (organism) — a video-player inside a
    page-section with a media-title + caption + transcript link.
  * **Why:** The demo shows this exact composition and it is reusable for
    lecture/course pages.
  * **Draft recipe:** `<page-section accent-color="blue"><video-player
    source="files/lecture.mp4" media-title="Lecture 1"></video-player></page-section>`

### 🛠 Implementation handoff
* contract-element-title: swap hardcoded .video-caption font-size/margin for
  DDD tokens in video-player.js via hax-webcomponent-dev.
* contract-iframe-embed-wrapper: decide whether video-player's iframe wrapper
  should adopt the contracted border/radius or document an intentional
  exemption.
* ingest: add org-video-feature to DDDPatternLibrary.js (human-approved).
```

## Implementing the Recommendations

This audit is the diagnosis step. Apply fixes with:

- **`hax-webcomponent-dev`** — element source edits: swap hardcoded values for
  DDD tokens, add `heading-button`, fix internal structure to honor a contract.
- **`hax-design-system`** — DDD token/class selection and SimpleColors migration
  for any swapped values.
- **`DDDPatternLibrary.js` registry** — ingest approved candidates by adding a
  new entry to the appropriate level array (ATOMS/MOLECULES/ORGANISMS/TEMPLATES)
  or a new object to INTERNAL_CONTRACTS, then running `yarn run build` in
  `elements/d-d-d` to regenerate docs metadata.
- **`hax-claudehax` / `hax-site-building`** — if a recipe mismatch is in
  authored page content (not the element source), fix the page HTML there.

**CLI rules (from PRAW RULES.md):** use the local/global `hax` command (not
`npx`); never hand-edit `site.json` for structure; `a11y-collapse` must set
`heading-button`; inputs via `simple-fields`; the ubiquity script and top-level
monorepo build are never run by the agent; element-local `yarn run build` only.

## Acceptance criteria (for the audit report itself)

- Every contract finding cites the contract id and the exact contracted token the
  element should use (not a vague "use tokens").
- Every composition finding cites the pattern id and the canonical recipe snippet.
- Ingest candidates include a draft `html` recipe following registry conventions
  (real HAX-capable tags only).
- The rating is one of: Conforming / Partial / Non-conforming.
- An element that extends DDD and honors all targeting contracts is not rated
  Non-conforming even if it has zero ingest candidates.
- HAX-capability gaps (missing `haxProperties`) are flagged distinctly from
  contract deviations.
- No finding edits source, the registry, or `site.json`.

## Gotchas

- **Contract vs token-usage.** This skill checks conformance to *named*
  contracts/recipes. If the only issue is "a hex color was used instead of a
  token," defer to `hax-design-system`. Do not double-report.
- **Not-covered is not a failure.** An element not in any pattern is an
  opportunity, not a conformance failure. Only flag it as an ingest candidate.
- **Registry bugs are real.** If a canonical recipe references a slot the
  element does not expose, that is a registry bug (fix the recipe), not an
  element bug. Report it as a Registry-bug status.
- **`designSystem: false` is valid.** An element that intentionally opts out of
  DDD (sets `designSystem: false` in haxProperties) should be reported as
  Non-conforming only if it was expected to conform; note the opt-out.
- **SimpleColors is allowed as a fallback.** Per the standing rule, SimpleColors
  fills gaps DDD does not cover. Do not flag SimpleColors usage as a deviation
  where DDD has no equivalent; only flag where a DDD token exists and was
  bypassed.
- **Don't edit here.** This skill emits a report. Source edits belong in
  `hax-webcomponent-dev`; registry ingest is a separate human-approved update.
- **Never run the ubiquity script or top-level monorepo build.** Element-local
  `yarn run build` only, and only when applying fixes (not during this audit).

## Dependencies

- **Reads:** the element source tree (`elements/<tag>/`) and the registry
  (`elements/d-d-d/lib/DDDPatternLibrary.js`) + its helpers.
- **Consults:** `references/pattern-library-map.md` (the verified pattern +
  contract map generated from the registry — single source of truth for ids,
  levels, components, tokens, targets).
- **Hands off to:** `hax-webcomponent-dev` (source remediation), `hax-design-system`
  (token/class selection + SimpleColors migration), the `DDDPatternLibrary.js`
  registry (ingest, human-approved).
- **Defers to:** `hax-a11y-audit` (authored-page WCAG), `hax-udl-audit` (UDL),
  `hax-content-chunking-audit` (cognitive load).

## References

- `references/pattern-library-map.md` — patterns + contracts map (verified from
  the registry; the iron rule for ids/tokens/targets).
- `elements/d-d-d/lib/DDDPatternLibrary.js` — the registry itself.
- `elements/d-d-d/lib/DDDStyleGuidePresets.js` — the style-guide presets that
  mirror the atom/molecule recipes.
- PRAW RULES.md: `~/Documents/git/haxtheweb/praw/RULES.md`.
