# hax-content-audits

Read-only audits for HAX content: WCAG 2.0 AA accessibility, UDL 3.0, cognitive-load chunking, Gagné's events of instruction, Mayer's multimedia principles, OER Schema, and content rating. Each audit ends with HAX-specific remediation.

**Who it is for:** You want to check existing HAX content for accessibility, learning design, and metadata quality.

## Install

```
/plugin marketplace add haxtheweb/praw
/plugin install hax-content-audits@haxtheweb
```

## Skills

| Skill | What it does |
|---|---|
| `hax-a11y-audit` | Read-only WCAG 2.0 AA audit of authored HAX pages with HAX remediation. |
| `hax-udl-audit` | Read-only UDL 3.0 audit of a HAX page. |
| `hax-content-chunking-audit` | Audit a page for cognitive load and chunking; recommend HAX remediation. |
| `oerschema-audit` | Read-only OER Schema diagnostic of authored content. |
| `haxcms-lrs-rater` | Content rating and minimum-age recommendation for a HAXcms site (BookLooky LRS). |
| `hax-instructional-events-audit` | Read-only check of a lesson against Gagné's nine events and Merrill's First Principles. |
| `hax-multimedia-principles-audit` | Read-only check of how a page combines words and media against Mayer's principles. |

## Where to start

Start with hax-a11y-audit on one page; it is the quickest first win.

## How this plugin is built

The skills live once, in `skills/` at the repo root. This plugin is a curated view over them (the marketplace entry lists the skill paths), so there is nothing to keep in sync here.
