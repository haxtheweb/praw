#!/usr/bin/env node
/**
 * youtube-metadata.cjs
 *
 * Resolve a YouTube video's title, author, and thumbnail URL with yt-dlp
 * (NOT curl/oEmbed, so no network call that needs interactive confirmation).
 * Used by the hax-tutorial-site skill for step 2 (video metadata).
 *
 *   - Resolves yt-dlp: PATH first, then a managed venv at
 *     ~/.hax-skills/yt-dlp-venv (auto-created + pip-installed on first run so
 *     it works on PEP 668 / externally-managed systems without sudo). This is
 *     the SAME venv the youtube-vtt skill uses, so a prior VTT run makes this
 *   instant.
 *   - Uses --dump-json (stable across yt-dlp versions) and prints a single
 *     JSON line: { title, author, thumbnail }.
 *
 * Usage:
 *   node youtube-metadata.cjs <watch-url>
 */
const fs = require("fs");
const os = require("os");
const path = require("path");
const { execFileSync, spawnSync } = require("child_process");

const VENV_DIR = path.join(os.homedir(), ".hax-skills", "yt-dlp-venv");

function isYouTubeUrl(url) {
  return /^https?:\/\/(www\.youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|www\.youtube\.com\/shorts\/)/i.test(
    url,
  );
}

// Find the yt-dlp executable: PATH first, then the managed venv (auto-created).
function resolveYtDlp() {
  const which = spawnSync("which", ["yt-dlp"], { encoding: "utf8" });
  if (which.status === 0) {
    const p = which.stdout.trim();
    if (p) {
      return { bin: p, source: "path", installed: false };
    }
  }
  const venvBin = path.join(VENV_DIR, "bin", "yt-dlp");
  if (fs.existsSync(venvBin)) {
    return { bin: venvBin, source: "venv", installed: false };
  }
  provisionVenv();
  return { bin: venvBin, source: "venv", installed: true };
}

function provisionVenv() {
  fs.mkdirSync(path.dirname(VENV_DIR), { recursive: true });
  execFileSync("python3", ["-m", "venv", VENV_DIR], { stdio: "pipe" });
  const venvPip = path.join(VENV_DIR, "bin", "pip");
  execFileSync(venvPip, ["install", "--quiet", "--upgrade", "pip"], {
    stdio: "pipe",
  });
  execFileSync(venvPip, ["install", "--quiet", "yt-dlp"], { stdio: "pipe" });
}

function main() {
  const [url] = process.argv.slice(2);
  if (!url) {
    console.error("Usage: node youtube-metadata.cjs <watch-url>");
    process.exit(1);
  }
  if (!isYouTubeUrl(url)) {
    console.error(`URL does not look like a YouTube video URL: ${url}`);
    process.exit(1);
  }

  let yt;
  try {
    yt = resolveYtDlp();
  } catch (e) {
    console.error(
      `Could not resolve or provision yt-dlp: ${e && e.message ? e.message : String(e)}`,
    );
    process.exit(1);
  }

  const res = spawnSync(
    yt.bin,
    [url, "--skip-download", "--no-playlist", "--no-warnings", "--dump-json"],
    { encoding: "utf8", maxBuffer: 20 * 1024 * 1024 },
  );
  if (res.status !== 0 || !res.stdout) {
    console.error(
      `yt-dlp metadata fetch failed: ${(res.stderr || "").trim()}`,
    );
    process.exit(2);
  }

  let info;
  try {
    info = JSON.parse(res.stdout);
  } catch (e) {
    console.error(`Could not parse yt-dlp JSON: ${e && e.message ? e.message : String(e)}`);
    process.exit(2);
  }

  const title = info.title || "";
  const author = info.uploader || info.channel || info.creator || "";
  const thumbnail = info.thumbnail || (info.thumbnails && info.thumbnails.length ? info.thumbnails[info.thumbnails.length - 1].url : "");

  console.log(
    JSON.stringify(
      {
        title,
        author,
        thumbnail,
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
