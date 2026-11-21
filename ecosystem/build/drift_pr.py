#!/usr/bin/env python3
"""The weekly drift run's two halves (.github/workflows/ecosystem-drift.yml, https://github.com/haxtheweb/issues/issues/3296).

  python3 -I drift_pr.py collect <folder>   after ecosystem/build/run.sh: copy what the generators changed under
                                            ecosystem/ into <folder>, with a manifest and the text of the proposal
  python3 -I drift_pr.py propose <folder>   put those files on the one rolling branch as a single commit on top
                                            of main, and open the pull request for it or update the one that is open

collect runs where the generators ran and needs no token. propose runs in a job of its own that holds the
write token and never runs a generator or anything the generators fetched: the folder is data, and every path
in it has to be a plain file under ecosystem/ or the run stops.

propose only ever writes one branch (ecosystem-web-drift) and one pull request. It doesn't merge, close or
delete anything; a person reviews and merges. Each run replaces the branch with one commit on the current main,
so the pull request always shows this week's drift against today's main. The commit is made through the GitHub
API without author details, so GitHub signs it as the workflow's own account.

Standard library only; propose calls the GitHub REST API through the gh CLI (GH_TOKEN, GITHUB_REPOSITORY,
GITHUB_SHA and BASE_BRANCH come from the workflow)."""
import base64, json, os, re, shutil, subprocess, sys

BRANCH = "ecosystem-web-drift"
TITLE = "Ecosystem web: weekly drift"
SAFE_PATH = re.compile(r"^ecosystem/(?:[A-Za-z0-9_][A-Za-z0-9._-]*/)*[A-Za-z0-9_][A-Za-z0-9._-]*$")
BODY_LIMIT = 60000  # GitHub's limit for a pull request body is 65536 characters
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def git(*args):
    return subprocess.run(["git", "-C", ROOT] + list(args), capture_output=True, text=True, check=True).stdout


def collect(out):
    """Copy what changed under ecosystem/ (tracked or new, never ignored files) into out/files and describe it."""
    changed, deleted = [], []
    status = git("status", "--porcelain", "-z", "--untracked-files=all", "--", "ecosystem")
    for entry in [e for e in status.split("\0") if e]:
        code, path = entry[:2], entry[3:]
        if not SAFE_PATH.match(path):
            sys.exit(f"drift: unexpected path in the working tree: {path!r}")
        if "R" in code or "C" in code:
            sys.exit(f"drift: unexpected rename in the working tree: {path!r}")
        full = os.path.join(ROOT, path)
        if "D" in code or not os.path.exists(full):
            deleted.append(path)
        elif os.path.isfile(full) and not os.path.islink(full):
            changed.append({"path": path, "mode": "100755" if os.access(full, os.X_OK) else "100644"})
            dest = os.path.join(out, "files", path)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copyfile(full, dest)
        else:
            sys.exit(f"drift: {path!r} is not a plain file")
    data = os.path.join(ROOT, "ecosystem", "build", "data")
    try:
        with open(os.path.join(data, "drift-report.md"), encoding="utf-8") as f:
            report = f.read()
        with open(os.path.join(data, "drift-report.json"), encoding="utf-8") as f:
            drift = bool(json.load(f).get("drift"))
    except (OSError, ValueError):
        report, drift = "The drift report was not written: the run stopped before ecosystem/build/drift.py finished.", True
    integrity = subprocess.run([sys.executable, "-I", os.path.join(ROOT, "ecosystem", "test", "integrity-check.py")],
                               capture_output=True, text=True, env={k: v for k, v in os.environ.items() if k != "GITHUB_ACTIONS"})
    check = integrity.stdout.strip()[-6000:]
    body = [
        "The weekly run of `ecosystem/build/run.sh`: every generator rerun against the latest source, so new CLI commands, endpoints, MCP tools, workflows, rules and the rest show up here for review.",
        "",
        f"- {len(changed)} files changed" + (f", {len(deleted)} removed" if deleted else "") + ".",
        "- Integrity check on the regenerated webs: " + ("passes." if integrity.returncode == 0 else "**fails** (below). Fix the source or the generator on `main` before merging."),
        "- Nothing here merges on its own. Each weekly run replaces this branch with one commit on the current `main`, so commit changes to `main`, not to this branch.",
        "- Pull requests opened by a workflow don't start other workflows. To run the page checks on this branch, start **Ecosystem web** and **hax.cloud** from the Actions tab with this branch selected.",
        "",
    ]
    if integrity.returncode != 0:
        body += ["## Integrity check", "", "```", check, "```", ""]
    room = BODY_LIMIT - len("\n".join(body)) - 200
    body.append(report if len(report) <= room else report[:room] + "\n\n(The report is longer than a pull request body holds; the workflow run's summary has all of it.)")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "body.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(body) + "\n")
    with open(os.path.join(out, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump({"changed": changed, "deleted": deleted, "drift": drift, "integrity": integrity.returncode == 0}, f, indent=1)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write(report + "\n\n## Integrity check\n\n```\n" + check + "\n```\n")
    print(f"drift: {len(changed)} changed, {len(deleted)} removed, drift {'found' if drift else 'not found'}, integrity {'passes' if integrity.returncode == 0 else 'fails'}")


def api(method, path, payload=None, missing_ok=False):
    """One GitHub REST call through gh. Returns the parsed answer, or None for a 404 when missing_ok."""
    cmd = ["gh", "api", "--method", method, "-H", "Accept: application/vnd.github+json", path]
    if payload is not None:
        cmd += ["--input", "-"]
    r = subprocess.run(cmd, input=json.dumps(payload) if payload is not None else None, capture_output=True, text=True)
    if r.returncode != 0:
        if missing_ok and "HTTP 404" in r.stderr:
            return None
        sys.exit(f"drift: {method} {path} failed: {r.stderr.strip()[-400:]}")
    return json.loads(r.stdout) if r.stdout.strip() else {}


def propose(folder):
    repo, base_sha, base = os.environ["GITHUB_REPOSITORY"], os.environ["GITHUB_SHA"], os.environ["BASE_BRANCH"]
    if not re.match(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$", repo) or not re.match(r"^[0-9a-f]{40}$", base_sha) or not re.match(r"^[A-Za-z0-9_./-]+$", base):
        sys.exit("drift: unexpected repository, commit or base branch")
    with open(os.path.join(folder, "manifest.json"), encoding="utf-8") as f:
        manifest = json.load(f)
    with open(os.path.join(folder, "body.md"), encoding="utf-8") as f:
        body = f.read()[:BODY_LIMIT + 2000]
    changed, deleted = manifest.get("changed") or [], manifest.get("deleted") or []
    if not changed and not deleted:
        print("drift: the generators changed no files; nothing to propose" + (" (the report still names drift: see the run summary)" if manifest.get("drift") else ""))
        return
    files = os.path.realpath(os.path.join(folder, "files"))
    tree = []
    for item in changed:
        path, mode = item.get("path"), item.get("mode")
        if not isinstance(path, str) or not SAFE_PATH.match(path) or mode not in ("100644", "100755"):
            sys.exit(f"drift: refusing the path {path!r}")
        full = os.path.realpath(os.path.join(files, path))
        if os.path.commonpath([files, full]) != files or not os.path.isfile(full):
            sys.exit(f"drift: {path!r} is not a file in the collected folder")
        with open(full, "rb") as f:
            blob = api("POST", f"repos/{repo}/git/blobs", {"content": base64.b64encode(f.read()).decode("ascii"), "encoding": "base64"})
        tree.append({"path": path, "mode": mode, "type": "blob", "sha": blob["sha"]})
    for path in deleted:
        if not isinstance(path, str) or not SAFE_PATH.match(path):
            sys.exit(f"drift: refusing the path {path!r}")
        tree.append({"path": path, "mode": "100644", "type": "blob", "sha": None})
    base_tree = api("GET", f"repos/{repo}/git/commits/{base_sha}")["tree"]["sha"]
    new_tree = api("POST", f"repos/{repo}/git/trees", {"base_tree": base_tree, "tree": tree})["sha"]
    if new_tree == base_tree:
        print("drift: the files match main already; nothing to propose")
        return
    ref = api("GET", f"repos/{repo}/git/ref/heads/{BRANCH}", missing_ok=True)
    head = api("GET", f"repos/{repo}/git/commits/{ref['object']['sha']}") if ref else None
    if head and head["tree"]["sha"] == new_tree and [p["sha"] for p in head["parents"]] == [base_sha]:
        print("drift: the branch already holds this proposal")
    else:
        message = f"ecosystem web: weekly drift\n\nRegenerated by ecosystem/build/run.sh from the latest source ({len(changed)} files changed, {len(deleted)} removed)."
        commit = api("POST", f"repos/{repo}/git/commits", {"message": message, "tree": new_tree, "parents": [base_sha]})["sha"]
        if ref:
            api("PATCH", f"repos/{repo}/git/refs/heads/{BRANCH}", {"sha": commit, "force": True})
        else:
            api("POST", f"repos/{repo}/git/refs", {"ref": f"refs/heads/{BRANCH}", "sha": commit})
        print(f"drift: {BRANCH} is now {commit}")
    owner = repo.split("/")[0]
    open_prs = api("GET", f"repos/{repo}/pulls?state=open&head={owner}:{BRANCH}&base={base}&per_page=5")
    if open_prs:
        pr = api("PATCH", f"repos/{repo}/pulls/{int(open_prs[0]['number'])}", {"body": body})
        print("drift: updated", pr.get("html_url"))
    else:
        pr = api("POST", f"repos/{repo}/pulls", {"title": TITLE, "head": BRANCH, "base": base, "body": body})
        print("drift: opened", pr.get("html_url"))


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("collect", "propose"):
        sys.exit(__doc__)
    (collect if sys.argv[1] == "collect" else propose)(os.path.abspath(sys.argv[2]))
