#!/usr/bin/env node
//
// contrast-report.cjs
//
// WCAG contrast check of the pairings DDD makes, read straight from the
// webcomponents source (Node built-ins only):
//
//   - every data-primary fill with the ink DDD assigns it
//     (--ddd-theme-bgContrast = white, --lowContrast-override = black)
//   - every primary as text on white, on coaly gray (dark surface) and on
//     each data-accent background
//   - every SimpleColors shade with its better ink
//
// Usage:
//   node contrast-report.cjs --webcomponents ../webcomponents [--json]
//
// Exits 1 when a regression gate fails: a primary fill whose DDD-assigned ink
// is below 4.5:1, or a SimpleColors shade with no ink at 4.5:1. Everything
// else is reported, not gated (coloured text on accents is a known trade-off).
//

'use strict'

var fs = require('fs')
var path = require('path')

var argv = process.argv.slice(2)
var wcArg = argv.indexOf('--webcomponents')
var WC = path.resolve(wcArg > -1 ? argv[wcArg + 1] : path.join(process.cwd(), '..', 'webcomponents'))
var asJson = argv.indexOf('--json') > -1

var dddPath = path.join(WC, 'elements', 'd-d-d', 'lib', 'DDDStyles.js')
var scPath = path.join(WC, 'elements', 'simple-colors-shared-styles', 'simple-colors-shared-styles.js')
if (!fs.existsSync(dddPath) || !fs.existsSync(scPath)) {
  console.error('ERROR: webcomponents checkout not found at ' + WC + '. Pass --webcomponents <path>.')
  process.exit(2)
}
var ddd = fs.readFileSync(dddPath, 'utf8')
var sc = fs.readFileSync(scPath, 'utf8')

// --------------------------------------------------------------- tokens --
var block = ddd.slice(ddd.indexOf('export const DDDVariables'), ddd.indexOf('export const DDDGlobalStyles'))
var vars = {}
var re = /--([\w-]+):\s*((?:[^;])+?);/g
var m
while ((m = re.exec(block))) vars[m[1]] = m[2].replace(/\s+/g, ' ').replace(/\( /g, '(').replace(/ \)/g, ')').trim()
function resolve (v, seen) {
  seen = seen || {}
  var r = /^var\(--([\w-]+)(?:,.*)?\)$/.exec(v)
  if (!r || seen[r[1]] || !vars[r[1]]) return v
  seen[r[1]] = true
  return resolve(vars[r[1]], seen)
}
function hexOf (name) {
  var v = resolve('var(--' + name + ')').toLowerCase()
  return /^#[0-9a-f]{6}$/.test(v) ? v : null
}

// ---------------------------------------------------------------- color --
function rgb (h) { return [1, 3, 5].map(function (i) { return parseInt(h.slice(i, i + 2), 16) }) }
function lum (h) {
  var c = rgb(h).map(function (v) { v = v / 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4) })
  return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
}
function cr (a, b) { var x = lum(a); var y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05) }
function level (r) { return r >= 7 ? 'AAA' : r >= 4.5 ? 'AA' : r >= 3 ? 'Large' : 'Fail' }
var WHITE = '#ffffff'
var BLACK = '#000000'
var COALY = hexOf('ddd-theme-default-coalyGray') || '#262626'

// -------------------------------------------------------------- pairings --
var primaries = []
for (var i = 0; i < 26; i++) {
  var hex = hexOf('ddd-primary-' + i)
  if (!hex) continue
  var rule = new RegExp('\\[data-primary="' + i + '"\\]\\s*\\{([^}]*)\\}').exec(ddd)
  var ink = rule && /--lowContrast-override:/.test(rule[1]) ? 'black' : 'white'
  var inkRatio = cr(hex, ink === 'white' ? WHITE : BLACK)
  primaries.push({
    n: i,
    hex: hex,
    ink: ink,
    fill: inkRatio,
    otherInk: cr(hex, ink === 'white' ? BLACK : WHITE),
    onWhite: cr(hex, WHITE),
    onCoaly: cr(hex, COALY)
  })
}
var accents = []
for (var a = 0; a < 15; a++) {
  var ah = hexOf('ddd-accent-' + a)
  if (ah) accents.push({ n: a, hex: ah })
}
var onAccent = 0
var accentTotal = 0
primaries.forEach(function (p) {
  accents.forEach(function (ac) { accentTotal++; if (cr(p.hex, ac.hex) >= 4.5) onAccent++ })
})

var scShades = []
var sre = /--simple-colors-fixed-theme-([a-z-]+)-(\d+):\s*(#[0-9a-fA-F]{6});/g
while ((m = sre.exec(sc))) {
  if (m[1] === 'accent') continue
  var h = m[3].toLowerCase()
  scShades.push({ name: m[1] + '-' + m[2], hex: h, best: Math.max(cr(h, WHITE), cr(h, BLACK)) })
}

// ----------------------------------------------------------------- gates --
var gates = []
primaries.forEach(function (p) {
  if (p.fill < 4.5) gates.push('primary-' + p.n + ' (' + p.hex + ') with DDD ' + p.ink + ' ink is ' + p.fill.toFixed(2) + ':1')
  if (p.otherInk > p.fill + 0.5) gates.push('primary-' + p.n + ': the other ink reads better (' + p.otherInk.toFixed(2) + ' vs ' + p.fill.toFixed(2) + ')')
})
scShades.forEach(function (s) {
  if (s.best < 4.5) gates.push('SimpleColors ' + s.name + ' (' + s.hex + ') has no ink at 4.5:1')
})

var summary = {
  primaries: primaries.length,
  fillsAtAA: primaries.filter(function (p) { return p.fill >= 4.5 }).length,
  textOnWhiteAA: primaries.filter(function (p) { return p.onWhite >= 4.5 }).length,
  textOnCoalyAA: primaries.filter(function (p) { return p.onCoaly >= 4.5 }).length,
  primaryOnAccentAA: onAccent,
  primaryOnAccentTotal: accentTotal,
  simpleColorsAA: scShades.filter(function (s) { return s.best >= 4.5 }).length,
  simpleColorsTotal: scShades.length,
  gates: gates
}

if (asJson) {
  console.log(JSON.stringify({ summary: summary, primaries: primaries }, null, 2))
} else {
  var out = []
  out.push('# DDD contrast report')
  out.push('')
  out.push('| Check | Result |')
  out.push('|---|---|')
  out.push('| Primary fills with DDD ink at AA | ' + summary.fillsAtAA + ' / ' + summary.primaries + ' |')
  out.push('| Primaries as text on white at AA | ' + summary.textOnWhiteAA + ' / ' + summary.primaries + ' |')
  out.push('| Primaries as text on coaly gray at AA | ' + summary.textOnCoalyAA + ' / ' + summary.primaries + ' |')
  out.push('| Primary text on accent backgrounds at AA | ' + summary.primaryOnAccentAA + ' / ' + summary.primaryOnAccentTotal + ' |')
  out.push('| SimpleColors shades with an AA ink | ' + summary.simpleColorsAA + ' / ' + summary.simpleColorsTotal + ' |')
  out.push('')
  out.push('| data-primary | Hex | DDD ink | Fill | On white | On coaly gray |')
  out.push('|---|---|---|---|---|---|')
  primaries.forEach(function (p) {
    out.push('| ' + p.n + ' | `' + p.hex + '` | ' + p.ink + ' | ' + p.fill.toFixed(2) + ' ' + level(p.fill) + ' | ' + p.onWhite.toFixed(2) + ' ' + level(p.onWhite) + ' | ' + p.onCoaly.toFixed(2) + ' ' + level(p.onCoaly) + ' |')
  })
  out.push('')
  out.push(gates.length ? '## Gate failures\n\n' + gates.map(function (g) { return '- ' + g }).join('\n') : 'All gates pass.')
  console.log(out.join('\n'))
}
process.exit(gates.length ? 1 : 0)
