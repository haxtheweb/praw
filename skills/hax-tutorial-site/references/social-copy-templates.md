# Social Copy Templates

These templates keep the promotional output consistent. Replace the placeholders using the
published site URL, the YouTube URL, the video title, the author profile
(`references/author-profile.json`), and the timestamps/chapters pulled from the DOCX.

Placeholders:
- `{{videoTitle}}` — the YouTube video title (also the site title)
- `{{siteUrl}}` — the published surge URL, e.g. `https://<slug>.surge.sh`
- `{{youtubeUrl}}` — the YouTube watch URL
- `{{authorName}}` — from author-profile.json (Bryan T Ollendyke)
- `{{linkedin}}` — author LinkedIn URL
- `{{github}}` — author GitHub URL
- `{{website}}` — author primary website (haxtheweb.org)
- `{{chapters}}` — timestamps/chapters list pulled from the DOCX (e.g. `0:00 Intro`, `1:30 Setup`)

## LinkedIn post

```
I just published a new tutorial: {{videoTitle}}.

In it I walk through [2-3 sentence summary of what the viewer learns — pull from the DOCX intro/sections].

Watch the video: {{youtubeUrl}}
Follow along with the written tutorial (screenshots + timestamps): {{siteUrl}}

#HAX #HAXTheWeb #WebComponents #EdTech #OpenSource #OER

{{authorName}}
{{linkedin}}
{{website}}
```

Notes:
- Professional tone, 4-7 sentences.
- Always include BOTH the YouTube link and the tutorial site link.
- Hashtags: include HAX-specific tags plus topic-relevant ones inferred from the video title.

## X / Mastodon post

```
New {{videoTitle}} tutorial is up 🎬

Written walkthrough with screenshots + clickable timestamps:
{{siteUrl}}

Full video: {{youtubeUrl}}

#HAX #HAXTheWeb #WebComponents
```

Notes:
- ≤280 characters for X (drop the YouTube line or shorten if needed; keep the tutorial site link).
- If `twitter`/`mastodon` in the profile are blank, do not invent a handle — the post stands on
  the content links. Optionally append `via {{website}}` if space allows.
- Mastodon can be longer; keep both links.

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

#HAX #HAXTheWeb #WebComponents #EdTech #OER [plus 2-3 topic-relevant hashtags]
```

Notes:
- The first 1-2 lines are the most important for SEO — front-load the video title and key terms.
- `{{chapters}}` is built from the timestamps found in the DOCX, formatted as
  `0:00 Intro\n1:30 Setup\n...` (one per line). These match the in-page `page-anchor` seek links.
- Always link the tutorial site URL near the top and in the Links section.
