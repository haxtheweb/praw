// Find the main content of a page, strip site chrome, and measure text fidelity.
import { parse } from "node-html-parser";

// pre must parse as HTML so <pre><code> can be matched; scripts and styles stay raw text
const PARSE_OPTS = { comment: false, blockTextElements: { script: true, noscript: true, style: true } };


const squash = (s) => String(s || "").replace(/\s+/g, " ").trim();

export function parseDoc(html) {
  return parse(html || "", PARSE_OPTS);
}

function textLen(el) {
  return el ? squash(el.text).length : 0;
}

function safeAll(root, sel) {
  try { return root.querySelectorAll(sel); } catch (e) { return []; }
}

/**
 * maps: block maps in precedence order (their contentSelectors/chromeSelectors are used first).
 * Returns { html, selector, textLength, title, method }.
 */
export function extractContent(doc, maps) {
  const title = squash((doc.querySelector("h1") || {}).text) || squash((doc.querySelector("title") || {}).text);
  const chrome = new Set();
  for (const m of maps) for (const c of m.chromeSelectors || []) chrome.add(c);
  for (const c of chrome) for (const n of safeAll(doc, c)) n.remove();

  const tried = [];
  for (const m of maps) for (const s of m.contentSelectors || []) if (!tried.includes(s)) tried.push(s);
  for (const sel of tried) {
    const nodes = safeAll(doc, sel);
    if (!nodes.length) continue;
    let best = nodes[0];
    for (const n of nodes) if (textLen(n) > textLen(best)) best = n;
    if (textLen(best) >= 150 || (sel !== "body" && best.querySelector("img, iframe, video"))) {
      return { html: best.innerHTML, selector: sel, textLength: textLen(best), title, method: "selector" };
    }
  }
  // fallback: remove landmarks that are never content, then take the densest block
  const body = doc.querySelector("body") || doc;
  for (const n of safeAll(body, "header, nav, footer, aside, [role=banner], [role=navigation], [role=contentinfo], form[role=search], script, style, noscript")) n.remove();
  let best = body;
  let bestScore = 0;
  for (const n of safeAll(body, "div, section, article")) {
    const pText = safeAll(n, "p, li, h2, h3, td").reduce((a, p) => a + squash(p.text).length, 0);
    const links = safeAll(n, "a").reduce((a, p) => a + squash(p.text).length, 0);
    const score = pText - links * 0.5;
    if (score > bestScore * 1.1) { best = n; bestScore = score; }
  }
  return { html: best.innerHTML, selector: best === body ? "body" : "density", textLength: textLen(best), title, method: "density" };
}

/** Words from visible text plus text-bearing attributes HAX elements carry (heading, caption, title, label...). */
export function words(html) {
  const doc = parse(html || "", PARSE_OPTS);
  for (const n of safeAll(doc, "script, style, template, svg")) n.remove();
  let txt = doc.text || "";
  const attrRe = /\s(heading|caption|title|label|media-title|name|position|citation|alt|text)="([^"]*)"/gi;
  let m;
  while ((m = attrRe.exec(html || ""))) txt += " " + m[2];
  return squash(txt.replace(/&[a-z]+;|&#\d+;/gi, " ")).toLowerCase().split(/[^\p{L}\p{N}]+/u).filter((w) => w.length > 1);
}

/** Share of source words (multiset) that survive conversion. */
export function fidelity(beforeHtml, afterHtml) {
  const a = words(beforeHtml);
  if (!a.length) return { ratio: 1, sourceWords: 0, keptWords: 0 };
  const counts = new Map();
  for (const w of words(afterHtml)) counts.set(w, (counts.get(w) || 0) + 1);
  let kept = 0;
  for (const w of a) {
    const c = counts.get(w) || 0;
    if (c > 0) { kept++; counts.set(w, c - 1); }
  }
  return { ratio: kept / a.length, sourceWords: a.length, keptWords: kept };
}

const STATE_CLASS = /^(is-|has-|js-|active$|show$|open$|hidden$|visible$|clearfix$|container$|row$|col$|wrapper$|inner$|content$|block$|align|text-|bg-|mt-|mb-|pt-|pb-|p-|m-|d-|flex|grid$|w-\d|h-\d)/i;
const NOISE_CLASS = /\d{3,}|[a-f0-9]{6,}|^css-|^sc-[a-z]+$|^astro-|^svelte-|^e-\d|^elementor-element-|^elementor-\d|^et_pb_\w+_\d|^yui_/i;

function signatureOf(el) {
  const cls = String(el.getAttribute("class") || "").split(/\s+/).filter(Boolean)
    .filter((c) => !STATE_CLASS.test(c) && !NOISE_CLASS.test(c));
  if (!cls.length) return null;
  return `${el.tagName.toLowerCase()}.${cls.sort().slice(0, 3).join(".")}`;
}

function structure(el) {
  const has = (sel) => safeAll(el, sel).length;
  return {
    img: has("img, picture, media-image, image-gallery, video-player, [style*='background-image']"),
    heading: has("h1, h2, h3, h4, h5, h6, [class*='title'], [class*='heading']"),
    link: has("a[href]"),
    text: has("p"),
    button: has("button, a[class*='btn'], a[class*='button']"),
    icon: has("svg, i[class*='icon'], i[class*='fa-'], span[class*='icon']"),
    number: /\b\d{1,3}(,\d{3})*(\.\d+)?\s*(%|\+|k|m)?\b/i.test(squash(el.text)) ? 1 : 0,
    date: has("time") || /\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+\d{1,2}\b/i.test(squash(el.text)) ? 1 : 0,
    list: has("li"),
  };
}

/**
 * After conversion, find repeated, class-named structures that no rule handled.
 * These are the raw material for custom block proposals.
 */
export function unmappedComponents(transformedHtml) {
  const doc = parse(`<div>${transformedHtml}</div>`, PARSE_OPTS);
  const out = new Map();
  const inHax = (el) => {
    for (let p = el; p; p = p.parentNode) if (p.tagName && (p.tagName.includes("-") || (p.getAttribute && p.getAttribute("data-hax-review")))) return true;
    return false;
  };
  for (const el of safeAll(doc, "div[class], section[class], li[class], aside[class], article[class], figure[class]")) {
    if (inHax(el)) continue;
    const sig = signatureOf(el);
    if (!sig) continue;
    const s = structure(el);
    const kinds = ["img", "heading", "link", "text", "button", "icon"].filter((k) => s[k] > 0).length;
    if (kinds < 2) continue;
    if (squash(el.text).length > 2500) continue; // a layout region, not a component
    const cur = out.get(sig) || { signature: sig, count: 0, structure: s, sample: el.outerHTML.slice(0, 1200), textLength: squash(el.text).length };
    cur.count++;
    out.set(sig, cur);
  }
  // keep the outermost signature when a parent and child always appear together
  return [...out.values()];
}
