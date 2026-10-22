# hax-component-dev

Build and maintain HAX web components: apply and sync DDD tokens, audit against the pattern library, prove an element in the real HAX editor, find OER Schema integration gaps, and translate i18n at scale.

**Who it is for:** You create or improve HAX web components, themes, and the DDD design system.

## Install

```
/plugin marketplace add haxtheweb/praw
/plugin install hax-component-dev@haxtheweb
```

## Skills

| Skill | What it does |
|---|---|
| `hax-mental-model` | Orient newcomers and agents: how the pieces of HAX fit together, with a glossary and a contribution path. |
| `hax-design-system` | Apply the DDD design system and manage SimpleColors legacy usage. |
| `hax-design-system-sync` | Maintain DDD across the ecosystem: lint tokens, check contrast, regenerate exports. |
| `hax-pattern-library-audit` | Read-only audit of one web component against the DDD Atomic Design pattern library. |
| `oerschema-integration-finder` | Scan code for surfaces that should emit or consume OER Schema but don't. |
| `hax-element-demo` | Build a throwaway demo of an element inside the real HAX editor to check wiring. |
| `hax-i18n-translate` | Scaffold and translate web component i18n locale files at scale. |

## Where to start

Start with hax-mental-model for the big picture, then hax-design-system; component scaffolding comes from hax-webcomponent-dev in create.

## Prerequisites

This plugin composes with interface skills owned by the `create` repo (`@haxtheweb/create`). Install them so dependencies resolve:

```
npm install -g @haxtheweb/create
hax skills install --all
```

Needed here: `hax-webcomponent-dev`.

## How this plugin is built

The skills live once, in `skills/` at the repo root. This plugin is a curated view over them (the marketplace entry lists the skill paths), so there is nothing to keep in sync here.
