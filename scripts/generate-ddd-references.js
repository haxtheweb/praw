#!/usr/bin/env node
//
// generate-ddd-references.js
//
// Builds the two references the hax-design-system skill points at, straight
// from the webcomponents source so they never drift from what ships:
//
//   skills/hax-design-system/references/ddd-tokens.md
//     every CSS custom property DDD declares (elements/d-d-d/lib/DDDStyles.js),
//     aliases resolved to hex, plus the HAX data-attribute vocabulary
//
//   skills/hax-design-system/references/simplecolors-migration.md
//     the SimpleColors palette (elements/simple-colors-shared-styles), its
//     dark-mode and contrast rules, and the nearest DDD token for every shade
//
// Usage:
//   node scripts/generate-ddd-references.js
//   node scripts/generate-ddd-references.js --webcomponents ../webcomponents
//
// --webcomponents defaults to ../webcomponents (the sibling checkout layout in
// AGENTS.md). Re-run after DDDStyles.js or SimpleColors change.
//

'use strict'

var fs = require('fs')
var path = require('path')
var vm = require('vm')

var argv = process.argv.slice(2)
var wcArg = argv.indexOf('--webcomponents')
var WC = path.resolve(wcArg > -1 ? argv[wcArg + 1] : path.join(__dirname, '..', '..', 'webcomponents'))
var OUT = path.join(__dirname, '..', 'skills', 'hax-design-system', 'references')

var dddPath = path.join(WC, 'elements', 'd-d-d', 'lib', 'DDDStyles.js')
var scPath = path.join(WC, 'elements', 'simple-colors-shared-styles', 'simple-colors-shared-styles.js')
var scDarkPath = path.join(WC, 'elements', 'simple-colors', 'simple-colors.js')
var dddPkgPath = path.join(WC, 'elements', 'd-d-d', 'package.json')
;[dddPath, scPath, scDarkPath].forEach(function (p) {
  if (!fs.existsSync(p)) {
    console.error('ERROR: ' + p + ' not found. Pass --webcomponents <path to the webcomponents checkout>.')
    process.exit(1)
  }
})

var ddd = fs.readFileSync(dddPath, 'utf8')
var dddVersion = JSON.parse(fs.readFileSync(dddPkgPath, 'utf8')).version

// ---------------------------------------------------------------- parsing --

// every `--name: value; /* comment */` inside the DDDVariables block, in order
function parseVariables (src) {
  var start = src.indexOf('export const DDDVariables')
  var end = src.indexOf('export const DDDGlobalStyles')
  var block = src.slice(start, end)
  var re = /--([\w-]+):\s*((?:[^;])+?);[ \t]*(?:\/\*\s*([\s\S]*?)\s*\*\/)?/g
  var vars = []
  var m
  while ((m = re.exec(block))) {
    var value = m[2].replace(/\/\*[\s\S]*?\*\//g, '').replace(/\s+/g, ' ').replace(/\( /g, '(').replace(/ \)/g, ')').trim()
    vars.push({ name: m[1], value: value, comment: (m[3] || '').replace(/\s+/g, ' ').trim() })
  }
  return vars
}

function evalObject (src, startMarker, endMarker, context) {
  var start = src.indexOf(startMarker)
  var body = src.slice(src.indexOf('{', start), src.indexOf(endMarker, start) + endMarker.length - 1)
  return vm.runInNewContext('(' + body + ')', context || {})
}

var vars = parseVariables(ddd)
var byName = {}
vars.forEach(function (v) { byName[v.name] = v })

function resolve (value, seen) {
  seen = seen || {}
  var m = /^var\(--([\w-]+)(?:,.*)?\)$/.exec(value)
  if (!m || seen[m[1]] || !byName[m[1]]) return value
  seen[m[1]] = true
  return resolve(byName[m[1]].value, seen)
}

var verbs = evalObject(ddd, 'export const learningComponentVerbs', '\n};')
var nouns = evalObject(ddd, 'export const learningComponentNouns', '\n};')
var attrSrcStart = ddd.indexOf('export const ApplicationAttributeData')
var attrSrc = ddd.slice(attrSrcStart, ddd.indexOf('\n};', attrSrcStart) + 3)
var attrs = vm.runInNewContext('(' + attrSrc.slice(attrSrc.indexOf('{'), attrSrc.lastIndexOf('}') + 1) + ')', {
  learningComponentTypes: Object.assign({}, verbs, nouns)
})

// SimpleColors: CSS custom properties are what renders, so read those
var sc = fs.readFileSync(scPath, 'utf8')
var scDark = fs.readFileSync(scDarkPath, 'utf8')
var hues = []
var shades = {}
var scRe = /--simple-colors-fixed-theme-([a-z-]+)-(\d+):\s*(#[0-9a-fA-F]{6});/g
var sm
while ((sm = scRe.exec(sc))) {
  if (sm[1] === 'accent') continue
  if (!shades[sm[1]]) { shades[sm[1]] = []; hues.push(sm[1]) }
  shades[sm[1]][Number(sm[2]) - 1] = sm[3].toLowerCase()
}
var darkBlock = scDark.slice(scDark.indexOf(':host([dark])'), scDark.indexOf(':host {'))
var darkOverrides = []
hues.forEach(function (h) {
  for (var i = 1; i <= 12; i++) {
    var dm = new RegExp('--simple-colors-default-theme-' + h + '-' + i + ':\\s*(#[0-9a-fA-F]{6});').exec(darkBlock)
    if (dm && dm[1].toLowerCase() !== shades[h][12 - i]) darkOverrides.push({ hue: h, shade: i, value: dm[1].toLowerCase(), inverse: shades[h][12 - i] })
  }
})
var contrasts = evalObject(sc, 'this.contrasts = {', '\n    };')

// ------------------------------------------------------------------ color --

function hexToRgb (hex) {
  var h = hex.replace('#', '')
  if (h.length === 3) h = h.split('').map(function (c) { return c + c }).join('')
  return [0, 2, 4].map(function (i) { return parseInt(h.slice(i, i + 2), 16) })
}
function luminance (hex) {
  var c = hexToRgb(hex).map(function (v) {
    v = v / 255
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4)
  })
  return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
}
function contrast (a, b) {
  var la = luminance(a)
  var lb = luminance(b)
  return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05)
}
function toLab (hex) {
  var c = hexToRgb(hex).map(function (v) {
    v = v / 255
    return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4)
  })
  var x = (c[0] * 0.4124 + c[1] * 0.3576 + c[2] * 0.1805) / 0.95047
  var y = c[0] * 0.2126 + c[1] * 0.7152 + c[2] * 0.0722
  var z = (c[0] * 0.0193 + c[1] * 0.1192 + c[2] * 0.9505) / 1.08883
  var f = function (t) { return t > 0.008856 ? Math.cbrt(t) : 7.787 * t + 16 / 116 }
  return [116 * f(y) - 16, 500 * (f(x) - f(y)), 200 * (f(y) - f(z))]
}
function deltaE (a, b) {
  var la = toLab(a)
  var lb = toLab(b)
  return Math.sqrt(Math.pow(la[0] - lb[0], 2) + Math.pow(la[1] - lb[1], 2) + Math.pow(la[2] - lb[2], 2))
}
var fmt = function (n) { return n.toFixed(1) }

// ------------------------------------------------------------- ddd-tokens --

function family (name) {
  var rules = [
    [/^ddd-theme-default-gradient-/, 'Gradients'],
    [/^ddd-theme-default-/, 'Base palette'],
    [/^ddd-primary-\d+-rgb$/, 'Primary colors as RGB channels'],
    [/^ddd-primary-\d+$/, 'Primary scale (data-primary)'],
    [/^ddd-accent-\d+$/, 'Accent scale (data-accent)'],
    [/^ddd-font-(primary|secondary|navigation)$/, 'Font families'],
    [/^ddd-font-weight-/, 'Font weights'],
    [/^ddd-font-size-/, 'Font sizes'],
    [/^ddd-theme-(h\d|body)-font-size$/, 'Heading and body sizes'],
    [/^ddd-ls-/, 'Letter spacing'],
    [/^ddd-lh-/, 'Line height'],
    [/^ddd-spacing-/, 'Spacing'],
    [/^ddd-border-/, 'Borders'],
    [/^ddd-theme-header-border-/, 'Heading line treatments'],
    [/^ddd-drop-zone-/, 'Drop zones'],
    [/^ddd-boxShadow-/, 'Shadows'],
    [/^ddd-breakpoint-/, 'Breakpoints'],
    [/^ddd-radius-/, 'Border radius'],
    [/^ddd-icon-/, 'Icon sizes'],
    [/^ddd-z-/, 'Z-index'],
    [/^ddd-opacity-/, 'Opacity'],
    [/^ddd-(duration|timing)-/, 'Motion'],
    [/^ddd-focus-/, 'Focus'],
    [/^ddd-textfield-height-/, 'Text field heights']
  ]
  for (var i = 0; i < rules.length; i++) if (rules[i][0].test(name)) return rules[i][1]
  return 'Component defaults DDD sets'
}

var primaryNames = attrs.primary
var accentNames = attrs.accent
var groups = []
var groupMap = {}
vars.forEach(function (v) {
  var f = family(v.name)
  if (!groupMap[f]) { groupMap[f] = []; groups.push(f) }
  groupMap[f].push(v)
})

function cell (s) { return String(s).replace(/\|/g, '\\|') }
function colorNote (v) {
  var r = resolve(v.value)
  if (!/^#[0-9a-f]{3,6}$/i.test(r)) return ''
  return 'white ' + fmt(contrast(r, '#ffffff')) + ':1 · black ' + fmt(contrast(r, '#000000')) + ':1'
}

var t = []
t.push('# DDD token reference', '')
t.push('Generated by `scripts/generate-ddd-references.js` from `elements/d-d-d/lib/DDDStyles.js` (`@haxtheweb/d-d-d` ' + dddVersion + '). Do not edit by hand: re-run the script after DDD changes.', '')
t.push('Every CSS custom property DDD declares on `:root`/`:host`, in source order. Aliases (`var(--…)`) are shown with the value they resolve to. Colour rows give contrast against white and black text.', '')
t.push('## Rules', '')
t.push('- Import `@haxtheweb/d-d-d/d-d-d.js` and extend `DDD` (or `DDDSuper(...)`); `super.styles` brings these variables, the reset and the data attributes.')
t.push('- Use `var(--ddd-…)` for colour, type, spacing, radius, borders, shadows and icon size. Never hardcode a value that has a token.')
t.push('- Components read the live slots `--ddd-theme-primary` and `--ddd-theme-accent` (set by `data-primary` / `data-accent`), not a specific numbered colour.')
t.push('- Text on a `--ddd-theme-primary` fill: `var(--lowContrast-override, var(--ddd-theme-bgContrast, …))`. DDD sets black or white per primary (see the primary table).')
t.push('- Dark mode: DDD sets `color-scheme: light dark` and switches pairs with `light-dark()` inside components. The base palette does not change.')
t.push('- Media queries cannot read custom properties: write the breakpoint px literally (360, 768, 1080, 1440).')
t.push('- Size icons with `--ddd-icon-*`; on `simple-icon-lite` set `--simple-icon-width` / `--simple-icon-height` to the token.')
t.push('- Need a colour DDD lacks? Use SimpleColors (see `simplecolors-migration.md`).', '')

t.push('## These do not exist', '')
t.push('Guidance elsewhere has named tokens DDD never declared. Do not use them:', '')
t.push('- `--ddd-text-*`: use `--ddd-theme-default-coalyGray` (ink) or the `light-dark()` pair the component needs.')
t.push('- `--ddd-inset-*`, `--ddd-gap-*`: use `--ddd-spacing-*`.')
t.push('- `--ddd-spacing-31` and up: the scale stops at `--ddd-spacing-30` (120px).')
t.push('- `--ddd-radius-s`, `-m`, `-l`: the radii are `0`, `xs`, `sm`, `md`, `lg`, `xl`, `rounded`, `circle`.')
t.push('- `--ddd-duration-instant`, `--ddd-duration-rapid`: durations are `fast`, `normal`, `slow`.', '')

groups.forEach(function (g) {
  var rows = groupMap[g]
  t.push('## ' + g, '')
  if (g === 'Primary scale (data-primary)') {
    t.push('`data-primary="N"` sets `--ddd-theme-primary` to `--ddd-primary-N`. "Text on fill" is what DDD pairs with it (`--ddd-theme-bgContrast` white or `--lowContrast-override` black).', '')
    var blackSet = {}
    var lowRe = /\[data-primary="(\d+)"\]\s*\{[^}]*--lowContrast-override:\s*black/g
    var lm
    while ((lm = lowRe.exec(ddd))) blackSet[lm[1]] = true
    t.push('| Token | Name | Resolves to | Text on fill | Contrast | Source note |', '|---|---|---|---|---|---|')
    rows.forEach(function (v) {
      var n = v.name.split('-').pop()
      t.push('| `--' + v.name + '` | ' + (primaryNames[n] || '') + ' | `' + resolve(v.value) + '` | ' + (blackSet[n] ? 'black' : 'white') + ' | ' + colorNote(v) + ' | ' + cell(v.comment) + ' |')
    })
  } else if (g === 'Accent scale (data-accent)') {
    t.push('`data-accent="N"` sets `--ddd-theme-accent` to `--ddd-accent-N`: pale block backgrounds behind body text.', '')
    t.push('| Token | Name | Resolves to | Contrast |', '|---|---|---|---|')
    rows.forEach(function (v) {
      var n = v.name.split('-').pop()
      t.push('| `--' + v.name + '` | ' + (accentNames[n] || '') + ' | `' + resolve(v.value) + '` | ' + colorNote(v) + ' |')
    })
  } else if (g === 'Base palette') {
    t.push('| Token | Value | Contrast | Source note |', '|---|---|---|---|')
    rows.forEach(function (v) { t.push('| `--' + v.name + '` | `' + cell(v.value) + '` | ' + colorNote(v) + ' | ' + cell(v.comment) + ' |') })
  } else {
    t.push('| Token | Value | Source note |', '|---|---|---|')
    rows.forEach(function (v) {
      var r = resolve(v.value)
      var shown = r !== v.value ? '`' + cell(v.value) + '` → `' + cell(r) + '`' : '`' + cell(v.value) + '`'
      t.push('| `--' + v.name + '` | ' + shown + ' | ' + cell(v.comment) + ' |')
    })
  }
  t.push('')
})

t.push('## Data attributes (HAX authoring)', '')
t.push('Set on plain HTML or any DDD element; values come from `ApplicationAttributeData` in `DDDStyles.js`.', '')
t.push('| Attribute | Values |', '|---|---|')
Object.keys(attrs).forEach(function (k) {
  var vals = Object.keys(attrs[k]).map(function (key) {
    var label = attrs[k][key]
    return '`' + key + '`' + (label && label !== key && k !== 'primary' && k !== 'accent' ? ' (' + label + ')' : '')
  })
  if (k === 'primary' || k === 'accent') vals = ['`0`–`' + (Object.keys(attrs[k]).length - 1) + '` (see the ' + k + ' table)']
  t.push('| `data-' + k + '` | ' + vals.join(', ') + ' |')
})
t.push('')
t.push('Also: `data-palette` (coordinated 7-colour palettes, `0`–`15` or by name), `data-width` (`25`/`50`/`75`/`100`, 600px+), `data-float-position` (`left`/`right`, 1440px+), `data-text-align`, `data-pulse` (`1`/`2`).', '')

fs.mkdirSync(OUT, { recursive: true })
fs.writeFileSync(path.join(OUT, 'ddd-tokens.md'), t.join('\n'))

// ------------------------------------------------- simplecolors-migration --

var dddColors = vars.filter(function (v) {
  return /^ddd-theme-default-/.test(v.name) && /^#[0-9a-f]{6}$/i.test(v.value)
})
function nearestDDD (hex) {
  var best = null
  dddColors.forEach(function (v) {
    var d = deltaE(hex, v.value)
    if (!best || d < best.d) best = { name: v.name, value: v.value, d: d }
  })
  return best
}

var s = []
s.push('# SimpleColors and migrating to DDD', '')
s.push('Generated by `scripts/generate-ddd-references.js` from `elements/simple-colors-shared-styles/simple-colors-shared-styles.js` and `elements/simple-colors/simple-colors.js`. Do not edit by hand.', '')
s.push('SimpleColors is the extended palette DDD builds on. Use DDD first; reach for SimpleColors only when DDD has no workable colour (charts, instructional-action icons, palettes, the `accent-color` attribute).', '')
s.push('## Structure', '')
s.push('- ' + hues.length + ' hues: ' + hues.map(function (h) { return '`' + h + '`' }).join(', ') + '. 12 shades each, 1 (palest) to 12 (deepest).')
s.push('- `--simple-colors-default-theme-<hue>-<n>` follows dark mode: under `[dark]`, shade n takes the value of shade 13−n.')
s.push('- `--simple-colors-fixed-theme-<hue>-<n>` never changes. Use it for brand fills, charts and palette swatches.')
s.push('- `--simple-colors-default-theme-accent-<n>` follows the element\'s `accent-color` attribute (grey when unset). Shade 7 is the CSS `accent-color`.')
if (darkOverrides.length) {
  s.push('- Dark mode is not a pure inversion for ' + darkOverrides.map(function (o) { return '`' + o.hue + '-' + o.shade + '` (`' + o.value + '`, not `' + o.inverse + '`)' }).join(', ') + '.')
}
s.push('')
s.push('## Contrast rule (WCAG AA)', '')
s.push('For text of shade N on another hue, the compliant shades of that hue. Grey pairs use the `greyColor` row; two colours use `colorColor`. "Large" means 18pt+ or bold 14pt+.', '')
s.push('| Shade | Colour on colour | Colour on colour, large | With grey | With grey, large |', '|---|---|---|---|---|')
for (var i = 0; i < 12; i++) {
  var rng = function (r) { return r.min === r.max ? String(r.min) : r.min + '–' + r.max }
  s.push('| ' + (i + 1) + ' | ' + rng(contrasts.colorColor.aa[i]) + ' | ' + rng(contrasts.colorColor.aaLarge[i]) + ' | ' + rng(contrasts.greyColor.aa[i]) + ' | ' + rng(contrasts.greyColor.aaLarge[i]) + ' |')
}
s.push('')
s.push('## Migration', '')
s.push('1. Find the SimpleColors variable and its hex below.')
s.push('2. If the nearest DDD token is a close match (ΔE under 10, marked ✓), replace it with that token, or with the `--ddd-primary-N` / `--ddd-accent-N` that aliases it when the colour is a theme choice.')
s.push('3. Otherwise keep SimpleColors: DDD has no equivalent. Prefer the `fixed` variant unless the colour should flip in dark mode.')
s.push('4. Re-check contrast for every text/fill pair you change, in light and dark.')
s.push('5. Note any SimpleColors that remains, and why, in the component\'s README.', '')
s.push('ΔE is CIE76 distance in Lab: under 2 is imperceptible, under 10 reads as the same colour, above 20 is a different colour.', '')
hues.forEach(function (h) {
  s.push('### ' + h, '')
  s.push('| Shade | Hex (fixed) | Nearest DDD | ΔE | White / black text |', '|---|---|---|---|---|')
  shades[h].forEach(function (hex, idx) {
    var n = nearestDDD(hex)
    s.push('| ' + (idx + 1) + ' | `' + hex + '` | `--' + n.name + '` `' + n.value + '` | ' + fmt(n.d) + (n.d < 10 ? ' ✓' : '') + ' | ' + fmt(contrast(hex, '#ffffff')) + ' / ' + fmt(contrast(hex, '#000000')) + ' |')
  })
  s.push('')
})
fs.writeFileSync(path.join(OUT, 'simplecolors-migration.md'), s.join('\n'))

console.log('wrote ' + path.relative(process.cwd(), path.join(OUT, 'ddd-tokens.md')) + ' (' + vars.length + ' tokens)')
console.log('wrote ' + path.relative(process.cwd(), path.join(OUT, 'simplecolors-migration.md')) + ' (' + hues.length + ' hues)')
