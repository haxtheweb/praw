#!/usr/bin/env node
// Run analyze over a labeled set of sites and score detection and conversion.
//
// Usage: node trial.mjs [../references/trial-sites.json] [--out ./trial-results] [--pages 4] [--only wordpress,drupal] [--concurrency 3]
import { mkdirSync, readFileSync, writeFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { analyzeSite, reportMarkdown } from "./analyze.mjs";

const args = process.argv.slice(2);
const val = (flag, d) => { const i = args.indexOf(flag); return i >= 0 ? args[i + 1] : d; };
const listFile = args.find((a) => a.endsWith(".json")) || new URL("../references/trial-sites.json", import.meta.url).pathname;
const out = val("--out", "./trial-results");
const pagesPer = Number(val("--pages", 4));
const only = val("--only", "") ? val("--only", "").split(",") : null;
const concurrency = Number(val("--concurrency", 3));

const list = JSON.parse(readFileSync(listFile, "utf8"));
const sites = list.sites.filter((s) => !s.skip && (!only || only.includes(s.platform)));
mkdirSync(join(out, "sites"), { recursive: true });

const slug = (u) => u.replace(/^https?:\/\//, "").replace(/[^a-z0-9]+/gi, "-").replace(/-$/, "").slice(0, 80);

async function runOne(site) {
  const file = join(out, "sites", `${slug(site.url)}.json`);
  if (existsSync(file) && !args.includes("--fresh")) return JSON.parse(readFileSync(file, "utf8"));
  let r;
  try {
    r = await analyzeSite(site.url, { pages: pagesPer });
  } catch (e) {
    r = { url: site.url, error: String(e && e.stack ? e.stack.split("\n").slice(0, 3).join(" ") : e) };
  }
  const slim = { ...r, expected: site, pages: (r.pages || []).map(({ html, ...rest }) => rest) };
  writeFileSync(file, JSON.stringify(slim, null, 2));
  writeFileSync(file.replace(/\.json$/, ".md"), reportMarkdown(r));
  console.log(`${site.platform.padEnd(14)} ${r.error ? "ERROR " + r.error : (r.fingerprint.primary.id + (r.fingerprint.layers.length ? "+" + r.fingerprint.layers.map((l) => l.id).join("+") : "")).padEnd(30)} ${site.url}`);
  return slim;
}

// different hosts in parallel, one request at a time per host (net.mjs enforces the delay)
const queue = [...sites];
const results = [];
await Promise.all(Array.from({ length: concurrency }, async () => {
  while (queue.length) { const s = queue.shift(); results.push(await runOne(s)); }
}));

// scoring
const ok = results.filter((r) => !r.error);
const byPlatform = {};
for (const r of results) {
  const e = r.expected;
  const p = (byPlatform[e.platform] = byPlatform[e.platform] || { sites: 0, errors: 0, correct: 0, layerHits: 0, layerExpected: 0, typeCorrect: 0, typeExpected: 0, fidelity: [], misses: [], gaps: {} });
  p.sites++;
  if (r.error) { p.errors++; continue; }
  const got = r.fingerprint.primary.id;
  if (got === e.platform) p.correct++;
  else p.misses.push(`${e.url} → ${got} (${r.fingerprint.primary.confidence})`);
  for (const l of e.layers || []) { p.layerExpected++; if (r.fingerprint.layers.some((x) => x.id === l)) p.layerHits++; }
  if (e.siteType) { p.typeExpected++; if (r.siteType.type === e.siteType) p.typeCorrect++; }
  if (r.fidelity != null) p.fidelity.push(r.fidelity);
  for (const b of r.gaps.blocks) p.gaps[b.signature] = (p.gaps[b.signature] || 0) + b.occurrences;
}
const pct = (a, b) => (b ? `${Math.round((a / b) * 100)}%` : "–");
const avg = (xs) => (xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : null);

const md = [];
md.push("# hax-url-migration trial", "", `Run ${new Date().toISOString()} · ${results.length} sites · ${pagesPer} sampled pages per site`, "");
const totalCorrect = ok.filter((r) => r.fingerprint.primary.id === r.expected.platform).length;
md.push(`**Platform detection:** ${totalCorrect}/${ok.length} correct (${pct(totalCorrect, ok.length)}), ${results.length - ok.length} sites could not be fetched.`, "");
md.push("| Platform | Sites | Fetch errors | Detected | Builder layers | Site type | Text kept (avg) |", "|---|---|---|---|---|---|---|");
for (const [k, p] of Object.entries(byPlatform).sort()) {
  const f = avg(p.fidelity);
  md.push(`| ${k} | ${p.sites} | ${p.errors} | ${pct(p.correct, p.sites - p.errors)} | ${p.layerExpected ? pct(p.layerHits, p.layerExpected) : "–"} | ${p.typeExpected ? pct(p.typeCorrect, p.typeExpected) : "–"} | ${f == null ? "–" : Math.round(f * 100) + "%"} |`);
}
md.push("", "## Misdetections", "");
for (const [k, p] of Object.entries(byPlatform)) for (const m of p.misses) md.push(`- expected **${k}**: ${m}`);
md.push("", "## Fetch errors", "", ...results.filter((r) => r.error).map((r) => `- ${r.url}: ${r.error}`));
md.push("", "## Lowest text retention", "");
for (const r of ok.flatMap((r) => r.pages.map((p) => ({ ...p, site: r.url }))).filter((p) => p.sourceWords > 50).sort((a, b) => a.fidelity - b.fidelity).slice(0, 15)) {
  md.push(`- ${Math.round(r.fidelity * 100)}% ${r.url} (content via \`${r.contentSelector}\`)`);
}
md.push("", "## Top unmapped components by platform", "");
for (const [k, p] of Object.entries(byPlatform)) {
  const top = Object.entries(p.gaps).sort((a, b) => b[1] - a[1]).slice(0, 8);
  if (!top.length) continue;
  md.push(`### ${k}`, "", ...top.map(([sig, n]) => `- \`${sig}\` ×${n}`), "");
}
md.push("## Theme recommendations", "", "| Site | Type | Theme | Custom theme? |", "|---|---|---|---|");
for (const r of ok) md.push(`| ${r.url} | ${r.siteType.type} | ${r.theme.recommendation.theme} | ${r.theme.recommendation.customThemeSuggested ? "yes" : ""} |`);
writeFileSync(join(out, "trial-report.md"), md.join("\n") + "\n");
writeFileSync(join(out, "trial-results.json"), JSON.stringify({ byPlatform, results: results.map((r) => ({ url: r.url, expected: r.expected, error: r.error, detected: r.fingerprint && r.fingerprint.primary, layers: r.fingerprint && r.fingerprint.layers.map((l) => l.id), siteType: r.siteType && r.siteType.type, fidelity: r.fidelity })) }, null, 2));
console.log(`\nWrote ${join(out, "trial-report.md")}`);
