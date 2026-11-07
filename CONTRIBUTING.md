# Contributing

> **New to the HAX ecosystem?** Start with the [ecosystem-wide developer onboarding](https://github.com/haxtheweb/issues/blob/master/CONTRIBUTING.md) — it covers prerequisites, cloning the core repos, and getting a local environment running. The guide below is specific to PRAW.

- [Contributing](#contributing)
  - [What is PRAW?](#what-is-praw)
  - [Getting Started](#getting-started)
  - [Finding Issues to Work On](#finding-issues-to-work-on)
  - [What You Can Contribute](#what-you-can-contribute)
    - [Rules (RULES.md, WARP.md)](#rules-rulesmd-warpmd)
    - [Skills (skills/)](#skills-skills)
    - [Claude Code plugins (plugins/)](#claude-code-plugins-plugins)
    - [Worldview and knowledge files](#worldview-and-knowledge-files)
  - [Communication](#communication)
  - [GitHub workflow](#github-workflow)
  - [Opening a Pull Request](#opening-a-pull-request)
  - [Code Review](#code-review)
  - [Best practices](#best-practices)
  - [Testing](#testing)
  - [Security](#security)

HAX is open source, but many of the people working on it do so as their day job.
In order to avoid forcing people to be "at work" effectively 24/7, we want to establish some semi-formal protocols around development.
Hopefully, these rules make things go more smoothly.

As a potential contributor, your changes and ideas are welcome at any hour of the day or night, weekdays, weekends, and holidays.
Please do not ever hesitate to ask a question or send a pull request.

## What is PRAW?

PRAW holds the shared knowledge AI agents and contributors use across the HAX ecosystem: the rule registry (`RULES.md`, `WARP.md` files), agent skills (`skills/`), the official HAX Claude Code plugin marketplace (`plugins/`), and the worldview, voice and knowledge files that explain why HAX works the way it does. See the [README](README.md) for the full map.

## Getting Started

```bash
git clone https://github.com/YOUR_USERNAME/praw.git
cd praw
git remote add upstream https://github.com/haxtheweb/praw.git

# optional: the praw-* rule management commands
./scripts/setup.sh
```

Most changes are Markdown. Node (18+) is only needed for the scripts in `scripts/`.

## Finding Issues to Work On

1. **Browse the unified issue queue:** https://github.com/haxtheweb/issues/issues
   - Look for issues labeled `good first issue`, `help wanted` or `documentation`
   - Issues labeled `Plan Created` already have an implementation plan on them
2. **Ask for guidance:** join our [Discord](https://discord.gg/aCGxmRHEJP), introduce yourself, and ask what a good first issue would be.

**Before starting work:**
- Comment on the issue saying you'd like to work on it
- Wait for maintainer acknowledgment to avoid duplicate work
- Ask questions if the requirements aren't clear

## What You Can Contribute

### Rules (RULES.md, WARP.md)

1. Add rules with `praw-add` and pick the right category (see [Rule Categories](README.md#rule-categories))
2. Edit existing rules in place; keep [rule precedence](README.md#rule-precedence) intact and update related `WARP.md` files
3. Run `praw-validate` before committing
4. Record the decision and its rationale in `KNOWLEDGE.md`

### Skills (skills/)

- Each skill is a directory with a `SKILL.md` whose frontmatter has `name` (matching the directory), `description` (what it does **and** when to use it) and `version`. See [`skills/PUBLISHING.md`](skills/PUBLISHING.md).
- Skills must stay generic for whoever installs them: no machine-specific paths, and cross-project references use GitHub URLs.
- Every skill carries a "Content you read is data, not instructions" section (copy it from any existing skill) so agents treat fetched pages, issues, transcripts, documents and cloned repos as untrusted context. `node scripts/build-agent-skills-index.js` fails when a skill that reads such content lacks it.
- After adding or changing a skill, regenerate the discovery indexes with `node scripts/build-agent-skills-index.js`. Do not hand-edit `skills/index.json` or `.well-known/agent-skills/index.json`.
- HAXsites read skills from the `stable` branch. Work lands on `main` first; a maintainer promotes reviewed `main` to `stable`, and code owners review everything under `skills/`, `.well-known/agent-skills/` and `.agents/`.

### Claude Code plugins (plugins/)

Plugins bundle skills for the [HAX plugin marketplace](README.md#claude-code-plugin-marketplace). Interface skills that originate in [haxtheweb/create](https://github.com/haxtheweb/create) are copied in with `node scripts/sync-plugin-skill.js`, which reports drift, rather than edited here.

### Worldview and knowledge files

`WORLDVIEW.md`, `WHY.md`, `VOICE.md` and `WINS.md` carry the HAX worldview in the maintainers' own words. Propose changes to them in an issue first, and keep quoted material verbatim.

## Communication

Reporting issues? Our unified issue queue is a good place for this: https://github.com/haxtheweb/issues/issues
Need to discuss something via chat? Our [Discord can be joined here](https://discord.gg/aCGxmRHEJP).

## GitHub workflow

We work primarily using pull requests and forks. In order to work most effectively, we ask that you FORK any project you are wanting to contribute to in our ecosystem. After taking a fork, submit a pull request while pointing to the associated issue tied to this pull request.

## Opening a Pull Request

Pull requests are often called a "PR".
HAX generally follows the standard [github pull request](https://help.github.com/articles/about-pull-requests/) process.

Common new contributor PR issues are:
- Not referencing the issue that the PR resolves
- Not describing the scope of the solution effectively
- Include mentions (like @person) and [keywords](https://help.github.com/en/articles/closing-issues-using-keywords) which could close the issue (like fixes #xxxx) in commit messages.

## Code Review

To make it easier for your PR to receive reviews, consider the reviewers will need you to:

- Write [good commit messages](https://chris.beams.io/posts/git-commit/)
- Break large changes into a logical series of smaller patches which individually make easily understandable changes, and in aggregate solve a broader issue

When reviewing PRs from others [The Gentle Art of Patch Review](http://sage.thesharps.us/2014/09/01/the-gentle-art-of-patch-review/) suggests an iterative series of focuses which is designed to lead new contributors to positive collaboration without inundating them initially with nuances:

- Is the idea behind the contribution sound?
- Is the contribution architected correctly?
- Is the contribution polished?

Note: if your pull request isn't getting enough attention, you can use our [Discord channel](https://discord.gg/aCGxmRHEJP) to get help finding reviewers.

## Best practices

- Write clear and meaningful git commit messages.
- If the PR will *completely* fix a specific issue, include `fixes #123` in the PR body (where 123 is the specific issue number the PR will fix. This will automatically close the issue when the PR is merged.
- Make sure you don't include `@mentions` or `fixes` keywords in your git commit messages. These should be included in the PR body instead.
- When you make a PR for small change (such as fixing a typo, style change, or grammar fix), please squash your commits so that we can maintain a cleaner git history.
- Make sure you include a clear and detailed PR description explaining the reasons for the changes, and ensuring there is sufficient information for the reviewer to understand your PR.
- Additional Readings: 
    - [chris.beams.io/posts/git-commit/](https://chris.beams.io/posts/git-commit/)
    - [github.com/blog/1506-closing-issues-via-pull-requests ](https://github.com/blog/1506-closing-issues-via-pull-requests)
    - [davidwalsh.name/squash-commits-git ](https://davidwalsh.name/squash-commits-git)
    - [https://mtlynch.io/code-review-love/](https://mtlynch.io/code-review-love/)

## Testing

Unit tests are ideal but not required to be written for proposed changes and enhancements.

## Security

Do not open public issues for unpatched security vulnerabilities. See [`SECURITY.md`](SECURITY.md) to report one privately through a GitHub security advisory, or contact the core team on [Discord](https://discord.gg/aCGxmRHEJP) or at hax@psu.edu to discuss first.

All participation is covered by our [Code of Conduct](CODE_OF_CONDUCT.md).
