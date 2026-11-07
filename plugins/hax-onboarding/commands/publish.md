---
description: Publish a HAXsite (surge / Netlify / Vercel) or set up CI deploy with the HAX CLI.
argument-hint: "[surge|netlify|vercel|github-actions|gitlab-ci] [--domain <name>] [--y]"
allowed-tools: Bash(hax:*), Bash(cd:*), Read
---

Publish or set up deployment for a HAXsite with the HAX CLI. Run from the site root (or pass
`--root ./<site>`).

User input: `$ARGUMENTS`

Targets:
- surge.sh: `hax site site:surge` (or `--domain my-site.surge.sh`)
- Netlify: `hax site site:netlify --y` (or `--domain <site-id>`)
- Vercel: `hax site site:vercel --y` (or `--domain <project-name>`)
- GitHub Actions (deploy on push): `hax site setup:github-actions`
- GitLab CI (deploy on push): `hax site setup:gitlab-ci`
- Sync the site's git remote: `hax site site:sync`

Guidance:
- Pick the target from the input; if it's ambiguous, ask which host.
- Publishing to a third-party host is **outward-facing**. Before running any `site:surge`,
  `site:netlify` or `site:vercel` command, stop and ask for an explicit confirmation in its
  own turn: name the host and the exact domain/project, then wait for the user's answer.
  This applies regardless of prior phrasing — a target or `--y` in `$ARGUMENTS`, or
  "publish it" in the original request, selects the target but is not the confirmation.
- Only after the user confirms, run the command (add `--y` so the CLI itself does not prompt).
- `setup:github-actions`, `setup:gitlab-ci` and `site:sync` write config or push to the site's
  own git remote; describe what they will do before running them.

Run the appropriate command and report the resulting URL or next steps.
