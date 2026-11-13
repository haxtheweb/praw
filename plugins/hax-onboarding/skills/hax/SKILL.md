---
name: hax
description: >-
  Onboard and drive the HAX CLI (@haxtheweb/create). Use when the user wants to set up
  the HAX development environment, create a HAX web component or HAXsite, scaffold a
  Lit/DDD component, audit DDD design-system compliance, run a HAXsite dev server,
  add/edit/delete pages or content, import or migrate content into a HAXsite,
  publish to surge/netlify/vercel/gh-pages, or otherwise run `hax` commands.
  Triggers include: hax, haxcms, haxsite, haxtheweb, web component, Lit element,
  DDD audit, "hax site", "hax webcomponent", onboarding, "set up HAX".
allowed-tools: Bash(hax:*), Bash(cd:*), Bash(npm install --global @haxtheweb/create*), Bash(npm install), Bash(npm start), Bash(npm run build), Bash(git clone:*), Read, Edit, Write, Glob, Grep
version: 1.2.0
license: Apache-2.0
metadata:
  author: haxtheweb
  tags: [hax, onboarding, setup, cli, environment, scaffolding, webcomponents, lit, ddd]
  source: create
---

# HAX CLI (`@haxtheweb/create`)

The `hax` command rapidly scaffolds and manages **HAX-capable web components** and
**HAXsites** (HAXcms single sites). It is the primary interface for the HAX
ecosystem. This skill gives you the command surface and the conventions that make
HAX work correctly.

## Installation & updates

```bash
npm install --global @haxtheweb/create   # installs `hax` and `create-haxtheweb`
hax update                               # self-update the CLI
hax --version                            # check installed version
```

This plugin's SessionStart hook checks for `hax` and, only when the user has opted
in with `HAX_PLUGIN_AUTOINSTALL=1`, installs the CLI. If `hax` isn't on PATH, run
the global install above (pin a version with `@haxtheweb/create@<version>` when
reproducibility matters). Do not fall back to `npx @haxtheweb/create` — an
unpinned `npx` run fetches and executes whatever is latest on the registry.
Requires Node `>=18.20.3`.

If you have a local development checkout of
[`create`](https://github.com/haxtheweb/create), set `HAX_DEV_PATH` to its path and
the hook skips the global install — the local copy is always the latest or even
experimental.

## Quickstart (golden path for a new user)

When someone is new to HAX or just wants to see something work, lead with the
shortest path to a **live site in the browser** — do not dump the full command
surface on them:

```bash
hax site my-hax-site --y --no-i     # 1. scaffold a HAXsite with defaults
cd my-hax-site && hax serve         # 2. serve it (background; long-running)
                                    # 3. surface the local URL + one next edit
```

The `/hax-onboarding:quickstart` command runs exactly this. Default the site name
if they don't supply one, background `hax serve`, report the URL, and point at a
single concrete next step. Save web components, audits, imports, theming, and
publishing for after they've seen their first site.

## Ecosystem onboarding (full setup)

For developers setting up a full HAX development environment:

1. **Clone Repositories**: Clone all HAX ecosystem repositories into
   a single workspace folder (ask the user where). Core repos: `webcomponents`, `create`,
   `haxcms-php`, `haxcms-nodejs`, `desktop`, `hax11ty`, `json-outline-schema`,
   `hax-schema`, `open-apis`, `docs`, and `issues`.
2. **Install HAX CLI**: `npm install --global @haxtheweb/create` (or opt in to the
   auto-install hook with `HAX_PLUGIN_AUTOINSTALL=1`). Update with `hax update`.
3. **Install Agent Skills**: Run `hax skills install --all` to install bundled
   interface skills (site building, ClaudeHAX, web component dev, onboarding)
   into `~/.agents/skills/` so any agent can use them.
4. **Configure Environment**: Start new shells in that workspace folder.
   Point your agent at PRAW's rules (Warp reads `WARP.md` on its own).
5. **Verify**: Run `hax --version` to confirm CLI installation, then
   `hax skills list` to confirm bundled skills are available.

## Command groups

```bash
hax start          # interactive menu (ascii art + Clack prompts)
hax serve          # run a HAXsite in dev mode at http://localhost
hax site           # create / administer a HAXsite
hax webcomponent   # create / work with a Lit + DDD web component (alias: hax wc)
hax audit          # audit web components for DDD compliance
hax skills         # list / install bundled agent skills
hax party          # community / get-involved options
hax update         # CLI self-update
hax platform       # HAXcms install: status / upgrade / verify / rollback (not on HAXiam)
hax help [command] # authoritative, up-to-date help; also `hax site --help`
```

Always trust `hax help`, `hax site --help`, and `hax webcomponent --help` for the
current flag list — they reflect the installed version.

## Global flags (apply across commands)

| Flag | Meaning |
|------|---------|
| `--y` / `--auto` | Yes to all prompts (scripting) |
| `--no-i` | No interactions / sub-processes (best for scripting) |
| `--quiet` | Suppress console logging |
| `--skip` | Skip frills/animations (faster) |
| `--v` | Verbose; `--debug` developer output |
| `--format <json|yaml>` | Output format (default json) |
| `--path <dir>` | Where to perform the operation |
| `--root <dir>` | Run the command as if from this directory |
| `--to-file <file>` | Redirect command output to a file |
| `--no-extras` | Skip automatic extra processing |
| `--npm-client <npm|yarn|pnpm>` | Package manager (default npm) |
| `--org <org>` / `--author <name>` | package.json / site metadata |

**For automation, prefer `--y --no-i` (optionally `--quiet`).** Without them, the
CLI may open interactive Clack prompts that stall a non-interactive session.

## Create a web component

```bash
hax webcomponent my-element --y                    # Lit + DDDSuper + i18n, defaults
hax webcomponent my-card --writeHaxProperties --y  # also emit haxProperties
```

- The name **must be hyphenated** (`my-element`, never `myElement`).
- LitElement-based, extends `DDDSuper` (the DDD design system), i18n-wired.
- In a **monorepo root**, the component is placed in the correct location and
  inherits settings — run from the repo root in that case.
- After creation: `cd my-element && npm install && npm start` to develop.
- `--writeHaxProperties` generates the schema that lets the component plug into
  the HAX authoring UI.

## Create a HAXsite

```bash
hax site mysite --y                                  # default theme
hax site mysite --theme "polaris-flex-theme" --y     # pick a theme
hax site mysite --skeleton-machine-name clean-one --y  # from an installed skeleton
hax site mysite --skeleton-file ./template.json --y    # from a local skeleton file
```

Custom theme starting point:

```bash
hax site mysite --theme "custom-theme" \
  --custom-theme-name "my-theme" \
  --custom-theme-template "base" --y      # templates: base | polaris-flex | polaris-sidebar
```

A HAXsite is a portable HAXcms site: `site.json` (JSON Outline Schema), `pages/`
content, `files/` assets, optional `theme/`. Preview with `hax serve` from the
site root.

## Work with an existing HAXsite

Run site sub-commands from inside the site folder, or target it with
`--root ./mysite`. As an agent, add `--agent` to every `hax site` command (or set
`HAX_ACTOR=agent`); the examples below that change a site include it. A person running them by hand
can leave it off.

### Content / node operations

Pages are always created, edited and deleted through the CLI, never by hand-editing `site.json` or
`pages/`. As an agent, add `--agent` to every `hax site` command (or set `HAX_ACTOR=agent`) so the
site history records your changes as agent changes. Pass values as `--flag=value`; a value that
starts with `-` must use that form.

```bash
# Add a page (the output includes the new item id)
hax site node:add --title="My summer vacation" \
  --content="<p>An awesome blog post.</p>" --y --no-i --agent

# Edit a page by id or slug: any field flags, applied together
hax site node:edit --item-id=<id> --title="New title" --y --no-i --agent
hax site node:edit --item-id=<id> --content="<p>New content</p>" --y --no-i --agent
hax site node:edit --item-id=<id> --parent=<parent-id> --y --no-i --agent   # move under a page
hax site node:edit --item-id=<id> --parent=null --y --no-i --agent          # move to the top level

# Delete a page (--y skips the confirmation)
hax site node:delete --item-id=<id> --y --no-i --agent

# Change the whole site's theme
hax site site:theme --theme=clean-two --y --no-i --agent

hax site node:stats                       # interactive node inspector
```

`node:edit` runs the same HAXcms operations as the site API, so it leaves `site.json` as the same
edit through the API or the HAX editor would. Field flags:

| Flag | What it changes |
|------|-----------------|
| `--title=<text>` | Title (the slug follows it unless the slug was set by hand) |
| `--slug=<path>` | Slug, marked as set by hand |
| `--content=<file, URL or HTML>` | Page body; description and reading time are regenerated (see below for how the input is detected) |
| `--description=<text>` | Description |
| `--tags=<a,b>` | Tags |
| `--published=true\|false` | Published state |
| `--hide-in-menu=true\|false` | Hidden from the menu |
| `--parent=<id-or-slug>` / `--parent=null` | Parent page; `null` is the top level |
| `--order=<number>` | Position among its siblings |
| `--theme=<theme>` | Theme for this page only |

**Order rule:** whenever `--parent` is given and no `--order`, the page goes after the last of its
siblings (highest order + 1, same as the API). This holds for `node:add` and `node:edit`. Pass
`--order` to place it yourself.

Interactive `--node-op` (without field flags) picks one field to edit: `title`, `content`, `slug`,
`published`, `tags`, `parent`, `order`, `theme` or `hideInMenu`. `description` is a flag, not a
node-op.

`--content` takes a file path, a URL or inline HTML. How the CLI tells them apart, and how to set
the format (`--content-format`), is documented in the `hax-site-building` skill (linked below);
follow it rather than guessing.

Page-creation flags for `node:add`: `--title`, `--content`, `--slug`, `--description`,
`--published`, `--tags`, `--parent`, `--order`, `--theme`, `--hide-in-menu`.

Full, version-matched docs: the `hax-site-building` skill
(https://github.com/haxtheweb/create/blob/main/src/skills/hax-site-building/SKILL.md, installed by
`hax skills install --all`) and `hax site --help`.

### Site operations

```bash
hax site site:stats                                  # site stats
hax site site:items --to-file export-items.json      # list nodes -> file
hax site site:items-import --items-import items.json --y --no-i --agent  # import nodes
hax site site:list-files                             # uploaded files
hax site site:search --search "lesson"               # full-text search
hax site site:search --search "video-player[src]" --search-selector  # HTML selector search
hax site site:theme --theme=clean-two --y --no-i --agent  # change theme
hax site site:html   --to-file output.html           # export site as HTML
hax site site:md     --to-file output.md             # export site as Markdown
hax site site:schema --to-file schema.json           # export HAXSchema (vdom)
hax site site:sync                                    # git sync (if remote configured)
```

### Skeleton templates (reusable site blueprints)

```bash
hax site site:skeleton-export --to-file ./template.json     # export current site
hax site site:skeleton-install                              # install current site as skeleton
hax site site:skeleton-install --skeleton-file ./template.json \
  --skeleton-machine-name course-template                  # install from file, rename
```

### Recipes

```bash
hax site recipe:read                          # print the recipe used to build the site
hax site recipe:play --recipe my.recipe --y --no-i --agent  # replay a recipe (scripted)
```

## Import & migrate content

```bash
hax site --import-site https://example.com --import-structure htmlToSite
```

`--import-structure` options: `pressbooksToSite`, `elmslnToSite`, `haxcmsToSite`,
`notionToSite`, `gitbookToSite`, `evolutionToSite`, `ploneToSite`,
`wordpressPagesToSite`, `drupalBookToSite`, `htmlToSite`, `docxToSite`. Tune
scraping with `--title-scrape` / `--content-scrape` (CSS selectors). Validate
source URLs before importing untrusted content.

## Serve locally

```bash
hax serve            # serves the HAXsite in the current dir at http://localhost
```

`hax serve` is **long-running** — start it in the background so the session stays
responsive, then report the local URL.

## Publish / deploy a HAXsite

Run from the site root (or pass `--root ./mysite`). Deploying is outward-facing.
**Always stop and get an explicit confirmation in its own turn before running any
`site:surge`, `site:netlify` or `site:vercel` command** — state the host and the
exact domain/project, then wait for the user to answer. Earlier phrasing such as
"publish it", "--y", or a target named in the original request does not count as
that confirmation; only a reply to the confirmation question does.

```bash
hax site site:surge   --domain my-blog.surge.sh      # surge.sh
hax site site:netlify --y                            # Netlify (or --domain <site-id>)
hax site site:vercel  --y                            # Vercel  (or --domain <project>)
hax site setup:github-actions                        # CI: deploy on git push (GH Pages)
hax site setup:gitlab-ci                             # CI: deploy on git push (GitLab)
```

## Audit components for DDD compliance

```bash
hax audit            # run from a component's root
hax --debug audit    # also print gathered .dddignore contents
```

- Audits CSS/structure against the **DDD** design system and suggests token-based
  fixes. Honors a `.dddignore` file (each generated component ships with one).
- **Required** before submitting theme components or PRs.
- Do **not** hand-edit auto-generated files like `custom-elements.json` — run the
  project build (`npm run build` / `yarn run build`) to regenerate them.

## Agent skills management

```bash
hax skills list                  # list bundled agent skills
hax skills install --all         # install all bundled skills into ~/.agents/skills/
hax skills install <name>        # install a specific skill
```

Bundled interface skills (version-locked to the CLI, shipped via npm in
`dist/skills/`): `hax-site-building`, `hax-claudehax`, `hax-webcomponent-dev`,
`hax-ecosystem-onboarding`, `hax-webcomponent-documentation-writer`.

## HAX conventions (important when editing generated code)

- **JavaScript only — no TypeScript.** HAX ships unbundled JS/HTML/CSS with no
  compile step. If you use a TS-authored library, import its prebuilt JS dist
  (e.g. `@vaadin/<c>/<c>.js`, `@shoelace-style/shoelace/dist/components/...`).
- Use `globalThis`, single quotes, ES modules; prefer functional patterns.
- **No optional chaining (`?.`)** — the Polymer parser has issues with this syntax.
- Components extend `DDDSuper`; HAXcms **themes** extend `HAXCMSLitElement`. After
  editing a theme, rebuild to regenerate `custom-elements.json`.
- Use DDD design tokens (CSS custom properties) for color/spacing/typography
  instead of hardcoded values.
- Web component & package names are hyphenated and should match.

## Typical workflows

- **New component:** `hax webcomponent my-thing --writeHaxProperties --y` → `cd` →
  `npm install` → `npm start` → edit → `hax audit`.
- **New site:** `hax site mysite --y` → `cd mysite` → `hax serve` → add pages with
  `hax site node:add ... --y --no-i --agent` → publish with `hax site site:vercel --y`.
- **Migrate a site:** `hax site newsite --import-site <url> --import-structure
  <method> --y` → review → `hax serve`.

When unsure of an exact flag for the installed version, run the relevant
`hax <command> --help` first and adapt.
