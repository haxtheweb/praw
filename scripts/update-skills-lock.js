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
names.forEach(function (name) {
  const entry = lock.skills[name];
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
  console.error(missing + ' entr' + (missing === 1 ? 'y' : 'ies') + ' point at files that do not exist; fix skills-lock.json by hand.');
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
