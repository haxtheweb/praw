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
| `hax-openstax2hax` | Convert OpenStax books into HAX sites via the openstax2hax plugin | `npx skills add haxtheweb/praw --skill hax-openstax2hax` |
| `audio-program-transcribe` | Transcribe and distill an owned audio/video program into a portable markdown staging tree | `npx skills add haxtheweb/praw --skill audio-program-transcribe` |
| `audio-program-hax` | Publish a transcribed audio/video program as a searchable HAXcms library site with inline playback | `npx skills add haxtheweb/praw --skill audio-program-hax` |
| `hax-a11y-audit` | Read-only WCAG 2.0 AA audit of authored HAX pages with HAX remediation | `npx skills add haxtheweb/praw --skill hax-a11y-audit` |
| `hax-udl-audit` | Read-only UDL 3.0 audit (Engagement, Representation, Action & Expression) of a HAX page | `npx skills add haxtheweb/praw --skill hax-udl-audit` |
| `hax-content-chunking-audit` | Audit a HAX page for cognitive load / chunking and recommend HAX remediation | `npx skills add haxtheweb/praw --skill hax-content-chunking-audit` |
| `hax-ubd-unit-audit` | Read-only UbD review of an existing HAX unit with remediation handoff | `npx skills add haxtheweb/praw --skill hax-ubd-unit-audit` |
| `hax-issue-research` | Research a HAX GitHub issue, draft a plan, and capture it as a "Plan Created" comment | `npx skills add haxtheweb/praw --skill hax-issue-research` |
| `hax-ubd-backward-design` | Design HAX course units via UbD backward design; emits unit plan + HAX site skeleton | `npx skills add haxtheweb/praw --skill hax-ubd-backward-design` |
| `hax-ubd-stage1` | UbD Stage 1 — unpack standards into big ideas, understandings, EQs, K/S, misconceptions | `npx skills add haxtheweb/praw --skill hax-ubd-stage1` |
| `hax-ubd-stage2` | UbD Stage 2 — build evidence scrapbook, GRASPS task, facet rubric, validity self-test | `npx skills add haxtheweb/praw --skill hax-ubd-stage2` |
| `hax-ubd-stage3` | UbD Stage 3 — plan learning experiences via WHERETO from Stages 1+2 | `npx skills add haxtheweb/praw --skill hax-ubd-stage3` |
| `hax-ubd-essential-questions` | Author UbD essential and entry questions from the six-facet starter bank | `npx skills add haxtheweb/praw --skill hax-ubd-essential-questions` |
| `hax-ubd-grasps` | Frame UbD GRASPS performance tasks and pick authentic-context HAX media | `npx skills add haxtheweb/praw --skill hax-ubd-grasps` |
| `hax-ubd-six-facets` | Apply UbD six facets to write understandings and build facet-mapped rubric criteria | `npx skills add haxtheweb/praw --skill hax-ubd-six-facets` |
| `oerschema-audit` | Read-only OER Schema diagnostic of authored content (HAX pages, VitePress, JSON-LD, Docs export) with class/property/surface remediation | `npx skills add haxtheweb/praw --skill oerschema-audit` |
| `oerschema-integration-finder` | Read-only scan of webcomponents/themes/backends/plugins for code surfaces that should emit or consume OER Schema but don't | `npx skills add haxtheweb/praw --skill oerschema-integration-finder` |

## Install All Skills

```bash
npx skills add haxtheweb/praw --all
```

## Companion Document Skills (not bundled)

The Anthropic document skills — `docx`, `pdf`, `pptx`, `xlsx` — are **not bundled** in this repository. They are source-available (not open source) and governed by Anthropic's terms, so this repo does not redistribute them. Install them on your machine from Anthropic's official repo if you need document creation/editing capabilities:

```bash
# Install all four document skills globally (into ~/.agents/skills/)
npx skills add anthropics/skills --skill docx --skill pdf --skill pptx --skill xlsx -g -y

# Or install individually
npx skills add anthropics/skills@docx -g -y
npx skills add anthropics/skills@pdf -g -y
npx skills add anthropics/skills@pptx -g -y
npx skills add anthropics/skills@xlsx -g -y
```

Target a specific agent with `-a <agent>` (e.g. `-a warp`, `-a claude-code`); omit `-g` for a project-local install. Per Anthropic's README these skills are provided for demonstration/educational purposes — verify the license terms and your entitlement before relying on them.

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
