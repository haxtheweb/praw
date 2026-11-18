#!/usr/bin/env node
// Render hax.cloud's static files with haxcms-nodejs main, in place:
//
//   node ecosystem/build/static_site.cjs <haxcms-nodejs checkout> <site folder>
//
// The site boilerplate site.sh copies in is a set of templates (index.html, ghpages.html, manifest.json,
// robots.txt, service-worker.js, ...). A HAXcms backend renders them from site.json; a static host serves them
// as they are. So the backend that owns the templates renders them here, from the same checkout site.sh took
// the boilerplate from, and the template syntax can never move ahead of the code that fills it in. This is
// what the HAX CLI's site:build-static does (haxtheweb/issues#3352), run against haxcms-nodejs main instead
// of whatever haxcms-nodejs the published CLI carries:
// - managed files rebuilt from site.json (rebuildManagedFiles), generated files refreshed (robots.txt,
//   llms.txt, sitemap, feeds, search index, agent skills: updateAlternateFormats)
// - ghpages.html is the entry point (index.html)
// - every published page rendered as <slug>/index.html with its title, description, canonical link,
//   JSON-LD and text (renderStaticPages), so search engines and agents read it without running JavaScript
//
// Invariant: no managed template the site ships still holds template syntax ({{ ... }} or {% ... %}). A
// template that can't render, or one that renders with syntax left over, fails the build rather than
// publishing a page that shows it.
"use strict";
const fs = require("fs");
const path = require("path");

const [hnDir, siteArg] = process.argv.slice(2);
if (!hnDir || !siteArg) {
  console.error("usage: static_site.cjs <haxcms-nodejs checkout> <site folder>");
  process.exit(2);
}
const os = require("os");
const site = path.resolve(siteArg);
const lib = path.resolve(hnDir, "src", "lib");
// HAXCMS.js finds its configuration in a _config/ folder above the working directory, else it makes one in
// the home folder and seeds an admin user there. A build has no users: give it a throwaway config folder.
const scratch = fs.mkdtempSync(path.join(os.tmpdir(), "hax-cloud-config-"));
fs.mkdirSync(path.join(scratch, "_config"));
fs.writeFileSync(path.join(scratch, "_config", ".isHAXcmsConfig"), "");
process.chdir(scratch);
const { HAXCMSSite } = require(path.join(lib, "HAXCMS.js"));
const { renderStaticPages } = require(path.join(lib, "staticPages.js"));

const TEMPLATE_SYNTAX = /\{\{\s*[A-Za-z_][\w.|()' ,]*\s*\}\}|\{%\s*(if|else|endif|for|endfor|set)\b[^%]*%\}/;

// the backend's managed templates (and the entry point copied from ghpages.html) as shipped; inline code
// spans are skipped, since AGENTS.md documents the syntax in backticks
function leftovers(s) {
  const found = [];
  for (const rel of Object.values(s.getManagedTemplateFiles())) {
    const p = path.join(site, rel);
    if (!fs.existsSync(p)) continue;
    const m = fs.readFileSync(p, "utf8").replace(/`[^`\n]*`/g, "").match(TEMPLATE_SYNTAX);
    if (m) found.push(`${rel}: ${m[0]}`);
  }
  return found;
}

(async () => {
  const s = new HAXCMSSite();
  await s.loadSingle(site);
  // a template that can't render throws here: the build stops instead of shipping it raw
  await s.rebuildManagedFiles();
  await s.updateAlternateFormats();
  fs.copyFileSync(path.join(site, "ghpages.html"), path.join(site, "index.html"));
  const pages = await renderStaticPages(s, { domain: "https://hax.cloud/" });
  for (const page of pages) {
    const out = path.join(site, page.path);
    // renderStaticPages only returns plain relative paths inside the site; check anyway before writing
    if (!out.startsWith(site + path.sep)) throw new Error(`page path outside the site: ${page.path}`);
    fs.mkdirSync(path.dirname(out), { recursive: true });
    fs.writeFileSync(out, page.html);
  }
  console.log(`static pages: ${pages.length} rendered with haxcms-nodejs main`);
  const left = leftovers(s);
  if (left.length) {
    console.error("template syntax left in shipped files:\n  " + left.join("\n  "));
    process.exitCode = 1;
  }
})()
  .catch((e) => {
    console.error(e && e.stack ? e.stack : e);
    process.exitCode = 1;
  })
  .finally(() => fs.rmSync(scratch, { recursive: true, force: true }));
