#!/usr/bin/env node
// graph-drift: check the HAX ecosystem graph against what has actually shipped.
//
// Reads hax-ecosystem.json, looks up every node that names a release source
//   "release": "npm:@haxtheweb/create"      latest version on npm
//   "release": "git:haxtheweb/haxcms-php"   newest version tag on GitHub
// and reports nodes whose recorded version or status no longer matches.
// A source with no published release is treated as pre-release.
//
// Usage:
//   node graph-drift.mjs [path/to/hax-ecosystem.json] [--write] [--strict]
//     --write   update versions, statuses and meta.checked in place
//     --strict  exit 1 when the graph is out of date (for a release step)
//
// Intended to run after each release (for example at the end of a ubiquity
// build) so the graph is flagged for an update instead of drifting silently.
// Needs only node, npm and git on the PATH.

import { readFileSync, writeFileSync } from "node:fs";
import { execFileSync } from "node:child_process";

const args = process.argv.slice(2);
const file = args.find((a) => !a.startsWith("--")) || "hax-ecosystem.json";
const write = args.includes("--write");
const strict = args.includes("--strict");
const doc = JSON.parse(readFileSync(file, "utf8"));

function run(cmd, argv) {
  try {
    return execFileSync(cmd, argv, { encoding: "utf8", stdio: ["ignore", "pipe", "ignore"], timeout: 60000 }).trim();
  } catch (e) {
    return null;
  }
}
function npmLatest(pkg) {
  const v = run("npm", ["view", pkg, "version"]);
  return v ? v : null;
}
function gitLatest(repo) {
  const out = run("git", ["ls-remote", "--tags", "--refs", `https://github.com/${repo}`]);
  if (out === null) return undefined; // repo unreachable: not the same as "no release"
  const tags = out
    .split("\n")
    .map((l) => (l.split("refs/tags/")[1] || "").trim())
    .filter((t) => /^v?\d+\.\d+(\.\d+)?$/.test(t))
    .map((t) => t.replace(/^v/, ""));
  tags.sort((a, b) => {
    const x = a.split(".").map(Number), y = b.split(".").map(Number);
    for (let i = 0; i < 3; i++) if ((x[i] || 0) !== (y[i] || 0)) return (y[i] || 0) - (x[i] || 0);
    return 0;
  });
  return tags[0] || null;
}

const rows = [];
let drift = 0;
for (const [id, n] of Object.entries(doc.nodes)) {
  if (!n.release) continue;
  const [kind, ref] = n.release.split(/:(.+)/);
  const latest = kind === "npm" ? npmLatest(ref) : kind === "git" ? gitLatest(ref) : undefined;
  if (latest === undefined) {
    rows.push([id, n.release, n.version || "-", "unreachable", "check by hand"]);
    continue;
  }
  const wantStatus = latest ? (n.status === "legacy" ? "legacy" : "released") : "prerelease";
  const changes = [];
  if ((n.version || null) !== latest) changes.push(`version ${n.version || "none"} -> ${latest || "none"}`);
  if (n.status !== wantStatus) changes.push(`status ${n.status || "none"} -> ${wantStatus}`);
  if (changes.length) {
    drift++;
    if (write) {
      if (latest) n.version = latest; else delete n.version;
      n.status = wantStatus;
    }
  }
  rows.push([id, n.release, latest || "no release", wantStatus, changes.join("; ") || "ok"]);
}

const today = new Date().toISOString().slice(0, 10);
const w = [10, 38, 12, 11];
console.log(["node", "source", "latest", "status", "result"].map((h, i) => h.padEnd(w[i] || 0)).join("  "));
for (const r of rows) console.log(r.map((c, i) => String(c).padEnd(w[i] || 0)).join("  "));
console.log("");
if (drift) console.log(`Graph needs an update: ${drift} node(s) changed since it was last checked.${write ? " Written." : " Re-run with --write to apply."}`);
else console.log("Graph matches the latest releases.");

if (write) {
  doc.meta = doc.meta || {};
  doc.meta.checked = today;
  doc.meta.releases = Object.fromEntries(rows.filter((r) => r[2] !== "unreachable").map((r) => [r[1], r[2]]));
  writeFileSync(file, JSON.stringify(doc, null, 1) + "\n");
}
if (strict && drift && !write) process.exit(1);
