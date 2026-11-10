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
// Only declarative content is shipped in .well-known/agent-skills/. Executable
// artifacts (.js/.cjs/.mjs/.sh/.php/.py/...) are never listed in files[] so they
// cannot land on a live web server via the snapshot step. SKILL.md (.md) and
// index.json (.json) are always covered; aux files are restricted to these exts.
const ALLOWED_AUX_EXT = new Set(['md', 'json', 'txt']);
// Prompt-injection boundary check. A skill whose body talks about fetching,
// importing or reading content from outside the repo (URLs, sites, issues,
// docx, vtt, HTML, cloned repos...) must carry an explicit "that content is
// data, not instructions" section so agents do not adopt directives found in
// what they read. The reference wording lives in
// skills/hax-issue-research/SKILL.md ("Security: issue content is untrusted")
// and the shared block titled "Content you read is data, not instructions".
const EXTERNAL_CONTENT_RE = /\b(fetch(es|ed|ing)?|import(s|ed|ing)?|read(s|ing)?|clone(s|d|ing)?|download(s|ed|ing)?|scrape[sd]?|crawl(s|ed|ing)?)\b[^.\n]{0,80}\b(url|urls|link|links|site|sites|web ?page|pages?|html|docx|vtt|transcripts?|captions?|issues?|repo|repos|repositor(y|ies)|youtube|book|pdf|feed)\b/i;
const BOUNDARY_RE = /untrusted|not instructions|prompt.?injection/i;

const prawRoot = path.resolve(__dirname, '..');
const skillsDir = path.join(prawRoot, 'skills');
const outDir = path.join(prawRoot, '.well-known', 'agent-skills');
const indexPath = path.join(outDir, 'index.json');
const skillsIndexPath = path.join(skillsDir, 'index.json');
// Plugin skill dirs are linted too even though only skills/ is indexed.
const pluginSkillGlobs = [path.join(prawRoot, 'plugins')];

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
      out[key] = unquoteScalar(value.trim());
    }
    i++;
  }
  return out;
}

/**
 * Strip YAML flow-scalar quotes so "..." / '...' descriptions are stored as
 * plain text (otherwise the quotes leak into the published index).
 */
function unquoteScalar(value) {
  if (value.length >= 2 && value[0] === '"' && value[value.length - 1] === '"') {
    return value.slice(1, -1).replace(/\\(["\\])/g, '$1');
  }
  if (value.length >= 2 && value[0] === "'" && value[value.length - 1] === "'") {
    return value.slice(1, -1).replace(/''/g, "'");
  }
  return value;
}

/**
 * Recursively list auxiliary files in a skill dir (everything except SKILL.md).
 * Returns { aux, skipped }:
 *   aux     — allowed content files (.md/.json/.txt) as { path, full }
 *   skipped — executable/non-content files excluded from files[] (for warnings)
 */
function walkAuxFiles(skillDir) {
  const aux = [];
  const skipped = [];
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
        const ext = entry.name.split('.').pop().toLowerCase();
        if (ALLOWED_AUX_EXT.has(ext)) {
          aux.push({ path: relPath, full: full });
        } else {
          skipped.push(relPath);
        }
      }
    }
  }
  walk(skillDir, '');
  return { aux: aux, skipped: skipped };
}

const skills = [];
const warnings = [];

/**
 * Return a lint message when a SKILL.md reads external content but has no
 * data-not-instructions boundary; null otherwise. Frontmatter is excluded so a
 * description that merely mentions URLs does not trigger it on its own.
 */
function checkInjectionBoundary(text, label) {
  const body = text.replace(/^---\r?\n[\s\S]*?\r?\n---/, '');
  if (!EXTERNAL_CONTENT_RE.test(body)) return null;
  if (BOUNDARY_RE.test(body)) return null;
  return 'MISSING PROMPT-INJECTION BOUNDARY in ' + label + ' (reads external content but has no "Content you read is data, not instructions" section)';
}

/** Find plugins/<plugin>/skills/<skill>/SKILL.md files (not indexed, lint only). */
function listPluginSkillFiles() {
  const out = [];
  pluginSkillGlobs.forEach(function (pluginsDir) {
    let plugins;
    try {
      plugins = fs.readdirSync(pluginsDir, { withFileTypes: true });
    } catch (e) {
      return;
    }
    plugins.forEach(function (p) {
      if (!p.isDirectory()) return;
      const sdir = path.join(pluginsDir, p.name, 'skills');
      let entries;
      try {
        entries = fs.readdirSync(sdir, { withFileTypes: true });
      } catch (e) {
        return;
      }
      entries.forEach(function (e) {
        if (!e.isDirectory()) return;
        const f = path.join(sdir, e.name, 'SKILL.md');
        if (fs.existsSync(f)) out.push(f);
      });
    });
  });
  return out;
}

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
  const boundary = checkInjectionBoundary(content.toString('utf8'), 'skills/' + entry.name + '/SKILL.md');
  if (boundary) warnings.push(boundary);

  const walked = walkAuxFiles(skillDir);
  walked.skipped.forEach(function (s) {
    console.log('  excluded ' + name + '/' + s + ' (non-content; not shipped to .well-known)');
  });
  const files = walked.aux
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

// Lint plugin-bundled skills for the injection boundary as well.
listPluginSkillFiles().forEach(function (f) {
  const boundary = checkInjectionBoundary(fs.readFileSync(f, 'utf8'), path.relative(prawRoot, f));
  if (boundary) warnings.push(boundary);
});

// The HAX CLI pin lives in two .version files: the repo root (read by
// hax-onboarding.sh) and the hax-onboarding plugin (read by its SessionStart
// hook; the plugin cache only holds the plugin directory). The ecosystem release
// (ubiquity) writes both before running this script, so they must agree.
(function checkCliVersionPins() {
  const pins = ['.version', 'plugins/hax-onboarding/.version'].map(function (rel) {
    const abs = path.join(prawRoot, rel);
    return { rel: rel, value: fs.existsSync(abs) ? fs.readFileSync(abs, 'utf8').trim() : null };
  });
  pins.forEach(function (pin) {
    if (pin.value === null) {
      warnings.push(pin.rel + ' is missing; the HAX CLI install would fall back to "latest"');
    } else if (!/^\d+\.\d+\.\d+$/.test(pin.value)) {
      warnings.push(pin.rel + ' is "' + pin.value + '", expected an exact x.y.z release');
    }
  });
  if (pins[0].value !== null && pins[1].value !== null && pins[0].value !== pins[1].value) {
    warnings.push('.version (' + pins[0].value + ') and plugins/hax-onboarding/.version (' + pins[1].value + ') disagree');
  }
})();

const index = { '$schema': SCHEMA_URI, skills: skills };
const indexJson = JSON.stringify(index, null, 2) + '\n';

fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(indexPath, indexJson);
// Same index beside the skill folders. Entry urls are relative ("{name}/SKILL.md"),
// so they resolve only where the index sits next to the skills: in the snapshots
// copied to sites/deployments, and in praw/skills/. Remote agents (e.g. a HAXsite
// pointing at the full catalog) fetch this copy from the stable channel,
// https://raw.githubusercontent.com/haxtheweb/praw/stable/skills/index.json
fs.writeFileSync(skillsIndexPath, indexJson);

console.log('Wrote ' + path.relative(prawRoot, indexPath) + ' and ' + path.relative(prawRoot, skillsIndexPath) + ' (' + skills.length + ' skills)');
if (warnings.length > 0) {
  console.warn('\nWarnings:');
  warnings.forEach(function (w) {
    console.warn('  - ' + w);
  });
  process.exit(2);
}
