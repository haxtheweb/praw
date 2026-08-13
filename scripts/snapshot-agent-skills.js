#!/usr/bin/env node
/**
 * Snapshot a curated set of agent skills from praw into a target
 * .well-known/agent-skills/ directory, for the ubiquity build.
 *
 * Usage: node scripts/snapshot-agent-skills.js <setName> <destDir>
 *   <setName>  "site" (10 curated skills -> per-site boilerplate) or
 *              "system" (21 skills -> nodejs/php deployment roots)
 *   <destDir>  absolute target directory, e.g.
 *              ~/haxtheweb/haxcms-nodejs/src/boilerplate/site/.well-known/agent-skills
 *
 * Reads the canonical index.json + agent-skills-sets.json from
 * praw/.well-known/agent-skills/, resolves the set ( "*" = all skills ),
 * then for the destination:
 *   1. removes + recreates destDir (keeps it in sync with praw, no stale skills)
 *   2. writes a filtered index.json ($schema + the set's skills[], preserving files[])
 *   3. copies each skill's SKILL.md + every files[].path from praw/skills/<name>/
 *      into destDir/<name>/, verifying sha256 of every copied byte against the
 *      declared digest (warns on mismatch, continues)
 *
 * Does NOT copy agent-skills-sets.json (build-time input only).
 * No external dependencies — Node built-ins only.
 */
'use strict';

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const prawRoot = path.resolve(__dirname, '..');
const wkDir = path.join(prawRoot, '.well-known', 'agent-skills');
const skillsSrcDir = path.join(prawRoot, 'skills');
const indexPath = path.join(wkDir, 'index.json');
const setsPath = path.join(wkDir, 'agent-skills-sets.json');

// Scoped .htaccess written into every snapshot dest dir. CORS open so
// browser-based agents on other origins can fetch the index + skills; script
// execution hardened off so a slipped-through script can never run server-side.
// The discovery index only ships .md/.json/.txt; this is defense in depth.
// Harmless on Node/static-hosted targets (ignored).
const AGENT_SKILLS_HTACCESS = '# HAXcms Agent Skills discovery (agentskills.io v0.2.0)\n'
  + '# CORS: open so browser-based agents on other origins can fetch the index + skills.\n'
  + '<IfModule mod_headers.c>\n'
  + '  Header set Access-Control-Allow-Origin "*"\n'
  + '  Header set Vary "Origin"\n'
  + '</IfModule>\n'
  + '# Defense in depth: the discovery index only ships .md/.json/.txt, but harden\n'
  + '# so a slipped-through script file can never execute server-side here.\n'
  + '<FilesMatch "\\.(php|phtml|php[3-7]|phps|pht|sh|cgi|pl|py)$">\n'
  + '  php_flag engine off\n'
  + '  RemoveHandler .php .phtml .php3 .php4 .php5 .php7\n'
  + '  SetHandler text/plain\n'
  + '  ForceType text/plain\n'
  + '</FilesMatch>\n';

function sha256(buf) {
  return 'sha256:' + crypto.createHash('sha256').update(buf).digest('hex');
}

function die(msg) {
  console.error('snapshot-agent-skills: ' + msg);
  process.exit(1);
}

// Defense in depth: even if files[] somehow lists a non-content extension,
// never copy it to a web-served destination. Mirrors the generator's allowlist.
const ALLOWED_AUX_EXT = new Set(['md', 'json', 'txt']);

const setName = process.argv[2];
const destDir = process.argv[3];
if (!setName || !destDir) {
  die('usage: node scripts/snapshot-agent-skills.js <setName> <destDir>');
}
if (setName !== 'site' && setName !== 'system') {
  die('unknown set "' + setName + '" (expected "site" or "system")');
}
const destAbs = path.resolve(destDir.replace(/^~(?=[/\\]|$)/, function (m) { return process.env.HOME; }));

let index, sets;
try { index = JSON.parse(fs.readFileSync(indexPath, 'utf8')); }
catch (e) { die('could not read canonical index ' + indexPath + ': ' + e.message); }
try { sets = JSON.parse(fs.readFileSync(setsPath, 'utf8')); }
catch (e) { die('could not read sets ' + setsPath + ': ' + e.message); }

if (!index.skills || !Array.isArray(index.skills)) {
  die('canonical index has no skills[] array');
}
const byName = {};
index.skills.forEach(function (s) { byName[s.name] = s; });

// resolve the set's skill names
let wanted = sets[setName] && sets[setName].skills;
if (!Array.isArray(wanted)) {
  die('set "' + setName + '" has no skills[] array in agent-skills-sets.json');
}
let resolved;
if (wanted.length === 1 && wanted[0] === '*') {
  resolved = index.skills.map(function (s) { return s.name; });
} else {
  resolved = wanted.slice();
}

// validate every name resolves
const missing = resolved.filter(function (n) { return !byName[n]; });
if (missing.length > 0) {
  die('set "' + setName + '" references skills not in the canonical index: ' + missing.join(', '));
}

const filtered = resolved.map(function (n) { return byName[n]; });

// 1. clean + recreate destDir (sync with praw; remove stale skills)
fs.rmSync(destAbs, { recursive: true, force: true });
fs.mkdirSync(destAbs, { recursive: true });

// 2. write filtered index.json (preserve $schema + skills[] with files[])
fs.writeFileSync(
  path.join(destAbs, 'index.json'),
  JSON.stringify({ '$schema': index['$schema'], skills: filtered }, null, 2) + '\n'
);
// 2b. scoped .htaccess: CORS + script-execution hardening for Apache-hosted
// deployments/sites. Harmless on Node/static-hosted targets (ignored).
fs.writeFileSync(path.join(destAbs, '.htaccess'), AGENT_SKILLS_HTACCESS);

// 3. copy each skill's declared files with digest verification
const warnings = [];
let copiedFiles = 0;
let copiedSkills = 0;
filtered.forEach(function (skill) {
  const skillSrc = path.join(skillsSrcDir, skill.name);
  const skillDest = path.join(destAbs, skill.name);
  fs.mkdirSync(skillDest, { recursive: true });

  // SKILL.md (covered by top-level url + digest)
  const skillMdSrc = path.join(skillSrc, 'SKILL.md');
  if (!fs.existsSync(skillMdSrc)) {
    warnings.push(skill.name + ': SKILL.md missing in praw source, skipping skill');
    return;
  }
  const skillMdBytes = fs.readFileSync(skillMdSrc);
  const skillMdDest = path.join(skillDest, 'SKILL.md');
  fs.writeFileSync(skillMdDest, skillMdBytes);
  copiedFiles++;
  if (sha256(skillMdBytes) !== skill.digest) {
    warnings.push(skill.name + '/SKILL.md digest mismatch (index ' + skill.digest + ' vs source)');
  }

  // auxiliary files (references/**, evals/**, etc.) — content extensions only
  (skill.files || []).forEach(function (f) {
    const ext = f.path.split('.').pop().toLowerCase();
    if (!ALLOWED_AUX_EXT.has(ext)) {
      warnings.push(skill.name + '/' + f.path + ' has non-content extension .' + ext + ', skipping (only .md/.json/.txt shipped)');
      return;
    }
    const fSrc = path.join(skillSrc, f.path);
    const fDest = path.join(skillDest, f.path);
    if (!fs.existsSync(fSrc)) {
      warnings.push(skill.name + '/' + f.path + ' missing in praw source, skipping file');
      return;
    }
    fs.mkdirSync(path.dirname(fDest), { recursive: true });
    const fBytes = fs.readFileSync(fSrc);
    fs.writeFileSync(fDest, fBytes);
    copiedFiles++;
    if (sha256(fBytes) !== f.digest) {
      warnings.push(skill.name + '/' + f.path + ' digest mismatch (index ' + f.digest + ' vs source)');
    }
  });
  copiedSkills++;
});

console.log(
  'snapshot-agent-skills: set=' + setName + ' -> ' + destAbs +
  ' (' + copiedSkills + ' skills, ' + copiedFiles + ' files)'
);
if (warnings.length > 0) {
  console.warn('  warnings:');
  warnings.forEach(function (w) { console.warn('    - ' + w); });
  process.exit(2);
}
