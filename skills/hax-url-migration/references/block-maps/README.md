# Block maps

A block map turns one platform's rendered markup into HAX-authorable HTML. Maps are data, so adding support for a new builder or widget is a JSON edit, not code. `scripts/validate-maps.mjs` checks every map against `../hax-blocks.json` (the HAX blocks a map may target) and fails on unknown targets or broken selectors.

Maps apply in this order: builder layers (Elementor, Divi, Starlight), then the platform (Drupal, Ghost), then `generic-html`. The first rule that matches a node wins, and nodes inside a converted node are not matched again, so put specific rules before general ones.

## Map fields

| Field | Meaning |
|---|---|
| `id` | Must equal the file name. Fingerprints reference it through `blockMap`. |
| `contentSelectors` | Where the page's main content lives, tried in order. The first match with real text wins. |
| `chromeSelectors` | Site chrome removed before conversion (menus, share bars, comments). |
| `rules` | Conversion rules, applied in order. |

## Rule fields

| Field | Meaning |
|---|---|
| `id` | Unique within the map. Reported in stats as `<map>:<id>`. |
| `match` | CSS selector (css-select; `:has()` and `:scope` work). |
| `to` | A HAX tag from `hax-blocks.json`, or one of: `keep` (leave as is), `unwrap` (replace with children), `drop` (remove), `flag` (keep, mark `data-hax-review`, and report for a human), `link` (replace an embed with a plain link), `html` (replace with the literal `html` field). |
| `attrs` | Map of HAX property (camelCase; written as kebab-case attributes) to an extractor. |
| `content` | Extractor for the default slot. HTML results are converted recursively. |
| `slots` | Map of slot name to extractor. Text results become `<span slot>`; HTML results become `<div slot>`. |
| `children` | For containers: `select` picks the outermost matching descendants; either `slot` (`col-{n}` numbers them) with `content`, or `to` plus `attrs`/`content` to build one child element each. |
| `layout` | `auto` sets grid-plate's `layout` to equal columns from the child count (2–6, otherwise the rule is skipped). `fromClass` reads `layoutClassMap`. |
| `asset` | Add URLs found in `attrs` (and links, for `keep`) to the file map. |
| `flag`, `gapKey` | For `to: flag`: the review category (`form`, `gap`, `dynamic-listing`, `custom-html`, `h5p`, `shortcode`) and an extractor naming the gap (for example a Paragraphs bundle). |
| `skipInside` | Tag names; the rule does not fire inside them. |
| `confidence` | `high`, `medium` or `low`; how often the rule is right, used to prioritize review. |
| `note` | Human guidance shown in reports. |

## Extractors

An extractor is one or more alternatives joined by `|`; the first non-empty one wins.

| Form | Value |
|---|---|
| `=text` | The literal `text`. |
| `sel@attr` | Attribute of the first `sel` inside the node. An empty `sel` means the node itself; a `sel` starting with `>` is relative to the node's direct children. |
| `sel@text` | Collapsed text. |
| `sel@html` / `sel@outer-html` | Inner / outer HTML. |
| `sel@html-without:sel2` | Inner HTML with `sel2` removed (for example a `summary` already used as a heading). |
| `sel@raw-template` | Text wrapped in `<template preserve-content="preserve-content">`, the form `code-sample` expects. |
| `sel@attr~regex` | First capture group of `regex` applied to the attribute. |
| `sel@attr#key` | Key read from JSON stored in the attribute (Elementor `data-settings`). |

## Adding a platform

1. Add a fingerprint in `../fingerprints.json` with decisive signals (generator tag, header, API probe) at weight 10 and markup patterns at 4. Point `blockMap` at the new map.
2. Write the map. Start from the platform's documented block list and read real markup before guessing class names.
3. Add a synthetic fixture to `scripts/test/` for the fingerprint and each high-confidence rule.
4. Run `npm run validate` and `npm test`, then add real sites to `../trial-sites.json` and run the trial for that platform (`node trial.mjs --only <id>`).
