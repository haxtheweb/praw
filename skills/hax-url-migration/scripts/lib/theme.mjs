// Theme brief: read a site's look and structure, snap it to DDD, and pick the
// closest HAXcms theme (or say a custom theme is warranted).
import { readFileSync } from "node:fs";
import { parse } from "node-html-parser";

// pre must parse as HTML so <pre><code> can be matched; scripts and styles stay raw text
const PARSE_OPTS = { comment: false, blockTextElements: { script: true, noscript: true, style: true } };


const REF = new URL("../../references/", import.meta.url);
const ddd = JSON.parse(readFileSync(new URL("ddd-palette.json", REF), "utf8"));
const themes = JSON.parse(readFileSync(new URL("hax-themes.json", REF), "utf8")).themes;

function hexToRgb(h) {
  let x = h.replace("#", "");
  if (x.length === 3) x = x.split("").map((c) => c + c).join("");
  if (x.length === 8) x = x.slice(0, 6);
  const n = parseInt(x, 16);
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
}
const toHex = ([r, g, b]) => "#" + [r, g, b].map((v) => v.toString(16).padStart(2, "0")).join("");

function isNeutral([r, g, b]) {
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  return max - min < 18; // grays, white, black
}

// perceptual-ish distance (redmean)
function dist(a, b) {
  const rm = (a[0] + b[0]) / 2;
  const dr = a[0] - b[0], dg = a[1] - b[1], db = a[2] - b[2];
  return Math.sqrt((2 + rm / 256) * dr * dr + 4 * dg * dg + (2 + (255 - rm) / 256) * db * db);
}

export function nearestDDD(hex) {
  const c = hexToRgb(hex);
  let best = null;
  for (const [name, h] of Object.entries(ddd.colors)) {
    const d = dist(c, hexToRgb(h));
    if (!best || d < best.distance) best = { token: `--ddd-theme-default-${name}`, hex: h, distance: Math.round(d) };
  }
  return best;
}

/** Count colors in CSS text and inline styles; return the brand-ish ones. */
export function colorsFrom(cssText) {
  const counts = new Map();
  const re = /#([0-9a-f]{6}|[0-9a-f]{3})\b|rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})/gi;
  let m;
  while ((m = re.exec(cssText))) {
    const rgb = m[1] ? hexToRgb(m[1]) : [Number(m[2]), Number(m[3]), Number(m[4])];
    if (isNeutral(rgb)) continue;
    const hex = toHex(rgb);
    counts.set(hex, (counts.get(hex) || 0) + 1);
  }
  return [...counts.entries()].sort((a, b) => b[1] - a[1]).slice(0, 6).map(([hex, n]) => ({ hex, uses: n, ddd: nearestDDD(hex) }));
}

export function fontsFrom(cssText, html) {
  const out = new Map();
  const re = /font-family\s*:\s*([^;}{]+)/gi;
  let m;
  while ((m = re.exec(cssText))) {
    const first = m[1].split(",")[0].replace(/["']/g, "").trim();
    if (!first || /^(inherit|initial|var\(|sans-serif|serif|monospace|system-ui|-apple-system)/i.test(first)) continue;
    out.set(first, (out.get(first) || 0) + 1);
  }
  const g = /fonts\.googleapis\.com\/css2?\?family=([^"'&]+)/gi;
  while ((m = g.exec(html))) for (const f of decodeURIComponent(m[1]).split("|")) out.set(f.split(":")[0].replace(/\+/g, " "), 99);
  return [...out.entries()].sort((a, b) => b[1] - a[1]).slice(0, 4).map(([name]) => name);
}

/** Layout features from the home page and one inner page. */
export function layoutFeatures(homeHtml, innerHtml) {
  const home = parse(homeHtml || "", PARSE_OPTS);
  const inner = parse(innerHtml || homeHtml || "", PARSE_OPTS);
  const f = new Set();
  const nav = home.querySelector("header nav, nav[aria-label*=main i], nav.navbar, [role=navigation]") || home.querySelector("nav");
  if (nav) {
    const topItems = nav.querySelectorAll(":scope > ul > li, :scope > div > ul > li").length;
    const links = nav.querySelectorAll("a").length;
    const nested = nav.querySelectorAll("li ul, li [class*=sub], li [class*=dropdown], li [class*=mega]").length;
    if (nested >= 3 && links >= 15) f.add("mega-menu");
    else if (nested > 0) f.add("dropdown-nav");
    if (topItems > 0) f.add(`top-nav:${topItems}`);
  }
  if (inner.querySelector("aside, .sidebar, #sidebar, [class*=sidebar], [role=complementary]")) f.add("sidebar");
  const main = home.querySelector("main") || home.querySelector("body");
  const firstBlock = main ? main.querySelector("section, div, figure") : null;
  if (firstBlock && /hero|banner|jumbotron|masthead|cover|slider|carousel/i.test(firstBlock.getAttribute("class") || "")) f.add("hero");
  if (home.querySelector("[class*=carousel], [class*=slider], [class*=slideshow], .rslides")) f.add("carousel");
  const footer = home.querySelector("footer");
  if (footer) {
    const cols = footer.querySelectorAll("ul").length;
    if (cols >= 3) f.add("footer-columns");
  }
  if (/position\s*:\s*(sticky|fixed)/i.test(homeHtml) && /header|nav/i.test(homeHtml)) f.add("sticky-header");
  if (inner.querySelectorAll("a").some((a) => /^(next|previous|prev)\b/i.test((a.text || "").trim()))) f.add("prev-next");
  if (/<video[^>]+autoplay|bg-video|background-video/i.test(homeHtml)) f.add("video");
  return [...f];
}

/** Score HAX themes against the site type and features. */
export function recommendTheme(siteType, features) {
  const nav = features.includes("mega-menu") ? "mega" : features.includes("sidebar") ? "sidebar" : "top";
  const scored = Object.entries(themes).map(([id, t]) => {
    let score = 0;
    const reasons = [];
    if (t.siteTypes.includes(siteType)) { score += 5; reasons.push(`suits ${siteType} sites`); }
    if (t.nav === nav) { score += 3; reasons.push(`${nav} navigation`); }
    const overlap = t.features.filter((x) => features.includes(x));
    score += overlap.length * 2;
    if (overlap.length) reasons.push(`handles ${overlap.join(", ")}`);
    if (!t.verified) score -= 1;
    return { id, score, reasons, verified: t.verified };
  }).sort((a, b) => b.score - a.score);
  const best = scored[0];
  const handled = new Set(themes[best.id].features);
  const unhandled = features.filter((x) => !x.startsWith("top-nav") && !handled.has(x) && !["dropdown-nav"].includes(x));
  return {
    theme: best.id,
    alternatives: scored.slice(1, 3).map((s) => s.id),
    reasons: best.reasons,
    unhandledFeatures: unhandled,
    customThemeSuggested: best.score < 6 || unhandled.length >= 3,
  };
}
