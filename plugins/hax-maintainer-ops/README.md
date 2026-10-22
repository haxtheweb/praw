# hax-maintainer-ops

Maintainer workflows: summarize and analyze issues across the ecosystem, research an issue into a documented plan, and manage the PRAW rules registry.

**Who it is for:** You triage issues, plan work, or maintain PRAW rules.

## Install

```
/plugin marketplace add haxtheweb/praw
/plugin install hax-maintainer-ops@haxtheweb
```

## Skills

| Skill | What it does |
|---|---|
| `hax-issue-analysis` | Fetch, analyze, and summarize GitHub issues across the HAX ecosystem. |
| `hax-issue-research` | Research a HAX issue, draft a plan, and capture it as a 'Plan Created' comment. |
| `hax-rule-management` | Add, search, validate, and export PRAW rules stored in RULES.md. |

## Where to start

Start with hax-issue-analysis for a ranked view of what needs attention.

## How this plugin is built

The skills live once, in `skills/` at the repo root. This plugin is a curated view over them (the marketplace entry lists the skill paths), so there is nothing to keep in sync here.
