#!/usr/bin/env node
/**
 * Build hax-imports/import-example.html, the sample for HAX's HTML file import,
 * from a checkout of Learn HAX (https://github.com/haxtheweb/learn), so the
 * sample always shows current HAX documentation instead of a frozen copy.
 *
 *   git clone --depth 1 https://github.com/haxtheweb/learn
 *   node scripts/build-import-example-html.js <learn checkout> [output]
 *
 * The output is a HAXcms site export wrapped in haxcms-print-theme and loaded
 * from the HAX CDN, so opening the file shows the real blocks. Each page is a
 * heading followed by its content in a data-jos-item-id div: top-level pages
 * are h1 and every page below them is h2, the two levels the HTML importer
 * turns into pages and child pages. Content headings move down to h3 or lower
 * so they stay inside their page.
 *
 * So that an import works anywhere:
 * - relative src/href values become absolute URLs on the site's domain;
 * - site-only elements (built in the site's custom/ folder, not on the HAX
 *   CDN) are removed; learn-shelf, which lists a page's children, becomes a
 *   list of links to them; a childless page built around a site-only element
 *   (the arcade) is left out.
 *
 * Node built-ins only.
 */
const fs = require("fs");
const path = require("path");

const CDN = "https://cdn.hax.cloud/cdn/";
// Elements Learn defines in its own custom/ build; the HAX CDN doesn't serve them.
// learn-shelf lists a page's child pages, so it becomes a plain list of links.
const SITE_ONLY = ["learn-latest", "learn-arcade-cabinet"];

const src = process.argv[2];
const out =
  process.argv[3] ||
  path.join(__dirname, "..", "hax-imports", "import-example.html");
if (!src || !fs.existsSync(path.join(src, "site.json"))) {
  console.error(
    "usage: node scripts/build-import-example-html.js <learn checkout> [output]",
  );
  process.exit(1);
}

const site = JSON.parse(fs.readFileSync(path.join(src, "site.json"), "utf8"));
const domain = String(
  (site.metadata && site.metadata.site && site.metadata.site.domain) || "",
).replace(/\/?$/, "/");
if (!/^https:\/\//.test(domain)) {
  console.error("site.json metadata.site.domain must be an https URL");
  process.exit(1);
}
const lang = (site.metadata && site.metadata.site && site.metadata.site.lang) || "en";

function esc(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// pages in outline order: each parent, then its children by order
const items = site.items.slice();
const kids = new Map();
for (const item of items) {
  const p = item.parent || "";
  if (!kids.has(p)) kids.set(p, []);
  kids.get(p).push(item);
}
for (const list of kids.values()) {
  list.sort((a, b) => (a.order || 0) - (b.order || 0));
}
const ordered = [];
(function walk(parent, depth) {
  for (const item of kids.get(parent) || []) {
    ordered.push({ item, depth });
    walk(item.id, depth + 1);
  }
})("", 0);

function absolutize(html) {
  return html.replace(
    /\b(src|href|source)="(?!https?:|#|mailto:|tel:|data:|\/\/)([^"]*)"/g,
    (m, attr, value) => `${attr}="${domain}${value.replace(/^\.?\//, "")}"`,
  );
}

function stripSiteOnly(html) {
  for (const tag of SITE_ONLY) {
    html = html.replace(
      new RegExp(`<${tag}\\b[^>]*>[\\s\\S]*?</${tag}>`, "g"),
      "",
    );
  }
  return html;
}

function shelfToList(html, item) {
  return html.replace(/<learn-shelf\b[^>]*>[\s\S]*?<\/learn-shelf>/g, () => {
    const list = (kids.get(item.id) || [])
      .map((k) => `<li><a href="${domain}${esc(k.slug)}">${esc(k.title)}</a></li>`)
      .join("");
    return list ? `<ul>${list}</ul>` : "";
  });
}

function demoteHeadings(html) {
  const levels = [...html.matchAll(/<h([1-6])\b/g)].map((m) => Number(m[1]));
  if (!levels.length) return html;
  const shift = Math.max(0, 3 - Math.min(...levels));
  if (!shift) return html;
  return html.replace(/<(\/?)h([1-6])\b/g, (m, close, n) => {
    return `<${close}h${Math.min(6, Number(n) + shift)}`;
  });
}

// whether any text sits outside the tags (a check, not a sanitizer: nothing is removed)
function hasText(html) {
  let inTag = false;
  for (const ch of html) {
    if (ch === "<") inTag = true;
    else if (ch === ">") inTag = false;
    else if (!inTag && ch.trim()) return true;
  }
  return false;
}

const body = [];
let pages = 0;
for (const { item, depth } of ordered) {
  let html = "";
  try {
    html = fs.readFileSync(path.join(src, item.location), "utf8");
  } catch {
    continue;
  }
  const usedSiteOnly = SITE_ONLY.some((tag) => html.includes(`<${tag}`));
  if (usedSiteOnly && !kids.has(item.id) && !/<learn-shelf\b/.test(html)) {
    continue; // a page built around a site-only element, like the arcade, has nothing to import
  }
  html = shelfToList(stripSiteOnly(html), item);
  html = absolutize(html);
  html = demoteHeadings(html).trim();
  if (!hasText(html)) {
    html = "<p></p>"; // keep the page so its children stay under it
  }
  const h = depth === 0 ? "h1" : "h2";
  body.push(`<${h}>${esc(item.title)}</${h}>`);
  body.push(`<div data-jos-item-id="${esc(item.id)}">`);
  body.push(html);
  body.push("</div>");
  pages++;
}

const doc = [
  "<!DOCTYPE html>",
  `<html lang="${esc(lang)}">`,
  "<head>",
  '<meta charset="utf-8">',
  `<title>${esc(site.title || "Learn HAX")}</title>`,
  `<link rel="preconnect" crossorigin href="${CDN}">`,
  `<link rel="preload" href="${CDN}build.js" as="script" />`,
  `<link rel="preload" href="${CDN}wc-registry.json" as="fetch" crossorigin="anonymous" />`,
  `<link rel="stylesheet" href="${CDN}build/es6/node_modules/@haxtheweb/haxcms-elements/lib/base.css" />`,
  '<meta name="viewport" content="width=device-width, minimum-scale=1, initial-scale=1, user-scalable=yes">',
  "</head>",
  "<body>",
  "<haxcms-print-theme>",
  ...body,
  "</haxcms-print-theme>",
  "</body>",
  `<script>window.__appCDN="${CDN}";</script>`,
  `<script src="${CDN}build.js"></script>`,
  "</html>",
  "",
].join("\n");

fs.writeFileSync(out, doc);
console.log(`${path.basename(out)}: ${pages} pages from ${domain}`);
