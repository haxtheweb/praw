# hax-platform-dev

Platform development for HAXcms: keep the Node and PHP backends in step, build site importers, run the right tests per repo, and prepare maintainer release handoffs without running publish steps.

**Who it is for:** You work on HAXcms backends, importers, tests, or releases.

## Install

```
/plugin marketplace add haxtheweb/praw
/plugin install hax-platform-dev@haxtheweb
```

## Skills

| Skill | What it does |
|---|---|
| `hax-backend-dev` | Keep haxcms-nodejs and haxcms-php in step: mirror routes and OpenAPI specs. |
| `hax-importer-dev` | Build a site importer end to end: converters, dispatcher, spec, client, tests. |
| `hax-testing` | Find and run the right tests per HAX repo; write the test for a new endpoint. |
| `hax-release-prep` | Verify locally and write the maintainer handoff for ubiquity build and publish steps. |

## Where to start

Start with hax-testing so you know how to verify any change.

## How this plugin is built

The skills live once, in `skills/` at the repo root. This plugin is a curated view over them (the marketplace entry lists the skill paths), so there is nothing to keep in sync here.
