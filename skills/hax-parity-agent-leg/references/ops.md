# What each parity op means

Each line of `ops.jsonl` is one op: `i` (its number), `type`, and the fields below. Pages are named
by **logical key**: `L0` is the site's welcome page, `L1`, `L2`, ... are pages earlier `addPage` ops
created, in order. Your page id for a key is `keyToId[key]` in the `state.json` that `verify.cjs`
maintains in your `--state` directory.

This file says what the outcome should be, not which command produces it. Finding the command is the
point of the exercise: use the skills. Values are deliberately awkward (markup in titles, unicode,
leading spaces, slugs with `/`, duplicate titles, `<script>` in content). Pass them exactly as given
and let HAX sanitize or slugify them; do not clean them up yourself. Optional fields are absent when
unused: pass a flag only for a field the op has. Hand values over as argv elements from Node, never
through `$(…)` (see "Passing op values safely" in [setup.md](setup.md)).

The agent leg replays sequence **A** only, so these are the op types you will see. (Sequence B adds
API-only ops, such as outline reorders, move up/down, indent/outdent, lock, icon, slug normalization
and site language, which the CLI does not express.)

| Type | Fields | Outcome |
| --- | --- | --- |
| `addPage` | `key`, `title`, `content`, optional `parent`, `slug`, `description`, `tags` | A new page with that title and body HTML. With `parent`, it is a child of that page; without, top level. It goes after the existing pages at that level. `slug`, `description` and `tags` (a comma-separated string, as given) are set when present. The new page becomes `key`. |
| `editTitle` | `key`, `title` | The page's title is `title`. |
| `editContent` | `key`, `content` | The page body is replaced by `content` (inline HTML; how the CLI tells a file, a URL and HTML apart is in [create's hax-site-building skill](https://github.com/haxtheweb/create/blob/main/src/skills/hax-site-building/SKILL.md)). Nothing else about the page changes. |
| `editSlug` | `key`, `slug` | The page's slug (URL path) is set from `slug`. |
| `editDescription` | `key`, `description` | The page's description is `description`. |
| `editTags` | `key`, `tags` | The page's tags are `tags`, as given. |
| `editPublished` | `key`, `published` (true / false) | The page is published or unpublished. |
| `editHideInMenu` | `key`, `hideInMenu` (true / false) | The page is hidden from, or shown in, the site menu. |
| `editParent` | `key`, `parent` (a key, or `null`) | The page moves under `parent`, or to the top level for `null`, after the pages already at that level. Its own children move with it. |
| `editOrder` | `key`, `order` (a number) | The page's order value among its siblings is set to `order`. Its parent does not change. |
| `deletePage` | `key` | The page is deleted. Ops only delete pages that have no children. The replay is your confirmation; do not stop to ask. |
| `setTheme` | `theme` | The site's theme is the theme with that machine name. |

If an op names a key you never bound (an earlier `addPage` diverged), record it as blocked by that
earlier op and skip it; `verify.cjs` still needs to run for that op number so the next one lines up.
