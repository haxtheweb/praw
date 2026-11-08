#!/usr/bin/env node
// Check every block map: selectors parse, targets are real HAX blocks, and
// mapped attributes exist on the target. Exit 1 on errors; warnings print only.
import { readdirSync, readFileSync } from "node:fs";
import { parse } from "node-html-parser";

const REF = new URL("../references/", import.meta.url);
const catalog = JSON.parse(readFileSync(new URL("hax-blocks.json", REF), "utf8")).blocks;
const fps = JSON.parse(readFileSync(new URL("fingerprints.json", REF), "utf8"));
const SPECIAL = new Set(["keep", "unwrap", "drop", "flag", "link", "html"]);
const ALWAYS_OK = new Set(["layout"]); // grid-plate layout is set by the engine
const probe = parse("<div><p class=a>x</p></div>");
let errors = 0;
let warnings = 0;
const err = (m) => { errors++; console.log(`ERROR  ${m}`); };
const warn = (m) => { warnings++; console.log(`warn   ${m}`); };

function checkRule(mapId, rule, where) {
  try { probe.querySelectorAll(rule.match || rule.select); } catch (e) { err(`${mapId}/${where}: selector does not parse: ${rule.match || rule.select}`); }
  if (!rule.to) return;
  if (SPECIAL.has(rule.to)) return;
  const target = catalog[rule.to];
  if (!target) { err(`${mapId}/${where}: target <${rule.to}> is not in hax-blocks.json`); return; }
  for (const prop of Object.keys(rule.attrs || {})) {
    if (ALWAYS_OK.has(prop)) continue;
    if (!target.props.includes(prop)) warn(`${mapId}/${where}: <${rule.to}> has no configurable "${prop}" in its HAXSchema (may still be a valid attribute)`);
  }
  for (const slot of Object.keys(rule.slots || {})) {
    if (target.slots.length && !target.slots.includes(slot)) warn(`${mapId}/${where}: <${rule.to}> does not list slot "${slot}"`);
  }
}

const mapIds = new Set();
for (const f of readdirSync(new URL("block-maps/", REF)).filter((x) => x.endsWith(".json"))) {
  const map = JSON.parse(readFileSync(new URL(`block-maps/${f}`, REF), "utf8"));
  mapIds.add(map.id);
  if (`${map.id}.json` !== f) err(`${f}: id "${map.id}" does not match file name`);
  const ids = new Set();
  for (const r of map.rules) {
    if (ids.has(r.id)) err(`${map.id}: duplicate rule id ${r.id}`);
    ids.add(r.id);
    checkRule(map.id, r, r.id);
    if (r.children) checkRule(map.id, { ...r.children, match: r.children.select }, `${r.id}>children`);
  }
}
for (const p of fps.platforms) {
  if (p.blockMap && !mapIds.has(p.blockMap)) err(`fingerprints: ${p.id} points at missing block map ${p.blockMap}`);
  for (const s of p.signals) { try { new RegExp(s.match, "i"); } catch (e) { err(`fingerprints: ${p.id} bad regex ${s.match}`); } }
  if (p.parent && !fps.platforms.some((x) => x.id === p.parent)) err(`fingerprints: ${p.id} parent ${p.parent} missing`);
}
console.log(`\n${errors} error(s), ${warnings} warning(s)`);
process.exit(errors ? 1 : 0);
