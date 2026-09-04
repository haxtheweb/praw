---
name: hax-i18n-translate
description: >
  Scaffold and translate HAX web component i18n locale files at scale. Use when the user
  says "add translations to <element>", "translate the locales for <element>", "stub out
  translation files for <element>", "add support for the top 100 languages", "i18n my
  component", "extract the this.t strings", "set up locales for <element>", or references
  a HAX element's locales/ folder, this.t object, I18NMixin, registerLocalization, or
  translation-manifest — even when they don't say "skill" or "i18n". Covers both phases:
  (1) extracting English strings from the this.t object in the element's JS and stubbing
  out locale files for ~100 languages, and (2) threading out parallel translation of
  every stub into its target language, then validating.
version: 1.0.0
license: Apache-2.0
metadata:
  author: haxtheweb
  tags: [hax, i18n, translation, locales, internationalization, webcomponents, this.t, I18NMixin]
---

# HAX i18n translation at scale

Add full multi-language support to a HAX web component in two phases. This exists
because the job is mechanical to scaffold (~100 locale files copied from English)
and embarrassingly parallel to translate (~4,000+ strings), but slow and error-prone
to do ad hoc. The bundled scripts handle the deterministic parts; parallel child
agents handle the translation.

## How HAX i18n works (the parts that matter)

A HAX component declares English strings in the constructor as a `this.t` object:
```js
this.t = this.t || {};
this.t = {
  ...this.t,
  embeddedMedia: "embedded media",
  gizmoTitle: "Video",
};
this.registerLocalization({
  context: this,
  localesPath: new URL("./locales/video-player.es.json", import.meta.url).href + "/../",
});
```
At runtime the i18n manager fetches `locales/<namespace>.<lang>.json` (namespace =
the tag name from `static get tag()`) and merges matching keys into `this.t`. A
scanner, `webcomponents/scripts/generate-translation-manifest.js`, reads every
`locales/` folder and writes `elements/i18n-manager/lib/translation-manifest.json`,
which the manager uses to know which languages an element supports (and avoid 404s).

Two consequences shape this skill:
- The `this.t` object is the source of truth for the English string set — not any
  existing `en.json`, which can lag behind it.
- Adding a language = adding a `locales/<namespace>.<lang>.json` file, then
  regenerating the manifest. Never hand-edit the manifest.

## Phase 1 — Extract and stub

Produce `locales/<namespace>.en.json` (canonical English) plus a placeholder stub
for every supported language, each holding the English values ready to translate.

Run the extractor from the webcomponents root:
```bash
python3 <skill>/scripts/extract_and_stub.py elements/<element-dir>
```
It finds the main JS file, reads `static get tag()` for the namespace (falls back
to the directory name), parses the `this.t = { ... }` block, writes `en.json`,
then writes `<namespace>.<lang>.json` for every code in `references/languages.json`
— copying the English values as placeholders. Existing locale files are never
clobbered, so this is safe to re-run on elements that already have some translations.

Then register the new languages by regenerating the manifest:
```bash
node scripts/generate-translation-manifest.js
```
This is a scanner, not a build and not the ubiquity script — safe to run from the
webcomponents root. Commit the new locale files and the regenerated manifest together.

If the extractor reports fewer keys than you see in `this.t`, the object probably
contains string concatenation or template literals it can't parse. Fix those in the
source so the strings are simple double-quoted values, then re-run.

## Phase 2 — Thread out and translate

Replace the English placeholder values in each stub with real translations, in
parallel, without flooding the orchestrator's context.

### Translation guidelines (give these to every child agent)

- Never change keys. Only translate values. Preserve key order from `en.json`.
- Keep these untranslated: brand names ("YouTube"), technical acronyms ("URL",
  "CORS"), and `crossoriginTitle` ("Crossorigin" is an HTML attribute keyword).
- `englishLabel` is the NAME of the English language written in the target
  language (French -> "Anglais", Japanese -> "English in that script").
- `gizmoTitle` ("Video"), `tagMedia` / `tagAudioVideo` ("Media"), `sourceTitle`
  ("Source"): use the common word in the target language; if the English loanword
  is the standard term there, keep it.
- Translate the meaning naturally in the target script and sentence-case
  conventions. Write valid JSON: 2-space indent, trailing newline, UTF-8, no BOM.
- For RTL languages (Hebrew, Persian, Pashto, Urdu, Western Punjabi/Shahmukhi,
  Yiddish, Sindhi), write values in the correct script; the JSON itself is standard.
- Keep already-translated values unchanged (Phase 2 may re-run on partial files).
- For low-resource languages, still produce the best translation, but report the
  code as "low-confidence" so it can be flagged for native review.

### Orchestration pattern

Dispatch parallel child agents, each owning a batch of language codes. Put the
shared English source and the guidelines above in `base_prompt`; put each child's
language codes (with names from `references/languages.json`) and the absolute
locales path in its per-agent prompt. ~8 languages per batch is a good size; ~100
languages -> ~12 batches. Each child reads each stub, translates values that still
equal the English source, preserves the rest, and writes the file back.

Per-agent prompt skeleton:
```
Your languages: af=Afrikaans, am=Amharic, az=Azerbaijani, ...
For each code, read elements/<element>/locales/<namespace>.<code>.json, translate
every value that still equals the English source, keep already-translated values,
preserve key order, write the file back with create_file (2-space indent, trailing
newline). Report files written + any low-confidence codes.
```

## Validation

When all children finish, run:
```bash
python3 <skill>/scripts/validate.py elements/<element-dir>
```
It reports JSON parse errors and any keys whose value still equals the English
source, excluding `englishLabel` and known loanword keys (`crossoriginTitle`,
`gizmoTitle`, `tagMedia`, `tagAudioVideo`, `sourceTitle`). Genuine leftovers mean
re-dispatch those languages. Collect low-confidence codes from child reports and
flag them for native review (expect this for e.g. gn, qu, sn, xh, zu, wuu, yi).

## What not to do

- Don't run a build, lint, format, or the ubiquity script. The manifest scanner is
  the only command this skill runs.
- Don't edit `translation-manifest.json` by hand — the scanner owns it.
- Don't clobber existing locale files in Phase 1; only create missing stubs.
- Don't translate keys, brand names, or the CORS / Crossorigin / URL tokens.
