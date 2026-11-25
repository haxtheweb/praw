import json, re

GH = "https://github.com/haxtheweb"
WINS = "https://github.com/haxtheweb/praw/blob/main/WINS.md"
WORLDVIEW = "https://github.com/haxtheweb/praw/blob/main/WORLDVIEW.md"
HAXLAB = "https://github.com/haxtheweb/lab"
HTW = "https://haxtheweb.org"
ART = "https://github.com/haxtheweb/art/tree/main/future-traveler"
ISS = "https://github.com/haxtheweb/issues/issues/"
ADV = "https://github.com/haxtheweb/issues/security/advisories/"
SIIP = "https://www.youtube.com/watch?v=TNF0uzYi9Kk"
APEREO_HAX = "https://www.apereo.org/programs/software/HAX"
AP19 = "https://www.slideshare.net/slideshow/haxtheweb-apereo-19/148822203"
# Penn State News, 6 November 2024: ODL creates a platform to simplify website content (HAX, its people, units and reach)
PSUNEWS = "https://www.psu.edu/news/arts-and-architecture/story/office-digital-learning-creates-platform-simplify-website-content"
LEARN = "https://learn.hax.cloud"


def anchor(h):
    s = h.strip().lower()
    s = re.sub(r"[^\w\- ]", "", s)
    return WINS + "#" + s.replace(" ", "-")


W = {k: anchor(v) for k, v in {
    "flourish": "Learn to Flourish Hub: flourish.hhd.psu.edu (2026)",
    "industry": "From HAX Lab to industry",
    "dashboard": "Site Dashboard, three generations of students (2022–2026)",
    "ddd": "Students built the design system",
    "winston": "Winston White: student to trainer",
    "clubs": "Student clubs: 30 security fixes",
    "tags": "640+ open HTML tags, used across Penn State",
    "collins": "Faculty building on HAX: Michael Collins",
    "grants": "HAX Lab faculty grants",
    "npm": "289 packages, about 49,000 downloads a month",
    "agents": "Agents with context: 90% then 211%",
    "skeletons": "Skeletons and benevolent restrictions (HAX 25)",
    "fast": "Fast without a build step",
    "camp": "First hax-camp, 40+ people",
    "migrations": "Migrations in seconds, not months",
    "reach": "Reach by early 2026",
    "nara": "National Archives usability audit (2019)",
    "since2020": "Every site since 2020 still works",
    "cd101": "Customer Discovery 101: Invent Penn State LaunchBox",
    "dbf": "Digital Beaumont & Fletcher: students edit the rarely taught plays",
}.items()}

def L(label, url):
    return {"label": label, "url": url}

nodes = {}
def N(id, **kw):
    nodes[id] = kw

# ---- center and pillars
N("human", desc="People are the center of HAX: authors, students, faculty, staff and contributors. Every pillar exists for them.", source=L("PRAW WORLDVIEW.md", WORLDVIEW), always=True)
N("traveler", desc="The HAX mascot, the Future Traveler: \"Dream it, remix it, have it, share it.\" Here he stands for your AI companion, working alongside people.", source=L("haxtheweb/art: the Future Traveler", ART), links={"repo": ART}, always=True)
# the seven pillars: phrase, description, icon and color live in build/data/pillars.json (the Why layer)
_PD = json.load(open("ext/pillars.json"))
P = {p["id"]: p["phrase"] for p in _PD["pillars"]}
for p in _PD["pillars"]:
    N(p["id"], desc=p["phrase"] + " " + p["desc"], source=L(_PD["source"]["label"], _PD["source"]["url"]), always=True, **({"note": p["note"]} if p["note"] else {}))

# ---- core platform
N("haxcms", desc="\"A hybrid static site generator, a new class of CMS\": a microsite generator and manager that doesn't need the command line.", source=L("haxtheweb.org: Why HAXcms", HTW), links={"docs": "https://learn.hax.cloud", "repo": GH + "/haxcms-nodejs"}, status="released", year=2019, yearNote="HAXcms announced at DrupalCon; the first site goes live", yearSource=L("WINS.md SIIP timeline", WINS))
N("editor", desc="HAX, the Headless Authoring eXperience: \"a WYSIWYG unlike any other. You extend your world by extending the web through the web component standard.\"", source=L("haxtheweb.org: What is HAX", HTW), links={"npm": "https://www.npmjs.com/package/@haxtheweb/hax-body", "demo": "https://hax.cloud"}, release="npm:@haxtheweb/hax-body", status="released", year=2017, yearNote="HAX first presented at DrupalCon Baltimore by Bryan Ollendyke and Michael Potter", yearSource=L("DrupalCon Baltimore 2017 session", "https://events.drupal.org/baltimore2017/sessions/mad-scientist-road-show"))
N("merlin", desc="HAX's command program, marked by the wand: search for and run actions while editing. HAX Tips will surface here.", source=L("haxtheweb/issues #3172", ISS + "3172"), status="released")
N("dashboard", desc="app-hax, where people create and manage sites. Three generations were built by student teams from 2022 to 2026.", source=L("WINS.md: Site Dashboard", W["dashboard"]), links={"npm": "https://www.npmjs.com/package/@haxtheweb/app-hax"}, release="npm:@haxtheweb/app-hax", status="released", year=2022, yearNote="Dashboard 1.0 built by a student team in one semester", yearSource=L("WINS.md", W["dashboard"]))
N("files", desc="", status="released")
N("themes", desc="Ways to theme HAXcms matched to skill set: skin a site with CSS, or build a theme from web components. Themes grew from 14 at the end of 2024 to more than 30.", source=L("haxtheweb.org: Theming; WINS.md: Reach", W["reach"]), links={"npm": "https://www.npmjs.com/package/@haxtheweb/haxcms-elements"}, release="npm:@haxtheweb/haxcms-elements", status="released")

# ---- backends and identity
N("php", desc="HAXcms on PHP. Kept in step with the Node.js backend through a shared OpenAPI contract; powers haxtheweb.org through HAXiam.", source=L("haxtheweb.org", HTW), links={"repo": GH + "/haxcms-php"}, release="git:haxtheweb/haxcms-php", status="released")
N("nodejs", desc="HAXcms on Node.js, started with npx @haxtheweb/haxcms-nodejs. The most-downloaded @haxtheweb package.", source=L("haxtheweb.org; WINS.md: 289 packages", W["npm"]), links={"repo": GH + "/haxcms-nodejs", "npm": "https://www.npmjs.com/package/@haxtheweb/haxcms-nodejs"}, release="npm:@haxtheweb/haxcms-nodejs", status="released")
N("browser", desc="haxcms-nodejs bundled to run in a browser tab: no install, no server. Sites save to a folder, the browser, or cloud storage (Google Drive, OneDrive, Dropbox, Box, WebDAV); people sign in with an account they have; and sites publish straight to Surge, GitHub Pages, GitLab Pages, Codeberg Pages, Netlify or Vercel. Open its web for every service.", source=L("haxtheweb/issues #3331", ISS + "3331"), links={"repo": GH + "/haxcms-browser", "site": "https://browser.hax.cloud", "issue": ISS + "3341", "setup": GH + "/haxcms-browser/blob/main/docs/providers.md"}, status="deployed", year=2026, yearNote="HAXcms runs in a browser tab")
N("desktop", desc="haxcms-nodejs wrapped in Electron as a desktop app. It starts the real server in a no-login local mode that only listens on your own computer, and keeps your sites in a folder in your home directory.", source=L("haxtheweb/haxcms-desktop README", GH + "/haxcms-desktop#readme"), links={"repo": GH + "/haxcms-desktop"})
N("haxiam", desc="Makes HAXcms multi-tenant: hundreds of sites from one core behind institutional login. hax.psu.edu runs on it.", source=L("haxiam on GitHub", GH + "/haxiam"), links={"repo": GH + "/haxiam"}, status="deployed")
N("haxpsu", desc="Penn State's HAXcms service, run on HAXiam behind Penn State login: 302 sites, 368 users and 17,100 pages. \"Free, open source, forever, transformative, unleashing creativity in a sustainable way.\" Open its web for courses by college.", source=L("hax.psu.edu", "https://hax.psu.edu"), links={"site": "https://hax.psu.edu"}, status="deployed", year=2020, yearNote="hax.psu.edu opens on HAXiam")
N("ssr", desc="Lit server-side rendering so elements render for search engines and AI crawlers. Publish-time static SSR landed with static export in core, and elements were made SSR-safe; serving SSR live from the page route stays parked until it is stable.", source=L("haxtheweb/issues #3161", ISS + "3161"), links={"issue": ISS + "3161", "static": ISS + "3162", "live": ISS + "3170", "earlier": ISS + "2082"}, status="released", year=2026, yearNote="Publish-time SSR lands in core")
N("hax11ty", desc="\"HAX + 11ty = HAX11ty! The best of SEO from 11ty while using the HAX editor and the HAXcms theme engine.\"", source=L("haxtheweb.org: HAX11ty", HTW), links={"repo": GH + "/hax11ty", "docs": "https://haxtheweb.github.io/hax11ty/"}, release="git:haxtheweb/hax11ty", status="released")

# ---- tooling and community
N("cli", desc="hax: install with npm install --global @haxtheweb/create, then run hax start. Creates sites and components, audits DDD and publishes. Needs Node 20+.", source=L("haxtheweb.org", HTW), links={"repo": GH + "/create", "npm": "https://www.npmjs.com/package/@haxtheweb/create"}, release="npm:@haxtheweb/create", status="released", year=2025, yearNote="Winston White builds much of the HAX CLI", yearSource=L("WINS.md: Winston White", W["winston"]))
N("ubiquity", desc="The webcomponents release build that ships every element, as one tested set, to haxcms-nodejs and the other backends.", source=None, links={"repo": GH + "/webcomponents"}, release="git:haxtheweb/webcomponents", status="released")
N("staticpub", desc="Static export and Lit SSR built into haxcms-nodejs, haxcms-php and the CLI, so any site publishes as static files from core; HAX11ty becomes a wrapper around it.", source=L("haxtheweb/issues #3162", ISS + "3162"), links={"issue": ISS + "3162"}, status="released", year=2026, yearNote="Static export moves into core: hax site site:build-static")
N("magiclink", desc="One-time login links issued from the CLI (hax site site:login-link), so an admin can recover or hand out access without a password.", source=L("haxtheweb/issues #2854", ISS + "2854"), links={"issue": ISS + "2854"}, status="released", year=2026, yearNote="One-time login links")
N("importers", desc="Every way content gets into HAX: whole sites from WordPress, Drupal, Plone, ELMS:LN, Notion, GitBook, VitePress, Quarto, Pressbooks, OpenStax or any HTML site; a site from one Word, PowerPoint, Excel, PDF or HTML file; and documents, media or links dropped into the page you are writing.", source=L("system-spec.yaml", GH + "/haxcms-nodejs/blob/main/src/openapi/system-spec.yaml"), links={"code": GH + "/haxcms-nodejs/tree/main/src/systemRoutes/v1/routes/imports"}, status="released")
N("flows", desc="Three paths through HAX in order: how a page loads, how a page is added, and how a site is restructured with the outline designer. Open it and press Play.", always=True)
N("learnhax", desc="Learn HAX: tutorials, reference and onboarding for the HAX ecosystem, at learn.hax.cloud. This web is meant to fold into it.", source=L("learn.hax.cloud", LEARN), links={"site": LEARN, "repo": GH + "/learn"}, status="living")
N("deploy", desc="Publish targets for HAX sites: surge, Netlify, Vercel, GitHub Pages, GitLab Pages and Codeberg Pages, as static files, from the CLI or straight from HAXcms in the browser.", status="released")
N("ai", desc="AI features inside HAX: Dave Fusco's AI integration from the AI and HAX grant, and Zach Dodson's AI chat agent.", status="in-progress", year=2025, yearNote="AI arrives inside HAX")
N("agents", desc="Agent skills for HAX, split between PRAW (community and administration) and create (using HAX). With PRAW's context, closed issues per month rose about 90%, then 211%.", source=L("WINS.md: Agents with context", W["agents"]), links={"repo": GH + "/praw"}, status="released")
N("mcp", desc="An MCP server so agents can work with HAXcms sites. It connects to the Node.js and PHP backends and the CLI; it is not enabled on HAXiam deployments.", source=L("haxtheweb/haxcms-mcp", GH + "/haxcms-mcp"), links={"repo": GH + "/haxcms-mcp"}, release="git:haxtheweb/haxcms-mcp", status="prerelease")
N("praw", desc="Patterns, Rules, Agents, Worldview: HAX's networked brain, the worldview, voice, wins and skills that keep agents and contributors consistent.", source=L("PRAW README", GH + "/praw"), links={"repo": GH + "/praw", "Growth": "https://hax.cloud/growth"}, status="living")
N("issues", desc="The unified HAX issue queue for every project, including published security advisories.", links={"repo": GH + "/issues"}, status="living")
N("wins", desc="\"Sourced stories that prove the worldview works.\" A good win has a person, a before and after, and a source.", source=L("PRAW WINS.md", WINS), links={"repo": WINS}, status="living")
N("haxcamp", desc="Gatherings to learn web components. The first, hosted by Duke, drew over 40 people.", source=L("WINS.md: First hax-camp", W["camp"]), year=2019, yearNote="HAX Camp at Duke", yearSource=L("hax-lab README", HAXLAB))

# ---- content and design
N("components", desc="About 640 web components open sourced by May 2026; 289 @haxtheweb packages on npm, downloaded about 49,000 times a month. Open the Web components web to see the 60 blocks in the HAX app store.", source=L("WINS.md: 640+ open HTML tags", W["tags"]), links={"repo": GH + "/webcomponents"}, release="git:haxtheweb/webcomponents", status="released", year=2017, yearNote="The first web component brick", yearSource=L("WINS.md SIIP timeline", WINS))
N("ddd", desc="DDD (Design, Develop, Deliver), the HAX design system. It began as Keith Charlton Jr's class project and now spans 60+ elements: \"PSU-esque designs by PSU.\"", source=L("WINS.md: Students built the design system", W["ddd"]), links={"npm": "https://www.npmjs.com/package/@haxtheweb/d-d-d", "repo": GH + "/webcomponents"}, release="npm:@haxtheweb/d-d-d", status="released", year=2024, yearNote="Keith Charlton creates DDD", yearSource=L("hax-lab README", HAXLAB))
N("plugins", desc="A plugin architecture in progress: spec and examples in haxcms-plugin-examples, while core keeps the evolving baseline (SEO, accessibility, sitemaps).", source=L("haxtheweb/issues #3176", ISS + "3176"), links={"repo": GH + "/haxcms-plugin-examples", "issue": ISS + "3176"}, status="in-progress")
N("languages", desc="Internationalization for any web component, plus one canonical registry of 102 supported languages shared by the installer, system settings and site settings.", source=L("haxtheweb/issues #3165", ISS + "3165"), links={"issue": ISS + "3165"}, status="released")
N("insights", desc="Site Insights: an admin dashboard of reports computed from site content, including content, live outside link status, accessibility and where to add activities.", source=L("haxtheweb/issues #3167", ISS + "3167"), links={"issue": ISS + "3167", "pr": "https://github.com/haxtheweb/webcomponents/pull/1146"}, status="released")

# ---- communication
N("whatsnew", desc="A What's New dialog on the dashboard that tells people about new features, read by the CLI and agents too.", source=L("haxtheweb/issues #3172", ISS + "3172"), links={"issue": ISS + "3172"}, status="in-progress")
N("presentations", desc="Talks, podcasts and webinars about HAX from 2017 to 2026. Open the Presentations web to see each one, who gave it, where and what it covered.", source=L("PRAW talks", "https://github.com/haxtheweb/praw/blob/main/talks/README.md"), links={"notes": "https://github.com/haxtheweb/praw/blob/main/talks/README.md", "playlist": "https://www.youtube.com/watch?v=q0IjUz2_IhA&list=PLJQupiji7J5eTqv8JFiW8SZpSeKouZACH"}, year=2017, yearNote="The first HAX talk, at DrupalCon Baltimore", yearSource=L("DrupalCon Baltimore 2017 session", "https://events.drupal.org/baltimore2017/sessions/mad-scientist-road-show"))
N("ist256", desc="Bryan's advanced web development course at Penn State: vanilla web components and Lit, ending in real contributions to HAX. Taught from fall 2019 to spring 2026; many class projects became HAX components. Open the IST 256 web for semesters and projects.", source=L("btopro/edtechjoker README", "https://github.com/btopro/edtechjoker"), links={"repo": "https://github.com/btopro/edtechjoker"}, year=2019, yearNote="Bryan's first IST 256 semester")
N("grants", desc="Faculty and unit grants that fund real student work on HAX. Grant sizes are left out on purpose: it isn't a competition, and this work doesn't need much money.", source=L("WINS.md: HAX Lab faculty grants", W["grants"]))
N("g_fusco", desc="Dave Fusco's grant for AI and HAX: Canvas AI analysis built by students through the HAX CLI, reporting how AI-ready a course's assignments are and launching a live HAX site.", source=L("WINS.md: HAX Lab faculty grants", W["grants"]))
N("g_frank", desc="Jennifer Frank's grant for the International Student Portfolio: Winston White's work on HAXcms and skeletons, so students get portfolios they can take with them.", source=L("WINS.md: HAX Lab faculty grants", W["grants"]))
N("g_hhd", desc="With Health and Human Development: Bryan, Bill and Blake Colaianne, for making more games and improving web components and HAXcms.")
N("games", desc="Playful games and media built from HAX web components, like rpg-character games starring the Future Traveler.", source=L("haxtheweb/art", "https://github.com/haxtheweb/art"))
N("buttercups", desc="Buttercups Training, a UK training company that contributed to ELMS:LN and the HAX editor from 2019 to 2022: HAX content hooks, a TinCan (xAPI) bridge fix, H5P updates and MOOC content.", source=L("elmsln/elmsln pull requests from buttercupstraining", "https://github.com/elmsln/elmsln/pull/2698"), links={"site": "https://github.com/buttercupstraining"}, year=2019, yearNote="Buttercups Training starts contributing to ELMS:LN", yearSource=L("elmsln commit history", "https://github.com/elmsln/elmsln"))
N("innovationhub", desc="The Eric J. Barron Innovation Hub, Penn State's coworking and collaboration space in downtown State College. Its earlier site was built on hax.psu.edu.", source=L("innovationhub.launchbox.psu.edu", "https://innovationhub.launchbox.psu.edu/about/"), links={"site": "https://innovationhub.launchbox.psu.edu"})
N("tips", desc="HAX Tips, including a tip of the day, surfaced in Merlin and sharing the What's New system.", source=L("haxtheweb/issues #3172", ISS + "3172"), links={"issue": ISS + "3172"}, status="in-progress")

# ---- practices and standards
N("wcstandard", desc="The browser-native component model HAX is built on: \"Web components effectively turn the HTML of a site into a consistent API.\"", source=L("haxtheweb.org F.A.Q.", HTW), year=2016, yearNote="Mike Potter points Bryan to the web component standard", yearSource=L("WORLDVIEW.md: People who shaped it", WORLDVIEW))
N("security", desc="39 published advisories in the unified queue, many found by Penn State's CCSO students, who helped resolve 30 vulnerabilities over two years.", source=L("haxtheweb/issues security advisories", "https://github.com/haxtheweb/issues/security/advisories"), links={"advisories": "https://github.com/haxtheweb/issues/security/advisories"}, year=2025, yearNote="CCSO's first audit; the first CVEs are published", yearSource=L("haxtheweb/issues advisories", ADV + "GHSA-vj5q-3jv2-cg5p"))
N("testing", desc="Automated tests that check human- and AI-made changes: Chromium on every pull request, full cross-browser runs outside CI.")
N("design", desc="The UX and visual design practice behind HAX UI and DDD, shaped by student UX groups and the 2019 National Archives usability audit.", source=L("WINS.md: National Archives usability audit", W["nara"]))

# ---- schemas
N("jos", desc="JSON Outline Schema: the site structure (site.json) HAXcms is built on, effectively one to one.", links={"repo": GH + "/json-outline-schema", "npm": "https://www.npmjs.com/package/@haxtheweb/json-outline-schema"}, release="npm:@haxtheweb/json-outline-schema", status="released")
N("haxschema", desc="\"For your element to talk to the HAX editor, you implement static get haxProperties()\": the schema that gives every block its editing form.", source=L("haxtheweb.org: HAX schema", HTW))
N("appstore", desc="The app store spec: the autoloader \"loads all the elements that will be available to your users\", plus stax (templates) and blox (layouts).", source=L("haxtheweb.org: HAX app store", HTW))
N("oerschema", desc="Metadata for open educational resources, kept with the content so it can be found, credited and remixed. Authored by Michael Collins.", links={"site": "https://oerschema.org", "repo": GH + "/webcomponents/tree/master/elements/oer-schema"})
N("openapi", desc="The shared contract that keeps haxcms-nodejs and haxcms-php input and output identical.")
N("community", desc="How HAX is run: roles and succession, how a decision is made in the open, the documents every repo keeps, and where people meet.", links={"governance": "https://github.com/haxtheweb/issues/blob/main/GOVERNANCE.md"}, always=True)
N("quality", desc="Every safeguard on what enters HAX: blocking pull request gates, advisory checks, and nightly and weekly jobs, generated from the CI that actually runs.", links={"tracking": "https://github.com/haxtheweb/issues/issues/3262"}, always=True)
N("heosat", desc="HEOSAT, Apereo's Higher Education Open Source Assessment Toolkit: 47 questions in 9 sections on licensing, governance, community, docs, operations, security, standards, adoption and sustainability. HAX runs it with AI through the heosat skill in PRAW, a process worked out with Apereo. Open it to see every question and what answers it.", links={"heosat": "https://github.com/apereo/heosat", "map": "https://github.com/haxtheweb/praw/blob/main/ecosystem/heosat-evidence-map.json", "issue": "https://github.com/haxtheweb/issues/issues/3256"}, always=True)
N("booklooky", desc="BookLooky, a fellow open source project. HAX's AI-run HEOSAT process helped it go through Apereo incubation more accurately, and PRAW's haxcms-lrs-rater skill runs its Looky Rating System.", links={"issue": "https://github.com/haxtheweb/issues/issues/3256"}, always=True)
N("wcag", desc="WCAG, the Web Content Accessibility Guidelines from the W3C. HAX elements are built to meet them by default; element test suites run axe accessibility checks where an element has tests, and the weekly accessibility sweep checks every demo.", links={"spec": "https://www.w3.org/WAI/standards-guidelines/wcag/"}, always=True)
N("html", desc="The format every HAX page is saved in. A site's pages are plain HTML files with web components as their tags, so what you make stays readable and yours to take anywhere, with or without HAX.", source=L("PRAW ecosystem/build/data/pillars.json", "https://github.com/haxtheweb/praw/blob/main/ecosystem/build/data/pillars.json"), links={"spec": "https://html.spec.whatwg.org/"})
N("meaningchannels", desc="The meaning channels standard: anything that carries meaning or a consequential decision (correct versus incorrect, confirm versus deny, saving or deleting permanently) is conveyed through five channels at once: a label on hover and focus, a distinct color (green for correct, purple for incorrect, not red), a focus state, a texture that survives grayscale, and an icon unique to that meaning. Written into PRAW RULES.md; not yet in the DDD docs, and no gate enforces it yet.", status="in-progress", links={"rule": "https://github.com/haxtheweb/praw/blob/main/RULES.md#meaning-channels--meaning-and-consequential-decisions-use-all-five", "tracking": "https://github.com/haxtheweb/issues/issues/3262"}, always=True)
N("rules", desc="Rules and guarantees: every rule HAX keeps, generated from PRAW's RULES.md and each repo's AGENTS.md, linked up to the pillars it serves, across to the parts it touches and down to the checks that enforce it. A rule nothing enforces shows as a gap.", links={"rules": "https://github.com/haxtheweb/praw/blob/main/RULES.md"}, always=True)
N("contracts", desc="Every data contract in one view: the schema files each HAX format is defined by, and who reads and writes them.", always=True)
N("anatomy", desc="What a HAX site is made of on disk: site.json, pages, files, theme, the registry and the files HAXcms generates.", always=True)
N("xapi", desc="Learner activity recorded as xAPI-style statements, ready to move from local storage to a learning record store.", year=2016, yearNote="Dave Fusco works on xAPI integration", yearSource=L("hax-lab README", HAXLAB))

# ---- skeletons and use cases
N("skeletons", desc="Full working starter sites anyone can export and hand to someone else, \"hundreds of clicks closer to done.\"", source=L("WINS.md: Skeletons and benevolent restrictions", W["skeletons"]), year=2025, yearNote="Skeletons arrive in HAX 25", yearSource=L("WINS.md", W["skeletons"]))
N("course", desc="Online courses in multiple Penn State colleges; HAX began for online courses in Arts and Architecture. About 67,000 students educated through HAX-based systems in A&A alone.", source=L("WINS.md: Reach by early 2026", W["reach"]))
N("blog", desc="")
N("portfolio", desc="Portfolios students can take with them, starting with the International Student Portfolio and a set of student-built portfolio themes.", source=L("WINS.md: HAX Lab faculty grants", W["grants"]), year=2025, yearNote="Student-built portfolio themes", yearSource=L("hax-lab README", HAXLAB))
N("dept", desc="Department and unit sites owned without a web team, like the Learn to Flourish Hub at flourish.hhd.psu.edu.", source=L("WINS.md: Learn to Flourish Hub", W["flourish"]), links={"example": "https://flourish.hhd.psu.edu"}, year=2026, yearNote="flourish.hhd.psu.edu launches", yearSource=L("WINS.md", W["flourish"]))
N("flourish", desc="The Learn to Flourish Hub's public site, flourish.hhd.psu.edu. The Hub, in Health and Human Development and directed by Blake Colaianne, built it on HAX with A&A's Office of Digital Learning and runs it from hax.psu.edu without a web team. It launched in September 2026 as the face of the Hub for donors, students and partners. It shows HAX meeting goals at every level: Penn State's plan (health and wellness in a community focused on flourishing; partnerships with communities; advocates and investors), HHD's plan (student success; land-grant impact), A&A's plan (collaboration across colleges) and UN goals 3 and 17.", source=L("WINS.md: Learn to Flourish Hub", W["flourish"]), links={"site": "https://flourish.hhd.psu.edu", "team": "https://flourish.hhd.psu.edu/team", "goals": "https://github.com/haxtheweb/praw/blob/main/ecosystem/build/data/strategic-plans.json"}, year=2026, yearNote="flourish.hhd.psu.edu launches", yearSource=L("WINS.md", W["flourish"]))
N("cd101", desc="Customer Discovery 101, a public entrepreneurship training program from Invent Penn State LaunchBox, built on HAX by a team with limited design experience; users have praised both its functionality and design.", source=L("WINS.md: Customer Discovery 101", W["cd101"]), links={"site": "https://invent.psu.edu/programs/customer-discovery-101/", "story": APEREO_HAX, "news": PSUNEWS})
N("dbf", desc="Digital Beaumont & Fletcher, an open-access edition of the rarely taught Beaumont and Fletcher plays, with every text prepared by undergraduate and graduate students and published with HAX for classroom use.", source=L("WINS.md: Digital Beaumont & Fletcher", W["dbf"]), links={"site": "https://openpublishing.psu.edu/digital-beaumont-fletcher-about-project", "story": APEREO_HAX, "news": PSUNEWS})
N("jukebox", desc="The Jukebox, required listening for INART 116, History of Rock and Roll: 1950s, from the Office of Digital Learning: a one-column introduction, then audio on the left with annotation on the right, then collapsible lyrics, all built in HAX.", source=L("Apereo: HAX project page", APEREO_HAX), links={"story": APEREO_HAX})
N("docs", desc="Project documentation. The old docs site is retired: tutorials and reference live in Learn HAX, the rules, pledges and worldview in PRAW (hax.cloud), and the case for HAX on haxtheweb.org.", links={"site": LEARN, "repo": GH + "/praw"})
N("textbook", desc="Open books from Pressbooks, OpenStax or Word, pulled in, edited and published as open sites in minutes.", source=L("WINS.md: Migrations in seconds", W["migrations"]))

# ---- organizations
N("psu", desc="Where HAX was founded and is backed. \"HAX at Penn State is hosted and supported by a collaboration of several Penn State colleges and outside contributors.\"", source=L("hax.psu.edu", "https://hax.psu.edu"), links={"site": "https://hax.psu.edu"}, year=2015, yearNote="HAX starts as a note card at Penn State", yearSource=L("WINS.md: One maintainer, more rockets", WINS))
N("aa", desc="The College of Arts and Architecture, where HAX began for online courses and where HAX Lab and the Office of Digital Learning work. ODL built HAX and runs 47 online courses (more than 250 sections) on it each year, for more than 12,000 World Campus and University Park students.", source=L("Penn State News (2024)", PSUNEWS), links={"news": PSUNEWS}, year=2015, yearNote="HAX begins for online courses in Arts and Architecture", yearSource=L("WINS.md", W["tags"]))
N("ist", desc="The College of Information Sciences and Technology. IST 256 teaches modern front-end development with HAX; home of CCSO and UXDC.", source=L("WINS.md: SIIP lessons learned", WINS))
N("hhd", desc="Health and Human Development, home of the Learn to Flourish Hub and a partner on the games and platform grant. Its strategic plan opens from Penn State's.", source=L("WINS.md: Learn to Flourish Hub", W["flourish"]), year=2026)
N("eberly", desc="The Eberly College of Science: 14 courses on hax.psu.edu with 1,803 pages, from BIOL 110 and CHEM 110 to PHYS 211 and 212, serving its online students.", source=L("hax.psu.edu stats snapshot", "https://hax.psu.edu"), links={"news": PSUNEWS})
N("libraries", desc="Penn State University Libraries publishes XML-based plays with HAX, starting with The Sea Voyage in 2022.", source=L("WINS.md: 640+ open HTML tags", W["tags"]), links={"news": PSUNEWS})
N("haxlab", desc="Students and contributors working on HAX through courses, independent studies and internships; alumni now work at Red Hat, Adobe, IBM, Ford and PennDOT.", source=L("hax-lab README", HAXLAB), links={"repo": HAXLAB, "site": "https://lab.hax.cloud", "news": PSUNEWS}, year=2016, yearNote="The first HAX Lab contribution (xAPI and AI integration)", yearSource=L("hax-lab README", HAXLAB))
N("ccso", desc="Penn State's student cyber security club. Two long-form audits helped find and resolve 30 vulnerabilities over two years.", source=L("WINS.md: Student clubs", W["clubs"]), links={"site": "https://psuccso.org/"}, year=2025, yearNote="CCSO runs the 2025 HAX pentest", yearSource=L("hax-lab README", HAXLAB))
N("uxdc", desc="A student UX and design organization in IST, formerly UXPA (same organization, new name). Four members applied their UX training to HAX.", source=L("WINS.md: Student clubs (listed as UXPA)", W["clubs"]), links={"site": "https://discover.psu.edu/organization/uxdc"})
N("apereo", desc="An open source foundation for higher education. HAX is one of its software projects, with a project page, news and a donation form for individual supporters. Bryan has presented HAX at Apereo since 2019, most recently the SIIP talk at its May 2026 microconference.", source=L("Apereo: HAX project page", APEREO_HAX), links={"site": "https://www.apereo.org/", "project": APEREO_HAX, "donate": "https://apereo.civicrm.org/civicrm/contribute/transact?reset=1&id=7"}, year=2019, yearNote="HAXTheWeb @ Apereo 19", yearSource=L("Slides on SlideShare", AP19))
N("gatech", desc="Georgia Tech, where undergraduates contribute features to HAX alongside Penn State students.", source=L("Apereo: HAX project page", APEREO_HAX), links={"site": "https://www.gatech.edu/"})
N("github", desc="Hosts every HAX repository, the issue queue and its security advisories.", links={"site": GH})
N("npm", desc="Distributes 289 @haxtheweb packages, about 49,000 downloads a month.", source=L("WINS.md: 289 packages", W["npm"]), links={"site": "https://www.npmjs.com/org/haxtheweb"})
N("reclaim", desc="Reclaim Hosting, the hosting company that hosted HAX Camp at Duke; HAXcms installs on its hosting.", links={"site": "https://www.reclaimhosting.com/"}, year=2019, yearNote="Reclaim Hosting hosts HAX Camp at Duke")
N("uvic", desc="University of Victoria, where Jennifer Frank is now.", links={"site": "https://www.uvic.ca/"}, year=2026)
N("duke", desc="Hosted the first HAX Camp, which drew over 40 people to learn web components.", source=L("WINS.md: First hax-camp", W["camp"]), year=2019, yearNote="HAX Camp at Duke", yearSource=L("hax-lab README", HAXLAB))
N("drupalcon", desc="Where HAX was first shown: DrupalCon Baltimore 2017 (Bryan Ollendyke and Michael Potter), DrupalCon Nashville 2018, and HAXcms announced at DrupalCon Seattle with Red Hat.", source=L("DrupalCon Nashville 2018 session", "https://events.drupal.org/nashville2018/sessions/webcomponents-polymer-and-hax-decoupling-authoring-drupal-and-beyond"), links={"site": "https://events.drupal.org/nashville2018/sessions/webcomponents-polymer-and-hax-decoupling-authoring-drupal-and-beyond"}, year=2017, yearNote="HAX first presented at DrupalCon Baltimore", yearSource=L("DrupalCon Baltimore 2017 session", "https://events.drupal.org/baltimore2017/sessions/mad-scientist-road-show"))
N("elmsln", desc="ELMS:LN, the platform before HAX. Legacy now, but it is where the outline designer, Penn State's Drupal community and the first live web components began.", source=L("WINS.md: Foundations", WINS + "#foundations-before-hax"), links={"repo": "https://github.com/elmsln/elmsln"}, release="git:elmsln/elmsln", status="legacy")

# ---- people (hax-lab README, WINS.md, WORLDVIEW.md). role: staff | faculty | student | community
def person(id, role, did, link=None, src=None, year=None, yearNote=None, **kw):
    d = {"desc": did, "role": role}
    if link: d["links"] = {"profile": link}
    if src: d["source"] = src
    if year: d["year"] = year; d["yearNote"] = yearNote or did; d["yearSource"] = src
    d.update(kw)
    nodes[id] = d

HL = L("hax-lab README", HAXLAB)
person("bryan", "staff", "Creator of HAX and its lead; teaches IST 256 and runs HAX Lab. The rpg-character and the Future Traveler are caricatures of him.", src=L("WORLDVIEW.md", WORLDVIEW), always=True, github="btopro", link="https://github.com/btopro")
nodes["bryan"]["links"]["news"] = PSUNEWS
person("family", "family", "Bryan's grandfather, William \"Poppo\" Ollendyke, and his father, Todd: \"With the right tools you can build anything.\" A core motivator, and the idea of building anything out of imagination.", src=L("WHY.md: With the right tools", "https://github.com/haxtheweb/praw/blob/main/WHY.md#with-the-right-tools"))
person("billrose", "staff", "HAX product owner: the course ontology, cognitive apprenticeship framing and partner-facing voice. Leads the Office of Digital Learning team that built HAX.", src=L("WORLDVIEW.md: People who shaped it", WORLDVIEW), links={"news": PSUNEWS})
person("keithbailey", "staff", "Mentor who hired Bryan into online learning at Penn State and championed the work that led to HAX (1970–2020).", src=L("WORLDVIEW.md: People who shaped it", WORLDVIEW))
person("mikepotter", "community", "One of Bryan's best friends and a member of the ELMS:LN core team; pointed him to the web component standard in 2016 and co-presented the first HAX talks, starting at DrupalCon Baltimore 2017.", src=L("WORLDVIEW.md: People who shaped it", WORLDVIEW), year=2016, yearNote="Mike Potter points Bryan to the web component standard")
person("mcollins", "faculty", "Faculty member in Arts and Architecture who taught with ELMS:LN and now HAX, and builds his own flavor on it: the admin dashboard UI and the updated outline designer.", src=L("WINS.md: Michael Collins", W["collins"]), year=2026, yearNote="Michael Collins' admin dashboard and outline designer")
person("fusco", "faculty", "xAPI and AI integration (fall 2016); later funded Canvas AI analysis built by students through the HAX CLI.", src=L("hax-lab README; WINS.md: faculty grants", W["grants"]), link="https://github.com/djfusco", year=2016, yearNote="Dave Fusco: xAPI and AI integration")
person("jfrank", "faculty", "Funded the International Student Portfolio, so HAX grew into portfolios students can take with them.", src=L("WINS.md: HAX Lab faculty grants", W["grants"]))
person("blake", "faculty", "Director of the Learn to Flourish Hub in Health and Human Development; the Hub's faculty and students built its public site on HAX. Also on the HHD games and platform grant.", src=L("WINS.md: Learn to Flourish Hub", W["flourish"]), year=2026, yearNote="Learn to Flourish Hub site launches")
person("nikkimk", "contributor", "The second-largest contributor to the webcomponents monorepo (1,885 commits); co-presented HAX at DrupalCon Nashville 2018.", link="https://github.com/nikkimk", src=L("webcomponents contributors", "https://github.com/haxtheweb/webcomponents/graphs/contributors"), github="nikkimk")
GH_PEOPLE = [("cgldevel", "Chuck Lavera", "webcomponents and haxcms-php"), ("JAlbert2", "Jonah Albert", "webcomponents"), ("SanikaA3", "Sanika Ainchwar", "webcomponents, haxcms-php, haxcms-nodejs and create"), ("ChristianMurphy", "Christian Murphy", "webcomponents and haxcms-php"), ("aam198", "Allie Martz", "webcomponents"), ("firaol4", "Firaol Tulu", "webcomponents and haxcms-nodejs")]
for _l, _name, _repos in GH_PEOPLE:
    person("gh_" + _l.lower().replace("-", "_"), "community", f"{_name} (@{_l}), a contributor to {_repos}.", link=f"https://github.com/{_l}", src=L("GitHub contributors", "https://github.com/haxtheweb/webcomponents/graphs/contributors"), github=_l)
person("agearhart", "partner", "Works with HAX through Penn State University Libraries.", year=2022, yearNote="Andrew Gearhart and University Libraries")
person("rhumphries", "partner", "Leads Buttercups Training, Jack Davis's boss, whose team contributed to ELMS:LN, the editor and xAPI.", year=2019)
person("jackdavis", "community", "Buttercups Training developer; 59 commits to ELMS:LN from 2019 to 2022, including HAX content hooks and the TinCan bridge.", link="https://github.com/buttercupstraining", src=L("elmsln commit history", "https://github.com/elmsln/elmsln"), year=2019, yearNote="Jack Davis (Buttercups) contributes to ELMS:LN")
person("mark", "student", "Original ELMS:LN and Drupal student contributor (2017).", link="https://www.linkedin.com/in/mmilutinovic013/", src=HL, year=2017)
person("tom", "student", "HAX multimedia production, HAX Camp Duke planning committee and social media (2019).", link="https://www.linkedin.com/in/shiju-tom-varughese/", src=HL, year=2019)
person("tevin", "student", "Pre-release HAX UX study (2020).", link="https://www.linkedin.com/in/tevin-julien-b5123a185/", src=HL, year=2020)
person("sara", "student", "Media dashboard UX prototype (2020).", link="https://www.linkedin.com/in/saracunn/", src=HL, year=2020)
person("collin", "student", "Bootstrap theme for HAXcms (spring 2021).", link="https://github.com/collinkleest", src=HL, year=2021)
person("hanna", "student", "Built the vocab web component for presenting terms (2021); 15 commits to webcomponents as hvk5388.", link="https://www.linkedin.com/in/hannah-kern/", src=HL, year=2021, github="hvk5388")
person("jimmykane", "student", "Led the team that built Dashboard 1.0 and the 8-bit aesthetic HAX still uses (spring 2022); now an iOS engineer at Ford Motor Credit.", link="https://github.com/liljimmyk99", src=L("hax-lab README; WINS.md", W["dashboard"]), year=2022)
person("drewronk", "student", "8-bit video game aesthetic and site creation flow (spring 2022).", link="https://github.com/dronk6", src=HL, year=2022)
person("edelor", "student", "8-bit video game aesthetic and site creation flow (spring 2022).", link="https://github.com/elizabeth-delor", src=HL, year=2022)
person("liz", "student", "HAX Camp 2022 planning committee.", link="https://www.linkedin.com/in/lizblake17/", src=HL, year=2022)
person("taylor", "student", "HAX Camp 2022 planning committee.", link="https://www.linkedin.com/in/taylor-bracone/", src=HL, year=2022)
person("andrew", "student", "HAX Camp 2022 planning; JWT policy review and a headless login prototype (2023).", link="https://www.linkedin.com/in/maier-andrew/", src=HL, year=2022)
person("kcharlton", "student", "Turned a class project into the DDD design system (spring 2024).", link="https://github.com/kchar601", src=L("hax-lab README; WINS.md", W["ddd"]), year=2024)
person("zach", "student", "AI chat agent (summer 2024); sent the pull request that added the DDD audit to the CLI.", link="https://github.com/zdodson21", src=L("hax-lab README; WINS.md", W["ddd"]), year=2024)
person("kai", "student", "Audited DDD usage and QA'd elements in the monorepo (fall 2024).", link="https://github.com/klh6157", src=HL, year=2024)
person("ashley", "student", "Prototyped and gathered requirements for Dashboard 2.0 (2024), arriving with almost no coding experience.", src=L("WINS.md: Site Dashboard", W["dashboard"]), year=2024)
person("winston", "student", "Polaris themes (fall 2024), the theme CLI workflow and much of the HAX CLI (2025), skeleton templating (2026); TA'd the class after.", link="https://github.com/winstonwumbo", src=L("hax-lab README; WINS.md", W["winston"]), year=2024)
person("skyler", "student", "Start Journey screen (spring 2025); designed and built Dashboard 2.0 for HAX 25.", link="https://github.com/SkylerKoba88", src=L("hax-lab README; WINS.md", W["dashboard"]), year=2025)
person("isabella", "student", "Start Journey screen (spring 2025); designed and built Dashboard 2.0 for HAX 25.", link="https://github.com/izzabizz5", src=L("hax-lab README; WINS.md", W["dashboard"]), year=2025)
person("josh", "student", "Portfolio theme (spring 2025).", link="https://github.com/jno-de", src=HL, year=2025)
person("aarya", "student", "Two portfolio themes for HAXcms (summer 2025).", link="https://www.linkedin.com/in/aarya-awasthy/", src=HL, year=2025)
person("nazman", "student", "Glossy Portfolio theme for HAXcms (summer 2025).", link="https://www.linkedin.com/in/nazman-rosman/", src=HL, year=2025)
person("chloe", "student", "Dashboard 3.0: a Google Docs-style sites dashboard and admin UI.", src=L("WINS.md: Site Dashboard", W["dashboard"]), year=2026)
person("alyssa", "student", "Palettes and admin design thinking for Dashboard 3.0.", src=L("WINS.md: Site Dashboard", W["dashboard"]), year=2026)
ccso = [("jskeete", "Lead, discovery and reporting.", "https://indigosec.dev/", "Indigo-10", True),
        ("liam", "Lead, discovery and reporting.", "https://lfgberg.org", "lfgberg", False),
        ("asa", "Discovery and reporting.", "https://asareynolds.com/", "asareynolds", False),
        ("robert", "Discovery and reporting.", "https://github.com/userRPR", "userRPR", False),
        ("maguire", "Discovery and reporting.", "https://maguireyounes.com/", "23younesm", True),
        ("owen", "Reporting.", "https://www.linkedin.com/in/owendransfield/", "odransfield", True),
        ("nicholas", "Reporting.", "https://www.linkedin.com/in/nicholas-thomas485/", None, False),
        ("kekoa", "Reporting.", "https://www.linkedin.com/in/kekoa-merez/", None, False),
        ("miles", "Reporting.", "https://www.linkedin.com/in/mileshandelman", None, False)]
for pid, role, link, login, likely in ccso:
    extra = {}
    if login:
        extra["github"] = login
        if likely: extra["note"] = f"Advisory credits use the GitHub login {login}."
    person(pid, "student", "CCSO 2025 HAX pentest: " + role, link=link, src=HL, year=2025, yearNote="CCSO's 2025 HAX pentest", **extra)

# ---- evidence: CVEs from haxtheweb/issues advisories, keyed by advisory credit login
ADVS = [
 ("CVE-2025-32028", "GHSA-vj5q-3jv2-cg5p", "Insecure file upload leads to remote code execution", ["userRPR"]),
 ("CVE-2025-49141", "GHSA-g4cf-pp4x-hqgw", "haxcms-php command injection", ["userRPR"]),
 ("CVE-2025-49137", "GHSA-2vc4-3hx7-v7v7", "Stored cross-site scripting", ["lfgberg", "asareynolds"]),
 ("CVE-2025-49138", "GHSA-hxrr-x32w-cg8g", "Local file inclusion via saveOutline", ["Indigo-10"]),
 ("CVE-2025-49139", "GHSA-v3ph-2q5q-cg88", "Iframe phishing", ["lfgberg", "odransfield"]),
 ("CVE-2025-48996", "GHSA-fvx2-x7ff-fc56", "Unauthenticated disclosure of site listings", ["23younesm"]),
 ("CVE-2025-53642", "GHSA-g4f5-5w5j-p5jg", "Improper session termination", ["lfgberg"]),
 ("CVE-2025-54127", "GHSA-f38f-jvqj-mfg6", "Insecure default configuration", ["asareynolds"]),
 ("CVE-2025-54128", "GHSA-59g8-h59f-8hjp", "Disabled CSP enables XSS", ["asareynolds"]),
 ("CVE-2025-54129", "GHSA-wh3h-vfcv-m5g5", "User enumeration", ["lfgberg"]),
 ("CVE-2025-54134", "GHSA-pjj3-j5j6-qj27", "Improper error handling leads to DoS", ["asareynolds"]),
 ("CVE-2025-54137", "GHSA-5fpv-5qvh-7cf3", "Default secrets", ["lfgberg", "asareynolds"]),
 ("CVE-2025-54139", "GHSA-54vw-f4xf-f92j", "Clickjacking", ["lfgberg", "odransfield"]),
 ("CVE-2025-54378", "GHSA-9jr9-8ff3-m894", "Lack of authorization checks", ["lfgberg"]),
 ("CVE-2026-46392", "GHSA-hg33-w4j2-95qp", "Stored XSS via case-sensitivity mismatch", ["Indigo-10"]),
 ("CVE-2026-46399", "GHSA-q759-vxg8-vq5j", "Authenticated RCE via file overwrite", ["asareynolds"]),
 (None, "GHSA-f9mm-pqx5-j36f", "CDN fallback server exposes .git directory", ["Indigo-10"]),
]
login2person = {c[3]: c[0] for c in ccso if c[3]}
evidence = {}
def ev(key, label, url):
    evidence.setdefault(key, []).append(L(label, url))
for cve, ghsa, title, creds in ADVS:
    lab = f"{cve or ghsa}: {title}"
    ev("ccso>security", lab, ADV + ghsa)
    for c in creds:
        ev(login2person[c] + ">security", lab, ADV + ghsa)
ev("wins>ccso", "WINS: Student clubs, 30 security fixes", W["clubs"])
ev("wins>uxdc", "WINS: Student clubs (as UXPA)", W["clubs"])
ev("wins>security", "WINS: Student clubs, 30 security fixes", W["clubs"])
ev("wins>flourish", "WINS: Learn to Flourish Hub", W["flourish"])
ev("blake>flourish", "WINS: Learn to Flourish Hub", W["flourish"])
ev("flourish>hhd", "flourish.hhd.psu.edu", "https://flourish.hhd.psu.edu")
ev("flourish>aa", "WINS: Learn to Flourish Hub (with the Office of Digital Learning)", W["flourish"])
ev("flourish>psu", "PRAW strategic-plans.json", "https://github.com/haxtheweb/praw/blob/main/ecosystem/build/data/strategic-plans.json")
ev("flourish>sdgs", "PRAW sdg-links.json", "https://github.com/haxtheweb/praw/blob/main/ecosystem/build/data/sdg-links.json")
ev("wins>haxlab", "WINS: From HAX Lab to industry", W["industry"])
ev("wins>libraries", "WINS: 640+ open HTML tags", W["tags"])
ev("wins>apereo", "SIIP talk, Apereo microconference", SIIP)
ev("wins>cd101", "WINS: Customer Discovery 101", W["cd101"])
ev("wins>dbf", "WINS: Digital Beaumont & Fletcher", W["dbf"])
ev("gatech>components", "Apereo: HAX project page (Continuous Improvement)", APEREO_HAX)
ev("jukebox>course", "Apereo: HAX project page (The Jukebox)", APEREO_HAX)
ev("wins>npm", "WINS: 289 packages", W["npm"])
ev("wins>ddd", "WINS: Students built the design system", W["ddd"])
ev("wins>cli", "WINS: Winston White, student to trainer", W["winston"])
ev("wins>skeletons", "WINS: Skeletons and benevolent restrictions", W["skeletons"])
ev("wins>dashboard", "WINS: Site Dashboard, three generations", W["dashboard"])
ev("wins>portfolio", "WINS: HAX Lab faculty grants", W["grants"])
ev("psu>course", "WINS: 640+ open HTML tags", W["tags"])
ev("npm>components", "WINS: 289 packages", W["npm"])
ev("mikepotter>wcstandard", "WORLDVIEW: People who shaped it", WORLDVIEW + "#people-who-shaped-it")
ev("keithbailey>bryan", "WORLDVIEW: People who shaped it", WORLDVIEW + "#people-who-shaped-it")
ev("kcharlton>ddd", "WINS: Students built the design system", W["ddd"])
ev("zach>cli", "WINS: Students built the design system", W["ddd"])
ev("jimmykane>dashboard", "WINS: Site Dashboard", W["dashboard"])
ev("winston>cli", "WINS: Winston White", W["winston"])
ev("winston>skeletons", "WINS: Winston White", W["winston"])
ev("jfrank>portfolio", "WINS: HAX Lab faculty grants", W["grants"])
ev("fusco>cli", "WINS: HAX Lab faculty grants", W["grants"])
ev("mcollins>dashboard", "WINS: Michael Collins", W["collins"])
ev("andrew>haxcms", "Headless login prototype", ISS + "1007")
ev("hanna>components", "Vocab web component", ISS + "848")
ev("collin>themes", "Bootstrap theme for HAXcms", ISS + "212")
ev("tevin>haxcms", "Pre-release HAX UX study", "https://dev.to/techade1/haxcms-independent-study-pe2")
ev("bryan>traveler", "Future Traveler README", ART)
ev("editor>drupalcon", "DrupalCon Baltimore 2017: Mad Scientist Road show", "https://events.drupal.org/baltimore2017/sessions/mad-scientist-road-show")
ev("editor>drupalcon", "DrupalCon Nashville 2018: Webcomponents, Polymer and HAX", "https://events.drupal.org/nashville2018/sessions/webcomponents-polymer-and-hax-decoupling-authoring-drupal-and-beyond")
ev("editor>drupalcon", "Drupal GovCon 2018 (DC area): HAX session", "https://www.drupalgovcon.org/2018/program/sessions/hax-creating-best-drupal-authoring-experience-not-creating-it-drupal")
ev("bryan>drupalcon", "DrupalCon Baltimore 2017", "https://events.drupal.org/baltimore2017/sessions/mad-scientist-road-show")
ev("bryan>drupalcon", "DrupalCon Nashville 2018", "https://events.drupal.org/nashville2018/sessions/webcomponents-polymer-and-hax-decoupling-authoring-drupal-and-beyond")
ev("mikepotter>drupalcon", "DrupalCon Baltimore 2017", "https://events.drupal.org/baltimore2017/sessions/mad-scientist-road-show")
ev("mikepotter>editor", "DrupalCon Baltimore 2017", "https://events.drupal.org/baltimore2017/sessions/mad-scientist-road-show")
ev("mikepotter>elmsln", "Listed as ELMS:LN core team, DrupalCon Baltimore 2017", "https://events.drupal.org/baltimore2017/sessions/mad-scientist-road-show")
ev("haxcms>drupalcon", "WINS: HAXcms announced at DrupalCon", anchor("HAXcms announced at DrupalCon"))
for _k, _v in {"bryan>components": [{"label": "webcomponents contributors: btopro", "url": "https://github.com/haxtheweb/webcomponents/graphs/contributors"}], "nikkimk>components": [{"label": "webcomponents contributors: nikkimk", "url": "https://github.com/haxtheweb/webcomponents/graphs/contributors"}], "traveler>components": [{"label": "webcomponents contributors: claude", "url": "https://github.com/haxtheweb/webcomponents/graphs/contributors"}], "zach>components": [{"label": "webcomponents contributors: zdodson21", "url": "https://github.com/haxtheweb/webcomponents/graphs/contributors"}], "winston>components": [{"label": "webcomponents contributors: winstonwumbo", "url": "https://github.com/haxtheweb/webcomponents/graphs/contributors"}], "mikepotter>components": [{"label": "webcomponents contributors: heyMP", "url": "https://github.com/haxtheweb/webcomponents/graphs/contributors"}], "collin>components": [{"label": "webcomponents contributors: collinkleest", "url": "https://github.com/haxtheweb/webcomponents/graphs/contributors"}], "nazman>components": [{"label": "webcomponents contributors: NazmanRosman", "url": "https://github.com/haxtheweb/webcomponents/graphs/contributors"}], "isabella>components": [{"label": "webcomponents contributors: izzabizz5", "url": "https://github.com/haxtheweb/webcomponents/graphs/contributors"}], "gh_cgldevel>components": [{"label": "webcomponents contributors: cgldevel", "url": "https://github.com/haxtheweb/webcomponents/graphs/contributors"}], "gh_jalbert2>components": [{"label": "webcomponents contributors: JAlbert2", "url": "https://github.com/haxtheweb/webcomponents/graphs/contributors"}], "kai>components": [{"label": "webcomponents contributors: klh6157", "url": "https://github.com/haxtheweb/webcomponents/graphs/contributors"}], "josh>components": [{"label": "webcomponents contributors: jno-de", "url": "https://github.com/haxtheweb/webcomponents/graphs/contributors"}], "jackdavis>components": [{"label": "webcomponents contributors: JackWillDavis", "url": "https://github.com/haxtheweb/webcomponents/graphs/contributors"}], "gh_aam198>components": [{"label": "webcomponents contributors: aam198", "url": "https://github.com/haxtheweb/webcomponents/graphs/contributors"}], "chloe>components": [{"label": "webcomponents contributors: chloemartin312", "url": "https://github.com/haxtheweb/webcomponents/graphs/contributors"}], "gh_christianmurphy>components": [{"label": "webcomponents contributors: ChristianMurphy", "url": "https://github.com/haxtheweb/webcomponents/graphs/contributors"}], "skyler>components": [{"label": "webcomponents contributors: SkylerKoba88", "url": "https://github.com/haxtheweb/webcomponents/graphs/contributors"}], "kcharlton>components": [{"label": "webcomponents contributors: kchar601", "url": "https://github.com/haxtheweb/webcomponents/graphs/contributors"}], "aarya>components": [{"label": "webcomponents contributors: aarya0804", "url": "https://github.com/haxtheweb/webcomponents/graphs/contributors"}], "hanna>components": [{"label": "webcomponents contributors: hvk5388", "url": "https://github.com/haxtheweb/webcomponents/graphs/contributors"}], "jimmykane>components": [{"label": "webcomponents contributors: liljimmyk99", "url": "https://github.com/haxtheweb/webcomponents/graphs/contributors"}], "gh_firaol4>components": [{"label": "webcomponents contributors: firaol4", "url": "https://github.com/haxtheweb/webcomponents/graphs/contributors"}], "gh_sanikaa3>components": [{"label": "webcomponents contributors: SanikaA3", "url": "https://github.com/haxtheweb/webcomponents/graphs/contributors"}], "fusco>components": [{"label": "webcomponents contributors: djfusco", "url": "https://github.com/haxtheweb/webcomponents/graphs/contributors"}], "mcollins>components": [{"label": "webcomponents contributors: michael-collins", "url": "https://github.com/haxtheweb/webcomponents/graphs/contributors"}], "bryan>nodejs": [{"label": "haxcms-nodejs contributors: btopro", "url": "https://github.com/haxtheweb/haxcms-nodejs/graphs/contributors"}], "traveler>nodejs": [{"label": "haxcms-nodejs contributors: claude", "url": "https://github.com/haxtheweb/haxcms-nodejs/graphs/contributors"}], "winston>nodejs": [{"label": "haxcms-nodejs contributors: winstonwumbo", "url": "https://github.com/haxtheweb/haxcms-nodejs/graphs/contributors"}], "gh_sanikaa3>nodejs": [{"label": "haxcms-nodejs contributors: SanikaA3", "url": "https://github.com/haxtheweb/haxcms-nodejs/graphs/contributors"}], "mcollins>nodejs": [{"label": "haxcms-nodejs contributors: michael-collins", "url": "https://github.com/haxtheweb/haxcms-nodejs/graphs/contributors"}], "gh_firaol4>nodejs": [{"label": "haxcms-nodejs contributors: firaol4", "url": "https://github.com/haxtheweb/haxcms-nodejs/graphs/contributors"}], "bryan>php": [{"label": "haxcms-php contributors: btopro", "url": "https://github.com/haxtheweb/haxcms-php/graphs/contributors"}], "traveler>php": [{"label": "haxcms-php contributors: claude", "url": "https://github.com/haxtheweb/haxcms-php/graphs/contributors"}], "mikepotter>php": [{"label": "haxcms-php contributors: heyMP", "url": "https://github.com/haxtheweb/haxcms-php/graphs/contributors"}], "collin>php": [{"label": "haxcms-php contributors: collinkleest", "url": "https://github.com/haxtheweb/haxcms-php/graphs/contributors"}], "gh_cgldevel>php": [{"label": "haxcms-php contributors: cgldevel", "url": "https://github.com/haxtheweb/haxcms-php/graphs/contributors"}], "gh_sanikaa3>php": [{"label": "haxcms-php contributors: SanikaA3", "url": "https://github.com/haxtheweb/haxcms-php/graphs/contributors"}], "bryan>cli": [{"label": "create contributors: btopro", "url": "https://github.com/haxtheweb/create/graphs/contributors"}], "traveler>cli": [{"label": "create contributors: claude", "url": "https://github.com/haxtheweb/create/graphs/contributors"}], "winston>cli": [{"label": "create contributors: winstonwumbo", "url": "https://github.com/haxtheweb/create/graphs/contributors"}], "zach>cli": [{"label": "create contributors: zdodson21", "url": "https://github.com/haxtheweb/create/graphs/contributors"}], "jimmykane>cli": [{"label": "create contributors: liljimmyk99", "url": "https://github.com/haxtheweb/create/graphs/contributors"}], "bryan>praw": [{"label": "praw contributors: btopro", "url": "https://github.com/haxtheweb/praw/graphs/contributors"}], "traveler>praw": [{"label": "praw contributors: claude", "url": "https://github.com/haxtheweb/praw/graphs/contributors"}]}.items():
    for _x in _v: ev(_k, _x["label"], _x["url"])
ev("buttercups>editor", "PR #2698: HAX content hooks", "https://github.com/elmsln/elmsln/pull/2698")
ev("buttercups>xapi", "PR #2697: TinCan bridge fix", "https://github.com/elmsln/elmsln/pull/2697")
ev("buttercups>elmsln", "PR #2699: H5P 1.49 update", "https://github.com/elmsln/elmsln/pull/2699")
ev("buttercups>elmsln", "PR #2703: MOOC content fix", "https://github.com/elmsln/elmsln/pull/2703")
ev("buttercups>elmsln", "PR #2705: issue #956", "https://github.com/elmsln/elmsln/pull/2705")
ev("wins>innovationhub", "WINS: Reach by early 2026 (LaunchBox)", W["reach"])
ev("grants>wins", "WINS: HAX Lab faculty grants", W["grants"])
ev("fusco>g_fusco", "WINS: HAX Lab faculty grants", W["grants"])
ev("jfrank>g_frank", "WINS: HAX Lab faculty grants", W["grants"])
ev("winston>g_frank", "WINS: Winston White", W["winston"])
ev("winston>ist256", "WINS: Winston White (took IST 256 spring 2024)", W["winston"])
ev("kcharlton>ist256", "WINS: Students built the design system", W["ddd"])
ev("haxcamp>duke", "WINS: First hax-camp, 40+ people", W["camp"])

# ---- tours: audience, message, scenes
def S(c, *ids): return {"caption": c, "nodes": list(ids)}
tours = [
 {"id": "everyone", "label": "Everyone", "message": "HAX in one pass: people at the center, the pillars they hold, and everything that connects to them.", "scenes": [
   S("Humans are at the center of HAX.", "human"),
   S("People hold the seven pillars that make it powerful.", "accessible", "efficient", "extensible", "open", "agnostic", "remixable", "sustainable"),
   S("The Future Traveler is your AI companion, working alongside you.", "traveler"),
   S("It began at Penn State, with ELMS:LN and the people who built it.", "psu", "elmsln", "bryan", "billrose", "keithbailey"),
   S("Penn State backs the work through its colleges and University Libraries.", "aa", "ist", "hhd", "eberly", "libraries"),
   S("You build with HAXcms on PHP, Node.js, the CLI or HAX11ty.", "haxcms", "php", "nodejs", "cli", "haxiam", "hax11ty"),
   S("Authoring happens in the editor, Merlin, themes and the dashboard; open HAXcms for every admin piece.", "editor", "merlin", "themes", "dashboard", "haxcms"),
   S("The building blocks rest on the web component standard.", "components", "ddd", "plugins", "languages", "wcstandard", "mikepotter"),
   S("Schemas are the contracts that keep every part portable.", "jos", "haxschema", "appstore", "oerschema", "openapi", "xapi"),
   S("Skeletons make courses, blogs, portfolios and department sites reusable.", "skeletons", "course", "portfolio", "dept", "textbook"),
   S("HAX Lab and student clubs bring design and security; HAX Camp and DrupalCon grow the community.", "haxlab", "ccso", "uxdc", "design", "security", "haxcamp", "duke", "drupalcon"),
   S("Students and faculty built much of what you see.", "mcollins", "fusco", "jfrank", "blake", "mark", "tom", "tevin", "sara", "collin", "hanna", "jimmykane", "drewronk", "edelor", "liz", "taylor", "andrew", "kcharlton", "zach", "kai", "ashley", "winston", "skyler", "isabella", "josh", "aarya", "nazman", "chloe", "alyssa", "jskeete", "liam", "asa", "robert", "maguire", "owen", "nicholas", "kekoa", "miles"),
   S("The traveler learns from PRAW, skills, the MCP and the issue queue, checked by automated tests.", "praw", "agents", "mcp", "issues", "testing"),
   S("IST 256 turns students into contributors; grants fund the work.", "ist256", "grants", "g_fusco", "g_frank", "g_hhd", "games"),
   S("Apereo, GitHub and npm connect HAX to the open source world; Buttercups Training contributed from the UK.", "apereo", "github", "npm", "buttercups", "jackdavis", "innovationhub"),
   S("Ubiquity, Lit SSR and deploy targets ship it anywhere, fast.", "ubiquity", "ssr", "deploy"),
   S("WINS keeps the proof: the people and groups it helped.", "wins"),
   S("One web of connections. Every part makes every other part stronger."),
 ]},
 {"id": "faculty", "label": "Faculty", "message": "Build a course, portfolio or department site yourself, keep it accessible by default, and own it for good.", "scenes": [
   S("You are at the center, with the pillars that protect your work.", "human", "accessible", "remixable", "open"),
   S("HAXcms and the editor: authoring without a web team or the command line.", "haxcms", "editor", "merlin", "themes"),
   S("Start from a skeleton for a course, portfolio, textbook or department site.", "skeletons", "course", "portfolio", "textbook", "dept"),
   S("OER Schema and xAPI keep your content open and your learners' progress visible.", "oerschema", "xapi", "dashboard"),
   S("Faculty like you already build on it.", "mcollins", "jfrank", "blake", "flourish", "fusco", "hhd", "aa"),
   S("Penn State hosts it for you on hax.psu.edu.", "psu", "haxpsu", "haxiam", "wins"),
 ]},
 {"id": "students", "label": "Students", "message": "Learn modern front-end web by contributing to a real project. Your work ships, gets credited, and goes with you.", "scenes": [
   S("It starts with people, including you.", "human", "sustainable", "open"),
   S("HAX Lab, IST and the student clubs are the way in.", "haxlab", "ist", "aa", "ccso", "uxdc"),
   S("Web components, DDD and the CLI are what you'll learn and build.", "wcstandard", "components", "ddd", "cli", "themes", "dashboard"),
   S("Students built the dashboard, DDD, the CLI and skeletons.", "jimmykane", "ashley", "skyler", "isabella", "chloe", "alyssa", "kcharlton", "zach", "winston", "kai", "skeletons"),
   S("CCSO students found and fixed real vulnerabilities, with CVEs to show for it.", "security", "jskeete", "liam", "asa", "robert", "maguire", "owen", "nicholas", "kekoa", "miles"),
   S("Your contributions go on GitHub and npm, and into WINS.", "github", "npm", "issues", "wins"),
 ]},
 {"id": "developers", "label": "Developers", "message": "Standards all the way down: web components, an OpenAPI contract, a CLI and agent tooling you can extend without forking.", "scenes": [
   S("The web component standard is the foundation.", "wcstandard", "efficient", "agnostic"),
   S("Components, DDD and HAXSchema make every block editable by people and machines.", "components", "ddd", "haxschema", "appstore", "editor"),
   S("Two backends, one OpenAPI contract, plus the CLI and HAX11ty.", "haxcms", "php", "nodejs", "openapi", "cli", "hax11ty", "jos"),
   S("The MCP (pre-release), PRAW and skills let agents work the same way.", "traveler", "mcp", "praw", "agents", "extensible"),
   S("Ubiquity, SSR, tests and deploy targets ship it.", "ubiquity", "ssr", "testing", "deploy", "plugins"),
   S("Everything is on GitHub and npm, with one issue queue.", "github", "npm", "issues", "security"),
 ]},
 {"id": "partners", "label": "Partners", "message": "Free and open, backed by Penn State and the Apereo community, with sourced proof of what it does.", "scenes": [
   S("People and the pillars come first.", "human", "accessible", "efficient", "extensible", "open", "agnostic", "remixable", "sustainable"),
   S("Penn State backs HAX across its colleges and libraries.", "psu", "aa", "ist", "hhd", "eberly", "libraries"),
   S("Open source homes: Apereo, DrupalCon, GitHub and npm.", "apereo", "drupalcon", "github", "npm"),
   S("A pipeline of students keeps it moving, at Penn State and Georgia Tech.", "haxlab", "ccso", "uxdc", "gatech", "bryan", "billrose"),
   S("WINS has the proof.", "wins", "flourish", "dept", "course", "portfolio"),
   S("Proof outside the for-credit course: public training, open editions and a listening room.", "cd101", "dbf", "jukebox", "textbook"),
 ]},
 {"id": "administrators", "label": "Administrators", "message": "Host it your way: PHP or Node.js, many sites with HAXiam, static publishing, and a public security record.", "scenes": [
   S("Pick a backend: PHP or Node.js, kept identical by OpenAPI.", "php", "nodejs", "openapi", "agnostic"),
   S("HAXiam runs hundreds of sites from one core behind your login.", "haxiam", "haxcms", "psu"),
   S("Security is audited in public, with student auditors and automated tests.", "security", "ccso", "testing", "issues", "sustainable"),
   S("Publish static sites anywhere.", "deploy", "hax11ty", "libraries", "efficient"),
   S("The MCP is pre-release and not enabled on HAXiam.", "mcp"),
 ]},
]

meta = {
 "name": "HAX ecosystem",
 "updated": "2026-11-05",
 "checked": None,
 "about": "Details for hax-ecosystem.mmd. Structure lives in the Mermaid file; this file holds descriptions, links, releases, evidence, tours and timeline years. Run scripts/graph-drift.mjs after each release to refresh versions and flag what changed.",
 "pairs": [["php", "nodejs", "haxcms-php and haxcms-nodejs ship together and should carry the same version."]],
 "statusLabels": {"released": "Released", "prerelease": "Pre-release", "in-progress": "In progress", "planned": "Planned", "legacy": "Legacy", "living": "Living document", "deployed": "Deployed"},
}

for _p, _g in [("zach","zdodson21"),("winston","winstonwumbo"),("collin","collinkleest"),("nazman","NazmanRosman"),("isabella","izzabizz5"),("kai","klh6157"),("josh","jno-de"),("chloe","chloemartin312"),("jimmykane","liljimmyk99"),("skyler","SkylerKoba88"),("kcharlton","kchar601"),("aarya","aarya0804"),("mcollins","michael-collins"),("fusco","djfusco"),("jackdavis","JackWillDavis"),("bryan","btopro"),("mikepotter","heyMP")]:
    nodes[_p]["github"] = _g

# ---- story tours (from the "New Tours and Roadmap" doc) and the roadmap
import re as _re
_mmd = open("hax-ecosystem.mmd").read()
_pillar_edges = {}
for _l in _mmd.splitlines():
    _mm = _re.match(r"\s*(\w+)\s*==>\s*(?:\|[^|]*\|)?\s*(\w+)\s*$", _l)
    if _mm and _mm.group(2) in P: _pillar_edges.setdefault(_mm.group(2), []).append(_mm.group(1))
PILLAR_WORD = {"accessible": "Accessible", "efficient": "Efficient", "extensible": "Extensible", "open": "Open", "agnostic": "Agnostic", "remixable": "Remixable", "sustainable": "Sustainable"}
STORIES = [
 {"id": "content", "label": "Follow one piece of content", "kind": "story", "message": "What remixability means in practice: one page, from a person typing to a published, machine-readable site.", "scenes": [
   S("A person writes a page in the HAX editor.", "human", "editor", "components"),
   S("The page is saved as HTML in a site described by JSON Outline Schema, tagged with OER Schema.", "jos", "oerschema", "haxschema"),
   S("HAXcms on PHP or Node.js stores and serves it, both keeping the same OpenAPI contract.", "haxcms", "php", "nodejs", "openapi"),
   S("It leaves as a static publish or server-rendered for search engines and AI.", "deploy", "hax11ty", "ssr", "remixable"),
 ]},
 {"id": "sustainable", "label": "Why we're sustainable", "kind": "story", "message": "For funders, administrators and leadership: institutional backing plus open infrastructure means the project lasts.", "scenes": [
   S("Penn State backs HAX.", "psu", "haxpsu"),
   S("Five colleges and units teach and publish with it.", "aa", "ist", "hhd", "eberly", "libraries"),
   S("Students audit its security through CCSO.", "ccso", "security"),
   S("The Apereo Foundation supports it beyond one university.", "apereo"),
   S("GitHub and npm carry it as open infrastructure.", "github", "npm", "open"),
   S("WINS keeps the evidence.", "wins", "sustainable"),
 ]},
 {"id": "contribution", "label": "Your first contribution", "kind": "story", "message": "For students and new contributors: the path from coursework to real contributions.", "scenes": [
   S("A class project in IST 256.", "ist256"),
   S("Becomes a HAX component.", "components", "wcstandard", "ddd"),
   S("PRAW and its agent skills show you the conventions.", "praw", "agents", "issues"),
   S("The HAX CLI scaffolds, audits and ships it.", "cli", "testing", "ubiquity"),
 ]},
 {"id": "pillars", "label": "Pick your pillar", "kind": "story", "message": "One short scene per pillar, for a talk that needs one focused angle.", "scenes":
   [S(f"{PILLAR_WORD[p]}: {P[p]}", p, *sorted(set(_pillar_edges.get(p, [])) - {"human"})) for p in P] + [S("All seven pillars, held by people.", "human", *P)]},
 {"id": "companion", "label": "The AI companion", "kind": "story", "message": "HAX's AI-forward direction: humans and AI remixing each other's work in a standards-compliant, accessible way.", "scenes": [
   S("A person.", "human"),
   S("Works alongside the Future Traveler.", "traveler", "bryan"),
   S("Who learns the conventions from PRAW and its agent skills.", "praw", "agents"),
   S("And reaches HAXcms through the MCP (pre-release), the same OpenAPI contract people use.", "mcp", "openapi"),
   S("The HAX CLI is how both get work done.", "cli", "accessible"),
 ]},
 {"id": "origins", "label": "Where it came from", "kind": "story", "message": "The human story behind the project. The Over time tour has the full year-by-year version.", "scenes": [
   S("ELMS:LN at Penn State, a learning network built from many small apps.", "elmsln", "psu"),
   S("Keith Bailey championed it; Bill Rose and Bryan Ollendyke built it.", "keithbailey", "billrose", "bryan"),
   S("Mike Potter pointed Bryan to the web component standard.", "mikepotter", "wcstandard"),
   S("The HAX editor came first, then HAXcms on PHP, then Node.js, the CLI and the MCP.", "editor", "haxcms", "php", "nodejs", "cli", "mcp"),
   S("Now the Future Traveler works alongside everyone.", "traveler", "human"),
 ]},
 {"id": "course", "label": "Build a course in five minutes", "kind": "story", "message": "For faculty and instructional designers: a quick, use-case-driven path.", "scenes": [
   S("Start from the course skeleton.", "skeletons", "course"),
   S("Pick a theme.", "themes", "ddd"),
   S("Drop in instructional blocks.", "components", "editor", "oerschema"),
   S("Watch how it is used from the dashboard, with Insights on the way.", "dashboard", "xapi", "haxcms"),
 ]},
 {"id": "migrate", "label": "Migrate your site", "kind": "story", "message": "For people stuck on a legacy CMS: a clear way out.", "scenes": [
   S("Your site lives in WordPress, Drupal, Plone, Notion or somewhere else.", "importers"),
   S("The importers bring it in as a HAX site; open Importers for every platform and file type.", "importers", "haxcms", "jos"),
   S("Pick a theme and the DDD blocks do the rest.", "themes", "ddd", "components"),
   S("Or start from a skeleton and import into it.", "skeletons"),
   S("A working HAXcms site, yours to publish anywhere.", "haxcms", "deploy", "agnostic"),
 ]},
 {"id": "roadmap", "label": "What's coming", "kind": "story", "message": "The Future Traveler is from the future. Planned and in-progress parts show as ghosted tiles, each tied to its issue in the unified queue.", "scenes": [
   S("Landed from this roadmap in 2026: static export and publish-time SSR in core, one-time login links, Site Insights and one language registry.", "staticpub", "ssr", "magiclink", "insights", "languages", "cli"),
   S("A plugin architecture, from HAXiam system plugins down to site plugins.", "plugins", "haxiam", "haxcms"),
   S("What's New and Tips tell people about new features in the dashboard and in Merlin; open HAXcms for them.", "dashboard", "merlin", "haxcms"),
   S("AI inside HAX and the MCP leave pre-release.", "ai", "mcp", "agents"),
   S("Everything still coming, at once.", "plugins", "haxcms", "ai", "mcp"),
 ]},
]
# tours as pages (https://github.com/haxtheweb/issues/issues/3258): how work travels (Napkin to PR), the two roles
# the audience tours leave out (a student taking a course, an agent at work; "Build a course in five minutes" and
# Administrators are the instructor's and the site admin's), and the entry points people arrive through
STORIES += [
 {"id": "napkin", "label": "Napkin to PR", "kind": "story", "message": "How an idea becomes part of HAX: from a sketch on a napkin to a reviewed pull request, a release and the live sites that run it.", "scenes": [
   S("It starts with a person and an idea: something HAX should do.", "human"),
   S("The idea becomes a drawing. A napkin sketch or a screenshot is enough for the Future Traveler to start from, with PRAW's skills and rules to guide it.", "traveler", "design", "praw", "agents"),
   S("The work is tracked in the unified issue queue and arrives on GitHub as a pull request.", "issues", "github"),
   S("Gates and quality checks run on the pull request: tests, lint, accessibility and security. Nothing merges itself; a person reviews it.", "quality", "testing", "rules", "security"),
   S("The ubiquity build compiles every element into one tested set and writes the registry.", "ubiquity", "components", "registry"),
   S("The release goes out to npm, and on to both backends and the CLI.", "npm", "php", "nodejs", "cli"),
   S("Live sites pick it up: hax.psu.edu, HAXcms in the browser and every site published from HAX.", "haxpsu", "browser", "deploy"),
 ]},
 {"id": "learner", "label": "Learn in a HAX course", "kind": "story", "message": "For students: what a course built with HAX gives the person taking it.", "scenes": [
   S("You are a student, and a course built with HAX is in front of you.", "human", "course"),
   S("At Penn State it lives on hax.psu.edu, behind the login you already have.", "haxpsu", "haxiam", "psu"),
   S("Every page is built from accessible web components, so it works on any screen and in any browser.", "components", "accessible", "agnostic"),
   S("Self-checks and activities record what you do as xAPI-style statements, ready to move to a learning record store.", "xapi"),
   S("OER Schema describes what each page teaches, so the course stays open and remixable.", "oerschema", "open", "remixable"),
   S("And if you want to build it yourself, IST 256 and HAX Lab are the way in.", "ist256", "haxlab"),
 ]},
 {"id": "agent", "label": "An agent at work", "kind": "story", "message": "For AI agents and the people who direct them: how an agent finds HAX's skills, follows its rules and ships work through the same gates as everyone else.", "scenes": [
   S("An agent works alongside a person, as the Future Traveler does.", "traveler", "human"),
   S("It finds HAX's skills through the discovery index that every HAXcms deployment and every site carries.", "skillsindex", "agents"),
   S("PRAW gives it the rules, voice and worldview that keep its work consistent.", "praw", "rules"),
   S("The HAX CLI is how it does the work: creating sites and components, auditing and publishing.", "cli"),
   S("The MCP (pre-release) reaches HAXcms through the same OpenAPI contract people use.", "mcp", "openapi"),
   S("Its changes go through the issue queue and the same pull request checks as a person's.", "issues", "github", "quality", "testing"),
 ]},
 {"id": "start-cloud", "label": "Start from hax.cloud", "kind": "story", "message": "Five ways in from hax.cloud: the playground, the magic script, the element browser, RPG me and the desktop app.", "scenes": [
   S("The playground: HAXcms in a browser tab, with no install and no server.", "browser"),
   S("The magic script: two lines that load any HAX web component the moment it appears on a page, found through the registry.", "registry", "wcstandard"),
   S("The element browser: every HAX element, with live demos.", "components", "ddd"),
   S("RPG me: make the character that is you across HAX.", "games"),
   S("The desktop app: HAXcms as an application on your own computer.", "haxcms"),
 ]},
]
tours += STORIES

# versions accepted by drift.py --accept (graph-drift.mjs reads them from npm and GitHub tags)
import os as _os
if _os.path.exists("ext/versions.json"):
    _V = json.load(open("ext/versions.json"))
    for _k, _v in _V.get("nodes", {}).items():
        if _k in nodes: nodes[_k].update(_v)
    if _V.get("checked"): meta["checked"] = _V["checked"]
# details for parts that moved to a sub-web (admin files, What's New and Tips to HAXcms; blog and docs to skeletons) are kept for those builders, not drawn here
import re as _re
_drawn = set(_re.findall(r"^\s+(\w+)[\[\(\{>]", open("hax-ecosystem.mmd").read(), _re.M))
_moved = {k: nodes.pop(k) for k in list(nodes) if k not in _drawn}
json.dump(_moved, open("ext/main-moved.json", "w"), indent=1, ensure_ascii=False)
# evidence only for connections the web draws
_edges = set((a2, b2) for a2, b2 in _re.findall(r"^\s+(\w+) [-=.o>]+\|[^|]*\| (\w+)", open("hax-ecosystem.mmd").read(), _re.M))
evidence = {k: v for k, v in evidence.items() if tuple(k.split(">")) in _edges}
json.dump({"meta": meta, "nodes": nodes, "evidence": evidence, "tours": tours}, open("hax-ecosystem.json", "w"), indent=1, ensure_ascii=False)
print(len(nodes), "nodes;", sum(len(v) for v in evidence.values()), "evidence links;", len(tours), "tours")
