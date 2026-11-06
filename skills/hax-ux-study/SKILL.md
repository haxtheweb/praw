---
name: hax-ux-study
description: "Run and analyze an internal HAXcms UX study: record sessions with Merlin's >developer/ux-study, then turn the exported JSON into a findings report, a heatmap/replay review and confirmed issues in haxtheweb/issues. Use for \"ux study\", \"usability test\", \"analyze these recordings\", \"where do people get lost\", \"button visibility\"."
version: 1.0.0
license: Apache-2.0
metadata:
  author: PRAW
  tags: [ux, usability, user-research, heatmap, discoverability, visibility, haxcms, merlin, issues]
  requirements: "One or more ux-study-*.json session files exported from HAXcms (Merlin >developer/ux-study). Node 18+ for scripts/analyze.mjs. gh CLI only for the optional issue-filing step."
---

# HAX UX Study

Record how people actually use HAXcms, then find where the interface makes them hesitate,
miss, or give up. The recorder ships in HAXcms (webcomponents, `haxcms-elements`); this skill
covers running the study, analyzing the exports, and turning confirmed findings into issues.

**What it measures.** Clicks (with the real control they hit, through shadow DOM), dead and
rage clicks, near misses beside small targets, hover dwell before acting, pointer path,
scroll, route changes, Escape-after-open, and snapshots of every control on screen. Pointer
position is an **attention proxy, not eye tracking**: people often look ahead of the cursor.
Say so in every report.

**What it never records.** Typed characters (only the key category, like `char` or `Tab`),
input values, or anything outside the browser. Sessions stay in the participant's
`sessionStorage` until exported to a file.

## 1. Run a session

1. Sign in to the HAXcms site under study (latest `main` of the backend, not a published npm
   build, if you are testing new capability).
2. Open Merlin, type `>developer/ux-study`, type a **participant code** (P01, P02; never a
   name), and choose **Start UX study recording**. A "Recording UX study" pill stays on
   screen for the whole session; tell the participant what it is.
3. Give one task at a time. Before each, mark it: use the pill's **Mark task** button or
   Merlin (`>developer/ux-study`, type the task, choose **Mark task**). Write tasks as goals,
   not instructions ("Add a page about safety under Week 1", not "Click the + button").
4. Full page reloads are fine; the session resumes from `sessionStorage`.
5. Choose **Stop and export**. A `ux-study-<site>-<time>.json` file downloads. Collect the
   files from all participants into one folder.

Run the same tasks, in the same order, at the same viewport class (laptop vs phone) for
every participant, or the comparisons below are not apples to apples.

## 2. Analyze

```bash
node scripts/analyze.mjs ./sessions --out ./ux-study-out
# offline / pinned: --analyzer <your webcomponents checkout>/elements/haxcms-elements/lib/core/utils/UXStudyAnalyzer.js
```

This writes `ux-study-analysis.json` (findings, per-task medians, per-control exposure vs
use) and `ux-study-report.md`. The analyzer is the same module the viewer uses, so numbers
match.

For the heatmap and replay, open the viewer from the webcomponents demo
(`elements/haxcms-elements/demo/ux-study-viewer.html`, on the Vercel preview or a local
`hax serve` of the monorepo) and drop the same JSON files in. Selecting a finding outlines
its control on the wireframe.

## 3. Review every finding before reporting it

The analyzer is deliberately noisy-but-honest; a person (or you, carefully) confirms each
finding against the real UI before it becomes a claim:

- **Find the control.** Each finding carries a shadow-piercing `path`
  (`haxcms-site-editor-ui > #shadow > simple-toolbar-button#addpage`). Locate that element in
  webcomponents and check what it is supposed to do.
- **Dead clicks** on content text are often people reading or selecting text: drop them
  unless they cluster on something styled like a control (pointer cursor, button-like box).
- **Hesitation** on a control everyone eventually used correctly is weaker than hesitation
  followed by Escape, backtracking, or a different control.
- **Late discovery** only matters if the task needed that control early. Check the task
  marks.
- **"Used by no one"** is context, not a finding.
- Weight by **how many participants** hit it, not raw counts: one person rage-clicking ten
  times is one person.
- Low contrast is measured only where a control paints its own opaque background; anything
  else needs a real contrast check in light and dark mode.

## 4. Write the report

Lead with the 3 to 5 findings that most block the tasks, each with: what happened (evidence
with "N of M participants"), where (control + path), why it likely happened, and a suggested
direction. Then the task table, then the rest grouped by category. Recommendations must
respect HAX rules: redesigns don't change an element's front-end API (attributes, usage,
labels), use DDD tokens, keep purple for incorrect and green for correct, and stay
accessible. Mark which findings were confirmed by a human.

## 5. File issues (ask first)

Issues go to the unified queue, **haxtheweb/issues**, never individual repos.

1. Search for duplicates per finding:
   `gh issue list --repo haxtheweb/issues --search "<control label> in:title,body" --state all`.
2. Show the person the proposed list (title, severity, evidence, duplicate matches) and get
   an explicit yes per issue or for the batch. Do not file unconfirmed findings.
3. File each confirmed one:
   ```bash
   gh issue create --repo haxtheweb/issues \
     --title "[ux-study] <short title>" \
     --body-file finding-UX-01.md
   ```
   Body: evidence, the control path, the task it blocked, participant count (codes only),
   the suggested direction, and a note that the pointer heatmap is an attention proxy.
   Never attach raw session files to a public issue.
4. Reply with a clickable link to every issue created.

## Thresholds (from the analyzer)

| Signal | Rule |
|---|---|
| Rage click | 3+ clicks within 1s and 32px |
| Dead click | non-interactive target, no route or focus change within 1s |
| Near miss | dead click within 16px of a control in the current snapshot (no scroll since) |
| Hesitation | hover of 1.5s+ on a control |
| Late discovery | first use 30s+ after the control was first on screen |
| Backtrack | A → B → A with 10s or less on B |
| Small target | under 24px in either dimension (WCAG 2.2 target size) |
| Faded | opacity under 0.6 |

Change thresholds in webcomponents (`UXStudyAnalyzer.js`), not here, so the viewer and the
script stay in agreement.
