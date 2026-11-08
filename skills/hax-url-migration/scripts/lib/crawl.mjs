// Pick a small, varied sample of pages: sitemap first, then the home page's links.
import { parse } from "node-html-parser";

import { fetchPage, robotsAllows, robotsSitemaps } from "./net.mjs";

// pre must parse as HTML so <pre><code> can be matched; scripts and styles stay raw text
const PARSE_OPTS = { comment: false, blockTextElements: { script: true, noscript: true, style: true } };

const SKIP = /\.(pdf|docx?|xlsx?|pptx?|zip|jpe?g|png|gif|svg|webp|mp4|mp3|ics|xml|json|css|js)(\?|$)|\/(wp-admin|wp-login|user\/login|login|logout|cart|checkout|search|tag|tags|category|author|feed|comment)(\/|$)|[?&](replytocom|share|print)=/i;

function sameSite(a, b) {
  return a.replace(/^www\./, "") === b.replace(/^www\./, "");
}

function locsFrom(xml) {
  const out = [];
  const re = /<loc>\s*([^<\s]+)\s*<\/loc>/gi;
  let m;
  while ((m = re.exec(xml))) out.push(m[1].replace(/&amp;/g, "&"));
  return out;
}

async function sitemapUrls(origin, fetchOpts, budget = 4) {
  await robotsAllows(origin + "/", fetchOpts); // primes the robots cache
  const queue = [...robotsSitemaps(origin), `${origin}/sitemap.xml`, `${origin}/wp-sitemap.xml`, `${origin}/sitemap_index.xml`];
  const seen = new Set();
  const pages = [];
  while (queue.length && budget-- > 0) {
    const sm = queue.shift();
    if (seen.has(sm)) { budget++; continue; }
    seen.add(sm);
    const r = await fetchPage(sm, { ...fetchOpts, accept: "application/xml,text/xml" });
    if (r.status !== 200 || !/<(urlset|sitemapindex)/i.test(r.body)) continue;
    const locs = locsFrom(r.body);
    if (/<sitemapindex/i.test(r.body)) {
      // prefer page sitemaps over post/taxonomy ones
      locs.sort((a, b) => (/page/i.test(b) ? 1 : 0) - (/page/i.test(a) ? 1 : 0));
      queue.unshift(...locs.slice(0, 3));
    } else pages.push(...locs);
    if (pages.length > 400) break;
  }
  return { pages, sitemaps: [...seen] };
}

export function linksFrom(html, baseUrl) {
  const doc = parse(html || "", PARSE_OPTS);
  const out = [];
  for (const a of doc.querySelectorAll("a[href]")) {
    try {
      const u = new URL(a.getAttribute("href"), baseUrl);
      u.hash = "";
      out.push({ href: u.href, text: (a.text || "").replace(/\s+/g, " ").trim(), rel: a.getAttribute("rel") || "", inNav: !!a.closest("nav, header, [role=navigation]") });
    } catch (e) { /* ignore bad hrefs */ }
  }
  return out;
}

/** Choose up to n URLs spread across different top-level sections. */
export function pickVaried(urls, n, home) {
  const h = new URL(home);
  const buckets = new Map();
  for (const raw of urls) {
    let u;
    try { u = new URL(raw); } catch (e) { continue; }
    if (!sameSite(u.hostname, h.hostname) || SKIP.test(u.pathname + u.search)) continue;
    if (u.pathname === h.pathname) continue;
    const seg = u.pathname.split("/").filter(Boolean)[0] || "";
    if (!buckets.has(seg)) buckets.set(seg, []);
    const b = buckets.get(seg);
    if (!b.includes(u.href)) b.push(u.href);
  }
  const out = [];
  const lists = [...buckets.values()];
  for (let i = 0; out.length < n && lists.some((l) => l.length > i); i++) {
    for (const l of lists) if (l[i] && out.length < n) out.push(l[i]);
  }
  return out;
}

export async function discover(home, n, fetchOpts = {}) {
  const origin = new URL(home.finalUrl).origin;
  const sm = await sitemapUrls(origin, fetchOpts);
  const navLinks = linksFrom(home.body, home.finalUrl);
  const fromNav = navLinks.filter((l) => l.inNav).map((l) => l.href);
  const fromBody = navLinks.map((l) => l.href);
  // navigation pages first (they are what the menu promises), then sitemap, then any link
  const picked = pickVaried([...fromNav, ...sm.pages, ...fromBody], n, home.finalUrl);
  const allowed = [];
  for (const u of picked) if (await robotsAllows(u, fetchOpts)) allowed.push(u);
  return { urls: allowed, sitemapCount: sm.pages.length, sitemaps: sm.sitemaps, navCount: fromNav.length };
}
