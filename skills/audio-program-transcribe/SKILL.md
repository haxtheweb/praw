---
name: audio-program-transcribe
description: >
  Transcribe and distill a purchased audio or video program (CD rips, course
  downloads, lecture captures) into a portable staging tree of markdown notes:
  per-track verbatim transcripts, per-disc distilled notes, a program-level
  summary, and an overview. Use when the user says "transcribe <program>",
  "ingest this course", "rip and summarize these CDs", or points at a folder of
  audio/video files. Outputs a staging tree that audio-program-hax can publish
  as a HAX site, but works standalone for any markdown vault. Personal-use
  transcription of content you own; always credit the publisher and keep a
  copyright notice.
version: 0.1.0
license: Apache-2.0
metadata:
  author: rickmanelius / haxtheweb
  tags: [audio, video, transcription, whisper, distill, notes, ingestion]
  origin: >
    Adapted from Rick Manelius's audio-program-transcribe skill
    (https://www.rickmanelius.com/p/converting-professional-development)
---

# Audio Program Transcribe

Turn owned audio/video courses into a portable, searchable staging tree of markdown. Personal study use only; always include a copyright notice crediting the publisher. This skill produces the staging tree that `audio-program-hax` consumes to build a HAX library site, but it also works on its own for any Obsidian/markdown vault.

## When to use

- The user says "transcribe <program>", "ingest this course", "rip and summarize these CDs", or points at a folder of audio/video files.
- You need per-track transcripts plus per-disc distilled notes plus a program rollup.
- You are preparing content for `audio-program-hax` to publish.

## Prerequisites

A local speech-to-text CLI. Pick whichever runs on the host (the staging step is portable, not macOS-locked):

- macOS Apple Silicon: `mlx-whisper` (fast, free, on-device).
- Any OS: `openai-whisper` (`pip install openai-whisper`) or `whisper.cpp` (CPU/GPU, no Python).

Do not call cloud transcription APIs by default; the value here is private, on-device processing of material the user owns. Confirm the user has the rights to transcribe the source before proceeding.

## Output layout (mirror exactly)

```
staging/<Publisher>/<Program>/
  <Program> - Overview.md            authors, disc map, provenance, rip quirks
  <Program> - Distilled Notes.md     program-level rollup
  <Publisher> - Copyright Notice.md  per-publisher credit
  Disc 1/
    <original track name>.md         verbatim transcript per track
    <Program> - Disc 1 - Distilled Notes.md
  Disc 2/ ...
```

Why this shape: it preserves the publisher/program/disc/track hierarchy so the downstream HAX site can mirror it as JSON Outline Schema pages, and prefixing note filenames with the program name keeps links from colliding across programs. Keep original track filenames so a transcript always maps back to the exact source file.

Emit three files per track: the markdown transcript (for reading/search), a `.srt` (reference timestamps), and a `.vtt` (WebVTT — this is the format `audio-player` consumes directly for an interactive, click-to-seek transcript in the HAX site). Most whisper CLIs emit VTT natively (`whisper-cli -ovtt`, `openai-whisper --output_format vtt`); if your CLI only emits SRT, convert by prepending `WEBVTT\n\n` and replacing `,` with `.` in the timestamp lines.

Each transcript file gets YAML frontmatter so the HAX layer can map it to page metadata and OER Schema fields without re-parsing prose:

```yaml
---
title: <track name>
program: <Program>
publisher: <Publisher>
author: <author(s)>
disc: 1
track: <n>
source_file: <relative path to the audio asset>
date: <ISO date transcribed>
duration: <mm:ss or hh:mm:ss>
model: <whisper model id, e.g. mlx-community/whisper-large-v3-mlx>
license: personal-use
---
```

## Step 1: stage the source somewhere readable

macOS privacy protection (TCC) blocks agent subprocesses out of `~/Music` and `~/Documents`. Have the user copy the program to a plain working folder (e.g. `~/audio-work/`) in Finder or their own terminal first. On Linux there is no such restriction, but a plain working folder is still cleaner. Sanity-check the copy: list disc folders, count tracks, and read the audio files' metadata (artist/album tags) to identify author and publisher. Confirm the program name, publisher, author, and disc/track structure with the user before transcribing.

## Step 2: transcribe to the staging folder

Write a small runner script (python or shell) that walks each disc folder and, per track, shells out to whisper and writes a formatted markdown file to `staging/<Publisher>/<Program>/<Disc>/<track>.md` with the frontmatter above and the raw transcript joined into paragraphs.

Details that matter (these come from hard-won experience, not theory):

- Always pass an initial prompt seeded with the program's proper nouns (author names, technique names, jargon). It is the single biggest accuracy lever; without it names come out mangled.
- Skip tracks whose output already exists so the run is resumable.
- Run 2-3 whisper processes in parallel on big sets; each holds roughly 3GB of RAM.
- Whisper hallucinates during silence and music ("Thank you." loops) and truncates output filenames at interior dots. Detect repeated n-grams and flag them in the note; match output files by stem prefix.
- Run it in the background; a 7-hour program takes roughly 30-45 min on Apple Silicon.
- Always emit VTT (`-ovtt` / `--output_format vtt`) in addition to the text transcript. The VTT file is what makes the HAX site's `audio-player` show an interactive transcript where clicking any cue seeks to that moment — this is the mechanism that lets a user click directly to a quote they want to hear.
- If the user wants second-level citation timestamps later (for quote clips), enable word-level timestamps in the whisper call and store them alongside the transcript; otherwise segment-level VTT timestamps are sufficient for click-to-seek.

## Step 3: distill per disc

Spawn one subagent per disc, in parallel, as each disc's transcripts complete. Each agent:

1. Reads every transcript for its disc.
2. Writes the disc's distilled note (`<Program> - Disc N - Distilled Notes.md`): one-line disc purpose, key points organized by theme, exercises/protocols spelled out step by step, and a line on how the disc fits the program.
3. Flags any transcription artifacts it notices (hallucinated loops, mangled proper nouns) so the user can re-run those tracks.
4. Returns a compact disc summary (3-5 sentences) for the program rollup.

Distill per DISC, not per track, because tracks are usually too short to summarize meaningfully on their own.

## Step 4: program-level files

From the disc summaries write:

- The program rollup (`<Program> - Distilled Notes.md`): executive summary, source inventory, thematic synthesis, and an honest "reader's note" separating durable techniques from era-bound claims.
- The overview (`<Program> - Overview.md`): what the program is, disc/track map, provenance, known rip quirks (missing tracks, duplicated content, etc.).
- One copyright notice per publisher (`<Publisher> - Copyright Notice.md`) crediting the publisher and stating personal-use transcription of a personally owned copy.

## Hand-off

The staging tree this skill produces is the input to `audio-program-hax`, which mirrors it into a searchable HAXcms library site with inline audio playback and a publishable curated-quotes page. If the user only wants vault notes, the staging tree is already a complete vault on its own.

## Personal use and copyright

Only transcribe content the user owns or has clear rights to transcribe. Keep the copyright notice with the notes. Do not publish verbatim transcripts; the downstream HAX layer keeps transcript pages private/draft and publishes only distilled notes and short cited quotes.
