#!/usr/bin/env node
// Analyze one site: fingerprint, sample pages, convert content with block maps,
// classify the site, draft a theme brief, and propose missing blocks.
//
// Usage: node analyze.mjs <url> [--pages 6] [--out ./migration-report] [--probe auto|true|false] [--save-html]
import { mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { fetchPage, robotsAllows } from "./lib/net.mjs";
import { fingerprint } from "./lib/fingerprint.mjs";
import { mapsFor, convert } from "./lib/blocks.mjs";
import { parseDoc, extractContent, fidelity, unmappedComponents } from "./lib/extract.mjs";
import { discover, linksFrom } from "./lib/crawl.mjs";
import { classifySite } from "./lib/classify.mjs";
import { colorsFrom, fontsFrom, layoutFeatures, recommendTheme } from "./lib/theme.mjs";
import { proposeGaps } from "./lib/gaps.mjs";

function navText(html) {
  const doc = parseDoc(html);
  return doc.querySelectorAll("nav, header").map((n) => n.text).join(" ").replace(/\s+/g, " ").slice(0, 4000);
}

async function cssFor(page, fetchOpts, max = 2) {
  let css = "";
  const doc = parseDoc(page.body);
  for (const s of doc.querySelectorAll("style")) css += s.text + "\n";
  for (const el of doc.querySelectorAll("[style]")) css += el.getAttribute("style") + ";\n";
  const origin = new URL(page.finalUrl).origin;
  const links = doc.querySelectorAll("link[rel~=stylesheet][href]").map((l) => new URL(l.getAttribute("href"), page.finalUrl).href)
    .filter((h) => h.startsWith(origin) && !/wp-includes|block-library|jquery|bootstrap(\.min)?\.css|font-?awesome/i.test(h));
  for (const h of links.slice(0, max)) {
    const r = await fetchPage(h, { ...fetchOpts, accept: "text/css" });
    if (r.status === 200) css += r.body.slice(0, 400000) + "\n";
  }
  return css;
}

function analyzePage(page, maps) {
  const doc = parseDoc(page.body);
  const content = extractContent(doc, maps);
  const conv = convert(content.html, maps);
  const fid = fidelity(content.html, conv.html);
  return {
    url: page.finalUrl,
    status: page.status,
    title: content.title,
    contentSelector: content.selector,
    contentMethod: content.method,
    sourceWords: fid.sourceWords,
    fidelity: Number(fid.ratio.toFixed(3)),
    rules: conv.stats.rules,
    flags: conv.stats.flags.map((f) => ({ ...f, sample: f.sample.slice(0, 400) })),
    badSelectors: conv.stats.badSelectors,
    assets: conv.assets.length,
    unmapped: unmappedComponents(conv.transformed),
    html: conv.html,
  };
}

export async function analyzeSite(url, opts = {}) {
  const fetchOpts = { allowPrivate: !!opts.allowPrivate };
  const started = Date.now();
  if (!(await robotsAllows(url, fetchOpts))) return { url, error: "robots.txt disallows this URL" };
  const home = await fetchPage(url, fetchOpts);
  if (home.status !== 200 || !home.body) return { url, error: home.error || `HTTP ${home.status}`, status: home.status };
  const homeFp = await fingerprint(home, { probe: opts.probe, fetchOpts });
  const found = await discover(home, opts.pages || 6, fetchOpts);
  const pages = [home];
  for (const u of found.urls) {
    const r = await fetchPage(u, fetchOpts);
    if (r.status === 200 && /html/i.test(r.headers["content-type"] || "html")) pages.push(r);
  }
  // Builders often appear only on inner pages, so score layers across the whole sample.
  const sampleFp = await fingerprint({ ...home, body: pages.map((p) => p.body).join("\n") }, { probe: false, fetchOpts });
  const fp = homeFp.primary.id === "unknown" && sampleFp.primary.id !== "unknown" ? { ...sampleFp, source: "sample" } : { ...homeFp, source: "home" };
  if (fp.source === "home" && sampleFp.primary.id === homeFp.primary.id) {
    const seen = new Set(fp.layers.map((l) => l.id));
    fp.layers = [...fp.layers, ...sampleFp.layers.filter((l) => !seen.has(l.id))];
  }
  const maps = mapsFor(fp);
  const results = pages.map((p) => analyzePage(p, maps));
  const site = classifySite(
    pages.map((p) => ({ url: p.finalUrl, title: (results.find((r) => r.url === p.finalUrl) || {}).title, html: p.body, navText: navText(p.body), links: linksFrom(p.body, p.finalUrl) })),
    fp,
  );
  const css = await cssFor(home, fetchOpts);
  const features = layoutFeatures(home.body, pages[1] ? pages[1].body : home.body);
  const brief = {
    colors: colorsFrom(css),
    fonts: fontsFrom(css, home.body),
    features,
    recommendation: recommendTheme(site.type, features),
  };
  const gaps = proposeGaps(results);
  const totalWords = results.reduce((a, r) => a + r.sourceWords, 0);
  const keptWords = results.reduce((a, r) => a + r.sourceWords * r.fidelity, 0);
  const ruleTotals = {};
  for (const r of results) for (const [k, v] of Object.entries(r.rules)) ruleTotals[k] = (ruleTotals[k] || 0) + v;
  return {
    url,
    finalUrl: home.finalUrl,
    analyzedAt: new Date().toISOString(),
    seconds: Math.round((Date.now() - started) / 1000),
    fingerprint: fp,
    blockMaps: maps.map((m) => m.id),
    importPath: fp.primary.importer ? `existing importer: ${fp.primary.importer}` : "crawl + block maps",
    discovery: { sitemapUrls: found.sitemapCount, navLinks: found.navCount, sampled: pages.length },
    siteType: site,
    theme: brief,
    fidelity: totalWords ? Number((keptWords / totalWords).toFixed(3)) : null,
    rulesFired: ruleTotals,
    gaps,
    pages: results,
  };
}

export function reportMarkdown(r) {
  if (r.error) return `# ${r.url}\n\nCould not analyze: ${r.error}\n`;
  const fp = r.fingerprint;
  const lines = [];
  lines.push(`# Migration analysis: ${r.finalUrl}`, "");
  lines.push(`- **Platform:** ${fp.primary.label}${fp.primary.version ? ` ${fp.primary.version}` : ""} (${fp.primary.confidence} confidence, score ${fp.primary.score})`);
  if (fp.layers.length) lines.push(`- **Builders / layers:** ${fp.layers.map((l) => l.label).join(", ")}`);
  if (fp.hosting.length) lines.push(`- **Hosting hints:** ${fp.hosting.join(", ")}`);
  lines.push(`- **Import path:** ${r.importPath}`);
  lines.push(`- **Site type:** ${r.siteType.type} (${r.siteType.reasons.join("; ") || "default"})`);
  lines.push(`- **Theme:** ${r.theme.recommendation.theme} (${r.theme.recommendation.reasons.join(", ")})${r.theme.recommendation.customThemeSuggested ? " — custom theme suggested" : ""}`);
  lines.push(`- **Text kept after conversion:** ${r.fidelity == null ? "n/a" : Math.round(r.fidelity * 100) + "%"} across ${r.pages.length} pages`, "");
  lines.push("## Evidence", "", ...fp.primary.evidence.map((e) => `- ${e.type} (+${e.weight}): \`${e.hit}\``), "");
  lines.push("## Pages", "", "| Page | Content found by | Words | Text kept | Flags |", "|---|---|---|---|---|");
  for (const p of r.pages) lines.push(`| ${p.url} | ${p.contentSelector} | ${p.sourceWords} | ${Math.round(p.fidelity * 100)}% | ${p.flags.map((f) => f.flag).join(", ")} |`);
  lines.push("", "## Theme brief", "");
  lines.push(`- Features: ${r.theme.features.join(", ") || "none detected"}`);
  lines.push(`- Fonts: ${r.theme.fonts.join(", ") || "none detected"}`);
  lines.push(`- Colors (nearest DDD token): ${r.theme.colors.map((c) => `${c.hex} → ${c.ddd.token.replace("--ddd-theme-default-", "")}`).join(", ") || "none detected"}`);
  if (r.theme.recommendation.unhandledFeatures.length) lines.push(`- Not covered by ${r.theme.recommendation.theme}: ${r.theme.recommendation.unhandledFeatures.join(", ")}`);
  lines.push("", "## Proposed blocks", "");
  if (!r.gaps.blocks.length) lines.push("No repeated unmapped components.");
  for (const b of r.gaps.blocks.slice(0, 12)) {
    lines.push(`- \`${b.signature}\` on ${b.pages} page(s), ${b.occurrences} time(s): ${b.recommendation === "reuse" ? `reuse **${b.reuse.tag}** (${b.reuse.why})` : `new block **${b.proposedTag}**`}`);
  }
  lines.push("", "## Needs a human", "", ...Object.entries(r.gaps.flagsByKind).map(([k, v]) => `- ${k}: ${v}`));
  return lines.join("\n") + "\n";
}

async function main() {
  const args = process.argv.slice(2);
  const url = args.find((a) => /^https?:\/\//.test(a));
  if (!url) { console.error("Usage: node analyze.mjs <url> [--pages 6] [--out dir] [--probe auto|true|false] [--save-html]"); process.exit(1); }
  const val = (flag, d) => { const i = args.indexOf(flag); return i >= 0 ? args[i + 1] : d; };
  const probe = val("--probe", "auto");
  const r = await analyzeSite(url, { pages: Number(val("--pages", 6)), probe: probe === "true" ? true : probe === "false" ? false : "auto" });
  const out = val("--out", "./migration-report");
  mkdirSync(out, { recursive: true });
  const slim = { ...r, pages: (r.pages || []).map(({ html, ...rest }) => rest) };
  writeFileSync(join(out, "report.json"), JSON.stringify(slim, null, 2));
  writeFileSync(join(out, "report.md"), reportMarkdown(r));
  if (args.includes("--save-html")) {
    mkdirSync(join(out, "pages"), { recursive: true });
    (r.pages || []).forEach((p, i) => writeFileSync(join(out, "pages", `${String(i).padStart(2, "0")}.html`), `<!-- ${p.url} -->\n${p.html}\n`));
  }
  console.log(reportMarkdown(r));
}

if (import.meta.url === `file://${process.argv[1]}`) main();
