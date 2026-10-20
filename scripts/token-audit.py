#!/usr/bin/env python3
"""Token audit for PRAW agent-facing context (issue haxtheweb/issues#3136).

Measures what an agent pays before it does any work:

  A. Landing cost     - PRAW WARP.md files plus each repo's AGENTS.md
  B. Global rules     - the always-on block built from exports/rules-global.json
  C. Skill index      - skill descriptions from .well-known/agent-skills/index.json
  D. Targets          - pass/fail against the goals in #3136

Nothing here depends on a local checkout layout. PRAW files are resolved
relative to this script. Other repos' AGENTS.md files are fetched from their
public GitHub URLs by default, so the audit runs the same in a cloud agent,
CI, or a laptop. Use --local-root only to audit unpushed edits.

Tokenizer: tiktoken `o200k_base` when its vocabulary can be loaded. If the
vocabulary cannot be downloaded (offline or restricted network) the script
falls back to a bytes-per-token estimate and says so in the output. Set
TIKTOKEN_CACHE_DIR to a pre-seeded cache to stay exact offline.

Usage:
  python3 scripts/token-audit.py                 # public AGENTS.md via GitHub
  python3 scripts/token-audit.py --local-root .. # sibling checkouts (unpushed edits)
  python3 scripts/token-audit.py --json          # machine-readable output
  python3 scripts/token-audit.py --no-agents     # skip the network fetch

Exit code: 0 when every target is met, 1 otherwise (usable as a CI gate).
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

PRAW_ROOT = Path(__file__).resolve().parent.parent

# Public source for every repo that ships an AGENTS.md. Branch is the default
# branch of each repo.
AGENTS_REPOS = {
    "webcomponents": "master",
    "create": "main",
    "haxcms-php": "master",
    "haxcms-nodejs": "main",
    "hax11ty": "master",
}
RAW_URL = "https://raw.githubusercontent.com/haxtheweb/{repo}/{branch}/AGENTS.md"

# Targets from issue #3136.
TARGETS = {
    "always_on_total": 8000,
    "rules_block": 1500,
    "skill_index": 7000,
    "landing_agents_md": 3000,
    "landing_total": 5000,
    "skill_description": 80,
}

# Calibrated from the 2026-10-15 measurement in #3136: ~24 KB of AGENTS.md
# markdown measured ~5.9k o200k_base tokens.
BYTES_PER_TOKEN_ESTIMATE = 4.1


class Counter:
    def __init__(self):
        self.encoding = None
        self.exact = False
        try:
            import tiktoken  # type: ignore

            self.encoding = tiktoken.get_encoding("o200k_base")
            self.exact = True
        except Exception:
            pass

    @property
    def label(self):
        return "tiktoken o200k_base (exact)" if self.exact else (
            f"estimate: bytes/{BYTES_PER_TOKEN_ESTIMATE} (tiktoken vocabulary unavailable)"
        )

    def count(self, text):
        if self.exact:
            return len(self.encoding.encode(text, disallowed_special=()))
        return round(len(text.encode("utf-8")) / BYTES_PER_TOKEN_ESTIMATE)


def read(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        return None


def fetch(url):
    try:
        with urllib.request.urlopen(url, timeout=20) as resp:
            return resp.read().decode("utf-8")
    except Exception as exc:  # network failure is reported, not fatal
        return f"__FETCH_ERROR__ {exc}"


def ensure_rule_exports():
    exports = PRAW_ROOT / "exports" / "rules-global.json"
    if exports.exists():
        return True
    script = PRAW_ROOT / "scripts" / "build-rules.js"
    if not script.exists():
        return False
    subprocess.run(["node", str(script)], cwd=PRAW_ROOT, capture_output=True)
    return exports.exists()


def audit_landing(counter, args):
    praw_files = {}
    for rel in ["WARP.md", "webcomponents/WARP.md", "haxcms/WARP.md", "design-system/WARP.md"]:
        text = read(PRAW_ROOT / rel)
        if text is not None:
            praw_files[f"praw/{rel}"] = counter.count(text)

    agents = {}
    if not args.no_agents:
        for repo, branch in AGENTS_REPOS.items():
            if args.local_root:
                text = read(Path(args.local_root) / repo / "AGENTS.md")
            else:
                text = fetch(RAW_URL.format(repo=repo, branch=branch))
            if text is None or text.startswith("__FETCH_ERROR__"):
                agents[repo] = None
            else:
                agents[repo] = counter.count(text)
    return praw_files, agents


def audit_rules(counter):
    if not ensure_rule_exports():
        return None
    data = json.loads(read(PRAW_ROOT / "exports" / "rules-global.json"))
    rules = data["rules"] if isinstance(data, dict) else data
    per_rule = [(r["id"][:8], r.get("title", ""), counter.count(r["content"])) for r in rules]
    block = "\n".join(f"- {r['content']}" for r in rules)
    return {"count": len(rules), "tokens": counter.count(block), "per_rule": per_rule}


def audit_skills(counter):
    data = json.loads(read(PRAW_ROOT / ".well-known" / "agent-skills" / "index.json"))
    skills = data["skills"]
    rows = []
    for s in skills:
        entry = f"{s['name']}: {s.get('description', '')}"
        rows.append((s["name"], counter.count(s.get("description", "")), counter.count(entry)))
    return {
        "count": len(rows),
        "tokens": sum(r[2] for r in rows),
        "over_limit": sorted(
            [(n, d) for n, d, _ in rows if d > TARGETS["skill_description"]],
            key=lambda x: -x[1],
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--local-root", help="Directory containing sibling repo checkouts; read AGENTS.md from there instead of GitHub")
    parser.add_argument("--no-agents", action="store_true", help="Skip AGENTS.md measurement (no network)")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    counter = Counter()
    landing_praw, landing_agents = audit_landing(counter, args)
    rules = audit_rules(counter)
    skills = audit_skills(counter)

    always_on = (rules["tokens"] if rules else 0) + skills["tokens"]
    agents_measured = {k: v for k, v in landing_agents.items() if v is not None}
    worst_landing = 0
    if agents_measured:
        praw_landing = landing_praw.get("praw/WARP.md", 0)
        worst_landing = praw_landing + max(agents_measured.values())

    checks = [
        ("Always-on total", always_on, TARGETS["always_on_total"]),
        ("  rules block", rules["tokens"] if rules else 0, TARGETS["rules_block"]),
        ("  skill index", skills["tokens"], TARGETS["skill_index"]),
    ]
    for repo, tokens in agents_measured.items():
        checks.append((f"AGENTS.md {repo}", tokens, TARGETS["landing_agents_md"]))
    if agents_measured:
        checks.append(("Landing cost (praw WARP.md + largest AGENTS.md)", worst_landing, TARGETS["landing_total"]))
    checks.append(("Skills over description limit", len(skills["over_limit"]), 0))

    if args.json:
        print(json.dumps({
            "tokenizer": counter.label,
            "landing_praw": landing_praw,
            "landing_agents": landing_agents,
            "rules": rules,
            "skills": skills,
            "checks": [{"name": n, "value": v, "target": t, "pass": v <= t} for n, v, t in checks],
        }, indent=2))
    else:
        print(f"Tokenizer: {counter.label}\n")
        print("A. Landing cost")
        for name, tokens in landing_praw.items():
            print(f"   {name:<36}{tokens:>7}")
        for repo, tokens in landing_agents.items():
            shown = "unavailable" if tokens is None else tokens
            print(f"   {repo + '/AGENTS.md':<36}{shown:>7}")
        if rules:
            print(f"\nB. Global rules block: {rules['count']} rules, {rules['tokens']} tokens")
        else:
            print("\nB. Global rules block: exports/rules-global.json missing (run node scripts/build-rules.js)")
        print(f"\nC. Skill index: {skills['count']} skills, {skills['tokens']} tokens")
        for name, tokens in skills["over_limit"][:15]:
            print(f"   over {TARGETS['skill_description']}: {name} ({tokens})")
        if len(skills["over_limit"]) > 15:
            print(f"   ... and {len(skills['over_limit']) - 15} more")
        print("\nD. Targets")
        for name, value, target in checks:
            status = "ok  " if value <= target else "OVER"
            print(f"   [{status}] {name:<52}{value:>7} / {target}")

    sys.exit(0 if all(v <= t for _, v, t in checks) else 1)


if __name__ == "__main__":
    main()
