import { test } from "node:test";
import assert from "node:assert/strict";
import { fingerprint } from "../lib/fingerprint.mjs";
import { parseRobots } from "../lib/net.mjs";

// Synthetic pages carrying only the markers each platform emits.
const page = (body, headers = {}, url = "https://example.org/", setCookies = []) => ({ finalUrl: url, headers, setCookies, body });
const fp = (p) => fingerprint(p, { probe: false });

const cases = [
  ["wordpress", page('<meta name="generator" content="WordPress 6.6.2"><link rel="stylesheet" href="/wp-includes/css/dist/block-library/style.min.css"><div class="wp-block-columns"></div>')],
  ["wordpress", page("<p>x</p>", { link: '<https://example.org/wp-json/>; rel="https://api.w.org/"' })],
  ["pressbooks", page('<meta name="generator" content="WordPress 6.5"><meta name="generator" content="Pressbooks 6.20"><script src="/wp-content/plugins/pressbooks/x.js"></script>')],
  ["drupal", page('<meta name="Generator" content="Drupal 10 (https://www.drupal.org)"><script>var drupalSettings={}</script>')],
  ["drupal", page('<img src="/sites/default/files/a.jpg"><script src="/core/misc/drupal.js"></script>', { "x-drupal-cache": "HIT" })],
  ["grav", page('<meta name="generator" content="GravCMS" /><link href="/user/themes/quark/css/x.css">')],
  ["astro", page('<meta name="generator" content="Astro v4.15.0"><script src="/_astro/hoisted.js"></script>')],
  ["emdash", page('<meta name="generator" content="Astro v6.0.1"><figure class="emdash-image"><img src="/_emdash/api/media/file/a.jpg"></figure>')],
  ["eleventy", page('<meta name="generator" content="Eleventy v3.0.0">')],
  ["hugo", page('<meta name="generator" content="Hugo 0.134.2">')],
  ["jekyll", page("<!-- Begin Jekyll SEO tag v2.8.0 --><title>x</title>")],
  ["docusaurus", page('<meta name="generator" content="Docusaurus v3.5.2"><div id="__docusaurus"></div>')],
  ["vitepress", page('<meta name="generator" content="VitePress v1.3.4"><div class="vp-doc"></div>')],
  ["quarto", page('<meta name="generator" content="quarto-1.5.57">')],
  ["mkdocs", page('<meta name="generator" content="mkdocs-1.6.1, mkdocs-material-9.5.34"><div class="md-content"></div>')],
  ["nextjs", page('<script id="__NEXT_DATA__" type="application/json">{}</script><script src="/_next/static/chunks/a.js"></script>')],
  ["gatsby", page('<div id="___gatsby"></div>')],
  ["squarespace", page('<script>Static.SQUARESPACE_CONTEXT = {}</script><img src="https://images.squarespace-cdn.com/a.jpg">')],
  ["wix", page('<meta name="generator" content="Wix.com Website Builder">', { "x-wix-request-id": "1" })],
  ["webflow", page('<html data-wf-page="1" data-wf-site="2"><meta content="Webflow" name="generator">')],
  ["joomla", page('<meta name="generator" content="Joomla! - Open Source Content Management"><script src="/media/system/js/core.js"></script>')],
  ["concrete", page('<script>var CCM_DISPATCHER_FILENAME = "/index.php";</script><img src="/files/cache/71f859f0d35fb4d6864b991892a3b4ce_f21.png">')],
  ["ghost", page('<meta name="generator" content="Ghost 5.96"><figure class="kg-card kg-image-card"></figure>')],
  ["plone", page('<meta name="generator" content="Plone - https://plone.org/"><link href="/++plone++static/x.css">')],
  ["canvas", page("<p>x</p>", {}, "https://psu.instructure.com/courses/1")],
  ["moodle", page("<p>x</p>", {}, "https://example.org/", ["MoodleSession=abc; path=/"])],
];

for (const [expected, p] of cases) {
  test(`detects ${expected}`, async () => {
    const r = await fp(p);
    assert.equal(r.primary.id, expected, JSON.stringify(r.candidates));
  });
}

test("elementor is a layer on wordpress, with version", async () => {
  const r = await fp(page('<meta name="generator" content="Elementor 3.24.4; features: e_font_icon_svg"><div class="elementor-widget elementor-widget-image"></div><link href="/wp-content/plugins/elementor/assets/css/frontend.min.css">'));
  assert.equal(r.primary.id, "wordpress");
  assert.equal(r.layers[0].id, "elementor");
  assert.equal(r.layers[0].version, "3.24.4");
});

test("starlight is a layer on astro", async () => {
  const r = await fp(page('<meta name="generator" content="Astro v5.1.0"><meta name="generator" content="Starlight v0.30.0"><div class="sl-markdown-content"></div>'));
  assert.equal(r.primary.id, "astro");
  assert.deepEqual(r.layers.map((l) => l.id), ["starlight"]);
});

test("drupal version from header", async () => {
  const r = await fp(page("<p>x</p>", { "x-generator": "Drupal 10 (https://www.drupal.org)" }));
  assert.equal(r.primary.version, "10");
});

test("plain html is unknown", async () => {
  const r = await fp(page("<html><body><h1>Hello</h1><p>world</p></body></html>"));
  assert.equal(r.primary.id, "unknown");
});

test("robots parser respects * group", () => {
  const r = parseRobots("User-agent: Googlebot\nDisallow: /\n\nUser-agent: *\nDisallow: /private\nAllow: /private/ok\nSitemap: https://x/s.xml");
  assert.deepEqual(r.disallow, ["/private"]);
  assert.deepEqual(r.allow, ["/private/ok"]);
  assert.deepEqual(r.sitemaps, ["https://x/s.xml"]);
});
