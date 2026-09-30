---
name: heosat-report-site
description: Run a HEOSAT open source maturity assessment on a project and publish the result as a single-page HAXcms report site on surge — scorecard, per-question evidence, strengths, and prioritized recommendations, plus ready-to-post LinkedIn / X copy. Takes the same input as the heosat skill (a GitHub repo URL, owner/repo, or an existing assessment directory with scores.json/report.md). Use whenever the user says "publish the HEOSAT report", "make a HEOSAT report site for this repo", "assess this project and publish it", "put this assessment on surge", "turn this HEOSAT report into a site", or hands you a repo and wants a published, shareable maturity report link — even if they don't say "skill", "site", or "surge". Companion to the `heosat` skill; leverages the same site scaffold + surge publish workflow as `hax-tutorial-site`.
version: 1.0.0
license: Apache-2.0
metadata:
  author: haxtheweb
  tags: [hax, heosat, assessment, report, surge, resume-theme, editable-table, a11y-collapse, social-copy, skeleton-file, portable]
---

# HEOSAT Report Site

Assess an open source project with the **`heosat` skill** (9 sections, 45 questions, 0-5 maturity scale, evidence-backed scoring), then turn the resulting report into a **published single-page HAXcms site** the user can share as a link — scorecard, per-question evidence, strengths, prioritized recommendations, and provenance — plus ready-to-post LinkedIn / X copy.

## Inputs (two modes)

- **Fresh assessment (default)** — a GitHub URL, `owner/repo` shorthand, or any git repo URL. The workflow runs the full `heosat` skill first (clone to /tmp → evidence → 45 scores → validated `scores.json` + `report.md`), then builds and publishes the site.
- **Existing report** — a directory that already contains `scores.json` (and ideally `report.md`), e.g. a `/tmp/heosat-<owner>-<repo>/` scratch dir from a previous `heosat` run. Skip straight to site generation (step 4).

## Prerequisites

- The sibling **`heosat`** skill (`../heosat/`) — provides the rubric (`references/rubric.json`) for the fresh-assessment mode and for page question text.
- `hax` CLI (local copy — never `npx`), `surge`, `node` v18+, `gh` (installed — read its output directly, don't ask the user to verify).
- The `heosat-report` site skeleton is **bundled with this skill** at `references/heosat-report.json` (resume-theme + one placeholder page) and is used via `--skeleton-file`, so no personal-profile skeleton install is required.
- Sites live under `~/Documents/git/haxtheweb/ai-single-site-heosat-reports/` (create it if missing).

## The project profile rule (read before building the profile)

The resume-theme sidebar is an "author" card, but **the author here is the assessed PROJECT, never the publishing person**. No personal name, email, phone, or personal social links go anywhere in the published site — the sidebar card presents the project being graded:

- `name` — the project's display name (prefer the README H1 or package name; fall back to the repo slug title-cased)
- `image` — the project org/user avatar: `gh api repos/<owner>/<repo> --jq .owner.avatar_url`
- `location` — project facts line, e.g. `MIT License · TypeScript · Node 18+`
- `website` — the repository URL; `website2` — the project homepage (if it has one)
- NO `email`, `phone`, or `socialLink` fields — those slots stay empty for a project

The same rule applies to the social copy: no personal handles or signatures.

## Modes

- **Publish mode (default)** — the full workflow runs end to end: assess (if needed), scaffold, convert, publish to surge, generate copy, report back.
- **Review mode** — when the user's request implies oversight before publishing ("review before publishing", "let me look at it first", "don't publish yet"). Run through the convert step, then stop: report the local site directory and page file path, start `hax serve` from the site directory for in-browser review, and wait for the user's explicit go-ahead ("publish it") before the surge publish + copy steps. Stop the dev server before publishing.

## Execution style

Run the whole workflow straight through with minimal narration. Only report once, at the end: the published site URL, the local site path, and the copy blocks. If a step soft-fails, note it in one line and continue.

## Workflow

1. **Collect the input** — repo URL / `owner/repo` (fresh mode) or an existing scores directory (existing mode; verify `scores.json` exists there).
2. **Run the assessment (fresh mode only)** — execute the **`heosat` skill** end to end: clone the repo into `/tmp/heosat-<owner>-<repo>/`, gather evidence (static review only), score all 45 questions into `scores.json`, and run its `aggregate.py` until validation is clean, producing `<scores-dir>/report.md`. In existing mode, reuse the given directory as `<scores-dir>`.
3. **Write the project profile** — gather project details via `gh` and write `<scores-dir>/project-profile.json` per the profile rule above:
   ```bash
   gh repo view <owner/repo> --json name,description,homepageUrl,licenseInfo,primaryLanguage
   gh api repos/<owner>/<repo> --jq .owner.avatar_url
   ```
   ```json
   {
     "project": {
       "name": "BookLooky Official LRS Rater",
       "image": "https://avatars.githubusercontent.com/u/...",
       "location": "MIT License · TypeScript · Node 18+",
       "website": "https://github.com/TheWootini/booklooky-official-lrs-rater",
       "website2": "https://booklooky.com"
     }
   }
   ```
4. **Derive the machine name** — `heosat-<repo-slug>` (repo slug = repo name, kebab-case, no owner segment; e.g. `booklooky-official-lrs-rater` → `heosat-booklooky-official-lrs-rater`). If it already exists under `ai-single-site-heosat-reports/`, append `-2`, `-3`, etc. `metadata.site.name` MUST equal this folder name (the scaffold sets it; never modify it).
5. **Scaffold the site from the bundled skeleton** — run from the reports directory with automation flags (never `npx`; the `--y --no-i --auto --skip --quiet` flags prevent prompts and sub-process launches):
   ```bash
   mkdir -p ~/Documents/git/haxtheweb/ai-single-site-heosat-reports && cd ~/Documents/git/haxtheweb/ai-single-site-heosat-reports && \
     hax site <machine-name> --skeleton-file <skill-dir>/references/heosat-report.json \
       --y --no-i --auto --skip --quiet
   ```
6. **Convert the assessment into the site** — one pass builds the page (H1, overall stop-note, editable-table scorecard, a11y-collapse sections with every scored question and its evidence, strengths, recommendation collapses, About/provenance block), copies `report.md` + `scores.json` into the site's `files/`, and finalizes `site.json` (title, description, sidebar subtitle, root page label, and the PROJECT profile in `metadata.author`):
   ```bash
   node <skill-dir>/scripts/report-to-site.cjs <scores-dir> <site-dir>
   ```
   `report-to-site.cjs` resolves the rubric from `../heosat/references/rubric.json` automatically and the project profile from `<scores-dir>/project-profile.json` (both overridable with `--rubric` / `--project-profile`).
   **Review-mode fork:** stop here; start `hax serve` from `<site-dir>`, report the local paths, and wait for the user's go-ahead before step 7.
7. **Publish to surge** — the domain is `<machine-name>.surge.sh`:
   ```bash
   cd <site-dir> && hax site site:surge --domain <machine-name>.surge.sh \
     --y --no-i --auto --quiet
   ```
   The CLI auto-installs surge if missing and swaps in the static `index.html` for publish. Do NOT verify the surge URL after publishing (no curl/HTTP check, no opening it) — the user opens the published site manually once the workflow is done.
8. **Generate the sharing copy** — read `references/social-copy-templates.md` and produce the LinkedIn post and the X post (≤280 chars), each leading with the `📊🌐 Report:` link to the surge URL, using the overall score, band, and a 2-3 sentence verdict from the report. No personal handle or signature anywhere.
9. **Report back (concise)** — print only: the published site URL, the local site path, the overall score line, and the two copy blocks (LinkedIn, X). Keep it scannable so the user can copy/paste and post immediately. Remind them this is a locally generated assessment against the published HEOSAT rubric — not an official certification.

## Command reference

- Scaffold: `hax site <machine-name> --skeleton-file <skill-dir>/references/heosat-report.json --y --no-i --auto --skip --quiet`
- Convert + finalize: `node <skill-dir>/scripts/report-to-site.cjs <scores-dir> <site-dir> [--project-profile <path>] [--rubric <path>] [--description "<text>"]`
- Publish: `cd <site-dir> && hax site site:surge --domain <machine-name>.surge.sh --y --no-i --auto --quiet`
- Review-mode dev server: `cd <site-dir> && hax serve` (stop it before publishing)
- Fresh assessment: run the `heosat` skill (its own SKILL.md governs that workflow)

## How the page presents the report

All page elements are HAX-capable components (they could have been authored in the HAX editor), so the published page stays editable through HAX:

- `stop-note` — the overall score callout (title: `Overall: X.X / 5 (band)`)
- `editable-table` (bordered, condensed, responsive, striped) — the 9-section + overall scorecard with a caption
- `a11y-collapse-group` + `a11y-collapse` per section and per recommendation. `heading-button` (and the shared `icon`) are set on the **group**, not per-child — the group spreads all A11yCollapse properties and copies its defined values onto every child collapse on attach and on update, so the whole heading is clickable on every item (per-child `label`/`tooltip` stay unique and are never wiped, since the group leaves those undefined). Headings use the **slot method** (`<p slot="heading">…</p>` light DOM, not the `heading` attribute) because report headings are long — slotted headings wrap naturally as real content. Content shows each question as `LL1 — 3/5 (band)` + the question text + evidence list + notes
- DDD `data-margin` attributes (`s` on headings, `xs` on intro paragraphs) for consistent offsets
- The About block links the copied `files/heosat-report.md` (full report) and `files/heosat-scores.json` (machine-readable scores) and carries the HEOSAT attribution (adapted from the OSS Watch Openness Rating, guidance CC BY-SA 4.0)

## Guardrails (ecosystem rules)

- Use the **local** `hax` command, never `npx`.
- Always pass `--y --no-i --auto --skip --quiet` when scripting `hax` so no prompts or sub-processes launch.
- Keep `metadata.site.name` equal to the site folder name; never modify it (the converter also never touches it).
- No personal information in the published site or the copy — the resume-theme author slot carries the assessed PROJECT's details.
- Do not create `x/` routes (reserved for internal HAXcms paths).
- Do not run the monorepo build or the ubiquity script.
- After publishing to surge, do NOT verify the URL is live (no curl/HTTP check, no opening it).
- Avoid optional chaining (`?.`) in any generated code (the Polymer parser has issues with it).
- Use `globalThis` instead of `window` in generated JavaScript.

## References

- `references/heosat-report.json` — the `heosat-report` site skeleton bundled with this skill (resume-theme + settings + one placeholder "HEOSAT Report" page). Scaffolding uses `--skeleton-file` with this direct path, so the skill is self-contained and portable.
- `references/social-copy-templates.md` — LinkedIn / X copy templates for sharing the published report link (report framing, no YouTube/watch lines, no personal signature).
- `scripts/report-to-site.cjs` — the converter: reads `<scores-dir>/scores.json` + the heosat rubric, builds the single-page report (scorecard, section/recommendation collapses with heading-button, About block), copies `report.md`/`scores.json` into `files/`, and finalizes `site.json` (title, description, sidebar subtitle, root item title, project profile into `metadata.author`).
- **`heosat` skill** (`../heosat/`) — dependency for fresh assessments and the rubric source (`references/rubric.json`).
- **`hax-tutorial-site` skill** (`../hax-tutorial-site/`) — the site scaffold + surge publish pattern this skill mirrors.
