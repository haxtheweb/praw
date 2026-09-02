#!/usr/bin/env node
//
// sync-plugin-skill.js
//
// Copies a named interface skill from a `create` checkout path into a target
// plugin skills directory. Validates that the SKILL.md has YAML frontmatter
// with at least `name` and `description`. Reports drift (diff vs an existing
// copy if present).
//
// Usage:
//   node scripts/sync-plugin-skill.js <create-path> <plugin-skills-dir> <skill-name>
//
// Example:
//   node scripts/sync-plugin-skill.js ~/Documents/git/haxtheweb/create \
//     plugins/hax-onboarding/skills hax
//
// The source skill is expected at <create-path>/src/skills/<skill-name>/.
// The destination is <plugin-skills-dir>/<skill-name>/.
// If the destination already exists, a drift diff is printed before copying.
//

'use strict'

var fs = require('fs')
var path = require('path')
var cp = require('child_process')

function usage() {
  console.error('Usage: node scripts/sync-plugin-skill.js <create-path> <plugin-skills-dir> <skill-name>')
  process.exit(1)
}

function parseFrontmatter(content) {
  if (!content || content.slice(0, 3) !== '---') return null
  var end = content.indexOf('\n---', 3)
  if (end === -1) return null
  var block = content.slice(3, end).trim()
  var result = {}
  var lines = block.split('\n')
  for (var i = 0; i < lines.length; i++) {
    var line = lines[i]
    var idx = line.indexOf(':')
    if (idx === -1) continue
    var key = line.slice(0, idx).trim()
    var val = line.slice(idx + 1).trim()
    result[key] = val
  }
  return result
}

function validateFrontmatter(content, skillName) {
  var fm = parseFrontmatter(content)
  if (!fm) {
    console.error('ERROR: ' + skillName + '/SKILL.md has no YAML frontmatter')
    return false
  }
  if (!fm.name) {
    console.error('ERROR: ' + skillName + '/SKILL.md frontmatter is missing "name"')
    return false
  }
  if (!fm.description) {
    console.error('ERROR: ' + skillName + '/SKILL.md frontmatter is missing "description"')
    return false
  }
  console.log('OK: frontmatter validated (name=' + fm.name + ')')
  return true
}

function diffDirs(srcDir, dstDir) {
  try {
    var result = cp.spawnSync('diff', ['-rq', srcDir, dstDir], { encoding: 'utf8' })
    if (result.status === 0) {
      console.log('No drift detected — destination matches source.')
    } else if (result.stdout) {
      console.log('Drift detected (diff -rq):')
      console.log(result.stdout.trim())
    }
  } catch (e) {
    // diff not available — skip drift report
    console.log('Skipping drift check (diff not available).')
  }
}

function copyDir(src, dst) {
  fs.mkdirSync(dst, { recursive: true })
  var entries = fs.readdirSync(src, { withFileTypes: true })
  for (var i = 0; i < entries.length; i++) {
    var entry = entries[i]
    var srcPath = path.join(src, entry.name)
    var dstPath = path.join(dst, entry.name)
    if (entry.isDirectory()) {
      copyDir(srcPath, dstPath)
    } else {
      fs.copyFileSync(srcPath, dstPath)
    }
  }
}

function main() {
  var args = process.argv.slice(2)
  if (args.length < 3) usage()

  var createPath = path.resolve(args[0])
  var pluginSkillsDir = path.resolve(args[1])
  var skillName = args[2]

  var srcDir = path.join(createPath, 'src', 'skills', skillName)
  var dstDir = path.join(pluginSkillsDir, skillName)

  if (!fs.existsSync(srcDir)) {
    console.error('ERROR: source skill not found: ' + srcDir)
    process.exit(1)
  }

  var srcSkillFile = path.join(srcDir, 'SKILL.md')
  if (!fs.existsSync(srcSkillFile)) {
    console.error('ERROR: source SKILL.md not found: ' + srcSkillFile)
    process.exit(1)
  }

  var content = fs.readFileSync(srcSkillFile, 'utf8')
  if (!validateFrontmatter(content, skillName)) {
    process.exit(1)
  }

  // Report drift if destination already exists
  if (fs.existsSync(dstDir)) {
    console.log('Destination exists — checking for drift...')
    diffDirs(srcDir, dstDir)
  } else {
    console.log('Destination does not exist — creating fresh copy.')
  }

  copyDir(srcDir, dstDir)
  console.log('Synced: ' + skillName + ' -> ' + dstDir)
}

main()
