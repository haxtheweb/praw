#!/usr/bin/env node
/**
 * Build scoped rule exports from RULES.md and validate for duplicates.
 *
 * Parses praw/RULES.md where each rule is:
 *   ### Title
 *   - **Rule ID**: `id`
 *   - **Scope**: `global` | `webcomponents` | `haxcms` | `design-system`
 *   - **Content**: <rule text>
 *
 * Emits into praw/exports/:
 *   - rules-global.json    — the global-scope rules only (minimal always-on set
 *                            to sync into Warp's Global Rules store).
 *   - rules-by-scope.json  — all rules grouped by scope (audit + regenerating
 *                            the subdirectory WARP.md files).
 *   - rules-summary.json   — counts per scope + duplicate report.
 *
 * Validation (exit code 2 on warnings):
 *   - duplicate Rule IDs
 *   - duplicate normalized content (same rule text under different IDs)
 *   - missing/invalid Scope on any rule
 *   - unknown scope value
 *
 * No external dependencies — Node built-ins only (praw is not a node project).
 * Run: node scripts/build-rules.js
 */
'use strict';

const fs = require('fs');
const path = require('path');

const VALID_SCOPES = new Set(['global', 'webcomponents', 'haxcms', 'design-system']);

const prawRoot = path.resolve(__dirname, '..');
const rulesPath = path.join(prawRoot, 'RULES.md');
const exportsDir = path.join(prawRoot, 'exports');

function die(msg) {
  console.error('build-rules: ' + msg);
  process.exit(1);
}

/**
 * Normalize rule content for duplicate detection:
 * lowercase, collapse all whitespace, strip non-alphanumeric chars.
 */
function normalizeContent(text) {
  return String(text)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, ' ')
    .trim();
}

function parseRules(text) {
  const rules = [];
  const lines = text.split(/\r?\n/);
  let currentCategory = '';
  let currentTitle = '';
  let currentRule = null;
  // One ### heading may carry multiple Rule ID/Content pairs (legacy shape).
  // Each `- **Rule ID**: \`x\`` starts a new rule record; Scope/Content attach
  // to the most recent rule. A new ## or ### flushes the pending rule.
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (/^##\s/.test(line)) {
      if (currentRule) rules.push(currentRule);
      currentRule = null;
      currentCategory = line.replace(/^##\s+/, '').replace(/^[^\w\s]+\s*/, '').trim();
      continue;
    }
    if (/^###\s/.test(line)) {
      if (currentRule) rules.push(currentRule);
      currentRule = null;
      currentTitle = line.replace(/^###\s+/, '').trim();
      continue;
    }
    const idMatch = line.match(/^- \*\*Rule ID\*\*:\s*`([^`]+)`/);
    if (idMatch) {
      if (currentRule) rules.push(currentRule);
      currentRule = { title: currentTitle, category: currentCategory, id: idMatch[1], scope: null, content: null, line: i + 1 };
      continue;
    }
    const scopeMatch = line.match(/^- \*\*Scope\*\*:\s*`?([^`]+?)`?\s*$/);
    if (scopeMatch && currentRule) { currentRule.scope = scopeMatch[1].trim(); continue; }
    const contentMatch = line.match(/^- \*\*Content\*\*:\s*(.*)$/);
    if (contentMatch && currentRule) { currentRule.content = contentMatch[1].trim(); continue; }
  }
  if (currentRule) rules.push(currentRule);
  return rules.filter(function (r) { return r.id || r.content; });
}

function main() {
  let text;
  try {
    text = fs.readFileSync(rulesPath, 'utf8');
  } catch (e) {
    die('could not read ' + rulesPath + ': ' + e.message);
  }

  const rules = parseRules(text);
  if (rules.length === 0) {
    die('no rules parsed from ' + rulesPath + ' — check the ### / Rule ID / Content format');
  }

  const warnings = [];

  // Validate every rule has id + scope + content
  rules.forEach(function (r) {
    if (!r.id) {
      warnings.push('rule "' + r.title + '" (line ' + r.line + ') has no Rule ID');
    }
    if (!r.scope) {
      warnings.push('rule "' + r.title + '" (' + r.id + ', line ' + r.line + ') has no Scope');
    } else if (!VALID_SCOPES.has(r.scope)) {
      warnings.push('rule "' + r.title + '" (' + r.id + ') has unknown scope "' + r.scope + '"');
    }
    if (!r.content) {
      warnings.push('rule "' + r.title + '" (' + r.id + ', line ' + r.line + ') has no Content');
    }
  });

  // Duplicate Rule IDs
  const idCounts = {};
  rules.forEach(function (r) { if (r.id) idCounts[r.id] = (idCounts[r.id] || 0) + 1; });
  Object.keys(idCounts).forEach(function (id) {
    if (idCounts[id] > 1) {
      warnings.push('duplicate Rule ID "' + id + '" appears ' + idCounts[id] + ' times');
    }
  });

  // Duplicate normalized content (same text, different IDs)
  const contentMap = {};
  rules.forEach(function (r) {
    if (!r.content) return;
    const norm = normalizeContent(r.content);
    if (!contentMap[norm]) contentMap[norm] = [];
    contentMap[norm].push(r.id || r.title);
  });
  Object.keys(contentMap).forEach(function (norm) {
    if (contentMap[norm].length > 1) {
      warnings.push('duplicate content under IDs: ' + contentMap[norm].join(', '));
    }
  });

  // Group by scope (hyphen is fine in a JSON key, declare literally)
  const byScope = { global: [], webcomponents: [], haxcms: [], 'design-system': [] };
  rules.forEach(function (r) {
    if (r.scope && byScope[r.scope]) byScope[r.scope].push(r);
  });

  // Emit exports
  fs.mkdirSync(exportsDir, { recursive: true });

  const clean = function (r) {
    return { id: r.id, title: r.title, category: r.category, content: r.content };
  };

  fs.writeFileSync(
    path.join(exportsDir, 'rules-global.json'),
    JSON.stringify({ scope: 'global', count: byScope.global.length, rules: byScope.global.map(clean) }, null, 2) + '\n'
  );
  fs.writeFileSync(
    path.join(exportsDir, 'rules-by-scope.json'),
    JSON.stringify(
      Object.keys(byScope).map(function (s) {
        return { scope: s, count: byScope[s].length, rules: byScope[s].map(clean) };
      }),
      null, 2
    ) + '\n'
  );

  const summary = {
    totalRules: rules.length,
    byScope: Object.keys(byScope).map(function (s) {
      return { scope: s, count: byScope[s].length };
    }),
    duplicateIds: Object.keys(idCounts).filter(function (id) { return idCounts[id] > 1; }),
    duplicateContentGroups: Object.keys(contentMap).filter(function (n) { return contentMap[n].length > 1; }).map(function (n) { return contentMap[n]; }),
    warnings: warnings
  };
  fs.writeFileSync(
    path.join(exportsDir, 'rules-summary.json'),
    JSON.stringify(summary, null, 2) + '\n'
  );

  // Console report
  console.log('build-rules: parsed ' + rules.length + ' rules from ' + path.relative(prawRoot, rulesPath));
  summary.byScope.forEach(function (s) {
    console.log('  ' + s.scope + ': ' + s.count);
  });
  if (warnings.length > 0) {
    console.warn('  warnings (' + warnings.length + '):');
    warnings.forEach(function (w) { console.warn('    - ' + w); });
    process.exit(2);
  }
  console.log('  OK: no duplicate IDs, no duplicate content, all scopes valid');
}

main();
