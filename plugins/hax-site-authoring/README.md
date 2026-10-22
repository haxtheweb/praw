# hax-site-authoring

Author and maintain HAXcms sites: understand the portable file structure, write content with the right components, avoid hand-editing generated files, theme a site, and publish tutorials.

**Who it is for:** You build or maintain HAXcms sites and write content for them.

## Install

```
/plugin marketplace add haxtheweb/praw
/plugin install hax-site-authoring@haxtheweb
```

## Skills

| Skill | What it does |
|---|---|
| `hax-mental-model` | Orient newcomers and agents: how the pieces of HAX fit together, with a glossary and a contribution path. |
| `hax-site-structure` | Read and navigate an existing HAXcms site from its portable files (site.json, pages/, files/, theme). |
| `hax-content-authoring` | Author page content using HAX-capable web components, DDD attributes, and pages/ conventions. |
| `hax-managed-files` | Know which HAXcms files are generated vs authored, and the protective rules around builds. |
| `hax-theme-builder` | Turn a screenshot into an accessible, dark-mode-ready HAXcms theme. |
| `hax-tutorial-site` | Publish a HAXcms tutorial site from a YouTube video and DOCX transcript, plus social copy. |

## Where to start

Start with hax-mental-model for the big picture, then hax-site-structure, then hax-managed-files before you touch any build.

## Prerequisites

This plugin composes with interface skills owned by the `create` repo (`@haxtheweb/create`). Install them so dependencies resolve:

```
npm install -g @haxtheweb/create
hax skills install --all
```

Needed here: `hax-site-building`.

## How this plugin is built

The skills live once, in `skills/` at the repo root. This plugin is a curated view over them (the marketplace entry lists the skill paths), so there is nothing to keep in sync here.
