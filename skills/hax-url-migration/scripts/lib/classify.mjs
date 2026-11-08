// Decide what kind of site this is: course, psu-ddd, docs, blog, portfolio or general.
// Every signal is deterministic so results are repeatable and auditable.
const squash = (s) => String(s || "").replace(/\s+/g, " ").trim();

const COURSE_WORDS = /\b(lesson|module|unit|week\s*\d|syllabus|course|chapter|learning objectives?|assignment|quiz|lecture|reading[s]?|prerequisite)\b/gi;
const DOCS_PLATFORMS = new Set(["docusaurus", "vitepress", "mkdocs", "starlight", "gitbook", "quarto"]);
const BOOK_PLATFORMS = new Set(["pressbooks", "quarto"]);

/**
 * pages: [{ url, title, html (full page), navText, links: [{href,text,rel}] }]
 * fp: fingerprint result for the home page
 */
export function classifySite(pages, fp) {
  const s = { course: 0, "psu-ddd": 0, docs: 0, blog: 0, portfolio: 0, general: 1 };
  const why = { course: [], "psu-ddd": [], docs: [], blog: [], portfolio: [], general: [] };
  const add = (k, n, reason) => { s[k] += n; why[k].push(reason); };
  const home = pages[0] || { url: "https://x/", html: "" };
  const host = new URL(home.url).hostname;
  const all = pages.map((p) => p.html || "").join("\n");
  const nav = pages.map((p) => p.navText || "").join(" ");
  const titles = pages.map((p) => p.title || "").join(" ");

  // course
  const courseHits = ((nav + " " + titles).match(COURSE_WORDS) || []).length;
  if (courseHits >= 3) add("course", Math.min(courseHits, 12), `${courseHits} course words in navigation and titles`);
  const pager = pages.filter((p) => (p.links || []).some((l) => /^(next|previous|prev)\b/i.test(l.text || "") || /\b(next|prev)\b/i.test(l.rel || ""))).length;
  if (pager >= 2) add("course", 4, `previous/next links on ${pager} pages`);
  if (/h5p|instructure\.com|lti|class="[^"]*\b(quiz|question|self-check)/i.test(all)) add("course", 4, "quiz, H5P or LMS markup");
  if (/\b(lesson|module|unit|chapter|week)\s*\d+/i.test(titles)) add("course", 4, "numbered lessons or chapters in titles");
  if (fp && BOOK_PLATFORMS.has(fp.primary.id)) add("course", 6, `${fp.primary.label} book platform`);

  // psu-ddd
  if (/(^|\.)psu\.edu$/.test(host)) add("psu-ddd", 8, "psu.edu host");
  if (/Penn State|Pennsylvania State University/i.test(all)) add("psu-ddd", 3, "Penn State named on page");
  if (/family=Roboto\+Slab|font-family:[^;]*Roboto Slab/i.test(all)) add("psu-ddd", 2, "Roboto Slab (DDD/psu.edu type)");
  if (/#1e407c|#001e44|nittany|beaver ?blue/i.test(all)) add("psu-ddd", 3, "PSU palette colors in markup");
  if (/polaris|psu-brand|psu-header|brand\.psu\.edu/i.test(all)) add("psu-ddd", 4, "PSU brand components");

  // docs
  if (fp && (DOCS_PLATFORMS.has(fp.primary.id) || (fp.layers || []).some((l) => DOCS_PLATFORMS.has(l.id)))) add("docs", 8, "documentation generator");
  const code = (all.match(/<pre[\s>]/gi) || []).length;
  if (code >= 4) add("docs", Math.min(Math.floor(code / 4), 5), `${code} code blocks`);
  if (/\b(docs?|documentation|api reference|getting started|installation)\b/i.test(nav)) add("docs", 3, "docs vocabulary in navigation");

  // blog
  const times = (all.match(/<time[\s>]/gi) || []).length;
  if (times >= 3) add("blog", 3, `${times} <time> elements`);
  if (/application\/(rss|atom)\+xml/i.test(home.html || "")) add("blog", 2, "RSS/Atom feed");
  if (pages.some((p) => /\/(blog|news|posts?|\d{4}\/\d{2})\//i.test(p.url))) add("blog", 3, "blog-style URLs");

  // portfolio
  const imgs = (all.match(/<img[\s>]/gi) || []).length;
  const words = squash(all.replace(/<[^>]+>/g, " ")).split(" ").length;
  if (imgs > 20 && words / Math.max(imgs, 1) < 60) add("portfolio", 5, "image-heavy, text-light pages");
  if (/\b(portfolio|gallery|my work|projects)\b/i.test(nav)) add("portfolio", 3, "portfolio vocabulary in navigation");

  const ranked = Object.entries(s).sort((a, b) => b[1] - a[1]);
  return { type: ranked[0][0], scores: s, reasons: why[ranked[0][0]], runnerUp: ranked[1][0] };
}
