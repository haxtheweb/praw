#!/usr/bin/env node
/**
 * Ports `cleanTranscriptText` + `chunkTranscript` from `src/transcript.ts`
 * (booklooky-official-lrs-rater). If those library functions change, update
 * this script to match — this is a standalone (no-npm-install) copy so the
 * skill works in any environment.
 *
 * Usage: node chunk-transcript.js <transcript.txt> [outDir]
 * Writes <outDir>/chunks.json: [{ chunkIndex, text }, ...]
 * Prints the same JSON to stdout as well.
 */
const fs = require('fs');
const path = require('path');

// Mirrors OFFICIAL_SCAN_TRANSCRIPT_CHUNK_CHARS / _OVERLAP in src/constants.ts.
const CHUNK_CHARS = 100_000;
const CHUNK_OVERLAP = 4000;

function cleanTranscriptText(input) {
  return String(input || '')
    .replace(/\r\n/g, '\n')
    .replace(/\r/g, '\n')
    .replace(/[ \t]+\n/g, '\n')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

function chunkByChars(text, chunkSize, overlap) {
  const out = [];
  const t = text.trim();
  if (!t) return out;

  const size = Math.max(500, chunkSize);
  const ov = Math.max(0, Math.min(overlap, size - 50));

  let start = 0;
  while (start < t.length) {
    const end = Math.min(t.length, start + size);
    const slice = t.slice(start, end).trim();
    if (slice) out.push(slice);
    if (end >= t.length) break;
    start = Math.max(0, end - ov);
  }
  return out;
}

function chunkTranscript(text) {
  return chunkByChars(text, CHUNK_CHARS, CHUNK_OVERLAP);
}

function main() {
  const [, , transcriptPath, outDir] = process.argv;
  if (!transcriptPath) {
    console.error('Usage: node chunk-transcript.js <transcript.txt> [outDir]');
    process.exit(1);
  }

  const raw = fs.readFileSync(transcriptPath, 'utf8');
  const cleaned = cleanTranscriptText(raw);
  if (!cleaned) {
    console.error('Error: transcript is empty after normalization.');
    process.exit(1);
  }

  const texts = chunkTranscript(cleaned);
  const chunks = texts.map((text, chunkIndex) => ({ chunkIndex, text }));

  if (outDir) {
    fs.mkdirSync(outDir, { recursive: true });
    fs.writeFileSync(path.join(outDir, 'chunks.json'), JSON.stringify(chunks, null, 2), 'utf8');
    console.error(`Wrote ${chunks.length} chunk(s) to ${path.join(outDir, 'chunks.json')}`);
  }

  console.log(JSON.stringify(chunks));
}

main();
