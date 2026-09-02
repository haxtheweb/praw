# HAX Onboarding — Claude Code plugin

Golden-path onboarding for the [HAX CLI](https://www.npmjs.com/package/@haxtheweb/create)
(`@haxtheweb/create`, the `hax` command). Takes a brand-new user from nothing to a
**live HAXsite open in the browser** on their first session — and gives the
assistant the full command surface for everything that comes after.

## What's inside

- **Auto-install hook** — a `SessionStart` hook checks whether `hax` is on your
  `PATH`. If it's missing (and you don't have a local dev checkout), it installs
  `@haxtheweb/create` globally (one time). If a local development copy is detected
  under `~/Documents/git/haxtheweb/create`, it skips the install and uses that
  instead. Opt out with `export HAX_PLUGIN_NO_AUTOINSTALL=1`.
- **`hax` skill** — full command-surface knowledge (web components, sites,
  content/node ops, imports, skeletons, publishing, skills management) plus HAX
  conventions (JavaScript-only, DDD design tokens, `haxProperties`, no optional
  chaining). Claude loads it automatically when you talk about HAX.
- **Slash commands** for the top workflows:
  - `/hax-onboarding:quickstart` — **start here**: scaffold a HAXsite and open it live
  - `/hax-onboarding:site` — create or administer a HAXsite
  - `/hax-onboarding:webcomponent` — scaffold a Lit/DDD web component
  - `/hax-onboarding:audit` — audit components for DDD compliance
  - `/hax-onboarding:serve` — run a HAXsite dev server
  - `/hax-onboarding:publish` — deploy to surge / Netlify / Vercel or set up CI
- **Codex prompt** — a golden-path prompt for OpenAI Codex at
  [`codex/hax-quickstart.md`](codex/hax-quickstart.md). Copy it into
  `~/.codex/prompts/` to get the same quickstart in Codex.

## Install

This repo is a Claude Code plugin **marketplace**. Add it and install the plugin:

```text
/plugin marketplace add haxtheweb/praw
/plugin install hax-onboarding@haxtheweb
```

To develop against a local checkout instead:

```text
/plugin marketplace add /path/to/praw
/plugin install hax-onboarding@haxtheweb
```

## Quickstart (the golden path)

New to HAX? Once the plugin is installed, just run:

```text
/hax-onboarding:quickstart
```

It checks the CLI is ready (the auto-install hook handles that on session start),
scaffolds a HAXsite with sensible defaults, serves it locally, and hands you the
live URL with the one next edit to make. From nothing to a site you can see, in a
single step. Everything else (`/hax-onboarding:webcomponent`,
`/hax-onboarding:audit`, `/hax-onboarding:publish`, content/import operations)
builds out from there.

## Codex

Codex has no plugin/marketplace/hook system. For the same golden path in Codex,
use the prompt at [`codex/hax-quickstart.md`](codex/hax-quickstart.md) — copy it
into `~/.codex/prompts/hax-quickstart.md` and invoke it in Codex.

## Requirements

- Node.js `>=18.20.3` and `npm` on your `PATH` (so the CLI can be installed).

## Links

- HAX CLI source & docs: <https://github.com/haxtheweb/create>
- HAX: <https://haxtheweb.org/> · <https://hax.psu.edu/>
