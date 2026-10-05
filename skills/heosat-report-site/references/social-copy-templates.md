# Social Copy Templates (HEOSAT report sites)

These templates keep the sharing copy consistent. Replace the placeholders using
the published surge site URL, the assessed project's name/URL, and the
scorecard numbers (overall score, band, top section scores). The site.json
metadata carries the PROJECT's profile (not the publishing person's) — the copy
does NOT include a personal name, handle, or signature after the hashtags.

Hashtag sets (use exactly):
- LinkedIn: `#HAXTheWeb #OER #opensource #edtech #education #pennstate`
- X: `#HAXTheWeb` only

Placeholders:
- `{{projectName}}` — the assessed project's display name
- `{{projectUrl}}` — the assessed project's repository URL
- `{{siteUrl}}` — the published surge URL, e.g. `https://heosat-<slug>.surge.sh`
- `{{overall}}` — the overall score, e.g. `2.0/5`
- `{{band}}` — the nearest band label, e.g. `Documented`
- `{{summary}}` — 2-3 sentence verdict pulled from the report's strengths and recommendations
- `{{topStrength}}` — the strongest section or finding (e.g. "Legal & Licensing at 3.0/5")

## LinkedIn post

```
I just published a HEOSAT open source maturity assessment of {{projectName}} ({{projectUrl}}).

📊🌐 Report: {{siteUrl}}

Overall: {{overall}} ({{band}}) across 47 evidence-backed questions — governance, licensing, community, documentation, operations, security, accessibility, adoption, and sustainability. {{summary}}

#HAXTheWeb #OER #opensource #edtech #education #pennstate
```

Notes:
- The `📊🌐 Report:` link goes BEFORE the details/summary.
- Keep the assessment framing honest: it is a locally generated assessment
  against the published HEOSAT rubric, not an official certification.
- Do NOT include a personal name, links, or any signature after the hashtags.
- Professional tone, 4-7 sentences total.

## X post

```
HEOSAT maturity assessment of {{projectName}}: {{overall}} ({{band}})

📊🌐 Report: {{siteUrl}}

#HAXTheWeb
```

Notes:
- ≤280 characters for X. Simplified, punchy language. If over, shorten the
  opening line; keep the `📊🌐 Report:` line and the `#HAXTheWeb` hashtag.
- No personal handle. No hashtags other than `#HAXTheWeb`.
- Optional: append one highlight if length allows, e.g.
  `Strongest: {{topStrength}}.`

(No separate Mastodon output — X copy only.)
