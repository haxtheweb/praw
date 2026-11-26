#!/usr/bin/env python3
"""Mechanical checks for PRAW rules that nothing enforced yet (haxtheweb/issues#3295).

  python3 scripts/rule-checks.py mascot        Mascot Name: the Future Traveler (RULES.md 7d6f9c3e-...)
  python3 scripts/rule-checks.py local-paths   Cross-Repo References: No Local Paths (RULES.md bAKMWCMrqRLGdWmuNWgVUw)
  python3 scripts/rule-checks.py org-name      GitHub org spelling: links and package scopes say haxtheweb, not a near-miss
  python3 scripts/rule-checks.py skill-evals [--base REF]
                                               Rules and Skills Earn Their Tokens (RULES.md 09255ba6-...): every
                                               skills/*/evals/evals.json case records expected_output and
                                               baseline_behavior; with --base, a skill whose SKILL.md is new or
                                               changed by SUBSTANTIAL lines or more ships evals/evals.json
  python3 scripts/rule-checks.py self-test     the checks catch what they should and skip what they should

Each check reads the files git tracks, prints file:line for every hit and exits 1 when there is one.
Standard library only, so it runs anywhere Python 3 does.
"""
import difflib
import re
import subprocess
import sys

BINARY = re.compile(r"\.(png|jpe?g|gif|webp|ico|pdf|mp3|mp4|webm|woff2?|ttf|eot|zip|gz|csv)$", re.I)

# ---------- Mascot Name: the Future Traveler ----------
# The retired names, as words. "world-traveler" as a folder (art/world-traveler/) or as the retired icon
# names (hax:world-traveler, hax:world-traveler-plain) is allowed: the rule keeps those so old content draws.
RETIRED_NAME = re.compile(r"\bworld[ -]?(traveler|changer)s?\b", re.I)
ALLOWED_NAME_USE = [
    re.compile(r"hax:world-traveler(-plain)?\b", re.I),  # retired icon names kept in the iconset
    re.compile(r"world-traveler/", re.I),  # the art folder name
    re.compile(r"\"[^\"]*/[^\"]*world[ -]?(traveler|changer)[^\"]*\.(png|jpe?g|gif|svg|webp)\"", re.I),  # an uploaded file's name
]
# Files that state the rule (and quote the retired names to retire them), and files generated from RULES.md.
MASCOT_SKIP = [
    re.compile(r"^RULES\.md$"),
    re.compile(r"^exports/"),
    re.compile(r"^ecosystem/web/hax-rules\.json$"),
    re.compile(r"^scripts/rule-checks\.py$"),
]

# ---------- Cross-Repo References: No Local Paths ----------
# A path on one person's machine: a home folder or a checkout under it.
LOCAL_PATH = re.compile(
    r"(/Users/[A-Za-z0-9._-]+/|/home/(?!runner/)[a-z][a-z0-9._-]*/|~/Documents/git\b|~/git/|~/haxtheweb/|[A-Za-z]:\\Users\\)"
)
# Where the rule applies: rules, skills, agent instructions, docs and the ecosystem web. Not data snapshots of
# other repos' scripts (ecosystem/build/data/), which are copied as they are.
LOCAL_PATH_SCOPE = re.compile(r"(^skills/|^ecosystem/|^plugins/|\.md$|(^|/)(AGENTS|WARP|CLAUDE)\.md$)", re.I)
LOCAL_PATH_SKIP = [
    re.compile(r"^ecosystem/build/data/"),
    re.compile(r"^scripts/rule-checks\.py$"),
]

# ---------- GitHub org spelling ----------
# A near-miss of the org name (haxtheweeb, haxthweb, hax-the-web...) in a GitHub, raw or Pages URL or an npm
# scope gives a dead link or a missing package. Other orgs and scopes (lit, ossf, cloudflare...) are not
# near-misses and are left alone.
ORG = "haxtheweb"
ORG_REFS = [
    re.compile(r"(?:github\.com|githubusercontent\.com)/([A-Za-z0-9_.-]+)", re.I),
    re.compile(r"(?<![\w.])@([A-Za-z0-9_.-]+)/"),
    re.compile(r"\b([A-Za-z0-9-]+)\.github\.io\b", re.I),
]
ORG_NAME_SKIP = [
    re.compile(r"^scripts/rule-checks\.py$"),
]


def tracked_files():
    out = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True).stdout
    return [f for f in out.splitlines() if f and not BINARY.search(f)]


def read_lines(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read().splitlines()
    except (UnicodeDecodeError, OSError):
        return []


def mascot_hits_in_line(line):
    scrubbed = line
    for allowed in ALLOWED_NAME_USE:
        scrubbed = allowed.sub("", scrubbed)
    return RETIRED_NAME.findall(scrubbed)


def local_path_hits_in_line(line):
    return LOCAL_PATH.findall(line)


def org_name_hits_in_line(line):
    hits = []
    for rx in ORG_REFS:
        for name in rx.findall(line):
            lowered = name.lower()
            if lowered == ORG:
                continue
            if difflib.SequenceMatcher(None, lowered, ORG).ratio() >= 0.8:
                hits.append(name)
    return hits


def check(name, files, skip, scope, hit_fn, message):
    problems = []
    for path in files:
        if any(rx.search(path) for rx in skip):
            continue
        if scope is not None and not scope.search(path):
            continue
        for number, line in enumerate(read_lines(path), 1):
            if hit_fn(line):
                problems.append(f"{path}:{number}: {line.strip()[:160]}")
    if problems:
        print(f"{name}: {len(problems)} problem(s). {message}")
        for p in problems:
            print("  " + p)
        return 1
    print(f"{name}: OK")
    return 0


def run_mascot(files):
    return check(
        "Mascot name",
        files,
        MASCOT_SKIP,
        None,
        mascot_hits_in_line,
        "HAX's mascot is the Future Traveler; World Traveler / World Changer are retired names (RULES.md, Mascot Name).",
    )


def run_local_paths(files):
    return check(
        "No local paths",
        files,
        LOCAL_PATH_SKIP,
        LOCAL_PATH_SCOPE,
        local_path_hits_in_line,
        "Refer to other HAX repos by their GitHub URL, never a path on someone's machine (RULES.md, Cross-Repo References).",
    )


def run_org_name(files):
    return check(
        "GitHub org spelling",
        files,
        ORG_NAME_SKIP,
        None,
        org_name_hits_in_line,
        "The GitHub org and npm scope are spelled haxtheweb; a near-miss is a dead link or a missing package.",
    )


# ---------- Rules and Skills Earn Their Tokens ----------
SUBSTANTIAL = 20  # added + removed SKILL.md lines that make a change "substantial"


def eval_case_problems(case):
    """What an eval case is missing: the fields that say whether the skill changes what an agent does."""
    return [k for k in ("prompt", "expected_output", "baseline_behavior") if not str(case.get(k, "")).strip()]


def evals_problems(path, text):
    import json

    try:
        data = json.loads(text)
    except ValueError as e:
        return [f"{path}: not valid JSON ({e})"]
    cases = data.get("evals") if isinstance(data, dict) else data
    if not isinstance(cases, list) or not cases:
        return [f"{path}: no eval cases (an \"evals\" list)"]
    out = []
    for i, case in enumerate(cases):
        missing = eval_case_problems(case) if isinstance(case, dict) else ["prompt", "expected_output", "baseline_behavior"]
        if missing:
            out.append(f"{path}: case {case.get('id', i + 1) if isinstance(case, dict) else i + 1} has no {', '.join(missing)}")
    return out


def changed_lines(base, path):
    """Lines added plus removed in path since base (all of it when the file is new)."""
    out = subprocess.run(["git", "diff", "--numstat", base, "--", path], capture_output=True, text=True).stdout.split()
    if len(out) >= 2 and out[0].isdigit() and out[1].isdigit():
        return int(out[0]) + int(out[1])
    return 0


def run_skill_evals(files, base=None):
    hits = []
    evals = [f for f in files if re.match(r"^skills/[^/]+/evals/evals\.json$", f)]
    for f in evals:
        with open(f, encoding="utf-8") as fh:
            hits += evals_problems(f, fh.read())
    if base:
        merge_base = subprocess.run(["git", "merge-base", base, "HEAD"], capture_output=True, text=True).stdout.strip() or base
        for f in files:
            m = re.match(r"^skills/([^/]+)/SKILL\.md$", f)
            if not m:
                continue
            n = changed_lines(merge_base, f)
            if n >= SUBSTANTIAL and f"skills/{m.group(1)}/evals/evals.json" not in evals:
                hits.append(f"{f}: {n} lines changed since {base} and the skill ships no evals/evals.json; add cases with expected_output and baseline_behavior (RULES.md 09255ba6, Rules and Skills Earn Their Tokens)")
    for h in hits:
        print(h)
    print(f"skill-evals: {'OK' if not hits else str(len(hits)) + ' problem(s)'} ({len(evals)} eval files)")
    return 1 if hits else 0


def self_test():
    cases = [
        (mascot_hits_in_line, "Meet the World Traveler!", True),
        (mascot_hits_in_line, "our world changer mascot", True),
        (mascot_hits_in_line, "The Future Traveler says hi", False),
        (mascot_hits_in_line, 'icon="hax:world-traveler-plain"', False),
        (mascot_hits_in_line, "art/world-traveler/wave.png", False),
        (mascot_hits_in_line, '<img src="files/HAX.psu World changer-circle1.png">', False),
        (mascot_hits_in_line, "travel the world, traveler", False),
        (local_path_hits_in_line, "cd ~/Documents/git/haxtheweb/webcomponents", True),
        (local_path_hits_in_line, "see /Users/someone/haxtheweb/praw/RULES.md", True),
        (local_path_hits_in_line, "open /home/someone/haxtheweb/create", True),
        (local_path_hits_in_line, "C:\\Users\\someone\\haxtheweb", True),
        (local_path_hits_in_line, "runs in /home/runner/work/praw", False),
        (local_path_hits_in_line, "https://github.com/haxtheweb/praw/blob/main/RULES.md", False),
        (local_path_hits_in_line, "cd webcomponents  # your own clone", False),
        (org_name_hits_in_line, "https://github.com/haxtheweeb/issues/issues/1", True),
        (org_name_hits_in_line, "https://github.com/haxthweb/praw", True),
        (org_name_hits_in_line, "import '@haxthewb/d-d-d/d-d-d.js'", True),
        (org_name_hits_in_line, "https://haxtheweeb.github.io/", True),
        (org_name_hits_in_line, "https://raw.githubusercontent.com/hax-the-web/praw/main/llms.txt", True),
        (org_name_hits_in_line, "https://github.com/haxtheweb/praw/blob/main/RULES.md", False),
        (org_name_hits_in_line, "https://github.com/HAXTheWeb/webcomponents", False),
        (org_name_hits_in_line, "import '@haxtheweb/d-d-d/d-d-d.js'", False),
        (org_name_hits_in_line, "https://github.com/ossf/scorecard and @lit/reactive-element", False),
        (org_name_hits_in_line, "https://github.com/haxcms/haxcms and contact hax@psu.edu/", False),
    ]
    good = '{"evals": [{"id": 1, "prompt": "p", "expected_output": "e", "baseline_behavior": "b"}]}'
    cases += [
        (lambda t: evals_problems("x.json", t), good, False),
        (lambda t: evals_problems("x.json", t), '{"evals": [{"id": 1, "prompt": "p", "expected_output": "e"}]}', True),
        (lambda t: evals_problems("x.json", t), '{"evals": []}', True),
        (lambda t: evals_problems("x.json", t), "not json", True),
    ]
    failed = 0
    for fn, text, expect in cases:
        got = bool(fn(text))
        if got != expect:
            failed += 1
            print(f"FAIL {getattr(fn, '__name__', 'check')}({text!r}) -> {got}, expected {expect}")
    print("self-test: " + ("OK" if not failed else f"{failed} failed"))
    return 1 if failed else 0


def main(argv):
    if argv[1:2] == ["skill-evals"]:
        base = argv[argv.index("--base") + 1] if "--base" in argv and argv.index("--base") + 1 < len(argv) else None
        return run_skill_evals(tracked_files(), base)
    if len(argv) != 2 or argv[1] not in ("mascot", "local-paths", "org-name", "self-test"):
        print(__doc__)
        return 2
    if argv[1] == "self-test":
        return self_test()
    files = tracked_files()
    runners = {"mascot": run_mascot, "local-paths": run_local_paths, "org-name": run_org_name}
    return runners[argv[1]](files)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
