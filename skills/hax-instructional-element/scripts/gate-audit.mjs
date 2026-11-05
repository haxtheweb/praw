#!/usr/bin/env node
/**
 * Static gate audit of HAX instructional elements (read-only).
 *
 * Usage:
 *   node gate-audit.mjs <path-to-webcomponents-checkout> [tag=relative/path/to/element.js ...]
 *
 * With no tag arguments it audits every element in the monorepo that extends
 * QuestionElement or MicroGameBase, or declares `static get xapiVocabulary()`,
 * plus the known unassessed activities listed in EXTRA below.
 * Prints one tab-separated row per element. Columns are explained in the
 * hax-instructional-element SKILL.md ("Audit mode").
 *
 * This only covers what can be read from source. Dark-mode contrast, reduced
 * motion and phone width are runtime checks; see the SKILL.md for those.
 * Node built-ins only.
 */
import fs from "node:fs";
import path from "node:path";

const root = process.argv[2];
if (!root || !fs.existsSync(path.join(root, "elements"))) {
  console.error("usage: node gate-audit.mjs <webcomponents-checkout> [tag=path.js ...]");
  process.exit(1);
}
const EL = path.join(root, "elements");
// unassessed activities that may not emit xAPI yet, so discovery would miss them
const EXTRA = [
  "stop-note=stop-note/stop-note.js",
  "activity-box=course-design/lib/activity-box.js",
  "learning-component=course-design/lib/learning-component.js",
];
const SKIP = new Set(["user-action", "QuestionElement", "a11y-media-player", "audio-player", "video-player"]);

function discover() {
  const out = [];
  for (const pkg of fs.readdirSync(EL)) {
    for (const dir of [pkg, `${pkg}/lib`]) {
      const abs = path.join(EL, dir);
      if (!fs.existsSync(abs) || !fs.statSync(abs).isDirectory()) continue;
      for (const f of fs.readdirSync(abs)) {
        if (!f.endsWith(".js") || f.includes(".test.") || f.includes("haxProperties")) continue;
        const src = fs.readFileSync(path.join(abs, f), "utf8");
        const tagM = src.match(/static get tag\(\)\s*\{\s*return\s*["']([a-z0-9-]+)["']/);
        if (!tagM || SKIP.has(tagM[1]) || SKIP.has(f.replace(".js", ""))) continue;
        if (/extends\s+(QuestionElement|MicroGameBase|MarkTheWords|ConceptMapGame)\b|static get xapiVocabulary/.test(src)) {
          out.push(`${tagM[1]}=${dir}/${f}`);
        }
      }
    }
  }
  return out;
}

const args = process.argv.slice(3);
const list = [...new Set(args.length ? args : [...discover(), ...EXTRA])];
const vocabFile = path.join(EL, "user-action/lib/xapi-vocabulary.json");
const vocab = fs.existsSync(vocabFile) ? fs.readFileSync(vocabFile, "utf8") : "";
const rows = [];

for (const item of list) {
  const [tag, rel] = item.split("=");
  const f = path.join(EL, rel);
  if (!fs.existsSync(f)) {
    rows.push({ tag, missing: true });
    continue;
  }
  const src = fs.readFileSync(f, "utf8");
  const pkg = rel.split("/")[0];
  const hpf = [
    path.join(EL, pkg, "lib", `${tag}.haxProperties.json`),
    path.join(path.dirname(f), `${tag}.haxProperties.json`),
    path.join(EL, pkg, "lib", `${pkg}.haxProperties.json`),
  ].find((p) => fs.existsSync(p));
  let hj = null;
  try {
    hj = hpf ? JSON.parse(fs.readFileSync(hpf, "utf8")) : null;
  } catch (e) {
    hj = null;
  }
  const ext = ((src.match(/class\s+\w+\s+extends\s+([^{]+)\{/) || [])[1] || "?").trim().replace(/\s+/g, " ");
  const assessed = /QuestionElement|MarkTheWords/.test(ext);
  const hb = (src.match(/haxHooks\(\)\s*\{[\s\S]*?\n {2}\}/) || [""])[0];
  const hooks = (hb.match(/(\w+)\s*:/g) || []).map((m) => m.replace(/\s*:/, ""));
  const settings = hj && hj.settings
    ? Object.keys(hj.settings).filter((k) => (hj.settings[k] || []).length)
    : /configure\s*:/.test(src) ? ["inline"] : [];
  const ds = hj ? (hj.designSystem === undefined ? "none" : JSON.stringify(hj.designSystem)) : /designSystem/.test(src) ? "inline" : "none";
  const testDir = path.join(EL, pkg, "test");
  const tests = fs.existsSync(testDir) ? fs.readdirSync(testDir).filter((t) => t.endsWith(".js")) : [];
  const testSrc = tests.map((t) => fs.readFileSync(path.join(testDir, t), "utf8")).join("\n");
  const has = (name) => fs.existsSync(path.join(EL, pkg, "lib", `${tag}.${name}`)) || fs.existsSync(path.join(EL, pkg, "lib", `${pkg}.${name}`));
  const css = (src.match(/css`[\s\S]*?`/g) || []).join("\n");
  const code = src.replace(/\/\*[\s\S]*?\*\//g, "").replace(/^\s*\/\/.*$/gm, "");
  const emits = /xapiVocabulary/.test(src) || assessed || /MicroGameBase|ConceptMapGame/.test(ext);
  rows.push({
    tag,
    base: ext.slice(0, 40),
    shell: assessed || /renderDDDBlockHeader/.test(src) ? "y" : "-",
    designSystem: ds,
    settings: settings.join("/") || "-",
    demoSchema: hj ? (hj.demoSchema && hj.demoSchema.length ? "y" : "-") : "?",
    haxHooks: hooks.join(",") || (assessed ? "inherited" : "-"),
    xapiVocabulary: /static get xapiVocabulary/.test(src)
      ? (vocab.includes(`"${tag}"`) ? "y" : "y (not generated)")
      : (assessed || /MicroGameBase|ConceptMapGame/.test(ext) ? "inherited" : "-"),
    restore: /restoreLearnerResponse|_applyLearnerRecord|learner-progress-request/.test(src) ? "y" : (assessed ? "base" : "-"),
    i18n: /this\.t\b/.test(src) ? (fs.existsSync(path.join(EL, pkg, "locales")) ? "y" : "no locales") : "-",
    axeTest: /to\.be\.accessible|toBeAccessible/.test(testSrc) ? "y" : "-",
    xapiValidated: /xapi-validate/.test(testSrc) ? "y" : (emits ? "MISSING" : "n/a"),
    docs: has("docs.json") ? "y" : "-",
    motion: has("motion.json") ? "y" : "-",
    optionalChaining: /\?\.[A-Za-z_$[(]/.test(code) ? "USES ?." : "",
    hexColors: (css.match(/#[0-9a-fA-F]{3,8}\b/g) || []).length,
    minWidthOver360: (css.match(/min-width:\s*(\d{3,})px/g) || []).filter((m) => parseInt(m.match(/\d+/)[0], 10) > 360).join(" "),
  });
}

const cols = Object.keys(rows.find((r) => !r.missing) || { tag: 1 });
console.log(cols.join("\t"));
for (const r of rows) {
  console.log(r.missing ? `${r.tag}\tMISSING FILE` : cols.map((c) => r[c]).join("\t"));
}
