#!/usr/bin/env node
/**
 * Ports `dedupeExcerpts`, `normalizeOfficialScanReport` (src/report-utils.ts),
 * `normalizeOfficialScanMinimumAge`, and `normalizeAgeRecommendation`
 * (src/age-recommendation.ts). If those library functions change, update
 * this script to match.
 *
 * Assembles the final OfficialScanReport from the 10 reconciled category
 * results plus the age-recommendation JSON, deduping excerpts and clamping
 * values into range exactly like the library's own normalization.
 *
 * Usage: node build-report.js <reconciledDir> <ageRecommendation.json> [out.json]
 *   <reconciledDir>: directory of per-category reconcile-evidence.js output
 *                     JSON files (one per category, filename doesn't matter,
 *                     each must have a "category" field).
 *   <ageRecommendation.json>: raw JSON returned from the age-recommendation prompt.
 * Prints the final report JSON to stdout, and writes it to [out.json] if given.
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

const AGE_REASON_TITLES = [
  'Protagonist age & voice',
  'Content intensity (LRS)',
  'Tone & thematic maturity',
  'Comparable titles',
  'Edge cases & author notes',
];

const DEFAULT_ZERO_NOTE = 'No meaningful results discovered for this rating.';
const NOTE_RATING_ZERO_NO_VERIFIED_EVIDENCE =
  'No quotable transcript excerpts with explanations met our validation rules for this category, so the rating was set to 0.';

function clampInt0to5(n) {
  const x = Number(n);
  if (!Number.isFinite(x)) return 0;
  return Math.max(0, Math.min(5, Math.round(x)));
}

function clamp01(n) {
  const x = Number(n);
  if (!Number.isFinite(x)) return 0;
  return Math.max(0, Math.min(1, x));
}

function normalizeMinimumAge(value, fallback) {
  const n = Number(value);
  if (!Number.isFinite(n)) return fallback !== undefined ? fallback : 8;
  const rounded = Math.ceil(n);
  return Math.max(0, Math.min(rounded, 25));
}

function confidenceLabelToScore(label) {
  const s = String(label || '').trim().toLowerCase();
  if (s === 'high') return 0.85;
  if (s === 'medium') return 0.65;
  if (s === 'low') return 0.45;
  return 0.65;
}

function normalizeExcerptKey(text) {
  return String(text || '').replace(/\s+/g, ' ').trim().toLowerCase();
}

function dedupeExcerpts(excerpts) {
  const seen = new Set();
  const out = [];
  for (const e of excerpts) {
    const excerpt = String(e.excerpt || '').trim();
    const explanation = String(e.explanation || '').trim();
    if (!excerpt || !explanation) continue;
    const key = normalizeExcerptKey(excerpt);
    if (seen.has(key)) continue;
    seen.add(key);
    out.push({
      excerpt,
      explanation,
      locationHint: String(e.locationHint || '').trim() || undefined,
    });
  }
  return out;
}

function normalizeReason(raw, fallbackTitle) {
  const obj = raw && typeof raw === 'object' ? raw : {};
  const title = String(obj.title || fallbackTitle).trim() || fallbackTitle;
  const text = String(obj.text || obj.body || obj.rationale || '').trim();
  return { title, text };
}

function normalizeAgeRecommendation(raw, fallbackSummary) {
  const reasonsRaw = Array.isArray(raw && raw.reasons) ? raw.reasons : [];
  const reasons = AGE_REASON_TITLES.map((title, i) => {
    const fromRaw = normalizeReason(reasonsRaw[i], title);
    return { title: fromRaw.title || title, text: fromRaw.text };
  });

  const minimumAge = normalizeMinimumAge(raw && raw.minimumAge);
  const reasoningSummary =
    String((raw && raw.reasoningSummary) || '').trim() ||
    String(fallbackSummary || '').trim() ||
    'Age recommendation generated from transcript evidence and LRS ratings.';

  const confidence = ['high', 'medium', 'low'].includes(raw && raw.confidence)
    ? raw.confidence
    : confidenceLabelToScore(raw && raw.confidence) >= 0.75
      ? 'high'
      : confidenceLabelToScore(raw && raw.confidence) >= 0.55
        ? 'medium'
        : 'low';

  return {
    minimumAge,
    marketCategory: String((raw && raw.marketCategory) || '').trim() || 'General audience',
    confidence,
    reasons,
    detailedJustification: String((raw && raw.detailedJustification) || '').trim() || reasoningSummary,
    authorNotes: String((raw && raw.authorNotes) || '').trim() || undefined,
    reasoningSummary,
  };
}

function loadReconciled(reconciledDir) {
  const files = fs.readdirSync(reconciledDir).filter((f) => f.endsWith('.json'));
  const byCategory = {};
  for (const f of files) {
    const data = JSON.parse(fs.readFileSync(path.join(reconciledDir, f), 'utf8'));
    if (data && data.category) byCategory[data.category] = data;
  }
  return byCategory;
}

function buildReport(reconciledByCategory, ageRaw) {
  const ratings = {};
  for (const cat of OFFICIAL_SCAN_CATEGORIES) {
    const entry = reconciledByCategory[cat];
    const rating = clampInt0to5(entry && entry.rating);
    if (rating > 0) {
      ratings[cat] = {
        rating,
        excerpts: dedupeExcerpts(Array.isArray(entry.excerpts) ? entry.excerpts : []).slice(0, 5),
      };
    } else {
      const note = entry && entry.downgradedForMissingEvidence ? NOTE_RATING_ZERO_NO_VERIFIED_EVIDENCE : DEFAULT_ZERO_NOTE;
      ratings[cat] = { rating: 0, noteWhenZero: note };
    }
  }

  const ageRecommendation = normalizeAgeRecommendation(ageRaw, '');
  const minimumAge = ageRecommendation.minimumAge;
  const confidence = clamp01(confidenceLabelToScore(ageRecommendation.confidence));

  const report = {
    minimumAge,
    confidence,
    ratings,
    reasoningSummary: ageRecommendation.reasoningSummary || 'Ratings generated from transcript evidence.',
    ageRecommendation,
  };

  const contentAnalysis = {
    violence: clampInt0to5(ratings.violence.rating),
    romance: clampInt0to5(ratings.romance.rating),
    mentalHealth: clampInt0to5(ratings.mentalHealth.rating),
    fantasy: clampInt0to5(ratings.fantasy.rating),
    language: clampInt0to5(ratings.language.rating),
    substanceUse: clampInt0to5(ratings.substanceUse.rating),
    lgbtq: clampInt0to5(ratings.lgbtq.rating),
    fear: clampInt0to5(ratings.fear.rating),
    sciFi: clampInt0to5(ratings.sciFi.rating),
    disability: clampInt0to5(ratings.disability.rating),
    confidence,
    reasoning: report.reasoningSummary,
    minimumAge,
    ageSource: 'ai',
  };

  return { report, contentAnalysis };
}

function main() {
  const [, , reconciledDir, ageRecPath, outPath] = process.argv;
  if (!reconciledDir || !ageRecPath) {
    console.error('Usage: node build-report.js <reconciledDir> <ageRecommendation.json> [out.json]');
    process.exit(1);
  }

  const reconciledByCategory = loadReconciled(reconciledDir);
  const missing = OFFICIAL_SCAN_CATEGORIES.filter((cat) => !reconciledByCategory[cat]);
  if (missing.length > 0) {
    console.error(`Warning: missing reconciled results for categories: ${missing.join(', ')}. Treating as rating 0.`);
  }

  const ageRaw = JSON.parse(fs.readFileSync(ageRecPath, 'utf8'));
  const { report, contentAnalysis } = buildReport(reconciledByCategory, ageRaw);
  const output = JSON.stringify({ report, contentAnalysis }, null, 2);

  if (outPath) {
    fs.writeFileSync(outPath, output, 'utf8');
    console.error(`Wrote final report to ${outPath}`);
  }
  console.log(output);
}

main();
