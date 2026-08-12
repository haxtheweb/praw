#!/usr/bin/env node
/**
 * Ports `romanceRatingWithInnuendoRule` (src/scoring-rules.ts) and
 * `reconcileCategoryEvidence` / `excerptsFromChunkSignals` (src/analyzer.ts).
 * If those library functions change, update this script to match.
 *
 * Applies the deterministic post-processing rules on top of one category's
 * focus-pass result:
 *   1. Force romance rating to >= 1 if the rationale discusses innuendo-like
 *      content but the rating stayed 0.
 *   2. Require every positive rating to have at least one validated
 *      excerpt+explanation. Fall back to segment-scan chunk signals if the
 *      focus pass produced none. Downgrade to 0 (with a note) if still none.
 *
 * Usage: node reconcile-evidence.js <focusResult.json> <scansDir>
 *   <focusResult.json>: { category, rating, rationale, excerpts: [{excerpt, explanation, locationHint?}] }
 *   <scansDir>: directory of per-chunk segment-scan JSON files (same as rank-candidate-chunks.js)
 * Prints JSON: { category, rating, excerpts: [...], downgradedForMissingEvidence }
 */
const fs = require('fs');
const path = require('path');

const REASONING_INNUENDO_HINTS = [
  'innuendo',
  'double entendre',
  'euphemis',
  'sexual tension',
  'sexual subtext',
  'implied sexual',
  'flirtation',
  'flirting',
  'sexual humor',
  'off-color',
];

function reasoningImpliesInnuendoDiscussed(text) {
  const t = text.toLowerCase();
  for (const hint of REASONING_INNUENDO_HINTS) {
    const index = t.indexOf(hint);
    if (index !== -1) {
      const preceding = t.substring(Math.max(0, index - 45), index);
      if (!preceding.match(/\b(no|not|without|lack of|none|zero)\b/)) {
        return true;
      }
    }
  }
  return false;
}

/** Enforce romance >= 1 when the rationale admits innuendo-like content but the rating stayed 0. */
function romanceRatingWithInnuendoRule(rating, rationaleLike) {
  if (rating !== 0) return rating;
  if (reasoningImpliesInnuendoDiscussed(rationaleLike)) return 1;
  return rating;
}

function excerptsFromChunkSignals(category, scans, max) {
  const out = [];
  const seen = new Set();
  for (const scan of scans) {
    const signals = (scan.signals && scan.signals[category]) || [];
    for (const s of signals) {
      const excerpt = String(s.quote || '').trim();
      const explanation = String(s.why || '').trim();
      if (!excerpt || !explanation) continue;
      const key = excerpt.slice(0, 280);
      if (seen.has(key)) continue;
      seen.add(key);
      out.push({ excerpt, explanation });
      if (out.length >= max) return out;
    }
  }
  return out;
}

function reconcileCategoryEvidence(focused, scansSorted) {
  // First, apply the innuendo backstop (only meaningful for romance, but
  // harmless for other categories since their rationale won't match the hints).
  const rating = romanceRatingWithInnuendoRule(focused.rating, focused.rationale || '');
  const f = { ...focused, rating };

  if (f.rating <= 0) {
    return { ...f, excerpts: [], downgradedForMissingEvidence: false };
  }

  const excerpts = (f.excerpts || []).slice(0, 5).filter((e) => e.excerpt && e.explanation);
  if (excerpts.length > 0) {
    return { ...f, excerpts, downgradedForMissingEvidence: false };
  }

  const fromChunks = excerptsFromChunkSignals(f.category, scansSorted, 5);
  if (fromChunks.length > 0) {
    return { ...f, excerpts: fromChunks, downgradedForMissingEvidence: false };
  }

  return { ...f, rating: 0, excerpts: [], downgradedForMissingEvidence: true };
}

function loadScans(scansDir) {
  const files = fs.readdirSync(scansDir).filter((f) => f.endsWith('.json'));
  const scans = files.map((f) => JSON.parse(fs.readFileSync(path.join(scansDir, f), 'utf8')));
  scans.sort((a, b) => a.chunkIndex - b.chunkIndex);
  return scans;
}

function main() {
  const [, , focusResultPath, scansDir] = process.argv;
  if (!focusResultPath || !scansDir) {
    console.error('Usage: node reconcile-evidence.js <focusResult.json> <scansDir>');
    process.exit(1);
  }

  const focused = JSON.parse(fs.readFileSync(focusResultPath, 'utf8'));
  const scansSorted = loadScans(scansDir);
  const reconciled = reconcileCategoryEvidence(focused, scansSorted);

  console.log(JSON.stringify(reconciled, null, 2));
}

main();
