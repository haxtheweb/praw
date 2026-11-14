# Publishing Guide: HAX Ecosystem Skills to skills.sh

This guide outlines the exact steps to publish the PRAW skills to the skills.sh marketplace so they are discoverable and installable by any compatible AI agent.

## Prerequisites

- Node.js >= 18
- Git
- GitHub CLI (`gh`) — optional but helpful
- A public GitHub repository for the PRAW project (already exists: `haxtheweb/praw`)

## Understanding skills.sh

skills.sh is an open agent skills directory operated by Vercel Labs. There is **no formal submission or approval queue**. Skills appear automatically via install telemetry once the repo is public and someone installs the skill.

Key points:
- Skills are discovered from **public GitHub repositories**
- The install command is `npx skills add <owner/repo> --skill <skill-name>`
- Install counts aggregate across all agent platforms (Claude Code, Cursor, Codex, etc.)
- The directory updates within minutes of the first install

## Step-by-Step Publishing

### Step 1: Verify Skill Structure

Ensure each skill directory has the required structure:

```
skills/
├── <skill-name>/
│   ├── SKILL.md          ← required
│   └── scripts/          ← optional
└── README.md             ← human documentation, one row per skill
```

Each `SKILL.md` must have:
- YAML frontmatter with `name`, `description`, and `version`
- `name` must match the directory name (kebab-case, lowercase)
- `description` must say what the skill does AND when to use it (this is the routing trigger)
- Markdown body with instructions the agent follows

### Step 2: Validate Locally

Test each skill locally before publishing:

```bash
# From the PRAW repository root, for each skill you changed
npx skills add ./skills/<skill-name>
```

Verify:
- The skill installs without errors
- The `SKILL.md` frontmatter is parsed correctly
- The description is clear and would trigger on relevant prompts

### Step 3: Commit and Push to GitHub

```bash
node scripts/build-agent-skills-index.js   # refreshes the .well-known/agent-skills discovery index
git add skills/ .well-known/agent-skills/ llms.txt
git commit -m "feat: add <skill-name> skill"
```

Open a pull request; skills reach `main` through review like everything else.

### Step 4: Trigger skills.sh Discovery

The fastest way to get listed on skills.sh is to run the first install yourself. This triggers the install telemetry that indexes the skill.

Install from a fresh project directory (not the PRAW repo itself):

```bash
mkdir skill-test && cd skill-test

npx skills add haxtheweb/praw --skill <skill-name>   # one skill
npx skills add haxtheweb/praw --all                  # or all of them
```

This will:
1. Clone the `haxtheweb/praw` repo
2. Extract the requested skill(s)
3. Register them with the local agent runtime
4. Send install telemetry to skills.sh

### Step 5: Verify on skills.sh

Wait 2–5 minutes, then browse:

https://skills.sh

Search for your skills by name. They should appear with:
- Name matching the `name` field in frontmatter
- Description matching the `description` field
- Install count reflecting your test installs

If they don't appear immediately, check:
- The repo is public (not private)
- `SKILL.md` files are in the expected paths
- Frontmatter is valid YAML with required fields
- `name` fields match directory names exactly

### Step 6: Share Install Commands

Once verified, share the install commands with the HAX community:

```bash
npx skills add haxtheweb/praw --all
npx skills add haxtheweb/praw --skill <skill-name>
```

The per-skill commands are kept in [`README.md`](README.md) in this folder.

## Maintenance and Updates

### Versioning

Update the `version` field in `SKILL.md` frontmatter when making changes:

- **MAJOR** (x.0.0) — Breaking changes to skill structure or instructions
- **MINOR** (0.x.0) — New capabilities, patterns, or coverage
- **PATCH** (0.0.x) — Corrections, clarifications, or bug fixes

### Publishing Updates

skills.sh does not have a separate update mechanism. It pulls from the repo dynamically. To push an update:

1. Update the `SKILL.md` file(s)
2. Bump the `version` in frontmatter
3. Commit and push to `main`
4. Users running `npx skills update` will get the latest version automatically

### Pinning to Versions

Users can install a specific version by pinning to a git tag or commit:

```bash
npx skills add haxtheweb/praw --skill hax-webcomponent-dev@v1.0.0
```

Create git tags for releases:

```bash
git tag skills-v1.0.0
git push origin skills-v1.0.0
```

## Troubleshooting

### Skill not appearing on skills.sh

- Verify the repo is public
- Check that `SKILL.md` has valid YAML frontmatter (use a YAML linter)
- Ensure `name` matches the directory name exactly (kebab-case, lowercase)
- Ensure description is non-empty and under 1024 characters
- Try installing from a different machine/network to trigger telemetry

### Install fails locally

- Check Node.js version: `node --version` (need >= 18)
- Check `npx` is available: `which npx`
- Verify the repo URL is correct: `https://github.com/haxtheweb/praw`
- Check for typos in `--skill` argument (must match directory name)

### Description not triggering skill activation

The `description` field is the routing signal. If the skill never activates, rewrite the description to be more explicit about triggers:

```yaml
# Bad
description: Helps with web components.

# Good
description: >
  Develop HAX-capable web components using LitElement, DDD, and HAXSchema.
  Use when scaffolding new components, adding HAX editor support, or auditing
  accessibility in the webcomponents monorepo.
```

## Additional Distribution Channels

Beyond skills.sh, you can distribute skills through:

- **npm/skillpm** — Add a `package.json` to the skill root and publish to npm
- **GitHub releases** — Tag releases and point users to specific versions
- **llms.txt** — Already configured at repo root for agent discovery
- **.well-known/agent-skills/** — Already configured for automated agent discovery

## Resources

- [Agent Skills Standard](https://agentskills.io/)
- [skills.sh Directory](https://skills.sh)
- [Vercel Skills CLI](https://github.com/vercel-labs/skills)
- [SKILL.md Format Guide](https://www.creative-tim.com/blog/ai-agent/what-are-ai-agent-skills-a-practical-guide-to-skillmd)
