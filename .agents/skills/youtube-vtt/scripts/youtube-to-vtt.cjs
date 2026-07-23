#!/usr/bin/env node
/**
 * youtube-to-vtt.cjs
 *
 * Turn a YouTube (or any yt-dlp-supported) video URL into a single normalized
 * WebVTT transcript file WITHOUT downloading the video.
 *
 *   - Resolves yt-dlp: PATH first, then a managed venv at
 *     ~/.hax-skills/yt-dlp-venv (auto-created + pip-installed on first run so
 *     it works on PEP 668 / externally-managed systems without sudo).
 *   - Extracts subtitles only via --skip-download: tries manual subs first,
 *     then YouTube auto-generated captions.
 *   - Normalizes the sidecars yt-dlp emits (transcript.<lang>.vtt, etc.) to a
 *     single deterministic <output-dir>/transcript.vtt.
 *   - Prints a JSON status line and exits non-zero with a clear message if no
 *     captions are available (treated as a soft failure by callers).
 *
 * Usage:
 *   node youtube-to-vtt.cjs <watch-url> <output-dir> [--lang en]
 *
 * --lang defaults to "en".
 *
 * Leverages the yt-dlp engine (and the `yt-dlp` skill conventions); this script
 * adds the subtitle/VTT extraction + normalization that the yt-dlp skill's
 * download scripts do not provide.
 */
const fs = require("fs");
const os = require("os");
const path = require("path");
const { execFileSync, spawnSync } = require("child_process");

const VENV_DIR = path.join(os.homedir(), ".hax-skills", "yt-dlp-venv");

function parseFlags(argv) {
  const flags = { lang: "en" };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--lang") {
      flags.lang = argv[++i];
    }
  }
  return flags;
}

function isYouTubeUrl(url) {
  return /^https?:\/\/(www\.youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|www\.youtube\.com\/shorts\/)/i.test(
    url,
  );
}

// Find the yt-dlp executable: PATH first, then the managed venv (auto-created).
function resolveYtDlp() {
  // 1. PATH
  const which = spawnSync("which", ["yt-dlp"], { encoding: "utf8" });
  if (which.status === 0) {
    const p = which.stdout.trim();
    if (p) {
      return { bin: p, source: "path", installed: false };
    }
  }
  // 2. Managed venv
  const venvBin = path.join(VENV_DIR, "bin", "yt-dlp");
  if (fs.existsSync(venvBin)) {
    return { bin: venvBin, source: "venv", installed: false };
  }
  // 3. Provision the venv, then use it
  provisionVenv();
  return { bin: venvBin, source: "venv", installed: true };
}

function provisionVenv() {
  fs.mkdirSync(path.dirname(VENV_DIR), { recursive: true });
  // Create the venv (system-site packages off; upgrade pip quietly).
  execFileSync("python3", ["-m", "venv", VENV_DIR], { stdio: "pipe" });
  const venvPip = path.join(VENV_DIR, "bin", "pip");
  execFileSync(venvPip, ["install", "--quiet", "--upgrade", "pip"], {
    stdio: "pipe",
  });
  execFileSync(venvPip, ["install", "--quiet", "yt-dlp"], { stdio: "pipe" });
}

// Run yt-dlp with the given args (argv array after the binary); returns status.
function runYtDlp(bin, args) {
  const res = spawnSync(bin, args, { encoding: "utf8" });
  return {
    status: res.status,
    stdout: res.stdout || "",
    stderr: res.stderr || "",
  };
}

// Collect every .vtt file in a directory (sorted for determinism).
function listVtts(dir) {
  if (!fs.existsSync(dir)) {
    return [];
  }
  return fs
    .readdirSync(dir)
    .filter((f) => f.toLowerCase().endsWith(".vtt"))
    .map((f) => path.join(dir, f))
    .sort();
}

// --- VTT cleaning (YouTube auto-caption de-duplication) ---------------------
// YouTube auto-captions ship as 2-line "rolling" cues: each cue repeats the
// previous line plus the new line, and yt-dlp inserts 10ms "reset" cues with
// the plain text in between. The result is near-duplicate content for every
// phrase. cleanVtt() strips the inline karaoke timing tags (<HH:MM:SS.mmm> and
// <c>/<v> wrappers), drops the reset cues, de-duplicates the rolling
// repetition, and emits one clean cue per spoken phrase with consolidated
// timing. Also fixes the common "HackCMS"/"Hack CMS" speech-to-text typo.
function vttTsToSeconds(ts) {
  const parts = ts.split(":").map(Number);
  if (parts.some((n) => Number.isNaN(n))) return null;
  if (parts.length === 3) return parts[0] * 3600 + parts[1] * 60 + parts[2];
  if (parts.length === 2) return parts[0] * 60 + parts[1];
  return null;
}

function vttSecondsToTs(sec) {
  // Work in integer milliseconds so the seconds/minutes/hours carry correctly
  // and the fractional part is always exactly 3 digits (VTT requires .mmm).
  let totalMs = Math.max(0, Math.round(sec * 1000));
  const h = Math.floor(totalMs / 3600000);
  totalMs -= h * 3600000;
  const m = Math.floor(totalMs / 60000);
  totalMs -= m * 60000;
  const s = Math.floor(totalMs / 1000);
  const ms = totalMs - s * 1000;
  const pad = (n, l) => String(n).padStart(l, "0");
  return `${pad(h, 2)}:${pad(m, 2)}:${pad(s, 2)}.${pad(ms, 3)}`;
}

function cleanVtt(raw) {
  const lines = raw.split(/\r?\n/);
  // header: keep WEBVTT + optional KEY: value metadata lines
  const header = ["WEBVTT"];
  let i = 0;
  if (lines.length > 0 && /^WEBVTT/i.test(lines[0].trim())) i = 1;
  while (i < lines.length && /^[A-Za-z-]+:/i.test(lines[i].trim())) {
    const t = lines[i].trim();
    if (t) header.push(t);
    i++;
  }
  // parse cues (timestamp line -> text lines -> blank line ends cue)
  const cues = [];
  let cur = null;
  const cueRe =
    /^(\d{2}:\d{2}:\d{2}\.\d{3}|\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3}|\d{2}:\d{2}\.\d{3})/;
  for (; i < lines.length; i++) {
    const line = lines[i];
    const tm = cueRe.exec(line.trim());
    if (tm) {
      if (cur) cues.push(cur);
      cur = {
        start: vttTsToSeconds(tm[1]),
        end: vttTsToSeconds(tm[2]),
        textLines: [],
      };
      continue;
    }
    if (cur !== null) {
      // A cue ends on a truly empty line. YouTube rolling captions use a " "
      // (single space) line as an empty caption line WITHIN a cue, so only an
      // empty string (not whitespace-only) is a separator.
      if (line === "") {
        cues.push(cur);
        cur = null;
      } else {
        cur.textLines.push(line);
      }
    }
  }
  if (cur) cues.push(cur);

  // strip inline tags, fix speech-to-text typo, trim, drop empties
  const stripInline = (s) =>
    s
      .replace(/<[^>]+>/g, "")
      .replace(/Hack[ ]?CMS/gi, "HAXcms")
      .replace(/\s+/g, " ")
      .trim();
  for (const c of cues) {
    c.lines = c.textLines.map(stripInline).filter((l) => l !== "");
  }

  // de-duplicate the rolling repetition: emit only lines that differ from the
  // most recently emitted line.
  const emitted = [];
  let prevLine = "";
  for (const c of cues) {
    if (c.start === null) continue;
    for (const ln of c.lines) {
      if (ln === prevLine) continue;
      emitted.push({ start: c.start, text: ln });
      prevLine = ln;
    }
  }
  if (emitted.length === 0) return null;

  // build clean cues: each phrase starts at its source start and ends at the
  // next phrase's start (or +2s for the final one).
  const out = [];
  for (let k = 0; k < emitted.length; k++) {
    const start = emitted[k].start;
    let end = k + 1 < emitted.length ? emitted[k + 1].start : start + 2;
    if (!(end > start)) end = start + 2;
    out.push(
      `${vttSecondsToTs(start)} --> ${vttSecondsToTs(end)}\n${emitted[k].text}`,
    );
  }
  return header.join("\n") + "\n\n" + out.join("\n\n") + "\n";
}

// Normalize all .vtt sidecars into a single cleaned <dir>/transcript.vtt;
// remove the rest. Returns the final path or null if there were no .vtt files
// (or no usable cues after cleaning).
function normalizeVtt(dir) {
  const vtts = listVtts(dir);
  if (vtts.length === 0) {
    return null;
  }
  const finalPath = path.join(dir, "transcript.vtt");
  if (fs.existsSync(finalPath)) {
    fs.unlinkSync(finalPath);
  }
  const sidecars = listVtts(dir);
  if (sidecars.length === 0) {
    return null;
  }
  // read the first sidecar, clean it, and write the cleaned transcript
  const raw = fs.readFileSync(sidecars[0], "utf8");
  const cleaned = cleanVtt(raw);
  if (cleaned === null) {
    for (const sc of sidecars) {
      try {
        fs.unlinkSync(sc);
      } catch (e) {
        // best-effort cleanup
      }
    }
    return null;
  }
  fs.writeFileSync(finalPath, cleaned);
  for (const sc of sidecars) {
    if (sc !== finalPath) {
      try {
        fs.unlinkSync(sc);
      } catch (e) {
        // best-effort cleanup
      }
    }
  }
  return finalPath;
}

function main() {
  const rawArgv = process.argv.slice(2);
  const flags = parseFlags(rawArgv);
  const skipNext = new Set();
  for (let i = 0; i < rawArgv.length; i++) {
    if (rawArgv[i] === "--lang") {
      skipNext.add(i);
      skipNext.add(i + 1);
    }
  }
  const positional = rawArgv.filter((_, i) => !skipNext.has(i));
  const [url, outputDir] = positional;

  if (!url || !outputDir) {
    console.error(
      "Usage: node youtube-to-vtt.cjs <watch-url> <output-dir> [--lang en]",
    );
    process.exit(1);
  }
  if (!isYouTubeUrl(url)) {
    console.error(
      `URL does not look like a YouTube video URL: ${url}`,
    );
    process.exit(1);
  }

  fs.mkdirSync(outputDir, { recursive: true });

  let yt;
  try {
    yt = resolveYtDlp();
  } catch (e) {
    console.error(
      `Could not resolve or provision yt-dlp: ${e && e.message ? e.message : String(e)}`,
    );
    process.exit(1);
  }

  const baseArgs = [
    url,
    "--skip-download",
    "--no-playlist",
    "--sub-format",
    "vtt",
    "--convert-subs",
    "vtt",
    "-o",
    path.join(outputDir, "transcript.%(ext)s"),
  ];

  // Try 1: manual captions for the requested language.
  const manualRes = runYtDlp(yt.bin, [
    ...baseArgs,
    "--write-sub",
    "--sub-lang",
    flags.lang,
  ]);
  let vttPath = normalizeVtt(outputDir);
  let captionSource = "manual";

  // Try 2: auto-generated captions if manual produced nothing.
  if (!vttPath) {
    const autoRes = runYtDlp(yt.bin, [
      ...baseArgs,
      "--write-auto-sub",
      "--sub-lang",
      flags.lang,
    ]);
    vttPath = normalizeVtt(outputDir);
    captionSource = "auto";
    if (!vttPath) {
      console.error(
        `No ${flags.lang} captions (manual or auto) available for ${url}.`,
      );
      process.exit(2);
    }
  }

  console.log(
    JSON.stringify(
      {
        vttPath,
        lang: flags.lang,
        source: captionSource,
        ytDlp: yt.source,
        installed: yt.installed,
        bin: yt.bin,
      },
      null,
      2,
    ),
  );
}

main();
