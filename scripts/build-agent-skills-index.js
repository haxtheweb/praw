#!/usr/bin/env node
/**
 * Build the .well-known/agent-skills/index.json discovery index for praw.
 *
 * Implements the agentskills.io discovery spec v0.2.0:
 *   https://github.com/cloudflare/agent-skills-discovery-rfc
 *
 * Scans praw/skills/ (each subdir holding a SKILL.md), reads YAML frontmatter for
 * name + description, computes sha256 digests, and writes
 * .well-known/agent-skills/index.json with:
 *   { "$schema": "...", "skills": [ { name, type, description, url, digest, files[] } ] }
 *
 * - url is relative ("{name}/SKILL.md") so it resolves against each index's own
 *   location per RFC 3986, whether served from praw, the boilerplate, or a site.
 * - files[] (non-standard) enumerates auxiliary sibling files (references/**, etc.)
 *   with per-file sha256 digests, so the HAXcms managed-file copy step can copy +
 *   verify every declared file without recursion. Spec clients ignore files[].
 *
 * No external dependencies — Node built-ins only (praw is not a node project).
 * Run: node scripts/build-agent-skills-index.js
 */
'use strict';

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const SCHEMA_URI = 'https://schemas.agentskills.io/discovery/0.2.0/schema.json';
const NAME_RE = /^[a-z0-9]([a-z0-9-]{0,62}[a-z0-9])?$/;
const MAX_DESC = 1024;

const prawRoot = path.resolve(__dirname, '..');
const skillsDir = path.join(prawRoot, 'skills');
const outDir = path.join(prawRoot, '.well-known', 'agent-skills');
const indexPath = path.join(outDir, 'index.json');

function sha256(buf) {
  return 'sha256:' + crypto.createHash('sha256').update(buf).digest('hex');
}

/**
 * Minimal YAML frontmatter parser for the fields we need (name, description).
 * Handles folded (>) and literal (|) block scalars plus simple key: value lines.
 * Nested keys (metadata:) are ignored — we do not need them.
 */
function parseFrontmatter(text) {
  const fmMatch = text.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!fmMatch) return null;
  const lines = fmMatch[1].split(/\r?\n/);
  const out = {};
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    const kv = line.match(/^([A-Za-z][\w-]*)\s*:\s*(.*)$/);
    if (kv) {
      const key = kv[1];
      let value = kv[2];
      if (value === '>' || value === '|') {
        const fold = value === '>';
        const block = [];
        i++;
        while (i < lines.length && (/^[ \t]+/.test(lines[i]) || lines[i].trim() === '')) {
          block.push(lines[i].replace(/^[ \t]+/, ''));
          i++;
        }
        value = fold ? block.join(' ').replace(/\s+/g, ' ').trim() : block.join('\n').trim();
        out[key] = value;
        continue;
      }
      out[key] = value.trim();
    }
    i++;
  }
  return out;
}

/**
 * Recursively list auxiliary files in a skill dir (everything except SKILL.md),
 * returned as { path, full } with path relative to the skill dir (posix separators).
 */
function walkAuxFiles(skillDir) {
  const found = [];
  function walk(dir, rel) {
    let entries;
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch (e) {
      return;
    }
    for (let e = 0; e < entries.length; e++) {
      const entry = entries[e];
      if (entry.name === 'SKILL.md') continue;
      const full = path.join(dir, entry.name);
      const relPath = rel ? rel + '/' + entry.name : entry.name;
      if (entry.isDirectory()) {
        walk(full, relPath);
      } else if (entry.isFile()) {
        found.push({ path: relPath, full: full });
      }
    }
  }
  walk(skillDir, '');
  return found;
}

const skills = [];
const warnings = [];

let dirs;
try {
  dirs = fs.readdirSync(skillsDir, { withFileTypes: true });
} catch (err) {
  console.error('Could not read skills dir ' + skillsDir + ': ' + err.message);
  process.exit(1);
}

for (let d = 0; d < dirs.length; d++) {
  const entry = dirs[d];
  if (!entry.isDirectory()) continue;
  const skillDir = path.join(skillsDir, entry.name);
  const skillMdPath = path.join(skillDir, 'SKILL.md');
  if (!fs.existsSync(skillMdPath)) {
    warnings.push('skipped ' + entry.name + '/ (no SKILL.md)');
    continue;
  }
  const content = fs.readFileSync(skillMdPath);
  const fm = parseFrontmatter(content.toString('utf8'));
  const name = fm && fm.name ? fm.name : entry.name;
  const description = fm && fm.description ? fm.description : '';

  if (!NAME_RE.test(name)) {
    warnings.push('INVALID NAME "' + name + '" in ' + entry.name + '/ (must be 1-64 chars, lowercase alnum + hyphens, no leading/trailing hyphen)');
  }
  if (description.length > MAX_DESC) {
    warnings.push('LONG DESCRIPTION (' + description.length + ' > ' + MAX_DESC + ') in ' + name);
  }
  if (!description) {
    warnings.push('MISSING DESCRIPTION in ' + name);
  }

  const aux = walkAuxFiles(skillDir);
  const files = aux
    .map(function (a) {
      return { path: a.path, digest: sha256(fs.readFileSync(a.full)) };
    })
    .sort(function (a, b) {
      return a.path.localeCompare(b.path);
    });

  const skill = {
    name: name,
    type: 'skill-md',
    description: description,
    url: name + '/SKILL.md',
    digest: sha256(content)
  };
  if (files.length > 0) {
    skill.files = files;
  }
  skills.push(skill);
}

skills.sort(function (a, b) {
  return a.name.localeCompare(b.name);
});

const index = { '$schema': SCHEMA_URI, skills: skills };

fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(indexPath, JSON.stringify(index, null, 2) + '\n');

console.log('Wrote ' + path.relative(prawRoot, indexPath) + ' (' + skills.length + ' skills)');
if (warnings.length > 0) {
  console.warn('\nWarnings:');
  warnings.forEach(function (w) {
    console.warn('  - ' + w);
  });
  process.exit(2);
}
