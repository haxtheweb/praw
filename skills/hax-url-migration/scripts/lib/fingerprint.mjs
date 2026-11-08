// Score a fetched page against references/fingerprints.json.
import { readFileSync } from "node:fs";
import { fetchPage } from "./net.mjs";

const REF = new URL("../../references/", import.meta.url);
export function loadFingerprints() {
  return JSON.parse(readFileSync(new URL("fingerprints.json", REF), "utf8"));
}

function generators(html) {
  const out = [];
  const re = /<meta\b[^>]*>/gi;
  let m;
  while ((m = re.exec(html))) {
    const tag = m[0];
    if (/name\s*=\s*["']?generator/i.test(tag)) {
      const c = tag.match(/content\s*=\s*"([^"]*)"|content\s*=\s*'([^']*)'/i);
      if (c) out.push(c[1] || c[2]);
    }
  }
  return out;
}

function assetUrls(html) {
  const out = [];
  const re = /\b(?:src|href|data-src|srcset|content|action|poster)\s*=\s*["']([^"']+)["']/gi;
  let m;
  while ((m = re.exec(html))) out.push(m[1]);
  return out;
}

function cookieNames(setCookies) {
  return (setCookies || []).map((c) => String(c).split("=")[0].trim());
}

function testSignal(sig, ctx) {
  const re = new RegExp(sig.match, "i");
  switch (sig.type) {
    case "generator":
      for (const g of ctx.generators) { const m = g.match(re); if (m) return { hit: g, version: m[1] }; }
      return null;
    case "header": {
      const names = sig.name.toLowerCase().split("|");
      for (const n of names) {
        const v = ctx.headers[n];
        if (v != null) { const m = String(v).match(re); if (m) return { hit: `${n}: ${String(v).slice(0, 120)}`, version: m[1] }; }
      }
      return null;
    }
    case "html": { const m = ctx.html.match(re); return m ? { hit: m[0].slice(0, 120) } : null; }
    case "asset": { const a = ctx.assets.find((u) => re.test(u)); return a ? { hit: a.slice(0, 160) } : null; }
    case "host": return re.test(ctx.host) ? { hit: ctx.host } : null;
    case "cookie": { const c = ctx.cookies.find((n) => re.test(n)); return c ? { hit: `cookie ${c}` } : null; }
    default: return null;
  }
}

async function runProbe(sig, origin, fetchOpts) {
  const r = await fetchPage(origin + sig.path, { ...fetchOpts, accept: "application/json,text/html;q=0.5" });
  if (r.status !== (sig.expect.status || 200)) return null;
  if (sig.expect.jsonKey) {
    try {
      const j = JSON.parse(r.body);
      if (j && Object.prototype.hasOwnProperty.call(j, sig.expect.jsonKey)) return { hit: `probe ${sig.path} -> ${sig.expect.jsonKey}` };
    } catch (e) { return null; }
    return null;
  }
  if (sig.expect.bodyMatch && !new RegExp(sig.expect.bodyMatch, "i").test(r.body)) return null;
  return { hit: `probe ${sig.path} ${r.status}` };
}

function band(score) {
  if (score >= 10) return "high";
  if (score >= 4) return "medium";
  if (score > 0) return "low";
  return "none";
}

/**
 * page: { finalUrl, headers, setCookies, body }
 * opts.probe: "auto" (default) probes only when no platform is decisive, true always, false never.
 */
export async function fingerprint(page, opts = {}) {
  const fp = opts.fingerprints || loadFingerprints();
  const u = new URL(page.finalUrl);
  const ctx = {
    html: page.body || "",
    headers: page.headers || {},
    generators: generators(page.body || ""),
    assets: assetUrls(page.body || ""),
    cookies: cookieNames(page.setCookies),
    host: u.hostname.toLowerCase(),
  };
  const results = {};
  for (const p of fp.platforms) {
    const r = { id: p.id, label: p.label, kind: p.kind, parent: p.parent || null, importer: p.importer || null, blockMap: p.blockMap || null, score: 0, evidence: [], version: null };
    for (const s of p.signals) {
      if (s.type === "probe") continue;
      const hit = testSignal(s, ctx);
      if (hit) {
        r.score += s.weight;
        r.evidence.push({ type: s.type, weight: s.weight, hit: hit.hit });
        if (s.version && hit.version && !r.version) r.version = hit.version;
      }
    }
    results[p.id] = r;
  }
  const probeMode = opts.probe === undefined ? "auto" : opts.probe;
  const decisive = Object.values(results).some((r) => r.kind !== "layer" && r.score >= 10);
  if (probeMode === true || (probeMode === "auto" && !decisive)) {
    for (const p of fp.platforms) {
      for (const s of p.signals.filter((x) => x.type === "probe")) {
        const hit = await runProbe(s, u.origin, opts.fetchOpts || {});
        if (hit) { results[p.id].score += s.weight; results[p.id].evidence.push({ type: "probe", weight: s.weight, hit: hit.hit }); }
      }
    }
  }
  // children lend evidence to parents (elementor markup implies WordPress)
  const lent = {};
  for (const r of Object.values(results)) {
    if (r.parent && r.score > 0 && results[r.parent]) lent[r.parent] = Math.max(lent[r.parent] || 0, Math.min(r.score, 8));
  }
  for (const [id, s] of Object.entries(lent)) results[id].inherited = s;
  const effective = (r) => r.score + (r.inherited || 0);

  const platforms = Object.values(results).filter((r) => r.kind !== "layer" && effective(r) > 0);
  platforms.sort((a, b) => {
    const d = effective(b) - effective(a);
    if (d !== 0) return d;
    // tie: the more specific child wins (pressbooks over wordpress, emdash over astro)
    return (b.parent ? 1 : 0) - (a.parent ? 1 : 0);
  });
  let primary = platforms[0] || null;
  // a decisive child beats its parent even when the parent collected more points
  if (primary) {
    const child = platforms.find((r) => r.parent === primary.id && r.score >= 10);
    if (child) primary = child;
  }
  const lineage = new Set();
  for (let p = primary; p; p = p.parent ? results[p.parent] : null) lineage.add(p.id);
  const layers = Object.values(results)
    .filter((r) => r.kind === "layer" && r.score >= 4 && lineage.has(r.parent))
    .sort((a, b) => b.score - a.score)
    .map((r) => ({ id: r.id, label: r.label, score: r.score, version: r.version, blockMap: r.blockMap, evidence: r.evidence }));

  const hosting = [];
  for (const h of fp.hosting || []) {
    if (h.signals.some((s) => testSignal({ ...s, type: "header" }, ctx))) hosting.push(h.id);
  }
  return {
    primary: primary
      ? { id: primary.id, label: primary.label, kind: primary.kind, score: effective(primary), confidence: band(effective(primary)), version: primary.version, importer: primary.importer, blockMap: primary.blockMap, evidence: primary.evidence }
      : { id: "unknown", label: "Unknown (generic HTML)", kind: "unknown", score: 0, confidence: "none", version: null, importer: null, blockMap: null, evidence: [] },
    layers,
    candidates: platforms.slice(0, 5).map((r) => ({ id: r.id, score: effective(r) })),
    hosting,
    generators: ctx.generators,
  };
}
