---
name: audio-program-hax
description: >
  Publish a transcribed audio/video program as a searchable HAXcms library site:
  per-track transcript pages, per-disc distilled notes, a program-level summary,
  inline audio playback via media-playlist + audio-player, and a publishable
  "favorite quotes" page built from media-quote elements. Use when the user says
  "publish <program> to my HAX library", "add this course to my audio site",
  "put my transcripts into HAX", or "curate quotes from <program>". Consumes the
  staging tree produced by audio-program-transcribe. Depends on
  audio-program-transcribe, hax-claudehax, hax-site-building, and
  hax-design-system. Personal-use content; keep verbatim transcripts and audio
  assets private, publish only distilled notes and short cited quotes.
version: 0.1.0
license: Apache-2.0
metadata:
  author: rickmanelius / haxtheweb
  tags: [hax, audio, transcription, media-playlist, audio-player, media-quote, quotes, publish]
depends_on: [audio-program-transcribe, hax-claudehax, hax-site-building, hax-design-system]
---

# Audio Program HAX

Turn the staging tree from `audio-program-transcribe` into a live, searchable HAXcms library site you can serve locally and selectively publish. The site lets you listen to the original program inline (`media-playlist` + `audio-player`), read distilled notes, and publish a curated page of your favorite quotes (`media-quote`) with full citations back to disc/track/timestamp.

## Skill dependency resolution

This skill `depends_on` interface skills (`hax-claudehax`, `hax-site-building`) that now live in the `create` repo and ship with the `hax` CLI. They are resolved by name in this order: project `.agents/skills/`, then `~/.agents/skills/`, then `create`'s bundled `dist/skills/`. Install them with `hax skills install --all` (or `hax skills install hax-site-building hax-claudehax`). The workflow skills (`audio-program-transcribe`, `hax-design-system`) remain in PRAW.

## When to use

- The user says "publish <program> to my HAX library", "add this course to my audio site", "put my transcripts into HAX", or "curate quotes from <program>".
- A staging tree from `audio-program-transcribe` exists and the user wants a web surface for it.
- The user wants to publish a highlights/quotes page from an ingested program.

## Prerequisites

- The `hax` CLI installed globally (`npm install -g @haxtheweb/create`). Use the local/global `hax` binary, never `npx hax` (that resolves to a different npm package). Confirm with `hax --help`.
- The hax-site-ops plugin (`/plugin install hax-site-ops@haxtheweb`) if invoking via the `/hax` slash command. See the `hax-claudehax` skill.
- A staging tree from `audio-program-transcribe` at `staging/<Publisher>/<Program>/...`.
- The original audio assets (the CD rips / downloads), to copy into the site for inline playback.

## Page creation rule (critical)

Always create pages through the `hax` CLI, never by manually creating page directories or hand-editing `site.json`. Manual page creation bypasses the CLI's page-id generation, slug/location management, and atomic `site.json` updates, which corrupts the JSON Outline Schema structure and breaks the site in production. The CLI owns page structure; you only own page content.

Two supported CLI paths, run from inside the site directory:

- Single page: `hax site node:add --title "<title>" --slug "<slug>" --parent <parent-item-id> --content <path-to-html-file> --format html --y --no-i`. Capture the returned item id from the output to use as `--parent` for children.
- Bulk (preferred for a whole program): build a JOS items array (one object per page with `title`, `slug`, `parent`, `indent`, `order`, `metadata`, and `content`), then run `hax site site:items-import --items-import <items.json> --y --no-i`. The import remaps parent references to the newly generated ids automatically, so you can use stable temp ids in the import file as long as parents appear before children.

After creation, verify with `hax site site:items`. To mark a page draft/private (e.g. verbatim transcripts), set `metadata.published: false` in the import item (the CLI writes it through to `site.json`). Only copy audio assets and cover art into `files/` by hand — those are static assets, not pages.

## Architecture: one library site, many programs

Default to a single HAXcms site (e.g. `audio-library`) that holds every ingested program. This gives cross-program search via HAXcms's built-in `x/search` and `x/tags` for free, which is the whole point of making dead audio searchable. Each new program is added as a new top-level section in `site.json`, not a new site.

If the user explicitly wants one site per program, that works too, but they lose cross-program quote search.

## Output layout (mirror the staging tree as JOS)

The staging tree maps to JSON Outline Schema pages in one HAXsite:

```
audio-library/                  # one HAXcms site = your whole library
  site.json                     # JOS: program -> disc -> track tree
  pages/
    memory-optimizer.html               # Program landing (indent 0)
      mo-overview.html                  #   authors, disc map, provenance
      mo-distilled-notes.html           #   program rollup (public)
      mo-curated-quotes.html            #   PUBLISHABLE media-quote highlights
      mo-disc-1.html                    #   Disc 1 landing + media-playlist
        mo-disc-1-notes.html            #     disc distilled notes (public)
        mo-disc-1-track-01.html         #     verbatim transcript + audio-player (VTT)
        mo-disc-1-track-02.html         #     verbatim transcript + audio-player (VTT)
      mo-disc-2.html ...
  files/
    audio/<Publisher>/<Program>/<Disc>/<track>.mp3   # audio assets (local-only)
    audio/<Publisher>/<Program>/<Disc>/<track>.vtt   # VTT transcripts (publishable)
    copyright/<Publisher>.txt                        # per-publisher notice
```

Conventions this respects:

- `metadata.site.name` stays aligned to the folder name (`audio-library`); never rename it.
- Never create `x/search` or `x/tags` pages; those are built into HAXcms and are what make the library searchable.
- Verbatim transcript pages are published (`metadata.published: true`) so the full transcript is readable on the site; each includes an `audio-player` with `track` (VTT) for interactive click-to-seek. Audio asset files stay local-only by default (copyright).
- OER Schema metadata is applied to pages (author, publisher, learningResourceType, license) for semantic structure.

## Component mapping (use real HAX elements, not plain HTML)

The point of publishing to HAX is that every page is editable in the HAX editor afterward. Build pages from HAX-capable components.

### Listen to a whole disc inline -> media-playlist + audio-player

`media-playlist` is a DDD, HAX-capable grid element that presents players in a player + sidebar layout. Each `audio-player` child takes `source` (the audio file in `files/`), `media-title` (the track name), `thumbnail-src` (optional cover art), and `track` (a WebVTT captions file). Put one `media-playlist` on each disc landing page.

```html
<media-playlist>
  <audio-player
    source="files/audio/Learning Strategies/Memory Optimizer/Disc 4/01 Recovery.mp3"
    track="files/audio/Learning Strategies/Memory Optimizer/Disc 4/01 Recovery.vtt"
    media-title="01 Recovery rituals"
    thumbnail-src="files/audio/Learning Strategies/Memory Optimizer/cover.jpg">
  </audio-player>
  <audio-player
    source="files/audio/Learning Strategies/Memory Optimizer/Disc 4/02 Pressure bursts.mp3"
    track="files/audio/Learning Strategies/Memory Optimizer/Disc 4/02 Pressure bursts.vtt"
    media-title="02 Pressure bursts">
  </audio-player>
</media-playlist>
```

Why this matters: it is the gap Rick's original skill leaves open. With the audio assets copied into `files/`, the site plays the original program directly, so "the quote from Disc 4 Track 2" is one click away from actually hearing it.

### Interactive transcript (click a quote to hear it) -> audio-player track + VTT

`audio-player` (which extends `video-player`) renders an interactive transcript panel alongside the player when a `track` (WebVTT) URL is supplied. The transcript is clickable by default (`disableInteractive` defaults to false): clicking any cue seeks the audio to that moment. This is the mechanism that lets a user read the transcript and click directly to the exact passage they want to hear — no custom code required.

The VTT file is produced by the transcribe skill's `-ovtt` step. Copy it into `files/audio/<Publisher>/<Program>/<Disc>/<track>.vtt` alongside the audio asset, then reference it via the `track` attribute. Relevant `audio-player` properties:

- `track` — URL of a single VTT file (simplest; preferred for one-language transcripts).
- `tracks` — JSON array of track objects for multiple languages: `[{"src":"...track.vtt","kind":"subtitles","srclang":"en","label":"English"}]`.
- `hideTranscript` — defaults false (transcript panel shows). Set true to hide until the user toggles it.
- `disableInteractive` — defaults false (cues are clickable). Leave it false.
- `hideTimestamps` — set true to hide cue timestamps in the transcript panel.
- `lang` — language of the media, used as the track `srclang` fallback.

On the transcript page itself (see Step 3), also place an `audio-player` with the `track` wired up so the full transcript is both readable as page content and interactive as player cues.

### Publishable curated quotes -> media-quote

One `media-quote` per favorite passage on the program's Curated Quotes page. `media-quote` is a DDD, HAX-capable element with slots for `quote`, `author`, `author-detail`, `caption`, plus an image `src`/`alt`. Put the full citation in `author-detail` so every published quote links back to its source location.

```html
<media-quote src="files/audio/Learning Strategies/Memory Optimizer/cover.jpg" alt="Memory Optimizer cover art">
  <span slot="quote">Use a 15-second recovery ritual between pressure bursts to reset your nervous system.</span>
  <span slot="author">Jim Loehr</span>
  <span slot="author-detail">Learning Strategies · Memory Optimizer · Disc 4 · Track 1 · ~00:42:00</span>
  <span slot="caption">Cited from a personally owned copy.</span>
</media-quote>
```

### Track maps / disc inventory -> editable-table-display

Use `editable-table-display` for a consistent, scannable table of tracks per disc (this matches other HAX admin surfaces).

### Disc page organization -> a11y-collapse (with heading-button)

Use `a11y-collapse` to separate distilled notes from the track list and the media-playlist on disc pages. Always set `heading-button` on `a11y-collapse` so the entire heading is clickable to expand/collapse, not just the small toggle icon — it is much easier for end users to click the whole bar.

```html
<a11y-collapse heading-button expanded>
  <span slot="heading">Disc notes</span>
  <p>...</p>
</a11y-collapse>
```

### Styling -> DDD tokens

Use DDD design tokens for spacing (`--ddd-spacing-*`), font size (`--ddd-font-size-*`), and icon size (`--ddd-icon-size-*`), not inline styles. See the `hax-design-system` skill.

### Future: inline audio clips of quotes -> inline-audio

`inline-audio` plays a short MP3 inline with text (e.g. "Hear the 15-second recovery ritual"). It is HAX-capable and `inlineOnly`, purpose-built for this exact case. It is NOT used yet because it requires an actual MP3 clip per quote and there is no clipping tool in the pipeline today. When an mp3 clipping step is added to `audio-program-transcribe` (using word-level timestamps to cut a short clip per quote), wire each `media-quote` to a companion `inline-audio` with that clip. Leave this as a documented next step, not a now-step.

```html
<!-- future, once a clip exists -->
<inline-audio source="files/audio/clips/loehr-recovery.mp3" accent-color="orange">Hear the 15-second recovery ritual</inline-audio>
```

## Step 1: ensure or extend the library site

If `audio-library/` does not exist, scaffold it once:

```
hax site audio-library --y --no-i
```

If it already exists, do not re-scaffold; you will add to its `site.json` and `pages/`. Always use `hax site` to scaffold, never hand-create the site directory or its boilerplate.

## Step 2: copy audio + VTT assets into the site

Copy the original audio files into `files/audio/<Publisher>/<Program>/<Disc>/<track>.<ext>`, preserving the staging hierarchy. Copy the `.vtt` transcript files from the staging tree into the same disc folder (`files/audio/<Publisher>/<Program>/<Disc>/<track>.vtt`) so each `audio-player` can reference its VTT for the interactive transcript. Audio assets are for local playback via `hax serve` and are covered by the personal-use copyright notice; do not ship audio files in a public deploy unless the user has the rights to distribute them. VTT files are your own transcription and may be published.

## Step 3: create JOS pages mirroring the staging tree (via hax CLI)

Author each page's HTML content as a standalone string (the body only — headings, `media-playlist`, `media-quote`, `editable-table-display`, `a11y-collapse`, DDD classes/attributes). Then create the pages through the `hax` CLI per the Page creation rule above — do not hand-create page directories or edit `site.json` directly.

Mirror `staging/<Publisher>/<Program>/` as a JOS items array for `site:items-import`:

- One item per program (indent 0, parent null) -> program landing.
- Child items for overview, distilled notes, curated quotes, and each disc (indent 1, parent = program id).
- Grandchild items for each disc's notes and tracks (indent 2, parent = disc id).

Map staging frontmatter (author, publisher, disc, track, duration) into item `metadata` and OER Schema fields. Put short citable `tags` on each item so HAXcms `x/tags` groups them. Run the import once per program; verify with `hax site site:items`. See the `hax-site-building` skill for JOS structure rules.

The verbatim transcript page should be published (`metadata.published: true`) so the full transcript is readable on the site. Include an `audio-player` on that page with the `track` wired to the VTT so the transcript is also interactive (click a cue to hear that moment). For content where the user does not hold rights and wants to keep transcripts off a public deploy, set `published: false` and rely on local `hax serve` only — but the default is published, because a readable transcript is the whole point of the library.

## Step 4: curate publishable quotes (human-in-the-loop)

From the distilled notes and transcripts, surface the user's favorite passages, the ones they actually reference and want to share. For each candidate, build a `media-quote` record:

- `quote`: the passage, kept short and citable.
- `author`: the speaker.
- `author-detail`: the citation, formatted as `Publisher · Program · Disc N · Track M · ~HH:MM:SS`.
- `caption` / `src` / `alt`: optional cover art, with a "cited from a personally owned copy" caption.

Propose the candidates to the user and let them keep/remove before the page goes public. This is the layer that turns dead audio into something you can post to LinkedIn/X with a verifiable citation back to the source location. Do not auto-publish; quote selection is a judgment call.

## Step 5: serve and publish

- `hax serve` for local use. HAXcms's built-in `x/search` and `x/tags` now span every program ingested, so the whole library is searchable from one box.
- For public deployment, the transcript pages (with their interactive VTT player), distilled notes, and curated quotes are the public surface. Keep the `files/audio/` asset files private unless the user has the rights to distribute the original audio; the VTT files are the user's own transcription and may be published.

## Personal use and copyright

Only publish content the user has the rights to publish. The default: audio asset files stay local (they are the publisher's copyrighted audio), but the transcript text and VTT are the user's own transcription and are published so the library is readable and searchable. For content where the user does not hold rights and prefers to keep transcripts off a public deploy, set those pages to `published: false` and rely on local `hax serve`. Keep the per-publisher copyright notice in `files/copyright/` and reference it from the program overview page.

## Defaults (override if the user says otherwise)

- One library site for all programs (for cross-program search), not one site per program.
- Agent proposes quote candidates; human approves before publish.
- Transcript pages are published (`published: true`) so the full transcript is readable; include an `audio-player` with `track` (VTT) on the transcript page for interactive click-to-seek. Audio asset files stay local-only by default (copyright); VTT files may be published.
- `a11y-collapse` always uses `heading-button` so the whole heading is clickable.
- `inline-audio` quote clips are future work, pending an mp3 clipping tool in `audio-program-transcribe`.
- Citation granularity is `~HH:MM:SS` unless word-level timestamps were captured during transcription, in which case use exact offsets.

## References

- `media-playlist`: `webcomponents/elements/media-playlist` (`lib/media-playlist.haxProperties.json`)
- `audio-player`: `webcomponents/elements/audio-player`
- `media-quote`: `webcomponents/elements/media-quote` (`lib/media-quote.haxProperties.json`)
- `inline-audio`: `webcomponents/elements/inline-audio` (`lib/inline-audio.haxProperties.json`)
- Related skills: `hax-claudehax`, `hax-site-building`, `hax-design-system`, `audio-program-transcribe`.
