#!/usr/bin/env node
/**
 * Analyze HAXcms UX study sessions (exported from Merlin >developer/ux-study).
 *
 *   node analyze.mjs <session.json|folder> [...more] [--out <dir>] [--analyzer <path-or-url>]
 *
 * Writes <out>/ux-study-analysis.json and <out>/ux-study-report.md.
 * The analyzer module is the one shipped in webcomponents
 * (haxcms-elements/lib/core/utils/UXStudyAnalyzer.js), loaded from a local
 * checkout path when given, otherwise from the webcomponents master branch.
 */
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";

const DEFAULT_ANALYZER =
  "https://raw.githubusercontent.com/haxtheweb/webcomponents/master/elements/haxcms-elements/lib/core/utils/UXStudyAnalyzer.js";

const args = process.argv.slice(2);
let out = process.cwd();
let analyzerSrc = DEFAULT_ANALYZER;
const inputs = [];
for (let i = 0; i < args.length; i++) {
  if (args[i] === "--out") {
    out = args[++i];
  } else if (args[i] === "--analyzer") {
    analyzerSrc = args[++i];
  } else {
    inputs.push(args[i]);
  }
}
if (!inputs.length) {
  console.error(
    "usage: node analyze.mjs <session.json|folder> [...] [--out dir] [--analyzer path-or-url]",
  );
  process.exit(1);
}

const files = [];
inputs.forEach((p) => {
  const stat = fs.statSync(p);
  if (stat.isDirectory()) {
    fs.readdirSync(p)
      .filter((f) => f.endsWith(".json"))
      .forEach((f) => files.push(path.join(p, f)));
  } else {
    files.push(p);
  }
});

const sessions = [];
files.forEach((f) => {
  try {
    const data = JSON.parse(fs.readFileSync(f, "utf8"));
    if (data && typeof data.schema === "string" && Array.isArray(data.events)) {
      sessions.push(data);
    }
  } catch (e) {
    console.error(`skipping ${f}: ${e.message}`);
  }
});
if (!sessions.length) {
  console.error("no UX study sessions found");
  process.exit(1);
}

let mod;
if (/^https:\/\//.test(analyzerSrc)) {
  const res = await fetch(analyzerSrc);
  if (!res.ok) {
    console.error(
      `could not fetch analyzer (${res.status}); pass --analyzer <path to a webcomponents checkout's UXStudyAnalyzer.js>`,
    );
    process.exit(1);
  }
  const code = await res.text();
  mod = await import(
    `data:text/javascript;base64,${Buffer.from(code).toString("base64")}`
  );
} else {
  mod = await import(pathToFileURL(path.resolve(analyzerSrc)).href);
}

const analysis = mod.analyzeUXStudies(sessions);
fs.mkdirSync(out, { recursive: true });
const slim = Object.assign({}, analysis, { sessions: undefined });
fs.writeFileSync(
  path.join(out, "ux-study-analysis.json"),
  JSON.stringify(slim, null, 2),
);
fs.writeFileSync(
  path.join(out, "ux-study-report.md"),
  mod.uxStudyReportMarkdown(analysis),
);
const sev = (s) => analysis.findings.filter((f) => f.severity === s).length;
console.log(
  `${sessions.length} session(s), ${analysis.findings.length} finding(s): ${sev("high")} high, ${sev("medium")} medium, ${sev("low")} low`,
);
console.log(`wrote ${path.join(out, "ux-study-analysis.json")}`);
console.log(`wrote ${path.join(out, "ux-study-report.md")}`);
