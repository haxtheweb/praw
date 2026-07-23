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

// Normalize all .vtt sidecars into a single <dir>/transcript.vtt; remove the
// rest. Returns the final path or null if there were no .vtt files.
function normalizeVtt(dir) {
  const vtts = listVtts(dir);
  if (vtts.length === 0) {
    return null;
  }
  const finalPath = path.join(dir, "transcript.vtt");
  // If transcript.vtt already exists from a prior run, remove it so a fresh
  // copy is authoritative.
  if (fs.existsSync(finalPath)) {
    fs.unlinkSync(finalPath);
  }
  // Re-list without the (now removed) transcript.vtt, then copy the first
  // remaining sidecar into place and delete the rest.
  const sidecars = listVtts(dir);
  if (sidecars.length === 0) {
    return null;
  }
  fs.copyFileSync(sidecars[0], finalPath);
  for (let i = 0; i < sidecars.length; i++) {
    if (sidecars[i] !== finalPath) {
      try {
        fs.unlinkSync(sidecars[i]);
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
