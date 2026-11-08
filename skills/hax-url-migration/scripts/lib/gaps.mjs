// Turn what the block maps could not handle into proposals: reuse an existing
// HAX block with a preset, or build a new one (with a HAXSchema starting point).
import { parse } from "node-html-parser";

// pre must parse as HTML so <pre><code> can be matched; scripts and styles stay raw text
const PARSE_OPTS = { comment: false, blockTextElements: { script: true, noscript: true, style: true } };


const PREFIXES = /^(elementor-widget-|elementor-|wp-block-|sqs-block-|et_pb_|kg-|paragraph--type--|block-|c-|o-|m-|ccm-block-|w-|emdash-|sl-|theme-|field--name-field-)/;
const GENERIC = /^(elementor-element|elementor-widget|widget|item|card-body|card-content|module|component|section|block|box|wrap|wrapper|inner|container)$/;

function proposeName(signature) {
  const tokens = signature.split(".").slice(1).filter((t) => !GENERIC.test(t));
  const pick = tokens.sort((a, b) => b.length - a.length)[0] || signature.split(".").pop();
  let name = pick.replace(PREFIXES, "").replace(/[_\s]+/g, "-").replace(/[^a-z0-9-]/gi, "").toLowerCase().replace(/-+/g, "-").replace(/^-|-$/g, "");
  if (!name) name = "custom-block";
  if (!name.includes("-")) name = `${name}-block`; // custom element names need a hyphen
  return name;
}

/** Nearest existing HAX block for a structure, if one fits well enough to reuse. */
function nearestHax(s) {
  const has = (k) => s[k] > 0;
  if (has("img") && has("heading") && has("link") && !has("list")) return { tag: "ddd-card", fit: "high", why: "image + title + text + link" };
  if (has("img") && has("text") && /quote|testimonial|review/i.test(s.hint || "")) return { tag: "person-testimonial", fit: "high", why: "photo + quote + name" };
  if (has("number") && !has("img") && s.text <= 1 && /count|stat|number|metric|figure/i.test(s.hint || "")) return { tag: "count-up", fit: "medium", why: "large number + label" };
  if (has("date") && /event|calendar|date/i.test(s.hint || "")) return { tag: "date-card", fit: "medium", why: "date + title + location" };
  if (has("icon") && has("heading") && has("text")) return { tag: "accent-card", fit: "medium", why: "icon + title + text" };
  if (has("img") && has("heading") && has("text")) return { tag: "accent-card", fit: "medium", why: "image + heading + text" };
  if (has("heading") && has("button")) return { tag: "page-section", fit: "low", why: "heading + call to action (page-section preset)" };
  if (has("list") && has("icon")) return { tag: "ddd-steps-list", fit: "low", why: "icon list" };
  return null;
}

/** Draft HAXSchema settings from the sample's structure. */
function schemaFromSample(sample) {
  const el = parse(sample, PARSE_OPTS);
  const fields = [];
  const add = (property, title, inputMethod, extra = {}) => { if (!fields.some((f) => f.property === property)) fields.push({ property, title, inputMethod, ...extra }); };
  if (el.querySelector("h1, h2, h3, h4, h5, h6, [class*=title], [class*=heading]")) add("title", "Title", "textfield");
  if (el.querySelector("img, picture")) { add("image", "Image", "haxupload", { noVoiceRecord: true }); add("alt", "Image alt text", "alt"); }
  if (el.querySelector("a[href]")) add("link", "Link", "haxupload");
  if (el.querySelector("button, a[class*=btn], a[class*=button]")) add("label", "Button label", "textfield");
  if (el.querySelector("time")) add("date", "Date", "textfield");
  if (el.querySelector("svg, i[class*=icon], i[class*=fa-]")) add("icon", "Icon", "iconpicker");
  fields.push({ slot: "", title: "Content", inputMethod: "code-editor" });
  return fields;
}

/**
 * pageResults: [{ url, unmapped: [...], flags: [...] }]
 * Returns { blocks: [...proposals], flagsByKind: {...} }
 */
export function proposeGaps(pageResults) {
  const bySig = new Map();
  for (const p of pageResults) {
    for (const u of p.unmapped || []) {
      const cur = bySig.get(u.signature) || { signature: u.signature, occurrences: 0, pages: new Set(), structure: u.structure, sample: u.sample };
      cur.occurrences += u.count;
      cur.pages.add(p.url);
      bySig.set(u.signature, cur);
    }
    for (const f of p.flags || []) {
      if (f.flag !== "gap") continue;
      const sig = `gap.${f.gapKey || f.rule}`;
      const cur = bySig.get(sig) || { signature: sig, occurrences: 0, pages: new Set(), structure: null, sample: f.sample, fromRule: f.rule, note: f.note };
      cur.occurrences += 1;
      cur.pages.add(p.url);
      bySig.set(sig, cur);
    }
  }
  const blocks = [];
  for (const g of bySig.values()) {
    const repeated = g.pages.size >= 2 || g.occurrences >= 3 || g.fromRule;
    if (!repeated) continue;
    const el = parse(g.sample || "", PARSE_OPTS);
    const s = g.structure || (() => {
      const has = (sel) => el.querySelectorAll(sel).length;
      return { img: has("img"), heading: has("h1,h2,h3,h4,h5,h6"), link: has("a[href]"), text: has("p"), button: has("button"), icon: has("svg, i"), number: 0, date: has("time"), list: has("li") };
    })();
    const near = nearestHax({ ...s, hint: g.signature });
    const name = proposeName(g.signature);
    blocks.push({
      signature: g.signature,
      occurrences: g.occurrences,
      pages: g.pages.size,
      recommendation: near && near.fit !== "low" ? "reuse" : "new-block",
      reuse: near,
      proposedTag: name,
      haxSchemaDraft: near && near.fit !== "low" ? null : {
        gizmo: { title: name.replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase()), tags: ["Layout", "migration"], handles: [], meta: { author: "hax-url-migration draft" } },
        settings: { configure: schemaFromSample(g.sample || ""), advanced: [] },
        demoSchema: [{ tag: name, properties: {}, content: "" }],
      },
      sample: g.sample,
      note: g.note || "",
    });
  }
  blocks.sort((a, b) => b.pages - a.pages || b.occurrences - a.occurrences);
  const flagsByKind = {};
  for (const p of pageResults) for (const f of p.flags || []) flagsByKind[f.flag] = (flagsByKind[f.flag] || 0) + 1;
  return { blocks, flagsByKind };
}
