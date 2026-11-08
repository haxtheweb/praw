// Polite, bounded HTTP for site analysis.
// - identifies itself, honors robots.txt, waits between requests to a host
// - refuses private and loopback addresses unless allowPrivate is set (SSRF guard;
//   the haxcms-nodejs port must use its own safeFetch instead)
// - caps response size and time
import { lookup } from "node:dns/promises";
import net from "node:net";

export const USER_AGENT =
  "HAXcms-Import/1.0 (+https://github.com/haxtheweb/praw/tree/main/skills/hax-url-migration)";

export const LIMITS = {
  timeoutMs: 15000,
  maxBytes: 4 * 1024 * 1024,
  maxRedirects: 5,
  hostDelayMs: 750,
};

const lastHit = new Map();
const robotsCache = new Map();

function isPrivateIp(ip) {
  if (net.isIPv4(ip)) {
    const [a, b] = ip.split(".").map(Number);
    return (
      a === 10 || a === 127 || a === 0 ||
      (a === 169 && b === 254) ||
      (a === 172 && b >= 16 && b <= 31) ||
      (a === 192 && b === 168) ||
      (a === 100 && b >= 64 && b <= 127)
    );
  }
  const v = ip.toLowerCase();
  return v === "::1" || v.startsWith("fc") || v.startsWith("fd") || v.startsWith("fe80") || v.startsWith("::ffff:127.");
}

async function assertPublic(urlObj, allowPrivate) {
  if (allowPrivate) return;
  if (!/^https?:$/.test(urlObj.protocol)) throw new Error(`blocked protocol ${urlObj.protocol}`);
  const host = urlObj.hostname.replace(/^\[|\]$/g, "");
  const addrs = net.isIP(host) ? [{ address: host }] : await lookup(host, { all: true });
  for (const a of addrs) {
    if (isPrivateIp(a.address)) throw new Error(`blocked private address for ${host}`);
  }
}

async function waitForHost(host) {
  const last = lastHit.get(host) || 0;
  const wait = last + LIMITS.hostDelayMs - Date.now();
  if (wait > 0) await new Promise((r) => setTimeout(r, wait));
  lastHit.set(host, Date.now());
}

async function readCapped(res) {
  const reader = res.body && res.body.getReader ? res.body.getReader() : null;
  if (!reader) return await res.text();
  const chunks = [];
  let total = 0;
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    total += value.length;
    if (total > LIMITS.maxBytes) {
      try { await reader.cancel(); } catch (e) { /* ignore */ }
      chunks.push(value.slice(0, value.length - (total - LIMITS.maxBytes)));
      break;
    }
    chunks.push(value);
  }
  return Buffer.concat(chunks.map((c) => Buffer.from(c))).toString("utf8");
}

/**
 * Fetch a URL. Returns { url, finalUrl, status, headers (lowercased object),
 * setCookies (array), body, error, ms }. Never throws.
 */
export async function fetchPage(url, opts = {}) {
  const started = Date.now();
  let current = new URL(url);
  const headersOut = {};
  let setCookies = [];
  try {
    for (let hop = 0; hop <= LIMITS.maxRedirects; hop++) {
      await assertPublic(current, opts.allowPrivate);
      await waitForHost(current.host);
      const ctrl = new AbortController();
      const timer = setTimeout(() => ctrl.abort(), LIMITS.timeoutMs);
      let res;
      try {
        res = await fetch(current, {
          redirect: "manual",
          signal: ctrl.signal,
          headers: {
            "user-agent": USER_AGENT,
            accept: opts.accept || "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.5",
          },
        });
      } finally {
        clearTimeout(timer);
      }
      if (res.status >= 300 && res.status < 400 && res.headers.get("location")) {
        current = new URL(res.headers.get("location"), current);
        continue;
      }
      res.headers.forEach((v, k) => { headersOut[k.toLowerCase()] = v; });
      setCookies = typeof res.headers.getSetCookie === "function" ? res.headers.getSetCookie() : [];
      const body = opts.method === "HEAD" ? "" : await readCapped(res);
      return { url, finalUrl: current.href, status: res.status, headers: headersOut, setCookies, body, ms: Date.now() - started };
    }
    return { url, finalUrl: current.href, status: 0, headers: headersOut, setCookies, body: "", error: "too many redirects", ms: Date.now() - started };
  } catch (e) {
    return { url, finalUrl: current.href, status: 0, headers: headersOut, setCookies, body: "", error: String(e && e.message ? e.message : e), ms: Date.now() - started };
  }
}

/** Minimal robots.txt check for User-agent: * (and our own agent token). */
export async function robotsAllows(urlStr, opts = {}) {
  const u = new URL(urlStr);
  const key = u.origin;
  if (!robotsCache.has(key)) {
    const r = await fetchPage(`${u.origin}/robots.txt`, { ...opts, accept: "text/plain" });
    robotsCache.set(key, r.status === 200 ? parseRobots(r.body) : { disallow: [], allow: [], sitemaps: [] });
  }
  const rules = robotsCache.get(key);
  const path = u.pathname + u.search;
  const longest = (list) => list.filter((p) => p && path.startsWith(p)).reduce((m, p) => Math.max(m, p.length), -1);
  return longest(rules.allow) >= longest(rules.disallow);
}

export function robotsSitemaps(origin) {
  const r = robotsCache.get(origin);
  return r ? r.sitemaps : [];
}

export function parseRobots(text) {
  const out = { disallow: [], allow: [], sitemaps: [] };
  let applies = false;
  let sawAgentInGroup = false;
  for (const raw of String(text).split(/\r?\n/)) {
    const line = raw.replace(/#.*/, "").trim();
    if (!line) continue;
    const idx = line.indexOf(":");
    if (idx < 0) continue;
    const field = line.slice(0, idx).trim().toLowerCase();
    const value = line.slice(idx + 1).trim();
    if (field === "sitemap") { out.sitemaps.push(value); continue; }
    if (field === "user-agent") {
      if (!sawAgentInGroup) applies = false;
      sawAgentInGroup = true;
      if (value === "*" || /haxcms-import/i.test(value)) applies = true;
      continue;
    }
    sawAgentInGroup = false;
    if (!applies) continue;
    if (field === "disallow" && value) out.disallow.push(value.replace(/\*.*$/, ""));
    if (field === "allow" && value) out.allow.push(value.replace(/\*.*$/, ""));
  }
  return out;
}
