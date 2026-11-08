// Rule engine: turn a page's content HTML into HAX-authorable HTML using the
// block maps in references/block-maps/. See block-maps/README.md for the format.
import { readFileSync, existsSync } from "node:fs";
import { parse } from "node-html-parser";

// pre must parse as HTML so <pre><code> can be matched; scripts and styles stay raw text
const PARSE_OPTS = { comment: false, blockTextElements: { script: true, noscript: true, style: true } };


const MAPS = new URL("../../references/block-maps/", import.meta.url);
const MAX_DEPTH = 6;

export function loadMap(id) {
  const f = new URL(`${id}.json`, MAPS);
  if (!existsSync(f)) return null;
  return JSON.parse(readFileSync(f, "utf8"));
}

/** Maps in precedence order: builder layers, then the platform, then generic-html. */
export function mapsFor(fp) {
  const ids = [];
  for (const l of fp.layers || []) if (l.blockMap) ids.push(l.blockMap);
  if (fp.primary && fp.primary.blockMap) ids.push(fp.primary.blockMap);
  ids.push("generic-html");
  const seen = new Set();
  return ids.filter((i) => !seen.has(i) && seen.add(i)).map(loadMap).filter(Boolean);
}

export const escapeAttr = (s) => String(s).replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
export const escapeText = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const kebab = (s) => s.replace(/([a-z0-9])([A-Z])/g, "$1-$2").toLowerCase();
const squash = (s) => String(s || "").replace(/\s+/g, " ").trim();

function selectFrom(el, sel) {
  if (!sel) return el;
  try {
    return sel.startsWith(">") ? el.querySelector(`:scope ${sel}`) : el.querySelector(sel);
  } catch (e) {
    return null;
  }
}

/** Evaluate an extractor expression such as "img@data-src|img@src" or "=warning". */
export function extract(el, expr) {
  if (!expr) return { value: "", kind: "text" };
  for (const alt of String(expr).split("|")) {
    const a = alt.trim();
    if (!a) continue;
    if (a.startsWith("=")) return { value: a.slice(1), kind: "text" };
    const at = a.indexOf("@");
    if (at < 0) continue;
    const target = selectFrom(el, a.slice(0, at).trim());
    if (!target) continue;
    const rest = a.slice(at + 1);
    const opMatch = rest.match(/^([a-z][a-z-]*)(?::(.*?))?(?:~(.+)|#(.+))?$/i);
    if (!opMatch) continue;
    const [, op, opArg, regex, jsonKey] = opMatch;
    let value = "";
    let kind = "text";
    if (op === "text") value = squash(target.text);
    else if (op === "html") { value = target.innerHTML; kind = "html"; }
    else if (op === "outer-html") { value = target.outerHTML; kind = "html"; }
    else if (op === "html-without") {
      const frag = parse(target.innerHTML);
      if (opArg) for (const n of frag.querySelectorAll(opArg)) n.remove();
      value = frag.toString();
      kind = "html";
    } else if (op === "raw-template") {
      value = `<template preserve-content="preserve-content">${escapeText(target.text)}</template>`;
      kind = "html";
    } else {
      value = target.getAttribute(op);
      if (value == null) value = "";
      if (jsonKey && value) {
        try { const j = JSON.parse(value); value = j && j[jsonKey] != null ? String(j[jsonKey]) : ""; } catch (e) { value = ""; }
      }
    }
    if (regex && value) {
      const m = String(value).match(new RegExp(regex, "i"));
      value = m ? m[1] || m[0] : "";
    }
    if (kind === "html" ? squash(value.replace(/<[^>]+>/g, " ")) || /<(img|iframe|video|audio|svg|hr)/i.test(value) : squash(value)) {
      return { value, kind };
    }
  }
  return { value: "", kind: "text" };
}

function attrString(attrs) {
  return Object.entries(attrs)
    .filter(([, v]) => v !== "" && v != null)
    .map(([k, v]) => ` ${kebab(k)}="${escapeAttr(v)}"`)
    .join("");
}

function hasAncestorIn(node, set, root) {
  for (let p = node; p && p !== root; p = p.parentNode) if (set.has(p)) return true;
  return false;
}

function attached(node, root) {
  for (let p = node; p; p = p.parentNode) if (p === root) return true;
  return false;
}

function inside(node, selectors, root) {
  if (!selectors || !selectors.length) return false;
  for (let p = node.parentNode; p && p !== root; p = p.parentNode) {
    if (p.tagName && selectors.includes(p.tagName.toLowerCase())) return true;
  }
  return false;
}

function directChildren(el, sel) {
  let found;
  try { found = el.querySelectorAll(sel); } catch (e) { return []; }
  // keep only the outermost matches, so nested columns are not double-counted
  const set = new Set(found);
  return found.filter((n) => {
    for (let p = n.parentNode; p && p !== el; p = p.parentNode) if (set.has(p)) return false;
    return true;
  });
}

/** Build replacement HTML for a converted node. Returns null to leave the node alone. */
function buildElement(node, rule, ctx, depth) {
  const attrs = {};
  for (const [prop, expr] of Object.entries(rule.attrs || {})) {
    attrs[prop] = extract(node, expr).value;
  }
  let inner = "";
  if (rule.children) {
    const kids = directChildren(node, rule.children.select);
    if (!kids.length) return null;
    if (rule.layout === "auto") {
      if (kids.length > 6) return null;
      attrs.layout = Array(kids.length).fill("1").join("-");
      if (kids.length === 1) return null;
    }
    kids.forEach((k, i) => {
      if (rule.children.to) {
        inner += buildElement(k, rule.children, ctx, depth + 1) || "";
      } else {
        const slot = (rule.children.slot || "").replace("{n}", String(i + 1));
        const c = extract(k, rule.children.content || "@html");
        const body = c.kind === "html" ? transformHtml(c.value, ctx, depth + 1) : escapeText(c.value);
        inner += slot ? `<div slot="${slot}">${body}</div>` : body;
      }
    });
  }
  if (rule.layout === "fromClass" && rule.layoutClassMap) {
    const cls = String(node.getAttribute("class") || "").split(/\s+/);
    for (const [c, layout] of Object.entries(rule.layoutClassMap)) if (cls.includes(c)) attrs.layout = layout;
    if (!attrs.layout) attrs.layout = "1-1";
  }
  if (rule.content) {
    const c = extract(node, rule.content);
    inner += c.kind === "html" ? transformHtml(c.value, ctx, depth + 1) : escapeText(c.value);
  }
  for (const [slot, expr] of Object.entries(rule.slots || {})) {
    const c = extract(node, expr);
    if (!c.value) continue;
    inner += c.kind === "html"
      ? `<div slot="${slot}">${transformHtml(c.value, ctx, depth + 1)}</div>`
      : `<span slot="${slot}">${escapeText(c.value)}</span>`;
  }
  if (rule.asset) {
    for (const v of Object.values(attrs)) if (v && /^(https?:)?\/\/|^\//.test(v)) ctx.assets.add(v);
  }
  return `<${rule.to}${attrString(attrs)}>${inner}</${rule.to}>`;
}

function record(ctx, rule, node, extra = {}) {
  const k = `${ctx.mapIdOf.get(rule)}:${rule.id}`;
  ctx.stats.rules[k] = (ctx.stats.rules[k] || 0) + 1;
  if (rule.to === "flag") {
    let gapKey = rule.gapKey ? extract(node, rule.gapKey).value : "";
    ctx.stats.flags.push({ flag: rule.flag || "review", rule: k, gapKey, note: rule.note || "", sample: node.outerHTML.slice(0, 600), ...extra });
  }
}

/** Apply all rules to an HTML string. */
export function transformHtml(html, ctx, depth = 0) {
  if (depth > MAX_DEPTH || !html) return html || "";
  const root = parse(`<div id="hax-mig-root">${html}</div>`, PARSE_OPTS);
  const top = root.querySelector("#hax-mig-root");
  if (!top) return html;
  const done = new Set();
  for (const rule of ctx.rules) {
    let nodes;
    try { nodes = top.querySelectorAll(rule.match); } catch (e) { ctx.stats.badSelectors.add(rule.match); continue; }
    for (const node of nodes) {
      if (!attached(node, top) || hasAncestorIn(node, done, top)) continue;
      if (node.getAttribute && node.getAttribute("data-hax-review")) continue;
      if (inside(node, rule.skipInside, top)) continue;
      if (rule.to === "drop") { record(ctx, rule, node); node.remove(); continue; }
      if (rule.to === "unwrap") { record(ctx, rule, node); node.replaceWith(...node.childNodes); continue; }
      if (rule.to === "keep") {
        record(ctx, rule, node);
        if (rule.asset) {
          for (const a of node.querySelectorAll("a[href]").concat(node.tagName === "A" ? [node] : [])) ctx.assets.add(a.getAttribute("href"));
        }
        done.add(node);
        continue;
      }
      if (rule.to === "flag") { record(ctx, rule, node); done.add(node); node.setAttribute("data-hax-review", rule.flag || "review"); continue; }
      let out = null;
      if (rule.to === "html") out = rule.html || "";
      else if (rule.to === "link") {
        const href = extract(node, (rule.attrs && rule.attrs.href) || "a@href").value;
        out = href ? `<p><a href="${escapeAttr(href)}">${escapeText(squash(node.text) || href)}</a></p>` : null;
      } else out = buildElement(node, rule, ctx, depth);
      if (out == null) continue;
      record(ctx, rule, node);
      const frag = parse(out, PARSE_OPTS);
      const fresh = [...frag.childNodes];
      node.replaceWith(...fresh);
      for (const f of fresh) done.add(f);
    }
  }
  // flagged nodes keep their content but it still gets converted
  for (const f of top.querySelectorAll("[data-hax-review]")) {
    let outer = true;
    for (let p = f.parentNode; p && p !== top; p = p.parentNode) if (p.getAttribute && p.getAttribute("data-hax-review")) outer = false;
    if (outer) f.set_content(transformHtml(f.innerHTML, ctx, depth + 1));
  }
  return top.innerHTML;
}

const KEEP_ATTRS = new Set(["href", "src", "alt", "title", "id", "colspan", "rowspan", "scope", "headers", "lang", "dir", "start", "reversed", "value", "datetime", "cite", "slot", "data-hax-review", "width", "height", "type", "open", "preserve-content"]);
const WRAPPERS = new Set(["div", "span", "section", "article", "font", "center", "main"]);

/** Strip presentational wrappers and attributes from native tags; HAX elements keep theirs. */
export function cleanHtml(html) {
  const root = parse(`<div id="hax-mig-root">${html}</div>`, PARSE_OPTS);
  const top = root.querySelector("#hax-mig-root");
  const walk = (el) => {
    for (const child of [...el.childNodes]) {
      if (child.nodeType !== 1) continue;
      const tag = child.tagName.toLowerCase();
      const isCustom = tag.includes("-");
      if (!isCustom) {
        for (const name of Object.keys(child.attributes)) {
          if (!KEEP_ATTRS.has(name.toLowerCase())) child.removeAttribute(name);
        }
      }
      walk(child);
      if (!isCustom && WRAPPERS.has(tag) && !child.getAttribute("slot") && !child.getAttribute("data-hax-review") && !child.getAttribute("id")) {
        child.replaceWith(...child.childNodes);
      }
    }
  };
  walk(top);
  return top.innerHTML.replace(/\n{3,}/g, "\n\n").trim();
}

/** Convenience: transform + clean, returning html and stats. */
export function convert(html, maps) {
  const rules = [];
  const mapIdOf = new Map();
  for (const m of maps) for (const r of m.rules) { rules.push(r); mapIdOf.set(r, m.id); }
  const ctx = { rules, mapIdOf, stats: { rules: {}, flags: [], badSelectors: new Set() }, assets: new Set() };
  const transformed = transformHtml(html, ctx, 0);
  const out = cleanHtml(transformed);
  return { html: out, transformed, stats: { rules: ctx.stats.rules, flags: ctx.stats.flags, badSelectors: [...ctx.stats.badSelectors] }, assets: [...ctx.assets] };
}
