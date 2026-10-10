---
name: hax-design-system-sync
description: Maintain the DDD design system across the HAX ecosystem and keep every derived copy in step with the source. Lint for unknown or broken --ddd-* tokens and fix them, check WCAG contrast of DDD's pairings, regenerate the DTCG token export and the hax-design-system skill references, rebuild the claude.ai DDD Design System with the sync script, open the pull requests, and publish once merged. Use when a maintainer says "sync the design system", "run the DDD maintenance", "republish the DDD design system", "fix the unknown DDD tokens", "the token lint is failing", "update the design tokens", "regenerate ddd-tokens.md", or after DDDStyles.js, SimpleColors or a DDD-based element changes — even if they don't say "skill" or "sync".
version: 1.0.0
license: Apache-2.0
metadata:
  author: haxtheweb
  tags: [hax, ddd, design-system, design-tokens, dtcg, simplecolors, lint, contrast, wcag, maintenance, administration]
  depends_on: [hax-design-system, hax-managed-files]
---

# DDD Design System Sync

DDD lives in one place, `elements/d-d-d/lib/DDDStyles.js` in **haxtheweb/webcomponents**, together with SimpleColors. Everything else is derived from that source and goes stale when it changes:

| Derived copy | Where | Rebuilt by |
|---|---|---|
| DTCG design tokens (Tokens Studio, Style Dictionary) | webcomponents `elements/d-d-d/tokens/*.json` | `yarn tokens:ddd` |
| The claude.ai DDD Design System (every element live, light and dark) | webcomponents `elements/d-d-d/design-system/dist/` (gitignored), then published | `yarn design-system:sync` |
| Token and SimpleColors references for agents | praw `skills/hax-design-system/references/ddd-tokens.md`, `simplecolors-migration.md` | `node scripts/generate-ddd-references.js` |
| Skill discovery index | praw `.well-known/agent-skills/index.json` | `node scripts/build-agent-skills-index.js` |

This skill keeps those copies in step, and keeps the source clean while doing it.

## Inputs

- A **webcomponents** checkout and a **praw** checkout. The default layout is sibling folders, for example `~/Documents/git/haxtheweb/{webcomponents,praw}`.
- *(Optional)* the claude.ai DDD Design System artifact URL, needed only for the publish step.
- *(Optional)* scope: the full run (default), or one step, such as "just fix the lint".

## Prerequisites

- Node 22+ and `yarn install` at the webcomponents root. The sync's bundler, esbuild, comes from the repo's devDependencies. Under `bun` it uses `Bun.build` instead.
- `gh` for pull requests. Use the local `hax` CLI, never `npx`.
- Read **hax-managed-files** first: everything in the table above is generated. Never hand-edit a generated file; change the source or the generator, then rebuild.

## Workflow

Run it straight through and report once at the end. If a step soft-fails, say so in one line and continue.

1. **Branch from current master in both repos.** Run `git fetch` and branch from `origin/master`. If an open DDD PR already touches the same files, stack on it (base = that PR's branch) and say so.

2. **Lint the token references** (webcomponents root):
   ```
   node scripts/ddd-token-lint.js          # exit 1 on unknown tokens or broken border shorthands
   node scripts/ddd-token-lint.js --all    # everything, including baseline entries
   ```
   Fix every finding using `references/token-remediation.md`:
   - **The rule:** a reference with a fallback keeps what renders. A reference without one gets the token its name intended, and that counts as a visual change.
   - **The names table** gives the real token for names people commonly reach for.
   - **Border shorthands:** `--ddd-border-xs…lg` already include width, style and colour, so write `--ddd-border-size-*` in front of a style.

   Keep `scripts/ddd-token-lint.baseline.json` empty. Run `--update-baseline` only to *remove* fixed entries. Only add a name to the linter's `HOOK_TOKENS` when DDD reads it as a documented override hook with a fallback.

3. **Check contrast:**
   ```
   node <skill-dir>/scripts/contrast-report.cjs --webcomponents <webcomponents>
   ```
   It exits 1 when a regression gate fails:
   - a `data-primary` fill whose DDD-assigned ink is below 4.5:1, or where the other ink reads clearly better;
   - a SimpleColors shade with no ink at 4.5:1.

   Coloured text (primaries on white, on coaly gray and on accents) is reported but not gated. Mention it in the PR when the counts drop. If a component hard-codes a light-only colour, give it a `light-dark()` pair; `ddd-steps-list-item` is the model.

4. **Regenerate the derived files:**
   ```
   # webcomponents
   yarn tokens:ddd                       # DTCG export (CI runs build-tokens.js --check)
   yarn design-system:sync               # -> elements/d-d-d/design-system/dist/
   # praw
   node scripts/generate-ddd-references.js --webcomponents ../webcomponents
   node scripts/build-agent-skills-index.js
   ```
   **Sync warnings.** Resolve every one before opening the PR:
   - *"tokens.json has no entry for …"*: add each token to the right family in `elements/d-d-d/design-system/source/tokens.json` with a one-line `usage`. There are at most 12 extra families, and it is already at 12.
   - *"cards not in header.json"*: add `{"name":"<Card>"}` to `source/bundle/header.json` where the card should sort.
   - *"runtime file missing"*: fix or remove the path in `source/runtime/nm.json`.
   - **Limit warnings** (sizes, file counts, names): see `references/publishing.md`.

   **New DDD-based element.** Add its module to `source/bundle/entries.json` and a card (`source/components/<Name>/preview.html` + `README.md`) before syncing.

   **praw index.** `build-agent-skills-index.js` rewrites every entry. Commit only the entries for skills you changed, and leave unrelated entries alone.

5. **Open pull requests. Never merge.**
   - **One PR per repo per concern**: lint fixes, token or design changes, generated refreshes.
   - **Stack dependent PRs** (base = the branch they build on) and say so in the description.
   - **Describe each one.** Say what it touches and list every visual change. Include a was → now table when tokens are remapped.
   - **Give the commands.** Include what a reviewer can run to verify, and say plainly what you could not verify, such as no browser render or a package you couldn't install.
   - **Don't merge.** Maintainers review, discuss and merge.

6. **Publish the design system.** Do this only after merge, and only from master. Re-run the sync on master, then follow `references/publishing.md`:
   - read the existing artifact;
   - publish in batches of 255 files or fewer;
   - publish `design-system.json` last.

   This needs a Claude session with the Artifact tool. Any other agent stops after the sync and hands `dist/` to a maintainer.

7. **Report.** Give the PR links (merge order first), the lint and contrast results, the sync warnings you resolved, and what is left for the maintainer, such as review, merge or publish.

## Guardrails

- Never merge or approve PRs, push to master, or force-push someone else's branch.
- Never hand-edit generated files: `elements/d-d-d/tokens/*.json`, `design-system/dist/`, `references/ddd-tokens.md`, `references/simplecolors-migration.md`, `index.json`. Change the source and regenerate.
- Never grow the lint baseline to make CI pass.
- Don't run the top-level monorepo build or the ubiquity script. Use the targeted commands above.
- Use `globalThis` instead of `window`, and avoid optional chaining (`?.`) in generated element code (Polymer parser).
- DDD stands for **Design, Develop, Destroy**. Headings use `--ddd-font-primary` (Roboto); Roboto Slab is the opt-in secondary font.

## References

- `references/token-remediation.md`: the decision rule, the table of commonly mistaken names, and the border-shorthand rule.
- `references/publishing.md`: how the design system is published, who can publish it, and the artifact limits the sync enforces.
- `scripts/contrast-report.cjs`: the WCAG report and regression gates over DDD's pairings (Node built-ins only).
- **hax-design-system**: how to *use* DDD in components. This skill *maintains* it.
- webcomponents `elements/d-d-d/design-system/README.md`: what each sync output is generated from, and the common changes (new element, new token, runtime file).
