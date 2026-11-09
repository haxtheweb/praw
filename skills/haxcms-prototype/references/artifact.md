# Prototype page contract

One HTML page plus supporting files. Start from `template.html` in this folder: it implements the
header, stepper, variant switch, toggles, brief and review panels and renders from the brief, so only
the steps, base images and proposed regions are yours to write. The fidelity check reads the markers below, so use
them exactly.

`body` carries `data-variant` (`desktop-light`, `mobile-dark`, …). A proposal that must follow the
selected variant rather than the viewer's own theme sets `color-scheme` from it, for example
`body[data-variant$="dark"] .slot { color-scheme: dark; }`, so `light-dark()` inside the proposed
element matches the base capture.

## Files

```
index.html
tokens.css            # copied unchanged from the inventory
base/<state>/<variant>.png   # copied unchanged from the inventory's states/<state>/<variant>.png
branch/<state>/<variant>.png # branch mode only: copied unchanged from the branch inventory
```

Load `tokens.css` with a `<link>`. Never retype a token value; regenerate the inventory instead.

## Required markers

| Marker | Where | Purpose |
|---|---|---|
| `<script type="application/json" id="prototype-brief">` | once, in `<head>` | The brief (`brief.md`), verbatim. |
| `data-provenance` | the provenance strip | Must contain the inventory's `source.haxcmsNodejs` SHA and webcomponents source, the inventory's `generatedAt`, the fixture and the mode. |
| `data-step="<index>"` + `data-state="<state id>"` | each step | Matches `brief.steps`. |
| `data-proposed="<region id>"` | each proposed region | Matches `brief.regions`. Always visibly marked: a dashed `--ddd-accent` (or `--hax-ui` accent on admin surfaces) outline and a small "Proposed" badge, whether or not the toggle is on. |
| `data-prototype-chrome` | the page's own controls (header, stepper, toggles, panels) | Excluded from label checks. Its CSS goes between `/* chrome:start */` and `/* chrome:end */` and may use DDD tokens freely; nothing else on the page may use raw values. |

## Layout

1. **Header** (chrome): title, mode badge ("Branch prototype", "Overlay prototype", or "Concept, not
   the current UI"), provenance strip.
2. **Stepper** (chrome): one item per brief step, numbered, with its title.
3. **Stage**: the current step. Base image at its natural size inside a frame the size of the
   variant's viewport, with proposed regions absolutely positioned over it in CSS pixels of that
   capture. Variant switch (desktop / mobile, light / dark) swaps the base and repositions regions; a
   region the proposal has no layout for at a variant is hidden and listed as "not designed at this
   size".
4. **Show proposed** toggle: on dims everything that is not proposed (`filter: saturate(0.2) opacity(0.6)`
   on the base) so a reviewer sees in seconds what is real. **Current / Proposed** flip: current
   hides proposed regions (or, in branch mode, shows the main capture instead of the branch capture).
5. **Brief** panel: `what_exists`, regions, new labels, components, tokens, not shown, assumptions.
6. **Review** panel: the fidelity-check report, the independent reviewer's findings, and a feedback
   form whose first question is always "Is anything here not how HAXcms works today?" (step, what it
   shows, what is real). **Copy feedback** copies one plain-text block in the shape
   `hax-instructional-element` uses, so it can be pasted straight back into a session:

   ```text
   Prototype feedback for <title>, round <n>. Use the haxcms-prototype skill's deviation intake.
   <prototype-feedback prototype="<title>" round="<n>" issue="<issue url>" date="<yyyy-mm-dd>">
   <reviewer name="..." role="..." />
   <deviation step="2" shows="..." real="..." />
   <answer id="..." question="...">...</answer>
   </prototype-feedback>
   ```

   Draft answers may be kept in that viewer's browser storage (wrapped in `try/catch`); nothing is sent
   anywhere.

## Intake

Each `<deviation>` in pasted feedback is a fidelity bug: fix the prototype, then log the cause
(`deviation-log.md`) or fix the inventory, as SKILL.md step 8 says, before the next round.
