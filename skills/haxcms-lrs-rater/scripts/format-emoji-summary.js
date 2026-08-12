#!/usr/bin/env node
/**
 * Formats an LRS report as a BookLooky-style emoji summary — the same compact
 * format used on booklooky.com book pages.
 *
 * Usage: node format-emoji-summary.js <report.json> <title> [author] [url]
 *   <report.json>: output from build-report.js (has { report, contentAnalysis })
 *   <title>:        book or site title
 *   [author]:       author name (omit for sites)
 *   [url]:          BookLooky book URL or site URL (printed as the last line)
 *
 * Prints the emoji summary to stdout.
 */
const fs = require('fs');

const EMOJI_LINES = [
  { key: 'violence', label: '💥Violence' },
  { key: 'romance', label: '❤️Love & Romance' },
  { key: 'mentalHealth', label: '🧠Mental Health' },
  { key: 'fantasy', label: '🧙Fantasy' },
  { key: 'language', label: '💬Language' },
  { key: 'substanceUse', label: '🍷Substance Use' },
  { key: 'lgbtq', label: '🏳️‍🌈Representation' },
  { key: 'fear', label: '😨Fear / Horror' },
  { key: 'sciFi', label: 'sciFi' },
  { key: 'disability', label: 'disability' },
];

function main() {
  const [, , reportPath, title, author, url] = process.argv;
  if (!reportPath || !title) {
    console.error('Usage: node format-emoji-summary.js <report.json> <title> [author] [url]');
    process.exit(1);
  }

  const raw = JSON.parse(fs.readFileSync(reportPath, 'utf8'));
  // contentAnalysis has flat numeric ratings; fall back to report.ratings.*.rating
  const ca = raw.contentAnalysis || {};
  const rr = (raw.report && raw.report.ratings) || {};
  function ratingFor(key) {
    if (typeof ca[key] === 'number') return ca[key];
    if (rr[key] && typeof rr[key].rating === 'number') return rr[key].rating;
    return 0;
  }

  const lines = [];
  lines.push('BookLooky Rating for:');
  lines.push('');
  const byLine = author ? ` by ${author}` : '';
  lines.push(`📚 "${title}"${byLine}`);
  lines.push('');
  lines.push('Looky Rating System (LRS)');
  for (const { key, label } of EMOJI_LINES) {
    lines.push(`•${label}: ${ratingFor(key)}/5`);
  }
  lines.push('');
  if (url) lines.push(url);

  console.log(lines.join('\n'));
}

main();
