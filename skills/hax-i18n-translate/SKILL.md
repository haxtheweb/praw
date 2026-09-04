---
name: hax-i18n-translate
description: >
  Scaffold and translate HAX web component i18n locale files at scale. Use when the user
  says "Translate <element>", "add translations to <element>", "translate the locales for
  <element>", "stub out translation files for <element>", "add support for the top 100
  languages", "i18n my component", "extract the this.t strings", or "set up locales for
  <element>", or references a HAX element's locales/ folder, this.t object, I18NMixin,
  registerLocalization, or translation-manifest — even when they don't say "skill" or
  "i18n". Covers both phases: (1) extracting English strings from the this.t object and
  stubbing locale files for ~100 languages, and (2) translating every stub, choosing the
  lowest-cost path (inline single-response for small string sets, parallel agents for
  large ones), then validating.
version: 1.1.0
license: Apache-2.0
metadata:
  author: haxtheweb
  tags: [hax, i18n, translation, locales, internationalization, webcomponents, this.t, I18NMixin]
---

# HAX i18n translation at scale

Add full multi-language support to a HAX web component. This skill is built for a
high-volume initial pass across many elements, so it optimizes for token cost: the
deterministic work (extract, stub, manifest, validate) is handled by bundled scripts,
and translation uses the cheapest viable path — inline in one response for small
string sets, parallel child agents only when an element has many strings.

## The fast path: "Translate <element>"

When the user says "Translate stop-note" (or any element), run Phases 1–3 below in
order, fully, without stopping for confirmation. That phrase is the default invocation.

## How HAX i18n works (the parts that matter)

A component declares English strings in the constructor as a `this.t` object:
```js
this.t = this.t || {};
this.t = { ...this.t, moreInformation: "More Information" };
this.registerLocalization({ context: this, basePath: import.meta.url });
```
The i18n manager fetches `locales/<namespace>.<lang>.json` (namespace = the tag name
from `static get tag()`) and merges matching keys into `this.t`. A scanner,
`webcomponents/scripts/generate-translation-manifest.js`, reads every `locales/` folder
and writes `elements/i18n-manager/lib/translation-manifest.json`, which the manager uses
to know which languages an element supports (and avoid 404s).

Two consequences shape this skill:
- `this.t` is the source of truth for the English string set — not any existing
  `en.json`, which can lag behind it.
- Adding a language = adding a `locales/<namespace>.<lang>.json` file, then
  regenerating the manifest. Never hand-edit the manifest.

## Phase 1 — Extract and stub (always)

From the webcomponents root:
```bash
python3 <skill>/scripts/extract_and_stub.py elements/<element-dir>
node scripts/generate-translation-manifest.js
```
The extractor finds the main JS file, reads `static get tag()` for the namespace,
parses the `this.t = { ... }` block, writes `locales/<namespace>.en.json`, then writes
`<namespace>.<lang>.json` for every code in `references/languages.json` (copying English
values as placeholders). Existing locale files are never clobbered, so it is safe to
re-run on elements that already have some translations. Then run the manifest scanner so
the new languages are registered (a scanner, not a build and not the ubiquity script —
safe to run from the webcomponents root).

Note the extracted string count. If it is wrong (fewer keys than `this.t` shows), the
object has concatenation or template literals the parser can't handle — fix the source
so strings are simple double-quoted values, then re-run.

## Phase 2 — Translate (pick the cheaper path)

### Path A — Inline single response (default; cheapest)

Use this when the element has a small number of strings — roughly **8 or fewer**.
Produce ALL translations in ONE response as a single JSON map, then apply it with one
script run. No child agents, no round-trips, no per-file create_file calls. This is the
big cost win for the initial high-volume pass: ~100 languages × a few strings in a
single generation instead of ~100 separate agent conversations.

Build a JSON object keyed by language code, each value an object of key→translation:
```json
{
  "af": { "moreInformation": "Meer inligting" },
  "am": { "moreInformation": "ተጨማሪ መረጃ" },
  "zu": { "moreInformation": "Ukwaziswa okwengeziwe" }
}
```
Write it to a temp file and apply it:
```bash
python3 <skill>/scripts/apply_translations.py --map /tmp/<namespace>.translations.json elements/<element-dir>
```
`apply_translations.py` writes every language from the map in one pass, preserving the
`en.json` key order and merging with existing files (an already-translated `es.json` is
preserved). It prints the file count and any codes with missing keys.

To keep the map compact and the response cheap:
- One line per language is fine. Language code→name lookups come from
  `references/languages.json`; you don't need to repeat names in the map.
- Skip `en` in the map (the script ignores it). You only need codes that have a stub.
- Low-resource codes may be best-effort; flag them in your summary afterward.

### Path B — Parallel child agents (only for large string sets)

Use this when the element has many strings (roughly **more than 8**) where producing
all ~100 languages × many strings in one response would be too large or unreliable.
Dispatch child agents in batches of ~8 languages each (~12 batches for 100 languages).
Put the shared English source and the translation guidelines below in `base_prompt`;
put each child's language codes and the absolute locales path in its per-agent prompt.
Each child reads each stub, translates values that still equal the English source,
preserves the rest, and writes the file back with create_file.

Per-agent prompt skeleton:
```
Your languages: af=Afrikaans, am=Amharic, az=Azerbaijani, ...
For each code, read elements/<element>/locales/<namespace>.<code>.json, translate
every value that still equals the English source, keep already-translated values,
preserve key order, write the file back with create_file (2-space indent, trailing
newline). Report files written + any low-confidence codes.
```

### Translation guidelines (applies to both paths)

- Never change keys. Only translate values. Preserve key order from `en.json`.
- Keep these untranslated: brand names ("YouTube"), technical acronyms ("URL", "CORS"),
  and `crossoriginTitle` ("Crossorigin" is an HTML attribute keyword).
- `englishLabel` is the NAME of the English language written in the target language
  (French -> "Anglais", Japanese -> "English in that script").
- `gizmoTitle` ("Video"), `tagMedia` / `tagAudioVideo` ("Media"), `sourceTitle`
  ("Source"): use the common word in the target language; if the English loanword is
  the standard term there, keep it.
- Translate the meaning naturally in the target script and sentence-case conventions.
  JSON: 2-space indent, trailing newline, UTF-8, no BOM.
- For RTL languages (Hebrew, Persian, Pashto, Urdu, Western Punjabi/Shahmukhi,
  Yiddish, Sindhi), write values in the correct script; the JSON itself is standard.
- Keep already-translated values unchanged (Phase 2 may re-run on partial files).
- For low-resource languages, still produce the best translation, then flag the code
  as low-confidence in your summary so it can be reviewed.

## Phase 3 — Validate

```bash
python3 <skill>/scripts/validate.py elements/<element-dir>
```
Reports JSON parse errors and any keys whose value still equals the English source,
excluding `englishLabel` and known loanword keys (`crossoriginTitle`, `gizmoTitle`,
`tagMedia`, `tagAudioVideo`, `sourceTitle`). Genuine leftovers mean re-do those codes
(Path A: fix the map entries; Path B: re-dispatch those languages). Then summarize:
files written, validation result, and the low-confidence codes for native review
(expect this for e.g. gn, qu, sn, xh, zu, wuu, yi).

## What not to do

- Don't run a build, lint, format, or the ubiquity script. The manifest scanner is the
  only command this skill runs.
- Don't edit `translation-manifest.json` by hand — the scanner owns it.
- Don't clobber existing locale files in Phase 1; only create missing stubs.
- Don't translate keys, brand names, or the CORS / Crossorigin / URL tokens.
- Don't spawn child agents for small string sets — use Path A to keep cost down.
