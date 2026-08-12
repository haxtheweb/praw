#!/usr/bin/env node
/**
 * Ports the `candidatesByCategory` ranking loop from
 * `finalizeOfficialScanFromChunkScans()` in `src/analyzer.ts`. If that
 * ranking logic changes in the library, update this script to match.
 *
 * Given all per-chunk segment-scan results, ranks candidate chunks per
 * category by signal count (descending) and returns the top 3 chunk
 * indexes per category — the same chunks `extractForCategory()` would join
 * together for the category-focus pass.
 *
 * Usage: node rank-candidate-chunks.js <scansDir>
 *   <scansDir> must contain one JSON file per chunk scan, each matching the
 *   OfficialScanChunkScanResult shape: { chunkIndex, signals, notes? }.
 * Prints JSON: { "<category>": [chunkIndex, chunkIndex, chunkIndex], ... }
 */
const fs = require('fs');
const path = require('path');

const OFFICIAL_SCAN_CATEGORIES = [
  'violence',
  'romance',
  'mentalHealth',
  'language',
  'substanceUse',
  'fear',
  'fantasy',
  'lgbtq',
  'sciFi',
  'disability',
];

function loadScans(scansDir) {
  const files = fs.readdirSync(scansDir).filter((f) => f.endsWith('.json'));
  const scans = files.map((f) => JSON.parse(fs.readFileSync(path.join(scansDir, f), 'utf8')));
  scans.sort((a, b) => a.chunkIndex - b.chunkIndex);
  return scans;
}

function rankCandidateChunks(scans) {
  const candidatesByCategory = Object.fromEntries(OFFICIAL_SCAN_CATEGORIES.map((cat) => [cat, new Map()]));

  for (const scan of scans) {
    for (const cat of OFFICIAL_SCAN_CATEGORIES) {
      const count = scan.signals && scan.signals[cat] ? scan.signals[cat].length : 0;
      if (count > 0) {
        const m = candidatesByCategory[cat];
        m.set(scan.chunkIndex, (m.get(scan.chunkIndex) || 0) + count);
      }
    }
  }

  const ranked = {};
  for (const cat of OFFICIAL_SCAN_CATEGORIES) {
    ranked[cat] = Array.from(candidatesByCategory[cat].entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 3)
      .map(([chunkIndex]) => chunkIndex);
  }
  return ranked;
}

function main() {
  const [, , scansDir] = process.argv;
  if (!scansDir) {
    console.error('Usage: node rank-candidate-chunks.js <scansDir>');
    process.exit(1);
  }

  const scans = loadScans(scansDir);
  if (scans.length === 0) {
    console.error(`Error: no chunk scan JSON files found in ${scansDir}`);
    process.exit(1);
  }

  console.log(JSON.stringify(rankCandidateChunks(scans), null, 2));
}

main();
