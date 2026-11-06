#!/usr/bin/env node
/**
 * Fidelity check for HAXcms prototypes (haxcms-prototype skill).
 * Node built-ins only.
 *
 *   node fidelity-check.mjs check <prototype-dir> <inventory-dir> [--registry <wc-registry.json>] [--json]
 *   node fidelity-check.mjs compare <main-inventory-dir> <branch-inventory-dir> [--json]
 *
 * check   validates a prototype against the inventory it claims to be built on.
 *         Exit 1 on any error, 0 otherwise (warnings do not fail).
 * compare lists per-state label and component differences between two
 *         inventories (main vs a branch), for branch prototypes.
 */
import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import process from "node:process";

function sha256(file) {
  return crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function loadInventory(dir) {
  const manifestPath = path.join(dir, "manifest.json");
  if (!fs.existsSync(manifestPath)) {
    throw new Error("no manifest.json in " + dir + " (run npm run ui:inventory)");
  }
  const manifest = readJson(manifestPath);
  const labels = new Set();
  const tags = new Set();
  const hashes = new Map();
  const states = new Map();
  for (const state of manifest.states) {
    const stateLabels = new Set(state.labels);
    const stateTags = new Set();
    const domPath = path.join(dir, state.dom);
    if (fs.existsSync(domPath)) {
      for (const el of readJson(domPath)) {
        if (el.label) {
          stateLabels.add(el.label);
        }
        if (el.text) {
          stateLabels.add(el.text);
        }
        if (el.tag.indexOf("-") !== -1) {
          stateTags.add(el.tag);
        }
      }
    }
    for (const l of stateLabels) {
      labels.add(l);
    }
    for (const t of stateTags) {
      tags.add(t);
    }
    for (const variant of Object.keys(state.screenshots)) {
      const file = path.join(dir, state.screenshots[variant]);
      if (fs.existsSync(file)) {
        hashes.set(sha256(file), state.id + "/" + variant);
      }
    }
    states.set(state.id, { labels: stateLabels, tags: stateTags });
  }
  return { manifest, labels, tags, hashes, states };
}

// --- a small HTML tokenizer: enough to track nesting and text --------------

const VOID = new Set([
  "area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
  "source", "track", "wbr",
]);
const RAW = new Set(["script", "style", "template", "textarea", "title"]);

function attrsOf(src) {
  const attrs = {};
  const re = /([^\s=/>]+)(?:\s*=\s*("([^"]*)"|'([^']*)'|([^\s>]+)))?/g;
  let m = re.exec(src);
  while (m) {
    attrs[m[1].toLowerCase()] =
      m[3] !== undefined ? m[3] : m[4] !== undefined ? m[4] : m[5] !== undefined ? m[5] : "";
    m = re.exec(src);
  }
  return attrs;
}

function decode(text) {
  return text
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/\s+/g, " ")
    .trim();
}

function walkHtml(html, onOpen, onText) {
  const stack = [];
  const re = /<!--[\s\S]*?-->|<![^>]*>|<(\/?)([a-zA-Z][a-zA-Z0-9-]*)([^>]*)>|([^<]+)/g;
  let m = re.exec(html);
  while (m) {
    if (m[2]) {
      const tag = m[2].toLowerCase();
      if (m[1]) {
        for (let i = stack.length - 1; i >= 0; i--) {
          if (stack[i].tag === tag) {
            stack.length = i;
            break;
          }
        }
      } else {
        const attrs = attrsOf(m[3]);
        const node = { tag, attrs };
        onOpen(node, stack);
        if (RAW.has(tag)) {
          const close = new RegExp("</" + tag + "\\s*>", "ig");
          close.lastIndex = re.lastIndex;
          const end = close.exec(html);
          const body = html.slice(re.lastIndex, end ? end.index : html.length);
          node.body = body;
          onText(null, stack.concat(node), body);
          re.lastIndex = end ? close.lastIndex : html.length;
        } else if (!VOID.has(tag) && !/\/\s*$/.test(m[3])) {
          stack.push(node);
        }
      }
    } else if (m[4]) {
      const text = decode(m[4]);
      if (text) {
        onText(text, stack, null);
      }
    }
    m = re.exec(html);
  }
}

// --- check ------------------------------------------------------------------

function stripChrome(css) {
  return css.replace(/\/\*\s*chrome:start[\s\S]*?\*\/[\s\S]*?\/\*\s*chrome:end[\s\S]*?\*\//g, "");
}

function rawValueFindings(css, where) {
  const out = [];
  const body = stripChrome(css).replace(/\/\*[\s\S]*?\*\//g, "");
  const decls = body.split(/[;{}]/);
  for (const decl of decls) {
    const idx = decl.indexOf(":");
    if (idx === -1) {
      continue;
    }
    const prop = decl.slice(0, idx).trim().toLowerCase();
    const value = decl.slice(idx + 1).trim();
    if (!prop || prop.indexOf("--") === 0 || /^@|^\s*$/.test(prop)) {
      continue;
    }
    const noVars = value.replace(/var\([^)]*\)/g, "");
    if (/#[0-9a-f]{3,8}\b|\b(?:rgb|rgba|hsl|hsla|oklch|lab)\(/i.test(noVars)) {
      out.push(where + ": raw color in `" + prop + ": " + value + "`");
    }
    const lengths = noVars.match(/-?\d*\.?\d+(?:px|rem|em)\b/g) || [];
    const bad = lengths.filter((l) => !/^-?(?:0|1|2)(?:\.0+)?px$/.test(l));
    if (bad.length && !/^(?:top|left|right|bottom|width|height|inset|transform|translate)$/.test(prop)) {
      out.push(where + ": raw size " + bad.join(", ") + " in `" + prop + ": " + value + "`");
    }
  }
  return out;
}

function check(protoDir, invDir, registryPath) {
  const errors = [];
  const warnings = [];
  const inv = loadInventory(invDir);
  const htmlPath = path.join(protoDir, "index.html");
  if (!fs.existsSync(htmlPath)) {
    throw new Error("no index.html in " + protoDir);
  }
  const html = fs.readFileSync(htmlPath, "utf8");

  let registry = null;
  if (registryPath && fs.existsSync(registryPath)) {
    registry = new Set(Object.keys(readJson(registryPath)));
  }

  let brief = null;
  let provenance = "";
  const proposedIds = new Set();
  const usedTags = new Set();
  const images = [];
  const outsideText = [];
  const insideText = [];
  const cssChunks = [];

  walkHtml(
    html,
    (node, stack) => {
      if (node.tag === "script" && node.attrs.id === "prototype-brief") {
        node.isBrief = true;
      }
      if ("data-provenance" in node.attrs) {
        node.isProvenance = true;
      }
      if (node.attrs["data-proposed"]) {
        proposedIds.add(node.attrs["data-proposed"]);
      }
      const inChrome = stack.some((s) => "data-prototype-chrome" in s.attrs) || "data-prototype-chrome" in node.attrs;
      const inProposed = stack.some((s) => s.attrs["data-proposed"]) || !!node.attrs["data-proposed"];
      if (node.tag.indexOf("-") !== -1 && !inChrome) {
        usedTags.add(node.tag);
      }
      if (node.tag === "img" && node.attrs.src && !inChrome) {
        images.push({ src: node.attrs.src, inProposed });
      }
      if (node.attrs.style && !inChrome) {
        cssChunks.push({ css: "x{" + node.attrs.style + "}", where: "style attribute on <" + node.tag + ">" });
      }
      for (const a of ["aria-label", "title", "label", "placeholder", "alt"]) {
        if (node.attrs[a] && !inChrome && node.tag !== "img") {
          (inProposed ? insideText : outsideText).push(node.attrs[a]);
        }
      }
    },
    (text, stack, raw) => {
      const last = stack[stack.length - 1];
      if (raw !== null && last) {
        if (last.isBrief) {
          try {
            brief = JSON.parse(raw);
          } catch (e) {
            errors.push("prototype-brief is not valid JSON: " + e.message);
          }
        } else if (last.tag === "style") {
          cssChunks.push({ css: raw, where: "<style>" });
        }
        return;
      }
      const inChrome = stack.some((s) => "data-prototype-chrome" in s.attrs);
      const inProposed = stack.some((s) => s.attrs["data-proposed"]);
      if (stack.some((s) => s.isProvenance)) {
        provenance += " " + text;
      }
      if (inChrome) {
        return;
      }
      (inProposed ? insideText : outsideText).push(text);
    },
  );

  // brief + provenance
  if (!brief) {
    errors.push('missing <script type="application/json" id="prototype-brief">');
    brief = { steps: [], regions: [], newLabels: [], newComponents: [] };
  }
  const sha = inv.manifest.source && inv.manifest.source.haxcmsNodejs;
  if (!provenance.trim()) {
    errors.push("missing data-provenance strip");
  } else {
    if (sha && provenance.indexOf(sha.slice(0, 7)) === -1) {
      errors.push("provenance does not name the inventory's haxcms-nodejs commit " + sha.slice(0, 7));
    }
    if (inv.manifest.generatedAt && provenance.indexOf(inv.manifest.generatedAt.slice(0, 10)) === -1) {
      warnings.push("provenance does not show the inventory date " + inv.manifest.generatedAt.slice(0, 10));
    }
  }

  // steps reference real states
  for (const step of brief.steps || []) {
    if (!inv.states.has(step.state)) {
      errors.push('brief step "' + step.title + '" uses state "' + step.state + '" that the inventory does not have');
    }
  }

  // proposed regions declared
  const declared = new Set((brief.regions || []).map((r) => r.id));
  for (const id of proposedIds) {
    if (!declared.has(id)) {
      errors.push('data-proposed="' + id + '" is not declared in brief.regions');
    }
  }
  for (const id of declared) {
    if (!proposedIds.has(id)) {
      warnings.push('brief region "' + id + '" has no data-proposed element on the page');
    }
  }

  // base images are untouched inventory captures
  for (const img of images) {
    if (img.inProposed || /^(?:https?:|data:)/.test(img.src)) {
      continue;
    }
    const file = path.join(protoDir, img.src);
    if (!fs.existsSync(file)) {
      errors.push("image " + img.src + " is missing");
      continue;
    }
    if (/^(?:base|branch)\//.test(img.src)) {
      const hit = inv.hashes.get(sha256(file));
      if (!hit && img.src.indexOf("base/") === 0) {
        errors.push("base image " + img.src + " is not byte-identical to any inventory screenshot");
      }
    } else {
      warnings.push("image " + img.src + " outside base/ and outside a proposed region");
    }
  }

  // labels
  const newLabels = new Set((brief.newLabels || []).map((l) => (typeof l === "string" ? l : l.text)));
  for (const text of outsideText) {
    if (!inv.labels.has(text)) {
      errors.push('text outside proposed regions is not a real label: "' + text.slice(0, 80) + '"');
    }
  }
  for (const text of insideText) {
    if (!inv.labels.has(text) && !newLabels.has(text)) {
      errors.push('proposed text not in the inventory and not in brief.newLabels: "' + text.slice(0, 80) + '"');
    }
  }

  // components
  const newComponents = new Set(brief.newComponents || []);
  for (const tag of usedTags) {
    const known = inv.tags.has(tag) || (registry && registry.has(tag)) || newComponents.has(tag);
    if (!known) {
      errors.push("<" + tag + "> is not in the inventory" + (registry ? ", the registry" : "") + " or brief.newComponents");
    }
  }
  if (!registry) {
    warnings.push("no --registry given; components checked against the inventory only");
  }

  // tokens
  for (const chunk of cssChunks) {
    for (const f of rawValueFindings(chunk.css, chunk.where)) {
      errors.push(f);
    }
  }
  if (!/tokens\.css/.test(html)) {
    errors.push("tokens.css from the inventory is not linked");
  } else if (fs.existsSync(path.join(protoDir, "tokens.css")) && fs.existsSync(path.join(invDir, "tokens.css"))) {
    if (sha256(path.join(protoDir, "tokens.css")) !== sha256(path.join(invDir, "tokens.css"))) {
      errors.push("tokens.css differs from the inventory's copy");
    }
  }

  return { errors, warnings, inventory: inv.manifest.source };
}

// --- compare ----------------------------------------------------------------

function compare(mainDir, branchDir) {
  const a = loadInventory(mainDir);
  const b = loadInventory(branchDir);
  const out = [];
  const ids = new Set([...a.states.keys(), ...b.states.keys()]);
  for (const id of ids) {
    const sa = a.states.get(id);
    const sb = b.states.get(id);
    if (!sa || !sb) {
      out.push({ state: id, change: sa ? "missing on branch" : "new on branch" });
      continue;
    }
    const added = [...sb.labels].filter((l) => !sa.labels.has(l));
    const removed = [...sa.labels].filter((l) => !sb.labels.has(l));
    const tagsAdded = [...sb.tags].filter((t) => !sa.tags.has(t));
    const tagsRemoved = [...sa.tags].filter((t) => !sb.tags.has(t));
    if (added.length || removed.length || tagsAdded.length || tagsRemoved.length) {
      out.push({ state: id, added, removed, tagsAdded, tagsRemoved });
    }
  }
  return { main: a.manifest.source, branch: b.manifest.source, changes: out };
}

// --- cli --------------------------------------------------------------------

function main() {
  const argv = process.argv.slice(2);
  const json = argv.includes("--json");
  const regIdx = argv.indexOf("--registry");
  const registry = regIdx !== -1 ? argv[regIdx + 1] : null;
  const pos = argv.filter((x, i) => x.indexOf("--") !== 0 && argv[i - 1] !== "--registry");
  const [cmd, one, two] = pos;
  if (cmd === "check" && one && two) {
    const r = check(path.resolve(one), path.resolve(two), registry && path.resolve(registry));
    if (json) {
      console.log(JSON.stringify(r, null, 2));
    } else {
      console.log("Fidelity check against haxcms-nodejs " + ((r.inventory && r.inventory.haxcmsNodejs) || "?").slice(0, 7));
      for (const e of r.errors) console.log("  ERROR  " + e);
      for (const w of r.warnings) console.log("  warn   " + w);
      console.log(r.errors.length ? r.errors.length + " error(s)" : "pass");
    }
    process.exit(r.errors.length ? 1 : 0);
  }
  if (cmd === "compare" && one && two) {
    const r = compare(path.resolve(one), path.resolve(two));
    if (json) {
      console.log(JSON.stringify(r, null, 2));
    } else {
      for (const c of r.changes) {
        console.log("## " + c.state + (c.change ? " (" + c.change + ")" : ""));
        if (c.added && c.added.length) console.log("  + " + c.added.join(" · "));
        if (c.removed && c.removed.length) console.log("  - " + c.removed.join(" · "));
        if (c.tagsAdded && c.tagsAdded.length) console.log("  + <" + c.tagsAdded.join("> <") + ">");
        if (c.tagsRemoved && c.tagsRemoved.length) console.log("  - <" + c.tagsRemoved.join("> <") + ">");
      }
      if (!r.changes.length) console.log("no label or component differences");
    }
    process.exit(0);
  }
  console.error("usage:\n  fidelity-check.mjs check <prototype-dir> <inventory-dir> [--registry <file>] [--json]\n  fidelity-check.mjs compare <main-inventory> <branch-inventory> [--json]");
  process.exit(2);
}

main();
