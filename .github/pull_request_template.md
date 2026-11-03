## Related Issue

<!-- Link the issue in the unified queue this PR addresses -->

Closes https://github.com/haxtheweb/issues/issues/XXXX

## Description of Changes

### What changed:

-
-

### Why this change was needed:

<!-- Explain the problem this solves or the feature this adds -->

## Type of Change

- [ ] 📏 Rule added or changed (`RULES.md`, `WARP.md`)
- [ ] 🧠 Skill added or changed (`skills/`)
- [ ] 🔌 Plugin added or changed (`plugins/`)
- [ ] 🌍 Worldview / knowledge (`WORLDVIEW.md`, `WHY.md`, `VOICE.md`, `WINS.md`, `KNOWLEDGE.md`)
- [ ] 🔧 Scripts or CI (`scripts/`, `.github/`)
- [ ] 📚 Other documentation

## Checks Run

<!-- Say which you ran -->

- [ ] `praw-validate` (rule changes)
- [ ] `node scripts/build-agent-skills-index.js` and committed the regenerated indexes (skill changes)
- [ ] Each changed `SKILL.md` has `name` (matching its directory), `description` and `version` frontmatter
- [ ] No machine-specific paths; cross-project references use GitHub URLs
- [ ] Recorded the decision and rationale in `KNOWLEDGE.md` (rule changes)

## HAX Pillar Checks

<!-- For non-trivial changes. A "no" is fine: name it below, say why, and link a follow-up issue in https://github.com/haxtheweb/issues. Full questions: https://github.com/haxtheweb/praw/blob/main/WORLDVIEW.md#pillar-checks -->

- [ ] **Accessible**: guidance keeps HAX output at WCAG 2.0 AA without extra effort from authors
- [ ] **Efficient**: no new heavy dependency or build step without reason; a newcomer gets it in about three seconds
- [ ] **Extensible**: built on web standards; plugs into existing and future systems
- [ ] **Free and open**: no paywall, lock-in or required proprietary service
- [ ] **Platform agnostic**: works across agents and across backends (Node.js, PHP, static, desktop)
- [ ] **Remixable**: content stays portable (HTML, JSON Outline Schema); import and export still work
- [ ] **Sustainable**: someone other than the author could maintain it; sites made before this change still work
- [ ] **Human creativity first**: people keep the creative decisions and the output doesn't depend on one AI service

Any "no", and why:

## Additional Notes

<!-- Any additional context, decisions, or follow-up work -->

- [ ] I have read the [contributing guidelines](https://github.com/haxtheweb/praw/blob/main/CONTRIBUTING.md)
