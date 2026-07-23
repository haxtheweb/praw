# Social Copy Templates

These templates keep the promotional output consistent. Replace the placeholders using the
published site URL, the YouTube URL, the video title, and the timestamps/chapters pulled
from the DOCX. The author profile is already in `site.json` from step 7; do NOT append
author name/links/signature to the LinkedIn post after the hashtags.

Hashtag sets (use exactly):
- LinkedIn + YouTube: `#HAXTheWeb #OER #opensource #edtech #education #pennstate`
- X: `#HAXTheWeb` only

Placeholders:
- `{{videoTitle}}` — the YouTube video title (also the site title)
- `{{siteUrl}}` — the published surge URL, e.g. `https://<slug>.surge.sh`
- `{{youtubeUrl}}` — the YouTube watch URL
- `{{authorName}}` — from author-profile.json (used only in the YouTube description Links section)
- `{{linkedin}}` — author LinkedIn URL (YouTube description only)
- `{{github}}` — author GitHub URL (YouTube description only)
- `{{website}}` — author primary website, haxtheweb.org (YouTube description only)
- `{{chapters}}` — timestamps/chapters from the DOCX (e.g. `0:00 Intro`, `1:30 Setup`); if the DOCX has no timestamps, use a "What's covered" list of section headings instead

## LinkedIn post

```
I just published a new tutorial: {{videoTitle}}.

🎬 Watch: {{youtubeUrl}}
📝 Tutorial: {{siteUrl}}

[2-3 sentence summary of what the viewer learns — pull from the DOCX intro/sections].

#HAXTheWeb #OER #opensource #edtech #education #pennstate
```

Notes:
- The `🎬 Watch:` (YouTube) and `📝 Tutorial:` (site) links go BEFORE the details/summary.
- Do NOT include author name, LinkedIn/website links, or any signature after the hashtags.
- Professional tone, 4-7 sentences total.

## X post (also serves Mastodon — produce ONE, not two)

```
New {{videoTitle}} tutorial

🎬 Watch: {{youtubeUrl}}
📝 Tutorial: {{siteUrl}}

#HAXTheWeb
```

Notes:
- ≤280 characters for X. Simplified, punchy language. If over, shorten the opening line; keep
  both `🎬 Watch:` / `📝 Tutorial:` lines and the `#HAXTheWeb` hashtag.
- No personal handle. No hashtags other than `#HAXTheWeb`.
- Mastodon uses the same post verbatim.

## YouTube SEO description

```
{{videoTitle}} — full written tutorial with screenshots and clickable timestamps: {{siteUrl}}

In this tutorial, {{authorName}} walks through [1-2 sentence keyword-rich summary of what the
video covers, using terms people would search for]. Follow along step by step; every timestamp
below links straight to that moment in the video.

⏱️ Chapters
{{chapters}}

🔗 Links
Written tutorial + screenshots: {{siteUrl}}
{{authorName}}: {{linkedin}}
HAXTheWeb: {{website}}
GitHub: {{github}}

#HAXTheWeb #OER #opensource #edtech #education #pennstate
```

Notes:
- The first 1-2 lines are the most important for SEO — front-load the video title and key terms.
- `{{chapters}}` is built from the timestamps found in the DOCX, formatted as
  `0:00 Intro\n1:30 Setup\n...` (one per line). These match the in-page `page-anchor` seek links
  when present; if the DOCX has no timestamps, use a "What's covered" list of section headings.
- Use the SAME hashtags as the LinkedIn post.
- The Links section keeps author profiles — the "no author signature" rule applies only to the
  LinkedIn post, not the YouTube description.
