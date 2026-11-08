import { test } from "node:test";
import assert from "node:assert/strict";
import http from "node:http";
import { analyzeSite, reportMarkdown } from "../analyze.mjs";
import { LIMITS } from "../lib/net.mjs";

// A tiny local "WordPress course site" served over HTTP so the whole pipeline runs offline.
const shell = (title, body) => `<!doctype html><html><head><title>${title}</title>
<meta name="generator" content="WordPress 6.6.2"><link rel="stylesheet" href="/wp-content/themes/t/style.css">
<link href="https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@400&display=swap" rel="stylesheet"></head>
<body><header><nav><ul><li><a href="/lesson-1/">Lesson 1</a></li><li><a href="/lesson-2/">Lesson 2</a></li><li><a href="/syllabus/">Syllabus</a><ul><li><a href="/syllabus/grading/">Grading</a></li></ul></li></ul></nav></header>
<main><article><h1>${title}</h1><div class="entry-content">${body}</div></article></main>
<aside class="sidebar"><p>Course sidebar</p></aside><footer><p>Penn State</p></footer></body></html>`;
const lesson = (n) => shell(`Lesson ${n}`, `<p>Module ${n} reading about the water cycle and evaporation in Unit ${n}.</p>
<div class="wp-block-columns"><div class="wp-block-column"><p>Left column text for lesson ${n}.</p></div><div class="wp-block-column"><figure class="wp-block-image"><img src="/wp-content/uploads/${n}.jpg" alt="Diagram ${n}"><figcaption>Figure ${n}</figcaption></figure></div></div>
<div class="team-member"><img src="/t/${n}.jpg" alt="TA"><h3>TA ${n}</h3><p>Office hours</p><a href="/ta/${n}">Contact</a></div>
<iframe src="https://h5p.org/h5p/embed/1"></iframe>
<p><a href="/lesson-${n + 1}/">Next</a> <a href="/lesson-${n - 1}/">Previous</a></p>`);
const routes = {
  "/": shell("Intro to Earth Science", `<p>Welcome to the course syllabus and weekly lessons.</p>`),
  "/lesson-1/": lesson(1),
  "/lesson-2/": lesson(2),
  "/syllabus/": shell("Syllabus", `<p>Course syllabus, assignments, quiz policy and chapter readings.</p><details><summary>Late work</summary><p>Ten percent per day.</p></details>`),
  "/robots.txt": "User-agent: *\nDisallow: /private\n",
  "/sitemap.xml": `<?xml version="1.0"?><urlset><url><loc>BASE/lesson-1/</loc></url><url><loc>BASE/lesson-2/</loc></url><url><loc>BASE/syllabus/</loc></url></urlset>`,
  "/wp-content/themes/t/style.css": "a{color:#1e407c} .btn{background:#e98300} h1{font-family:'Roboto Slab',serif}",
};

test("analyzeSite runs end to end on a local WordPress course site", async () => {
  LIMITS.hostDelayMs = 0;
  const server = http.createServer((req, res) => {
    const base = `http://127.0.0.1:${server.address().port}`;
    const body = routes[req.url];
    if (!body) { res.writeHead(404); res.end("nope"); return; }
    const type = req.url.endsWith(".css") ? "text/css" : req.url.endsWith(".xml") ? "application/xml" : req.url.endsWith(".txt") ? "text/plain" : "text/html";
    res.writeHead(200, { "content-type": type });
    res.end(body.replace(/BASE/g, base));
  });
  await new Promise((r) => server.listen(0, "127.0.0.1", r));
  const url = `http://127.0.0.1:${server.address().port}/`;
  try {
    const r = await analyzeSite(url, { pages: 4, allowPrivate: true, probe: false });
    assert.equal(r.error, undefined, r.error);
    assert.equal(r.fingerprint.primary.id, "wordpress");
    assert.ok(r.blockMaps.includes("wordpress-gutenberg") || r.blockMaps.includes("generic-html"));
    assert.equal(r.siteType.type, "course", JSON.stringify(r.siteType));
    assert.ok(r.pages.length >= 3);
    assert.ok(r.fidelity > 0.95, `fidelity ${r.fidelity}`);
    const lessonPage = r.pages.find((p) => p.url.endsWith("/lesson-1/"));
    assert.match(lessonPage.html, /<grid-plate layout="1-1">/);
    assert.ok(lessonPage.flags.some((f) => f.flag === "h5p"));
    assert.ok(r.gaps.blocks.some((b) => b.signature === "div.team-member"));
    assert.ok(["clean-one", "clean-two", "learn-two-theme", "training-theme"].includes(r.theme.recommendation.theme), r.theme.recommendation.theme);
    assert.ok(r.theme.colors.some((c) => c.ddd.token.endsWith("beaverBlue")));
    assert.match(reportMarkdown(r), /Migration analysis/);
  } finally {
    server.close();
  }
});
