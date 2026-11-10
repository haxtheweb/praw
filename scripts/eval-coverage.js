#!/usr/bin/env node
/**
 * Report how much agent-loaded content praw has and how much of it is backed
 * by evals (rule "Rules and Skills Earn Their Tokens", 09255ba6…, tracking
 * https://github.com/haxtheweb/issues/issues/3298).
 *
 * For each skill under skills/<name>/SKILL.md it reports:
 *   - lines in SKILL.md
 *   - number of cases in evals/evals.json (if any)
 *   - how many of those cases record `baseline_behavior`, i.e. what an agent
 *     without the skill does; a case without it shows the skill works, not
 *     that it changes anything
 * plus the line count of RULES.md and the totals.
 *
 * Report-only: always exits 0 unless the files cannot be read, so it can feed
 * a weekly report or a trimming pass without blocking anything.
 *
 *   node scripts/eval-coverage.js          # table
 *   node scripts/eval-coverage.js --json   # machine-readable
 *
 * No external dependencies — Node built-ins only (praw is not a node project).
 */
'use strict';

const fs = require('fs');
const path = require('path');

const prawRoot = path.resolve(__dirname, '..');
const skillsDir = path.join(prawRoot, 'skills');
const asJson = process.argv.indexOf('--json') !== -1;

function countLines(file) {
  const text = fs.readFileSync(file, 'utf8');
  if (text.length === 0) return 0;
  return text.split('\n').length - (text.charAt(text.length - 1) === '\n' ? 1 : 0);
}

const rows = [];
fs.readdirSync(skillsDir).sort().forEach(function (name) {
  const skillMd = path.join(skillsDir, name, 'SKILL.md');
  if (!fs.existsSync(skillMd)) return;
  const row = { skill: name, lines: countLines(skillMd), evals: 0, withBaseline: 0, error: null };
  const evalsFile = path.join(skillsDir, name, 'evals', 'evals.json');
  if (fs.existsSync(evalsFile)) {
    try {
      const data = JSON.parse(fs.readFileSync(evalsFile, 'utf8'));
      const cases = data && Array.isArray(data.evals) ? data.evals : [];
      row.evals = cases.length;
      row.withBaseline = cases.filter(function (c) {
        return c && typeof c.baseline_behavior === 'string' && c.baseline_behavior.trim() !== '';
      }).length;
    } catch (err) {
      row.error = 'evals.json: ' + err.message;
    }
  }
  rows.push(row);
});

const rulesLines = countLines(path.join(prawRoot, 'RULES.md'));
const skillLines = rows.reduce(function (sum, r) { return sum + r.lines; }, 0);
const covered = rows.filter(function (r) { return r.evals > 0; });
const baselined = rows.filter(function (r) { return r.withBaseline > 0; });
const summary = {
  rulesLines: rulesLines,
  skillLines: skillLines,
  totalLines: rulesLines + skillLines,
  skills: rows.length,
  skillsWithEvals: covered.length,
  skillsWithBaseline: baselined.length,
  linesWithoutEvals: rows.filter(function (r) { return r.evals === 0; }).reduce(function (sum, r) { return sum + r.lines; }, 0)
};

if (asJson) {
  console.log(JSON.stringify({ summary: summary, skills: rows }, null, 2));
  process.exit(0);
}

const width = rows.reduce(function (w, r) { return Math.max(w, r.skill.length); }, 5);
function pad(s, n) { s = String(s); return s + ' '.repeat(Math.max(0, n - s.length)); }
console.log(pad('skill', width) + '  lines  evals  baseline');
rows.forEach(function (r) {
  console.log(pad(r.skill, width) + '  ' + pad(r.lines, 5) + '  ' + pad(r.evals, 5) + '  ' + r.withBaseline + (r.error ? '  (' + r.error + ')' : ''));
});
console.log('');
console.log('RULES.md: ' + rulesLines + ' lines; SKILL.md files: ' + skillLines + ' lines; total ' + summary.totalLines);
console.log(covered.length + ' of ' + rows.length + ' skills have evals; ' + baselined.length + ' record baseline_behavior');
console.log(summary.linesWithoutEvals + ' SKILL.md lines have no eval behind them');
