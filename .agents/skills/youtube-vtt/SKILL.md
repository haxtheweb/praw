---
name: youtube-vtt
description: >
  Generate a WebVTT (.vtt) transcript file from a YouTube video URL using the
  yt-dlp engine, WITHOUT downloading the video. Use this skill when the user
  says "generate a VTT from this YouTube video", "download the subtitles",
  "make a transcript from YouTube", "youtube to vtt", "get captions for this
  video", or "transcribe this youtube video" — even if they don't say "vtt" or
  "skill". Uses the yt-dlp CLI (engine + URL conventions) and adds subtitle-only
  extraction + VTT normalization that yt-dlp's download workflow does not
  provide. Auto-provisions yt-dlp via an isolated venv if it is not installed,
  so it works on PEP 668 / externally-managed systems without sudo.
version: 1.0.0
license: Apache-2.0
metadata:
  author: haxtheweb
  tags: [youtube, vtt, transcript, captions, subtitles, yt-dlp, webvtt]
---

# YouTube → VTT Transcript

Turn a YouTube video URL into a single normalized `transcript.vtt` WebVTT file
without downloading the video itself. The VTT is ready to attach to a
`<video-player track="...">` so learners get a searchable transcript that reads
along with the video.

## Inputs

- **YouTube watch URL** — e.g. `https://www.youtube.com/watch?v=XXXXXXXXXXX`,
  `https://youtu.be/XXXXXXXXXXX`, or a `/embed/` or `/shorts/` URL.
- **Output directory** — where `transcript.vtt` is written (created if missing).
- **`--lang` (optional)** — subtitle language code, defaults to `en`.

## Prerequisites (verified on this machine)

- `node` v22+ (the script is a Node `.cjs`).
- `ffmpeg` — required by yt-dlp's `--convert-subs vtt` (present: 6.1.1).
- `python3` — used only for the venv fallback when yt-dlp is not on PATH.
- `yt-dlp` is **auto-provisioned**: the script checks PATH first, then a managed
  venv at `~/.hax-skills/yt-dlp-venv`; if neither exists it creates the venv and
  `pip install`s yt-dlp there (venvs are exempt from Ubuntu's PEP 668
  externally-managed lock; no sudo, no system packages touched). The venv is
  reusable across runs.

## Relationship to the `yt-dlp` CLI

This skill shells out to the **`yt-dlp`** command-line tool (engine + URL-domain
conventions) and auto-provisions it via an isolated venv if it is not on PATH.
yt-dlp's download workflow fetches video/audio and does not write subtitles/VTT;
this skill adds the subtitle-only extraction and VTT normalization layer on top
of the same engine.

## Workflow

1. **Collect inputs** — YouTube URL + output dir (+ optional `--lang`).
2. **Validate** — the URL must look like a YouTube watch/shortlink/embed/shorts
   URL; reject otherwise.
3. **Resolve yt-dlp** — PATH → managed venv → auto-provision the venv.
4. **Extract subtitles (no video download)** —
   `yt-dlp --skip-download --no-playlist --write-sub --sub-lang <lang>
   --sub-format vtt --convert-subs vtt -o "<out>/transcript.%(ext)s" <url>`.
   If no manual captions are produced, retry with `--write-auto-sub` for
   YouTube auto-generated captions.
5. **Normalize** — collapse yt-dlp's sidecars (`transcript.<lang>.vtt`, etc.)
   into a single `<out>/transcript.vtt` and remove the leftovers.
6. **Report** — print a JSON status line:
   `{ vttPath, lang, source: "manual"|"auto", ytDlp: "path"|"venv", installed, bin }`.

## Command reference

- Generate VTT: `node scripts/youtube-to-vtt.cjs <watch-url> <output-dir> [--lang en]`
- Check yt-dlp (if on PATH): `yt-dlp --version`
- List available subtitle languages:
  `yt-dlp --list-subs --skip-download --no-playlist <url>`

## Error handling

- **No captions (manual or auto)** — the script exits non-zero with a clear
  message. Callers (e.g. `hax-tutorial-site`) treat this as a **soft
  failure** and continue without a transcript.
- **yt-dlp absent + venv provisioning fails** (e.g. no network) — the script
  errors clearly; callers fall back to no-transcript.
- **Non-YouTube URL** — rejected up front. (yt-dlp supports many platforms, but
  this skill is scoped to YouTube where the tutorial workflow needs it.)

## Guardrails (ecosystem rules)

- No optional chaining (`?.`) — the Polymer parser has issues with it.
- Use `globalThis` instead of `window` where applicable.
- No system `pip install` (PEP 668); use the isolated venv only.
- Do not run the ubiquity script or the monorepo build.

## References

- `scripts/youtube-to-vtt.cjs` — the VTT extractor + normalizer (yt-dlp
  subtitle-only, manual-then-auto, venv auto-provision, JSON status output).
- `yt-dlp` CLI — the underlying engine (auto-provisioned via venv by `scripts/youtube-to-vtt.cjs`).
