#!/usr/bin/env node
/**
 * Refresh the HAX impact data in praw/impact/ from public sources.
 *
 *   node scripts/impact-stats.mjs            # everything
 *   node scripts/impact-stats.mjs npm        # npm downloads for @haxtheweb
 *   node scripts/impact-stats.mjs velocity   # issues closed per HAX release
 *   node scripts/impact-stats.mjs prs        # merged PRs per month, core repos
 *   node scripts/impact-stats.mjs charts     # redraw SVG charts from the data
 *
 * Writes:
 *   impact/npm-downloads.json      totals + every package's weekly/monthly downloads
 *   impact/release-velocity.csv    closed issues in haxtheweb/issues per major release
 *   impact/merged-prs-by-month.csv merged pull requests per month across core repos
 *   impact/*.svg                   accessible charts drawn from the CSVs
 *
 * Needs Node 18+ (global fetch). Set GITHUB_TOKEN (or GH_TOKEN) to avoid
 * GitHub's 60-requests-an-hour limit for anonymous calls. Behind a proxy, run
 * with NODE_USE_ENV_PROXY=1 so fetch honors HTTPS_PROXY.
 *
 * Release windows: a "major release" is the first webcomponents tag of each
 * major version (1.0.0, 2.0.0 … 26.0.0), plus the newest tag as the open end.
 * Issues are counted by `closed_at` in the unified queue, haxtheweb/issues.
 */
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const OUT = join(ROOT, "impact");
const ORG = "haxtheweb";
const ISSUE_REPO = "issues";
const TAG_REPO = "webcomponents";
const CORE_REPOS = [
  "webcomponents",
  "haxcms-nodejs",
  "haxcms-php",
  "create",
  "praw",
  "issues",
];
const TOKEN = process.env.GITHUB_TOKEN || process.env.GH_TOKEN || "";
const DAY = 86400000;
const MONTH_DAYS = 30.4375;

mkdirSync(OUT, { recursive: true });

async function getJSON(url, headers = {}) {
  const res = await fetch(url, { headers });
  if (!res.ok) {
    throw new Error(`${res.status} ${res.statusText} for ${url}`);
  }
  return { body: await res.json(), headers: res.headers };
}

function ghHeaders() {
  const h = {
    Accept: "application/vnd.github+json",
    "User-Agent": "haxtheweb-praw-impact-stats",
  };
  if (TOKEN) {
    h.Authorization = `Bearer ${TOKEN}`;
  }
  return h;
}

// Page through a GitHub list endpoint by page number. (GitHub's Link headers
// point at /repositories/<id>/…, which some proxies refuse, so the original
// /repos/<owner>/<repo> path is kept.)
async function ghAll(path) {
  const base = `https://api.github.com${path}${path.includes("?") ? "&" : "?"}per_page=100`;
  const all = [];
  for (let page = 1; ; page++) {
    const { body } = await getJSON(`${base}&page=${page}`, ghHeaders());
    all.push(...body);
    if (body.length < 100) {
      break;
    }
  }
  return all;
}

function csv(rows) {
  return rows.map((r) => r.join(",")).join("\n") + "\n";
}

function readCSV(file) {
  const [head, ...lines] = readFileSync(join(OUT, file), "utf8")
    .trim()
    .split("\n");
  const keys = head.split(",");
  return lines.map((l) => {
    const v = l.split(",");
    return Object.fromEntries(keys.map((k, i) => [k, v[i]]));
  });
}

// ---------------------------------------------------------------- npm
async function npmStats() {
  const pkgs = [];
  for (let from = 0; ; from += 250) {
    const url = `https://registry.npmjs.org/-/v1/search?text=%40${ORG}&size=250&from=${from}`;
    const { body } = await getJSON(url);
    for (const o of body.objects) {
      if (o.package.name.startsWith(`@${ORG}/`)) {
        pkgs.push({
          name: o.package.name,
          version: o.package.version,
          weekly: (o.downloads && o.downloads.weekly) || 0,
          monthly: (o.downloads && o.downloads.monthly) || 0,
        });
      }
    }
    if (body.objects.length < 250) {
      break;
    }
  }
  const seen = new Map(pkgs.map((p) => [p.name, p]));
  const list = [...seen.values()].sort((a, b) => b.monthly - a.monthly);
  const sum = (k) => list.reduce((n, p) => n + p[k], 0);
  const data = {
    source: "npm registry search (registry.npmjs.org/-/v1/search)",
    retrieved: new Date().toISOString().slice(0, 10),
    scope: `@${ORG}`,
    packages: list.length,
    weekly: sum("weekly"),
    monthly: sum("monthly"),
    list,
  };
  writeFileSync(
    join(OUT, "npm-downloads.json"),
    JSON.stringify(data, null, 2) + "\n",
  );
  console.log(
    `npm: ${data.packages} packages, ${data.monthly} downloads in the last month`,
  );
}

// ------------------------------------------------------------ velocity
function parseVersion(name) {
  const m = name.match(/^v?(\d+)\.(\d+)\.(\d+)$/);
  return m ? m.slice(1, 4).map(Number) : null;
}

async function tagDate(sha) {
  const { body } = await getJSON(
    `https://api.github.com/repos/${ORG}/${TAG_REPO}/commits/${sha}`,
    ghHeaders(),
  );
  return new Date(body.commit.committer.date);
}

async function velocity() {
  const tags = (await ghAll(`/repos/${ORG}/${TAG_REPO}/tags`))
    .map((t) => ({ name: t.name, v: parseVersion(t.name), sha: t.commit.sha }))
    .filter((t) => t.v);
  const cmp = (a, b) => a.v[0] - b.v[0] || a.v[1] - b.v[1] || a.v[2] - b.v[2];
  tags.sort(cmp);
  const firstOfMajor = new Map();
  for (const t of tags) {
    if (!firstOfMajor.has(t.v[0])) {
      firstOfMajor.set(t.v[0], t);
    }
  }
  const points = [...firstOfMajor.values()];
  const newest = tags[tags.length - 1];
  if (newest && newest !== points[points.length - 1]) {
    points.push(newest);
  }
  for (const p of points) {
    p.date = await tagDate(p.sha);
  }
  // Open window: newest tag to today, so current work is counted too.
  points.push({ name: "today", date: new Date() });

  const closed = (
    await ghAll(`/repos/${ORG}/${ISSUE_REPO}/issues?state=closed`)
  )
    .filter((i) => !i.pull_request && i.closed_at)
    .map((i) => new Date(i.closed_at));

  const rows = [
    [
      "start_tag",
      "end_tag",
      "start_date",
      "end_date",
      "days",
      "closed_issues",
      "issues_per_month",
    ],
  ];
  for (let i = 0; i < points.length - 1; i++) {
    const a = points[i];
    const b = points[i + 1];
    const n = closed.filter((d) => d >= a.date && d < b.date).length;
    const days = (b.date - a.date) / DAY;
    if (rows.length === 1 && n === 0) {
      continue; // before the unified issue queue existed
    }
    rows.push([
      a.name,
      b.name,
      a.date.toISOString().slice(0, 10),
      b.date.toISOString().slice(0, 10),
      days.toFixed(1),
      n,
      days > 0 ? (n / (days / MONTH_DAYS)).toFixed(1) : "",
    ]);
  }
  writeFileSync(join(OUT, "release-velocity.csv"), csv(rows));
  console.log(`velocity: ${rows.length - 1} release windows`);
}

// ---------------------------------------------------------------- prs
async function mergedPRs() {
  const byMonth = new Map();
  for (const repo of CORE_REPOS) {
    const prs = await ghAll(`/repos/${ORG}/${repo}/pulls?state=closed`);
    for (const pr of prs) {
      if (!pr.merged_at) {
        continue;
      }
      const m = pr.merged_at.slice(0, 7);
      const row =
        byMonth.get(m) || Object.fromEntries(CORE_REPOS.map((r) => [r, 0]));
      row[repo]++;
      byMonth.set(m, row);
    }
  }
  // Every month from the first merge to now, including months with none.
  const seen = [...byMonth.keys()].sort();
  const months = [];
  if (seen.length) {
    let [y, m] = seen[0].split("-").map(Number);
    const end = new Date().toISOString().slice(0, 7);
    for (;;) {
      const key = `${y}-${String(m).padStart(2, "0")}`;
      months.push(key);
      if (key >= end) {
        break;
      }
      m++;
      if (m > 12) {
        m = 1;
        y++;
      }
    }
  }
  const zero = () => Object.fromEntries(CORE_REPOS.map((r) => [r, 0]));
  const rows = [["month", ...CORE_REPOS, "total"]];
  for (const m of months) {
    const r = byMonth.get(m) || zero();
    const total = CORE_REPOS.reduce((n, k) => n + r[k], 0);
    rows.push([m, ...CORE_REPOS.map((k) => r[k]), total]);
  }
  writeFileSync(join(OUT, "merged-prs-by-month.csv"), csv(rows));
  console.log(`prs: ${months.length} months across ${CORE_REPOS.length} repos`);
}

// -------------------------------------------------------------- charts
function esc(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;");
}

// A plain, accessible bar chart: title + desc for screen readers, one color,
// labels in text, no reliance on color alone.
function barChart({ title, desc, labels, values, unit, every = 1 }) {
  const W = 960;
  const H = 440;
  const pad = { l: 72, r: 16, t: 48, b: 96 };
  const max = Math.max(1, ...values);
  const bw = (W - pad.l - pad.r) / values.length;
  const y = (v) => H - pad.b - (v / max) * (H - pad.t - pad.b);
  const ticks = 4;
  let g = "";
  for (let i = 0; i <= ticks; i++) {
    const v = Math.round((max / ticks) * i);
    g += `<line x1="${pad.l}" x2="${W - pad.r}" y1="${y(v)}" y2="${y(v)}" stroke="#d0d7de"/>`;
    g += `<text x="${pad.l - 8}" y="${y(v) + 4}" text-anchor="end" font-size="12">${v}</text>`;
  }
  values.forEach((v, i) => {
    const x = pad.l + i * bw;
    g += `<rect x="${(x + bw * 0.15).toFixed(1)}" y="${y(v).toFixed(1)}" width="${(bw * 0.7).toFixed(1)}" height="${(H - pad.b - y(v)).toFixed(1)}" fill="#1e407c"><title>${esc(labels[i])}: ${v} ${esc(unit)}</title></rect>`;
    if (i % every === 0 || i === values.length - 1) {
      g += `<text x="${(x + bw / 2).toFixed(1)}" y="${H - pad.b + 16}" font-size="11" text-anchor="end" transform="rotate(-45 ${(x + bw / 2).toFixed(1)} ${H - pad.b + 16})">${esc(labels[i])}</text>`;
    }
  });
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" role="img" aria-labelledby="t d" font-family="system-ui, sans-serif" fill="#1f2328">
<title id="t">${esc(title)}</title>
<desc id="d">${esc(desc)}</desc>
<rect width="${W}" height="${H}" fill="#ffffff"/>
<text x="${pad.l}" y="28" font-size="18" font-weight="600">${esc(title)}</text>
${g}
</svg>
`;
}

function charts() {
  const vel = readCSV("release-velocity.csv");
  const vLabels = vel.map((r) => `${r.start_tag}→${r.end_tag}`);
  const vValues = vel.map((r) => Number(r.issues_per_month) || 0);
  writeFileSync(
    join(OUT, "release-velocity.svg"),
    barChart({
      title: "Issues closed per month, by HAX release",
      desc: `Issues closed per month in haxtheweb/issues for each major HAX release window. ${vLabels
        .map((l, i) => `${l}: ${vValues[i]}`)
        .join("; ")}.`,
      labels: vLabels,
      values: vValues,
      unit: "issues a month",
    }),
  );
  const prs = readCSV("merged-prs-by-month.csv").slice(-36);
  const pLabels = prs.map((r) => r.month);
  const pValues = prs.map((r) => Number(r.total));
  writeFileSync(
    join(OUT, "merged-prs-by-month.svg"),
    barChart({
      title: "Merged pull requests per month, core HAX repos",
      desc: `Merged pull requests per month across ${CORE_REPOS.join(", ")}, last ${prs.length} months. ${pLabels
        .map((l, i) => `${l}: ${pValues[i]}`)
        .join("; ")}.`,
      labels: pLabels,
      values: pValues,
      unit: "merged PRs",
      every: 3,
    }),
  );
  console.log("charts: release-velocity.svg, merged-prs-by-month.svg");
}

const cmd = process.argv[2] || "all";
const steps = {
  npm: [npmStats],
  velocity: [velocity],
  prs: [mergedPRs],
  charts: [charts],
  all: [npmStats, velocity, mergedPRs, charts],
}[cmd];
if (!steps) {
  console.error(
    `Unknown command "${cmd}". Use npm, velocity, prs, charts or all.`,
  );
  process.exit(1);
}
for (const step of steps) {
  await step();
}
