# HAX Ecosystem Agent Skills

Reusable agent skills for the HAX (Headless Authoring eXperience) ecosystem. These skills encode HAX-specific conventions, design systems, and workflows so any compatible AI agent can work effectively within the HAX ecosystem without starting from scratch.

## Available Skills

| Skill | Description | Install |
|-------|-------------|---------|
| `hax-webcomponent-dev` | Develop HAX-capable web components with LitElement, DDD, and HAXSchema | `npx skills add haxtheweb/praw --skill hax-webcomponent-dev` |
| `hax-site-building` | Build and maintain HAXcms sites with JSON Outline Schema and themes | `npx skills add haxtheweb/praw --skill hax-site-building` |
| `hax-design-system` | Apply the DDD design system and manage SimpleColors legacy usage | `npx skills add haxtheweb/praw --skill hax-design-system` |
| `hax-ecosystem-onboarding` | Onboard new developers to the HAX ecosystem | `npx skills add haxtheweb/praw --skill hax-ecosystem-onboarding` |
| `hax-rule-management` | Manage PRAW rules and conventions stored in RULES.md | `npx skills add haxtheweb/praw --skill hax-rule-management` |
| `hax-issue-analysis` | Fetch, analyze, and summarize GitHub issues across the HAX ecosystem | `npx skills add haxtheweb/praw --skill hax-issue-analysis` |
| `hax-claudehax` | Operate HAX sites via the ClaudeHAX plugin in Claude Code | `npx skills add haxtheweb/praw --skill hax-claudehax` |

## Install All Skills

```bash
npx skills add haxtheweb/praw --all
```

## What Are Agent Skills?

Agent skills are portable, versioned instruction packages that any compatible AI agent (Claude Code, Cursor, GitHub Copilot, Codex, etc.) can load and use. They follow the open [Agent Skills standard](https://agentskills.io/) and are distributed via [skills.sh](https://skills.sh).

Each skill is a folder containing a `SKILL.md` file with YAML frontmatter and structured instructions. The agent reads the description to decide when to activate the skill, then loads the full instructions only when needed.

## HAX Ecosystem Context

The HAX ecosystem consists of multiple interconnected repositories:

- **`webcomponents`** — 250+ LitElement-based web components, themes, and the DDD design system
- **`create` (@haxtheweb/create)** — HAX CLI for scaffolding and workflow management
- **`haxcms-php` / `haxcms-nodejs`** — Content management backends
- **`desktop`** — Electron-based local development environment
- **`docs`** — Official HAX documentation
- **`issues`** — Unified issue tracking

These skills encode years of ecosystem knowledge so AI agents can work productively without requiring the user to explain HAX conventions every session.

## Contributing

To add a new skill or update an existing one:

1. Create or edit the skill directory under `skills/`
2. Ensure `SKILL.md` has valid YAML frontmatter with `name`, `description`, and `version`
3. Follow the [Agent Skills specification](https://agentskills.io/) for structure
4. Keep `SKILL.md` body focused and under 2KB — move deep reference material to `references/` or `scripts/`
5. Test locally with `npx skills add ./skills/<skill-name>` before committing

## License

Apache-2.0
