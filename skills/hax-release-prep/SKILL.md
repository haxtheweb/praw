---
name: hax-release-prep
description: "Prepare HAX changes for a maintainer release: verify locally, then write the handoff for the ubiquity build and publish steps an agent must never run. Use when work is done and heading to release, or when asked what happens next."
version: 1.0.0
license: Apache-2.0
metadata:
  author: haxtheweb
  depends_on: [hax-managed-files, hax-testing]
  tags: [hax, release, ubiquity, wc-registry, handoff, publishing]
---

# HAX release prep

Some steps belong to a maintainer, not an agent. This skill is the line between them: do everything up to
it, then hand off clearly.

## Agent never does

- Runs the ubiquity script. It builds the CDN registry and distribution.
- Runs a build at the top of the `webcomponents` monorepo.
- Edits `build/`, `node_modules/`, or generated files such as `wc-registry.json` and
  `custom-elements.json`.
- Runs release or publish commands: `npm run release` in haxcms-nodejs, `yarn release` in haxcms-php,
  `lerna publish` in webcomponents. These tag, push, and publish.
- Merges its own PRs.

## Agent does

1. **Verify locally.** Run the tests for what changed (`hax-testing`) and each repo's pre-submission
   check. Do not report a result you did not observe.
2. **Regenerate through source.** For elements, run the component's own `yarn run build` so
   `custom-elements.json` is regenerated, never hand-edited. New elements are created with
   `hax webcomponent`, not by hand.
3. **Fix at the source.** If minified output in a backend is wrong, fix it in `webcomponents`, verify,
   then hand off. Do not patch the output.
4. **Commit cleanly.** Use conventional commit messages; the release tooling derives versions and
   changelogs from them.
5. **Open PRs and stop.** One per repo, cross-linked, referencing the issue in
   https://github.com/haxtheweb/issues.

## Registry implications to call out

`wc-registry.json` is built by the ubiquity script and drives the magic-script autoloader. It lists
every element published on the CDN and hydrates a tag when it is undefined in the DOM. So say whether
the change adds, renames, or removes an element tag. Any of those changes the registry on the next
ubiquity run, and downstream sites depend on it.

## Handoff note (put in the final PR or issue comment)

- **What changed**, by repo, with PR links.
- **Verified**: commands run and results; anything that could not run, and why.
- **Registry impact**: added, renamed, or removed element tags, or "none".
- **Maintainer steps**: run the ubiquity build, then release per repo, in that order.
- **Not done**: anything left out on purpose.

References: https://github.com/haxtheweb/praw/blob/main/skills/hax-managed-files/SKILL.md and
https://github.com/haxtheweb/praw/blob/main/RULES.md.
