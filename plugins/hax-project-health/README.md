# hax-project-health

Assess open source project maturity with HEOSAT and publish the evidence-backed scorecard as a single-page HAXcms report site.

**Who it is for:** You assess open source project maturity and want a shareable report.

## Install

```
/plugin marketplace add haxtheweb/praw
/plugin install hax-project-health@haxtheweb
```

## Skills

| Skill | What it does |
|---|---|
| `heosat` | Run the HEOSAT open source maturity assessment into an evidence-backed scorecard. |
| `heosat-report-site` | Publish a HEOSAT assessment as a single-page HAXcms report site. |

## Where to start

Run heosat against a repo, then heosat-report-site to publish the result.

## Prerequisites

This plugin composes with interface skills owned by the `create` repo (`@haxtheweb/create`). Install them so dependencies resolve:

```
npm install -g @haxtheweb/create
hax skills install --all
```

Needed here: `hax-site-building`.

## How this plugin is built

The skills live once, in `skills/` at the repo root. This plugin is a curated view over them (the marketplace entry lists the skill paths), so there is nothing to keep in sync here.
