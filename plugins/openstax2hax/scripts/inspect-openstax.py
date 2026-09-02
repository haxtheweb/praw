#!/usr/bin/env python3
"""Inspect a downloaded OpenStax web/HTML mirror and summarize its structure.

This is a BUNDLED helper so the agent never has to inline Python (no
``python3 -c`` and no ``python3 - <<'EOF'`` heredocs, both of which get scanned
by Claude Code's command analyzer). Invoke it by path with simple arguments:

    # Chapter/section structure of the whole mirror:
    python3 "${CLAUDE_PLUGIN_ROOT}/scripts/inspect-openstax.py" ./source/openstax.org
    python3 "${CLAUDE_PLUGIN_ROOT}/scripts/inspect-openstax.py" ./source/openstax.org --json

    # Per-page element detection (figures, tables, math, callouts, objectives,
    # examples, key terms, review questions, headings, links). Accepts a single
    # HTML file OR a directory (aggregates across all section pages):
    python3 "${CLAUDE_PLUGIN_ROOT}/scripts/inspect-openstax.py" --elements <file-or-dir>
    python3 "${CLAUDE_PLUGIN_ROOT}/scripts/inspect-openstax.py" --elements <file-or-dir> --json

It only reads files; it never writes or modifies the source. Titles are derived
from each page's own <title>/<h1>, so no book content is hardcoded here.

Stdlib only; works on the system python3.
"""

import json
import os
import re
import sys
from html.parser import HTMLParser

SECTION_RE = re.compile(r"^(\d+)-(\d+)-(.+)\.html?$", re.IGNORECASE)
INTRO_RE = re.compile(r"^(\d+)-(introduction|intro)\b.*\.html?$", re.IGNORECASE)
TITLE_SUFFIX_RE = re.compile(r"\s+[-|]\s+.*$")  # strip " - Book - OpenStax"


class _TitleExtractor(HTMLParser):
    """Pull the first <title> and first <h1> text from an HTML document."""

    def __init__(self):
        super().__init__()
        self.in_title = False
        self.in_h1 = False
        self.title = ""
        self.h1 = ""

    def handle_starttag(self, tag, attrs):
        if tag == "title" and not self.title:
            self.in_title = True
        elif tag == "h1" and not self.h1:
            self.in_h1 = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "h1":
            self.in_h1 = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        elif self.in_h1:
            self.h1 += data


def find_pages_dir(start):
    """Return a directory that contains OpenStax section HTML files."""
    if os.path.isdir(start):
        # Direct hit: this dir already holds section files.
        for name in os.listdir(start):
            if SECTION_RE.match(name):
                return start
        # Otherwise look for a nested "pages" directory.
        for dirpath, dirnames, filenames in os.walk(start):
            if os.path.basename(dirpath) == "pages" and any(
                SECTION_RE.match(f) for f in filenames
            ):
                return dirpath
        # Fall back to any directory that has section files.
        for dirpath, dirnames, filenames in os.walk(start):
            if any(SECTION_RE.match(f) for f in filenames):
                return dirpath
    return None


def derive_title(path, slug):
    """Best-effort human title from the page's own HTML, else from the slug."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            head = fh.read(20000)
    except OSError:
        head = ""
    parser = _TitleExtractor()
    try:
        parser.feed(head)
    except Exception:
        pass
    raw = (parser.h1 or parser.title or "").strip()
    raw = TITLE_SUFFIX_RE.sub("", raw).strip()
    if raw:
        return " ".join(raw.split())
    return slug.replace("-", " ").title()


def collect(pages_dir):
    chapters = {}
    for name in sorted(os.listdir(pages_dir)):
        match = SECTION_RE.match(name)
        if not match:
            continue
        chap = int(match.group(1))
        sec = int(match.group(2))
        slug = match.group(3)
        title = derive_title(os.path.join(pages_dir, name), slug)
        chapters.setdefault(chap, []).append(
            {"section": sec, "slug": slug, "title": title, "file": name}
        )
    for chap in chapters:
        chapters[chap].sort(key=lambda s: s["section"])
    return chapters


ELEMENT_PATTERNS = {
    "learningObjectives": [r"learning[\s-]*objectives", r"by the end of this section"],
    "figures": [r"<figure\b"],
    "tables": [r"<table\b"],
    "math": [r"<math\b", r"MathJax", r"math-container", r"\\\(", r"\\\["],
    "notesCallouts": [
        r"link[\s-]*to[\s-]*learning",
        r"everyday[\s-]*(connection|application)",
        r"think[\s-]*it[\s-]*through",
        r"callout",
        r"<aside\b",
    ],
    "examples": [r'class="[^"]*example[^"]*"', r"worked[\s-]*example"],
    "keyTerms": [r"key[\s-]*terms", r"<dfn\b"],
    "glossaryTerms": [r"glossary", r"<dl\b"],
    "reviewQuestions": [r"review[\s-]*questions", r"conceptual[\s-]*questions"],
    "exercises": [r"\bexercises?\b", r"\bproblems?\b"],
    "references": [r"\breferences\b"],
    "links": [r"<a\b[^>]*href="],
    "sectionHeadings": [r"<h[23]\b[^>]*>"],
}


def analyze_elements(path):
    """Count OpenStax content elements in a single HTML file."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            html = fh.read()
    except OSError:
        return None
    counts = {}
    for name, patterns in ELEMENT_PATTERNS.items():
        total = 0
        for pat in patterns:
            total += len(re.findall(pat, html, re.IGNORECASE))
        counts[name] = total
    parser = _TitleExtractor()
    try:
        parser.feed(html[:20000])
    except Exception:
        pass
    title = (parser.title or parser.h1 or "").strip()
    title = TITLE_SUFFIX_RE.sub("", title).strip()
    return {"title": " ".join(title.split()), "elements": counts}


def iter_section_files(target):
    """Yield (path, name): one file, or every section file in a directory."""
    if os.path.isfile(target):
        yield target, os.path.basename(target)
        return
    pages_dir = find_pages_dir(target)
    if not pages_dir:
        return
    for name in sorted(os.listdir(pages_dir)):
        if SECTION_RE.match(name):
            yield os.path.join(pages_dir, name), name


def elements_report(target):
    """Per-file element counts plus an aggregate total."""
    pages = []
    totals = {name: 0 for name in ELEMENT_PATTERNS}
    for path, name in iter_section_files(target):
        result = analyze_elements(path)
        if result is None:
            continue
        for key, val in result["elements"].items():
            totals[key] += val
        pages.append({"file": name, "title": result["title"], "elements": result["elements"]})
    return {"target": target, "pageCount": len(pages), "totals": totals, "pages": pages}


def print_elements(report):
    print("Target: " + report["target"])
    print("Pages analyzed: " + str(report["pageCount"]))
    print("Totals across pages:")
    for name in ELEMENT_PATTERNS:
        print("  " + name + ": " + str(report["totals"][name]))
    for page in report["pages"]:
        print("")
        print(page["file"] + ": " + (page["title"] or "(untitled)"))
        for name in ELEMENT_PATTERNS:
            print("  " + name + ": " + str(page["elements"][name]))


def to_json(pages_dir, chapters):
    return {
        "pagesDir": pages_dir,
        "chapterCount": len(chapters),
        "chapters": [
            {"chapter": chap, "sectionCount": len(chapters[chap]), "sections": chapters[chap]}
            for chap in sorted(chapters)
        ],
    }


def print_text(pages_dir, chapters):
    print("Pages directory: " + pages_dir)
    print("Chapters detected: " + str(len(chapters)))
    for chap in sorted(chapters):
        sections = chapters[chap]
        print("Ch" + str(chap) + ": " + str(len(sections)) + " sections")
        for s in sections:
            print("  " + str(chap) + "." + str(s["section"]) + " " + s["title"])


def main(argv):
    args = argv[1:]
    want_json = "--json" in args
    want_elements = "--elements" in args
    positional = [a for a in args if not a.startswith("--")]
    if not positional:
        sys.stderr.write(
            "Usage:\n"
            "  python3 inspect-openstax.py <source-path> [--json]\n"
            "  python3 inspect-openstax.py --elements <file-or-dir> [--json]\n"
        )
        return 2
    target = positional[0]

    if want_elements:
        if not os.path.exists(target):
            sys.stderr.write("Path not found: " + target + "\n")
            return 1
        report = elements_report(target)
        if report["pageCount"] == 0:
            sys.stderr.write("No HTML pages to analyze under: " + target + "\n")
            return 1
        if want_json:
            print(json.dumps(report, indent=2))
        else:
            print_elements(report)
        return 0

    pages_dir = find_pages_dir(target)
    if not pages_dir:
        sys.stderr.write(
            "No OpenStax section pages (N-M-slug.html) found under: " + target + "\n"
        )
        return 1
    chapters = collect(pages_dir)
    if want_json:
        print(json.dumps(to_json(pages_dir, chapters), indent=2))
    else:
        print_text(pages_dir, chapters)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
