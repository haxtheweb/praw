#!/usr/bin/env python3
"""HEOSAT skill — re-sync references/ from the upstream HEOSAT tool.

The HEOSAT web app (https://locusplex.us/HEOSAT/) is a static page whose rubric
lives embedded as a `window.HEOSAT_DATA = {...}` object inside
assets/js/heosat.js. This script fetches that JS (or reads a local copy), peels
out the data object, and writes:

  references/rubric.json  — raw extracted data + provenance
  references/rubric.md    — readable rubric (scale, sections, questions,
                            evidence checklists, learn links)

Usage:
  python3 update-rubric.py                    # fetch from locusplex.us
  python3 update-rubric.py path/to/heosat.js  # use an already-downloaded copy
"""

import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
REFS_DIR = SKILL_ROOT / "references"
HEOSAT_JS_URL = "https://locusplex.us/HEOSAT/assets/js/heosat.js"

# ---------------------------------------------------------------- local extensions
#
# These questions/evidence close gaps between the upstream HEOSAT rubric and
# Apereo Foundation Incubation Process Section 5 (Exit Criteria) that upstream
# does not cover: standard voting practices (5.4), a conflict resolution
# policy (5.6), and a stricter contributor-agreement bar (5.1.3). Because
# rubric.json/rubric.md are regenerated wholesale from the upstream tool on
# every sync, they are NOT hand-maintained in those files directly — this
# function re-applies them after every fetch so a `python3 update-rubric.py`
# re-sync never silently drops them. If upstream ever adds equivalent
# coverage (same question id, or GV6/GV7 ids reused for something else),
# re-check this list by hand before the next sync.

_LL4_EXTRA_WHY = (
    " A stated policy is a 2 (Documented); projects that also collect and "
    "track signed agreements from active and former contributors \u2014 the "
    "stricter bar some incubation programs (e.g. Apereo) require at exit \u2014 "
    "demonstrate the practice is actually followed and can score a 3 or higher."
)

_LL4_EXTRA_EVIDENCE = [
    "CLA/DCO signature bot records (e.g. EasyCLA, CLA Assistant logs)",
    "Roster or count of signed ICLAs/CCLAs/SGLAs, if used",
]

_LOCAL_EXTENSION_QUESTIONS = {
    "Governance & Decision-Making": [
        {
            "id": "GV6",
            "text": "The project documents and practices a standard voting procedure for decisions requiring formal approval.",
            "guidance": {
                "why": "<p>Consensus works until it doesn't. A documented voting procedure (e.g., lazy consensus with a fallback to a majority or supermajority vote) gives a project a clear path to a decision when consensus stalls, and makes outcomes legitimate and auditable.</p><p><strong>Higher education perspective.</strong> Apereo's Incubation Process requires incubating projects to adopt and demonstrate standard voting practices before graduation, since multi-institutional communities cannot rely on one maintainer's informal judgment call.</p><p><strong>What good looks like.</strong> A mature project documents voting thresholds and eligible voters, and can point to at least one real vote on record, not just a hypothetical procedure.</p>",
                "evidence": [
                    "Documented voting procedure and thresholds (majority, supermajority, lazy consensus)",
                    "Defined quorum rules and eligible-voter roster",
                    "Evidence of an actual vote on record (meeting minutes, mailing list, issue/PR)",
                    "Escalation from stalled consensus to a formal vote",
                ],
                "learn": [
                    {"title": "Apereo Incubation", "url": "https://www.apereo.org/programs/software-incubation"},
                    {"title": "Producing Open Source Software", "url": "https://producingoss.com/"},
                    {"title": "CHAOSS Metrics Models", "url": "https://chaoss.community/kb/metrics-models/"},
                ],
            },
        },
        {
            "id": "GV7",
            "text": "The project has an adopted, documented process for resolving community or governance disputes.",
            "guidance": {
                "why": "<p>Disagreements over technical direction, roles, or conduct are normal in any community; what distinguishes a mature project is having an agreed path to resolve them rather than letting disputes fester or drive out contributors.</p><p><strong>Higher education perspective.</strong> Apereo's Incubation Process requires an explicit conflict resolution policy, distinct from a conflict-of-interest policy, as an exit criterion \u2014 multi-institutional governance needs a known escalation path when participants disagree.</p><p><strong>What good looks like.</strong> A mature project documents a dispute process with escalation steps (e.g., to mentors, a board, or a steering committee), distinguishes it from code-of-conduct incident response, and can show it has been invoked at least once.</p>",
                "evidence": [
                    "Documented conflict/dispute resolution process",
                    "Escalation path to mentors, board, or steering committee",
                    "Evidence the process was invoked (meeting minutes, issue, decision record)",
                    "Clear boundary between this process and code-of-conduct incident response",
                ],
                "learn": [
                    {"title": "Apereo Incubation", "url": "https://www.apereo.org/programs/software-incubation"},
                    {"title": "CHAOSS Metrics Models", "url": "https://chaoss.community/kb/metrics-models/"},
                    {"title": "It Takes a Village Guidebook", "url": "https://itav.lyrasis.org/guidebook/"},
                ],
            },
        },
    ],
}


def apply_local_extensions(data):
    """Re-apply the local Apereo-gap extensions on top of freshly-fetched
    upstream data (idempotent — safe to run on every sync)."""
    for section in data.get("sections", []):
        existing_ids = {q["id"] for q in section["questions"]}

        for q in section["questions"]:
            if q["id"] == "LL4":
                why = q.get("guidance", {}).get("why", "")
                if _LL4_EXTRA_WHY.strip() not in why:
                    closing = "</p>"
                    if why.endswith(closing):
                        why = why[: -len(closing)] + _LL4_EXTRA_WHY + closing
                    else:
                        why += _LL4_EXTRA_WHY
                    q["guidance"]["why"] = why
                evidence = q.get("guidance", {}).setdefault("evidence", [])
                for item in _LL4_EXTRA_EVIDENCE:
                    if item not in evidence:
                        evidence.append(item)

        extensions = _LOCAL_EXTENSION_QUESTIONS.get(section["title"], [])
        for ext_q in extensions:
            if ext_q["id"] not in existing_ids:
                section["questions"].append(json.loads(json.dumps(ext_q)))

    return data


# ---------------------------------------------------------------- HTML -> text

class _WhyText(HTMLParser):
    """Convert the rubric's `why` HTML into readable plain text."""

    def __init__(self):
        super().__init__()
        self.parts = []
        self.href = None

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.href = dict(attrs).get("href")
        elif tag in ("p", "ul", "ol"):
            self.parts.append("\n\n")
        elif tag == "li":
            self.parts.append("\n- ")
        elif tag == "br":
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag == "a":
            self.href = None

    def handle_data(self, data):
        text = data.strip()
        if not text:
            return
        self.parts.append(data)
        if self.href and text:
            self.parts.append(f" <{self.href}>")

    def result(self):
        out = "".join(self.parts)
        out = re.sub(r"[ \t]+\n", "\n", out)
        out = re.sub(r"\n{3,}", "\n\n", out)
        return out.strip()


def html_to_text(html):
    parser = _WhyText()
    parser.feed(html)
    return parser.result()


# ---------------------------------------------------------------- extraction

def extract_data(js_text):
    """Pull the window.HEOSAT_DATA object out of the app JS."""
    marker = "window.HEOSAT_DATA"
    idx = js_text.find(marker)
    if idx == -1:
        raise SystemExit("error: no window.HEOSAT_DATA found — upstream layout changed")
    start = js_text.index("{", idx)
    data, _ = json.JSONDecoder().raw_decode(js_text[start:])
    return data


# ---------------------------------------------------------------- render .md

def render_markdown(rubric, fetched_from, fetched_at):
    lines = []
    lines.append(f"# {rubric['title']}")
    lines.append("")
    lines.append(f"> {rubric['subtitle']}")
    lines.append("")
    lines.append(f"Rubric version: **{rubric['version']}**")
    lines.append(f"Source: <{fetched_from}> (extracted {fetched_at})")
    lines.append("")
    lines.append("## Maturity scale")
    lines.append("")
    lines.append("Every question is scored on this 6-level scale (0-5):")
    lines.append("")
    for i, name in enumerate(rubric["scale"]):
        lines.append(f"- **{i} — {name}**")
    lines.append("")

    lines.append("## Contents")
    lines.append("")
    for i, section in enumerate(rubric["sections"], 1):
        qids = ", ".join(q["id"] for q in section["questions"])
        lines.append(f"- {i}. {section['title']} ({qids})")
    lines.append("")

    for i, section in enumerate(rubric["sections"], 1):
        lines.append(f"## {i}. {section['title']}")
        lines.append("")
        lines.append(section["description"])
        lines.append("")
        for q in section["questions"]:
            lines.append(f"### {q['id']} — {q['text']}")
            lines.append("")
            why = q.get("guidance", {}).get("why")
            if why:
                lines.append(html_to_text(why))
                lines.append("")
            evidence = q.get("guidance", {}).get("evidence") or []
            if evidence:
                lines.append("**Evidence to look for:**")
                lines.append("")
                for item in evidence:
                    lines.append(f"- {item}")
                lines.append("")
            learn = q.get("guidance", {}).get("learn") or []
            if learn:
                lines.append("**Learn more:**")
                lines.append("")
                for ref in learn:
                    lines.append(f"- [{ref['title']}]({ref['url']})")
                lines.append("")

    attrib = rubric.get("attributions", {})
    lines.append("## Attribution")
    lines.append("")
    if attrib.get("license"):
        lines.append(attrib["license"])
        lines.append("")
    for item in attrib.get("items", []):
        note = f" — {item['note']}" if item.get("note") else ""
        lines.append(f"- [{item['title']}]({item['url']}){note}")
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------- main

def main():
    if len(sys.argv) > 1:
        js_text = Path(sys.argv[1]).read_text(encoding="utf-8")
    else:
        req = urllib.request.Request(HEOSAT_JS_URL, headers={"User-Agent": "heosat-skill/1.0"})
        with urllib.request.urlopen(req, timeout=30) as res:
            js_text = res.read().decode("utf-8")

    data = extract_data(js_text)
    data = apply_local_extensions(data)
    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    questions = sum(len(s["questions"]) for s in data["sections"])
    if not data.get("sections") or not questions:
        raise SystemExit("error: extracted data has no sections/questions — refusing to write")

    REFS_DIR.mkdir(parents=True, exist_ok=True)

    (REFS_DIR / "rubric.json").write_text(
        json.dumps(
            {
                "source": HEOSAT_JS_URL,
                "fetchedAt": fetched_at,
                "data": data,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    (REFS_DIR / "rubric.md").write_text(
        render_markdown(data, HEOSAT_JS_URL, fetched_at) + "\n", encoding="utf-8"
    )

    print(f"HEOSAT rubric synced: {data['version']}")
    print(f"  sections: {len(data['sections'])}, questions: {questions} (includes local Apereo-gap extensions GV6/GV7)")
    print(f"  wrote {REFS_DIR / 'rubric.json'}")
    print(f"  wrote {REFS_DIR / 'rubric.md'}")


if __name__ == "__main__":
    main()
