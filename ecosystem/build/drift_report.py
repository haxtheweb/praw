#!/usr/bin/env python3
"""The weekly drift run's report (.github/workflows/ecosystem-drift.yml, https://github.com/haxtheweb/issues/issues/3296).

  python3 -I drift_report.py <folder>   after ecosystem/build/run.sh: copy what the generators changed under
                                        ecosystem/ into <folder>, with a manifest and the written report

It only reports. It needs no token and writes nothing to GitHub: no branch, no pull request, no comment. The
report goes to the run's summary and, with the changed files, into <folder> for the workflow to keep as an
artifact, so a person can read what drifted and decide what to do about it.

Standard library only."""

import json, os, re, shutil, subprocess, sys

SAFE_PATH = re.compile(r"^ecosystem/(?:[A-Za-z0-9_][A-Za-z0-9._-]*/)*[A-Za-z0-9_][A-Za-z0-9._-]*$")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def git(*args):
    return subprocess.run(["git", "-C", ROOT] + list(args), capture_output=True, text=True, check=True).stdout


def growth_summary():
    """Lines on the growth data layer (https://github.com/haxtheweb/issues/issues/3415): whether the refresh ran,
    and its headline counts, committed snapshot first and this run's second."""
    outcome = os.environ.get("GROWTH_OUTCOME", "")
    if not outcome:
        return []
    if outcome != "success":
        return ["- Growth data refresh (`ecosystem/build/build_growth.py`): **did not finish** (%s); the committed "
                "snapshot is unchanged. The step's log says why." % outcome]

    def counts(read):
        try:
            th, el, rp, pl = (json.loads(read(n)) for n in ("themes", "elements", "repos", "payload"))
            try:
                people = sum(1 for x in json.loads(read("contributors"))["people"] if x.get("kind") == "person")
            except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError):
                people = None
            return {"contributors": people,"themes": len(th["themes"]), "elements": len(el["elements"]), "repositories": len(rp["repos"]),
                    "dependency links": sum(len(e["dependsOn"]) for e in el["elements"]),
                    "KB gzipped in the shared core": round(pl["core"]["gz"] / 1024)}
        except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError):
            return None
    rel = "ecosystem/build/data/growth/%s.json"
    was = counts(lambda n: git("show", "HEAD:" + rel % n))
    now = counts(lambda n: open(os.path.join(ROOT, rel % n), encoding="utf-8").read())
    if not now:
        return ["- Growth data refresh: ran, but its files could not be read."]
    def part(k, v):
        if v is None:
            return "no %s" % k
        if was and was.get(k) is not None and was[k] != v:
            return "%s %s (was %s)" % (v, k, was[k])
        return "%s %s" % (v, k)
    parts = [part(k, v) for k, v in now.items()]
    return ["- Growth data refreshed: " + ", ".join(parts) + ". Its files are in the artifact with the rest."]


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
        "# Ecosystem web: weekly drift",
        "",
        "The weekly run of `ecosystem/build/run.sh`: every generator rerun against the latest source, so new CLI commands, endpoints, MCP tools, workflows, rules and the rest show up here.",
        "",
        f"- {len(changed)} files changed" + (f", {len(deleted)} removed" if deleted else "") + ". They are in this run's `ecosystem-drift` artifact, under `files/`.",
        "- Integrity check on the regenerated webs: " + ("passes." if integrity.returncode == 0 else "**fails** (below)."),
    ] + growth_summary() + [
        "- This run changes nothing in the repository. To take the changes, run `ecosystem/build/run.sh` locally and open a pull request.",
        "",
    ]
    if integrity.returncode != 0:
        body += ["## Integrity check", "", "```", check, "```", ""]
    body.append(report)
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(body) + "\n")
    with open(os.path.join(out, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump({"changed": changed, "deleted": deleted, "drift": drift, "integrity": integrity.returncode == 0}, f, indent=1)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write("\n".join(body) + "\n")
    print(f"drift: {len(changed)} changed, {len(deleted)} removed, drift {'found' if drift else 'not found'}, integrity {'passes' if integrity.returncode == 0 else 'fails'}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    collect(os.path.abspath(sys.argv[1]))
