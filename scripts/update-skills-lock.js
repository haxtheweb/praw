#!/usr/bin/env node
/**
 * Keep skills-lock.json in step with the SKILL.md files on disk.
 *
 * skills-lock.json records, for each skill it lists, the sha256 of that skill's
 * SKILL.md (the `computedHash` field, hex, no prefix). Stale hashes are worse
 * than none: a consumer that verifies them would reject the current, reviewed
 * content. This script recomputes every entry's hash from the file at
 * `skillPath` and rewrites the lock file. It does not add or remove entries;
 * the set of locked skills is a deliberate choice.
 *
 * Outside skills that run from npm (e.g. Modern Web Guidance) are recorded as
 * `sourceType: "npm"` entries instead: `package`, an exact `version` (never
 * `latest` or a range), the registry's `integrity` (sha512) and `license`.
 * Their content is not on disk, so this script does not hash them; it checks
 * the entry is a real pin. Bumping one is a reviewed PR that updates all four
 * fields (see the "Outside Skills Are Version-Pinned" rule in RULES.md).
 *
 *   node scripts/update-skills-lock.js          # rewrite stale hashes
 *   node scripts/update-skills-lock.js --check  # exit 1 if any hash is stale
 *
 * No external dependencies — Node built-ins only.
 */
'use strict';

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const prawRoot = path.resolve(__dirname, '..');
const lockPath = path.join(prawRoot, 'skills-lock.json');
const checkOnly = process.argv.indexOf('--check') !== -1;

function sha256Hex(buf) {
  return crypto.createHash('sha256').update(buf).digest('hex');
}

let lock;
try {
  lock = JSON.parse(fs.readFileSync(lockPath, 'utf8'));
} catch (err) {
  console.error('Could not read ' + lockPath + ': ' + err.message);
  process.exit(1);
}
if (!lock || typeof lock.skills !== 'object') {
  console.error(lockPath + ' has no "skills" object');
  process.exit(1);
}

const names = Object.keys(lock.skills).sort();
let stale = 0;
let missing = 0;
const EXACT_VERSION = /^\d+\.\d+\.\d+$/;
names.forEach(function (name) {
  const entry = lock.skills[name];
  if (entry && entry.sourceType === 'npm') {
    const problems = [];
    if (!entry.package) problems.push('no package');
    if (!entry.version || !EXACT_VERSION.test(entry.version)) problems.push('version must be exact x.y.z, got ' + JSON.stringify(entry.version));
    if (!entry.integrity || entry.integrity.indexOf('sha512-') !== 0) problems.push('integrity must be the registry sha512');
    if (!entry.license) problems.push('no license');
    if (problems.length > 0) {
      console.error('  ' + name + ': ' + problems.join('; '));
      missing++;
    }
    return;
  }
  const rel = entry && entry.skillPath;
  if (!rel) {
    console.error('  ' + name + ': no skillPath');
    missing++;
    return;
  }
  const full = path.join(prawRoot, rel);
  if (!fs.existsSync(full)) {
    console.error('  ' + name + ': ' + rel + ' not found');
    missing++;
    return;
  }
  const actual = sha256Hex(fs.readFileSync(full));
  if (entry.computedHash !== actual) {
    stale++;
    console.log('  ' + name + ': ' + (entry.computedHash || '(none)').slice(0, 12) + '… -> ' + actual.slice(0, 12) + '…');
    if (!checkOnly) entry.computedHash = actual;
  }
});

if (missing > 0) {
  console.error(missing + ' entr' + (missing === 1 ? 'y is' : 'ies are') + ' missing a file or not a valid pin; fix skills-lock.json by hand.');
  process.exit(1);
}

if (checkOnly) {
  if (stale > 0) {
    console.error(stale + ' stale hash' + (stale === 1 ? '' : 'es') + ' in skills-lock.json; run: node scripts/update-skills-lock.js');
    process.exit(1);
  }
  console.log('skills-lock.json is up to date (' + names.length + ' skills)');
  process.exit(0);
}

if (stale === 0) {
  console.log('skills-lock.json already up to date (' + names.length + ' skills)');
  process.exit(0);
}
fs.writeFileSync(lockPath, JSON.stringify(lock, null, 2) + '\n');
console.log('Updated ' + stale + ' hash' + (stale === 1 ? '' : 'es') + ' in skills-lock.json');
