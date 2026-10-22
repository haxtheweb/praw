# hax-media-ingest

Turn media into HAX content: transcribe and distill audio or video programs, publish them as searchable library sites, and generate WebVTT transcripts from YouTube without downloading video.

**Who it is for:** You turn audio, video, or YouTube content into searchable HAX sites.

## Install

```
/plugin marketplace add haxtheweb/praw
/plugin install hax-media-ingest@haxtheweb
```

## Skills

| Skill | What it does |
|---|---|
| `audio-program-transcribe` | Transcribe and distill an owned audio/video program into a markdown staging tree. |
| `audio-program-hax` | Publish a transcribed program as a searchable HAXcms library site with playback. |
| `youtube-vtt` | Generate a WebVTT transcript from a YouTube URL with yt-dlp, no video download. |

## Where to start

Run audio-program-transcribe first; audio-program-hax publishes its output.

## Prerequisites

This plugin composes with interface skills owned by the `create` repo (`@haxtheweb/create`). Install them so dependencies resolve:

```
npm install -g @haxtheweb/create
hax skills install --all
```

Needed here: `hax-site-building`.

## How this plugin is built

The skills live once, in `skills/` at the repo root. This plugin is a curated view over them (the marketplace entry lists the skill paths), so there is nothing to keep in sync here.
