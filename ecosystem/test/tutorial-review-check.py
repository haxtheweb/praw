"""Checks for ecosystem/build/tutorial_review.py: python3 -I ecosystem/test/tutorial-review-check.py

- every tile a tutorial teaches is in the record, and every code path on record is a relative path in a repository
- a change inside a tile's code names the tutorials that teach it; a change elsewhere names none
- a tile whose code is a whole repository only counts when asked for"""
import importlib.util, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("tutorial_review", os.path.join(os.path.dirname(HERE), "build", "tutorial_review.py"))
T = importlib.util.module_from_spec(spec); spec.loader.exec_module(T)
ok = 0
def check(cond, what):
    global ok
    if not cond: sys.exit("FAILED: " + what)
    ok += 1

rows = T.build_map()
taught = set(re.findall(r"^\s+\w+ -->\|teaches\| (\w+)\s*$", open(T.web_file("tutorials") + ".mmd").read(), re.M))
check(taught and {r["tile"] for r in rows} == taught, "every tile a tutorial teaches is in the record")
check(all(r["tutorials"] for r in rows), "every row names its tutorials")
for r in rows:
    if r["code"]:
        repo, path = r["code"]
        check(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", repo) and not path.startswith("/") and ".." not in path.split("/"), f"{r['tile']}: code is a repository and a path inside it")
with_path = next(r for r in rows if r["code"] and r["code"][1])
repo, path = with_path["code"]
hits = T.review(rows, [(repo, path + "/some-file.js")])
check({t["id"] for t in with_path["tutorials"]} <= set(hits), "a change inside a tile's code names its tutorials")
check(T.review(rows, [(repo, path + "-other/some-file.js"), ("not-a-hax-repo", path + "/x.js")]) == {}, "a change beside the path, or in another repository, names none")
whole = next((r for r in rows if r["code"] and not r["code"][1]), None)
if whole:
    check(not any(b["tile"] == whole["tile"] for h in T.review(rows, [(whole["code"][0], "anything.js")]).values() for b in h["because"]), "a whole-repository tile does not count by default")
    check(any(b["tile"] == whole["tile"] for h in T.review(rows, [(whole["code"][0], "anything.js")], True).values() for b in h["because"]), "it counts with --whole-repos")
print(f"tutorial-review-check: {ok} checks passed")
