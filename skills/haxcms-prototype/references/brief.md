# Prototype brief

Write the brief before building anything. It is also embedded in the prototype page as JSON, so the
fidelity check and reviewers read the same claims the agent built from.

## Fields

| Field | What it holds |
|---|---|
| `title` | Short name of the proposal. |
| `issue` | Full URL of the issue in <https://github.com/haxtheweb/issues> this prototypes. |
| `mode` | `branch`, `overlay` or `concept` (see SKILL.md step 3). |
| `audience` | Who reviews it and what decision it informs. |
| `fixture` | The site the states were captured on (the inventory default, or a named fixture). |
| `inventory` | `manifest.json` `source` values of the inventory the base came from (copied, not retyped). |
| `steps` | Ordered list, one per state shown. Each: `state` (an inventory state id), `title`, `what_exists` (one line, from the inventory), `proposed` (list of region ids, empty for an unchanged step). |
| `regions` | One per proposed region: `id`, `step`, `summary` (what changes), `surface` (`hax-ui` for admin and editor chrome, `ddd` for anything a visitor sees). |
| `newLabels` | Every visible string the proposal adds that is not in the inventory, with the region it belongs to. |
| `newComponents` | Custom element tags the proposal adds that are not in the registry. |
| `newTokens` | Tokens the proposal needs that do not exist yet (documentation until adopted, per the HAX UI rule). |
| `notShown` | Real states or capabilities the flow touches but the prototype leaves out, so silence is not read as removal. |
| `assumptions` | Anything the agent assumed rather than captured. Each becomes a review question. |

## Example

```json
{
  "title": "Staged-save count in the site admin action bar",
  "issue": "https://github.com/haxtheweb/issues/issues/0000",
  "mode": "overlay",
  "audience": "Platform owner; decides whether the count ships with the admin unification",
  "fixture": "inventory default (fresh site, Home page only)",
  "inventory": { "haxcmsNodejs": "<sha from manifest.json>", "webcomponents": "bundled build in src/public/build" },
  "steps": [
    { "state": "site-admin-details", "title": "Open Details", "what_exists": "Details section, Save quiet", "proposed": [] },
    { "state": "site-admin-details", "title": "Change the title", "what_exists": "Save lights up", "proposed": ["save-count"] }
  ],
  "regions": [
    { "id": "save-count", "step": 1, "summary": "Save shows the number of changed fields", "surface": "hax-ui" }
  ],
  "newLabels": [{ "text": "Save (1)", "region": "save-count" }],
  "newComponents": [],
  "newTokens": [],
  "notShown": ["Leave-with-unsaved-changes prompt"],
  "assumptions": ["Count includes fields changed in other sections"]
}
```

Keep `steps[].state` to ids that exist in the inventory. If the flow needs a state the inventory
lacks, add it to the inventory first (SKILL.md step 2) instead of drawing it.
