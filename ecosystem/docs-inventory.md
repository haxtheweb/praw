# HAX docs content inventory (haxtheweb.org)

Every page of [haxtheweb/docs](https://github.com/haxtheweb/docs), recorded so nothing is lost when the ecosystem web replaces haxtheweb.org. Each page maps to one to three ecosystem web nodes. WCFactory pages are marked to drop: the create CLI replaced it. The docs site's own pillar pages (under Welcome → Community → Pillars) should take the new pillar phrases and descriptions.

- Source: https://github.com/haxtheweb/docs at commit `ea4dd184bd3063c4993267fcde29dba89e5df4ba` (branch master)
- Total pages: **156** (site.json `items`: 156)
- Total words (visible page text, scripts/styles excluded): **39,889**
- Unpublished: Site things; published flag unset: AI integration
- Empty pages (0 words): 8 (Header, Providing Quality Feedback, Schema, Deprecated, Study Guide Approaches, Guided Practice, ODL Course Showcase, Site things)
- Note: links under github.com/elmsln/* still redirect today, but point at the old org and should be rewritten to haxtheweb/*.

## Proposed NEW graph nodes (9)

| key | label | pages mapped |
|---|---|---|
| `gallery` | Gallery of Online Excellence | 18 |
| `ontology` | HAX course ontology | 9 |
| `haxcloud` | HAX.cloud, CDN and magic script | 6 |
| `standalone` | Stand-alone tools | 6 |
| `cmsintegrations` | CMS integrations (Drupal, WordPress, Backdrop, Grav, ClassicPress) | 6 |
| `community` | Community and contributing | 3 |
| `roadmap` | Roadmap | 1 |
| `desktop` | HAX Desktop (Electron) | 1 |
| `outlinedesigner` | Outline designer | 1 |

## Stale / deprecated flags (33 pages)

| title | slug | flags |
|---|---|---|
| Welcome | `welcome` | links to old elmsln/issues queue |
| Project roadmap | `roadmap` | dated: 2025 roadmap, needs refresh for 2026 |
| Accessible | `community/pillars/accessibility` | links to elmsln/issues labels (moved to haxtheweb/issues); references Simple Colors (superseded by DDD) |
| Platform Agnostic | `welcome/community/pillars/platform-agnostic` | links to elmsln/issues labels (moved to haxtheweb/issues) |
| Sustainable | `welcome/community/pillars/sustainability` | mentions Project EdtechJoker pipeline (persona retired) |
| Environmental impact | `pledges/environmental-impact` | issue-report link points to elmsln/issues (moved) |
| Accessibility and Empowerment | `pledges/accessibility-empowerment` | issue-report link points to elmsln/issues (moved) |
| History | `welcome/community/history` | references Project EdTechJoker; timeline may stop short of 2025-2026 |
| Planning the Lecture | `planning-the-lecture` | Gallery content imported from iam.hax.psu.edu/bmr1/sites/haxcellence |
| ELMS:LN | `documentation/elmsln` | deprecated project page; elmsln.org http link may be dead |
| Peter Aeschbacher Exhibit | `peter-aeschbacher-exhibit` | contains 'Content goes here.' placeholder text |
| Desktop | `solutions/desktop` | possibly stale; verify desktop repo is maintained |
| Local Save | `the-future/stand-alone-tools/local-save` | links haxtheweb.org/assets/local-save.html, which may disappear when the site is replaced |
| Course Model Player | `page` | assets hosted under elmsln/lrnwebcomponents raw URLs (repo renamed); embeds media.ed.science.psu.edu H5P iframe |
| Effective Educational Video | `effective-educational-video` | internal links point to iam.hax.psu.edu/bmr1/sites/haxcellence (source site), not this site |
| In Brief: Design Guidelines and Principles | `design-guidelines-and-principles` | internal links point to iam.hax.psu.edu/bmr1 source site |
| Foster Student Engagement | `foster-student-engagement` | contains 'aaa bbb ccc' placeholder text |
| In Brief: A Sound Process | `in-short-a-sound-process` | internal links point to iam.hax.psu.edu/bmr1 source site |
| Gallery Exhibits | `gallery-exhibits` | exhibit links point to iam.hax.psu.edu/bmr1 source site |
| Frontend developers | `documentation/hax-frontend-devs` | links to elmsln/lrnwebcomponents (renamed to haxtheweb/webcomponents); links to elmsln/wc-workshop; links to old haxtheweb.org/documentation-1/... paths; haxapi.vercel.app link may be stale |
| Implementing DDD | `documentation/hax-frontend-devs/implementing-ddd` | DDDStyles link points to elmsln/lrnwebcomponents (renamed) |
| Data store | `documentation/developers/haxsite/data-store` | self-described as possibly out of date |
| WCFactory | `documentation/wcfactory` | deprecated tooling; uses old 'npm init @haxtheweb'; links elmsln/wcfactory, elmsln/lrnwebcomponents, webcomponents.org (retired); mentions Yarn/Lerna |
| Developers | `documentation/developers` | yarn-based contribution steps may be outdated |
| WCFactory | `documentation/developers/tools/wcfactory` | duplicate of deprecated WCFactory content; links haxtheweb/wcfactory |
| Tutorials | `tutorials` | links to elmsln/issues (moved to haxtheweb/issues) |
| Documentation | `documentation` | mentions wcfactory.js.org (deprecated) |
| Integrations | `documentation/haxcms/integrations` | links elmsln/hax-all-the-things (old org) |
| Drupal | `documentation/haxcms/integrations/drupal` | covers Drupal 6/7/8/9 only (EOL versions; no 10/11) |
| GravCMS | `documentation/integrations/gravcms` | plugins under elmsln org (possibly unmaintained) |
| Footer - bottom | `site-things/footer-bottom` | site chrome; copyright 2024; http:// PSU policy links |
| HAXiam | `solutions/haxiam` | links github.com/elmsln/HAXiam (old org) |
| The Future | `the-future` | latest horizon report is Oct 2023 |

## Pages by top-level section

Status: P = published, U = unpublished, ? = unset; H = hidden in menu. NEW nodes are in italics with a `NEW` tag.

### Welcome (29 pages, 6,803 words)

| title | slug | parent | status | words | summary | elements | mapped nodes | flags |
|---|---|---|---|---|---|---|---|---|
| Welcome | `welcome` |  | P | 344 | Landing page pitching HAX as simple create/share/remix web authoring, with HAX.cloud try-it, CLI install, and community links. | grid-plate, rpg-character, site-collection-list | `haxcms`, `cli`, `human` | links to old elmsln/issues queue |
| Why HAX? | `welcome/why-hax` | Welcome | P | 263 | Argues HAX's 1:1 edit-what-you-see model beats WYSIWYG editors like CKEditor/TinyMCE and lists trade-offs. |  | `editor`, `ubiquity`, `efficient` |  |
| Project roadmap | `roadmap` | Welcome | P | 479 | 2025 vision roadmap: DDD palette/theme stabilization, use-case skeletons via CLI recipe files, and related platform goals as of Jan 2025. |  | *roadmap* NEW, `ddd`, `skeletons` | dated: 2025 roadmap, needs refresh for 2026 |
| What is HAX? | `what-is-hax` | Welcome | P | 590 | Explains the ubiquity idea, what 'Headless Authoring eXperience' means, and shows an ecosystem diagram with an intro video. | media-image, video-player | `ubiquity`, `haxcms`, `wcstandard` |  |
| HAX Cloud | `welcome/hax-cloud` | What is HAX? | P | 179 | Describes HAX.cloud public infrastructure: CDN/magic script, Open APIs, PDF service, secure feedback, AI endpoint. |  | *haxcloud* NEW, `open`, `ai` |  |
| meme-maker | `welcome/what-is-hax/meme-maker` | What is HAX? | P | 200 | Teaches the HAX idea through the meme-maker web component: a custom tag that edits live and serializes to HTML. | code-sample, meme-maker | `components`, `haxschema`, `wcstandard` |  |
| Terminology | `welcome/terminology` | Welcome | P | 297 | Glossary of core terms: HAX/headless, web component, HAXcms, HAXsite, blocks and related vocabulary. |  | `wcstandard`, `haxcms`, `components` |  |
| Community | `community` | Welcome | P | 132 | Community hub: Discord, X, LinkedIn, issue queues, monthly meetups and hosting a HAX Camp; shows contributor RPG avatars. | github-rpg-contributors | *community* NEW, `haxcamp`, `issues` | hax.camp also linked via waxam.github.io mirror; verify which is canonical |
| Pillars | `welcome/community/pillars` | Community | P | 86 | Intro to the community pillars as the project's guiding values, listing child pillar pages. | site-collection-list | `accessible`, `open`, `sustainable` |  |
| Accessible | `community/pillars/accessibility` | Pillars | P | 200 | Accessibility pillar: HAX output and editor aim for high a11y with less author knowledge needed; cites SimpleColors. | grid-plate | `accessible` | links to elmsln/issues labels (moved to haxtheweb/issues); references Simple Colors (superseded by DDD) |
| Extensible | `welcome/community/pillars/extensibility` | Pillars | P | 185 | Extensibility pillar: built on the web component standard with VanillaJS/Lit, MobX, and an extensible theme engine. |  | `extensible`, `wcstandard`, `themes` |  |
| Free and Open | `welcome/community/pillars/free-and-open` | Pillars | P | 188 | Free and Open pillar: open community, 5Rs of OER, open docs/APIs, and equal footing for every hosting model. |  | `open`, `remixable`, `oerschema` |  |
| Efficient | `welcome/community/pillars/performant` | Pillars | P | 245 | Efficiency/performance pillar: low-level APIs, micro-services, lazy loading, and performance as an access issue. | grid-plate, un-sdg | `efficient`, `sustainable` |  |
| Platform Agnostic | `welcome/community/pillars/platform-agnostic` | Pillars | P | 296 | Platform agnostic pillar: HAX works standalone, in HAXcms/HAXiam, static pages, Drupal, WordPress, desktop, etc. | grid-plate | `agnostic`, `jos` | links to elmsln/issues labels (moved to haxtheweb/issues) |
| Remixable | `welcome/community/pillars/remixability` | Pillars | P | 253 | Remixability pillar: every HAX tool should let users remix and rapidly prototype solutions. |  | `remixable` |  |
| Sustainable | `welcome/community/pillars/sustainability` | Pillars | P | 317 | Sustainability pillar across environmental, technological and project dimensions, including CDN unbundling and Apereo membership. | grid-plate, video-player | `sustainable`, `apereo`, *haxcloud* NEW | mentions Project EdtechJoker pipeline (persona retired) |
| User Personas | `welcome/community/user-personas` | Community | P | 366 | User personas (Cat the author, Chuck the site builder, Sven the artist, and others) describing who HAX serves. | accent-card | `human`, `traveler` |  |
| Pledges | `pledges` | Community | P | 61 | Intro to the community pledges the project aspires to, with child pages listed. | site-collection-list | `sustainable`, `accessible` |  |
| Environmental impact | `pledges/environmental-impact` | Pledges | P | 110 | Environmental-impact pledge: standards over libraries, offline PWAs, caching, databaseless design, on-demand micro-services. |  | `sustainable`, `efficient` | issue-report link points to elmsln/issues (moved) |
| Accessibility and Empowerment | `pledges/accessibility-empowerment` | Pledges | P | 148 | Accessibility and empowerment pledge: broad definition of a11y, WCAG 2.0 AA, and auto-handling a11y concerns for authors. |  | `accessible` | issue-report link points to elmsln/issues (moved) |
| History | `welcome/community/history` | Community | P | 527 | Timeline of HAX origins from the 2007 e-Learning Institute and ELMS through HAX's first prototypes and later milestones. |  | `elmsln`, `bryan`, `billrose` | references Project EdTechJoker; timeline may stop short of 2025-2026 |
| Governance | `welcome/community/governance` | Community | P | 100 | Governance flowchart for what gets released, with exceptions for institutional security, keys, and PSU-branded assets. | media-image | `psu`, `open` |  |
| Contributor guide | `welcome/community/contributor-guide` | Community | P | 269 | Contributor guide pointing to developer onboarding, 'new here' issues, pillars, Discord, CLI, HAX Lab and grants. |  | *community* NEW, `learnhax`, `issues` |  |
| Marketing | `marketing` | Welcome | P | 25 | Marketing materials landing page embedding the HAX one-pager. | iframe-loader | `presentations` |  |
| Art / Media | `welcome/marketing/art-media` | Marketing | P | 59 | Art and media assets: the Future Traveler art repo and rpg-character avatar component. | grid-plate, media-image, rpg-character | `traveler`, `presentations`, `components` |  |
| Testimonials | `welcome/marketing/testimonials` | Marketing | P | 174 | Testimonials, chiefly the Customer Discovery 101 team describing building their course with HAX. | block-quote | `presentations`, `course` |  |
| HiTech Podcast: HAX Explained and Shown | `marketing/hitech-podcast-interview` | Marketing | P | 590 | Segmented HiTech podcast episode 168 (Oct 2024) where Bryan explains and demos HAX, with timestamped videos. | grid-plate, page-anchor, video-player | `presentations`, `bryan`, `wcstandard` |  |
| White papers | `documentation/white-papers` | Marketing | P | 60 | List of white papers from HAX and ELMS:LN eras (2014, 2015, 2018). |  | `presentations`, `elmsln` | papers are 2014-2018; no links to the files in text |
| I need help! | `welcome/i-need-help` | Welcome | P | 60 | Help page: file issues in the unified queue, chat on Discord, or type 'issues' in Merlin. | media-image | `issues`, `merlin` |  |

### Tutorials (34 pages, 2,476 words)

| title | slug | parent | status | words | summary | elements | mapped nodes | flags |
|---|---|---|---|---|---|---|---|---|
| Instructional | `tutorials/block-usage/instructional` | Block usage | P | 11 | Section stub introducing instructional blocks. |  | `components`, `course` | near-empty section page |
| Math | `tutorials/block-usage/instructional/math` | Instructional | P | 64 | Math block: inline LaTeX/MathML via lrn-math with an example and video. | grid-plate, lrn-math, media-image, video-player | `components`, `course` |  |
| Question types | `tutorials/block-usage/question-types` | Instructional | P | 10 | Section stub listing formative assessment question-type blocks. | site-collection-list | `components`, `course` | near-empty section page |
| Fill in the blanks | `tutorials/block-usage/instructional/question-types/fill-in-the-blanks` | Question types | P | 82 | Fill-in-the-blanks question: bracket syntax for answers, alternates and select options; install/source links. | code-sample, fill-in-the-blanks | `components`, `course` |  |
| Mark the Words | `tutorials/block-usage/instructional/question-types/mark-the-words` | Question types | P | 54 | Mark-the-words question where users select words in a sentence, with per-word feedback. | code-sample, mark-the-words | `components`, `course` |  |
| Matching / Drag and drop | `tutorials/block-usage/instructional/question-types/matching-drag-and-drop` | Question types | P | 58 | Matching / drag-and-drop question with multi-answer targets and distractors. | code-sample, matching-question | `components`, `course` |  |
| Multiple choice | `tutorials/block-usage/instructional/question-types/multiple-choice` | Question types | P | 66 | Multiple choice comprehension check with example and video; no data stored. | code-sample, grid-plate, multiple-choice, video-player | `components`, `course` |  |
| Short Answer Question | `tutorials/block-usage/instructional/question-types/short-answer-question` | Question types | P | 37 | Short answer question allowing multiple accepted single-word answers. | code-sample, short-answer-question | `components`, `course` |  |
| Sorting Question | `tutorials/block-usage/instructional/question-types/sorting-question` | Question types | P | 83 | Sorting question for ordering items with randomized retries and feedback. | code-sample, sorting-question | `components`, `course` |  |
| Tagging question | `tutorials/block-usage/instructional/question-types/tagging-question` | Question types | P | 51 | Tagging question where users select only correct tags among distractors. | code-sample, tagging-question | `components`, `course` |  |
| True false question | `tutorials/block-usage/instructional/question-types/true-false-question` | Question types | P | 40 | True/false question block bundled in the multiple-choice package. | code-sample, true-false-question | `components`, `course` |  |
| Self check | `tutorials/block-usage/instructional/self-check` | Instructional | P | 82 | Self-check block: image plus reflective question with click-to-reveal answer. | self-check, video-player | `components`, `course` |  |
| Stop note | `tutorials/block-usage/instructional/stop-note` | Instructional | P | 93 | Stop-note block for emphasizing critical information, with video. | stop-note, video-player | `components` |  |
| Table | `tutorials/block-usage/instructional/table` | Instructional | P | 63 | Editable table block for authoring tabular data without HTML knowledge. | editable-table, video-player | `components`, `accessible` |  |
| Timeline | `tutorials/block-usage/instructional/timeline` | Instructional | P | 42 | Timeline block for presenting events in sequence. | lrndesign-timeline, video-player | `components` |  |
| 3D Model | `tutorials/block-usage/multimedia/3d-model` | Multimedia | P | 44 | 3D Model block using model-viewer, including AR display. | model-viewer, video-player | `components` |  |
| First-time HAX User | `tutorials/brand-new-user` | Tutorials | P | 39 | First-time user tutorial video with a downloadable working document. | video-player | `learnhax`, `editor` |  |
| Collection List | `tutorials/block-usage/layout/collection-list` | Layout | P | 30 | Collection list block for presenting items as cards. | collection-item, collection-list | `components` |  |
| Column layout | `tutorials/block-usage/layout/column-layout` | Layout | P | 106 | Column layout (grid-plate) block for side-by-side content. | grid-plate, media-image, video-player | `components`, `ddd` |  |
| Block usage | `tutorials/block-usage` | Tutorials | P | 101 | Block usage catalog grouping documented block tutorials by category. |  | `components`, `learnhax` |  |
| Multimedia | `tutorials/block-usage/multimedia` | Block usage | P | 10 | Section stub for multimedia blocks. |  | `components` | near-empty section page |
| GIF player | `tutorials/block-usage/multimedia/gif-player` | Multimedia | P | 160 | Accessible GIF player that stops auto-play to reduce motion issues. | a11y-gif-player, grid-plate | `components`, `accessible` |  |
| Inline audio | `tutorials/block-usage/multimedia/inline-audio` | Multimedia | P | 102 | Inline audio block that highlights text while audio plays. | inline-audio, video-player | `components` |  |
| Video player | `tutorials/block-usage/video-player` | Multimedia | P | 61 | Video player block: YouTube/Vimeo/mp4, VTT captions and transcripts, a11y colors. | video-player | `components`, `accessible` |  |
| Media playlist | `tutorials/block-usage/multimedia/media-playlist` | Multimedia | P | 23 | Media playlist container with sidebar for video and audio. | media-playlist, video-player | `components` |  |
| Image gallery | `tutorials/block-usage/multimedia/image-gallery` | Multimedia | P | 24 | Image gallery block with grid, masonry and lightbox layouts. | image-gallery | `components` |  |
| Layout | `tutorials/block-usage/layout` | Block usage | P | 9 | Section stub for layout blocks. | site-collection-list | `components` | near-empty section page |
| Learning Component | `tutorials/block-usage/layout/page` | Layout | P | 144 | Learning Component block for flagging course activities (discussion, reading, etc.). | learning-component | `components`, `course` |  |
| Play list | `tutorials/block-usage/layout/play-list` | Layout | P | 20 | Play list block: slider/slideshow of images and blocks. | play-list | `components` |  |
| Tutorials | `tutorials` |  | P | 46 | Tutorials landing page with a full YouTube tutorial playlist. |  | `learnhax`, `flows` | links to elmsln/issues (moved to haxtheweb/issues) |
| Migrate data to HAX | `tutorials/migrate-data-to-hax` | Tutorials | P | 538 | Migration paths into HAX: DOCX, HAX-to-HAX, Notion, and other JOS-producing sources, with videos. | stop-note, video-player, worksheet-download | `importers`, `jos`, `remixable` |  |
| Managing Course Structure | `tutorials/page-1` | Tutorials | P | 33 | Short description of the outline designer for bulk outline management. |  | `haxcms`, `dashboard`, *outlinedesigner* NEW | very thin for a mission-critical tool |
| Reports | `tutorials/insights-dashboard` | Tutorials | P | 24 | Reports (beta) such as automated link checking, with video. | video-player | `dashboard` | labelled beta; verify current state |
| Changelog | `tutorials/changelog` | Tutorials | P | 126 | Changelog pointing to release feeds for each ecosystem repo. |  | `github`, `npm`, `issues` |  |

### Documentation (50 pages, 16,445 words)

| title | slug | parent | status | words | summary | elements | mapped nodes | flags |
|---|---|---|---|---|---|---|---|---|
| HAXElement Schema | `documentation/developers/schema/haxelement-schema` | Schema | P | 181 | Documents HAXElement Schema, the JSON abstraction of HTML elements used for templates, demoSchema and sanitizing. | code-sample | `haxschema`, `editor` |  |
| BackdropCMS | `documentation/integrations/backdropcms` | Integrations | P | 74 | Steps to install HAX in BackdropCMS via the Web components and HAX modules. |  | *cmsintegrations* NEW, `agnostic` |  |
| ELMS:LN | `documentation/elmsln` | Deprecated | P | 304 | Deprecated ELMS:LN overview: still used internally, but HAX/HAXcms are its successors. | stop-note | `elmsln` | deprecated project page; elmsln.org http link may be dead |
| example-hax-element | `documentation/developers/hax/example-hax-element` | HAXEditor | P | 305 | Walks through the example-hax-element source to show haxProperties and DDD wiring for a block. | code-sample | `haxschema`, `components`, `ddd` |  |
| apps | `documentation/developers/hax/app-store-api/apps` | App store API | P | 459 | Annotated App Store definition for the Flickr integration, explaining each field. | code-sample | `appstore` |  |
| Design Documentation | `documentation/ddd` | Frontend developers | P | 551 | DDD design documentation: Develop/Design/Destroy philosophy and the in-progress design system docs element. | d-d-docs | `ddd`, `design` |  |
| HAX11ty | `documentation/hax11ty` | Tools | P | 125 | HAX11ty: editing Markdown locally, building with 11ty into a valid HAXcms site package. |  | `hax11ty` |  |
| The Core | `ontology/page-5` | HAX Ontology | P | 70 | Ontology core: the six branches Outcomes, Pedagogy, Structure, Instruction, Content, Assessment. | simple-tags, video-player | *ontology* NEW, `course` |  |
| HAXiam | `documentation/developers/platforms/haxiam` | Platforms | P | 528 | HAXiam install scripts and organization-wide shared skeletons with resolution order and git workflow. |  | `haxiam`, `skeletons`, `php` |  |
| Platforms | `documentation/developers/platforms` | Developers | P | 10 | Section stub for platform-level developer docs. |  | `haxcms` | near-empty section page |
| HAXcms | `documentation/developers/platforms/haxcms` | Platforms | P | 213 | HAXcms as a UI-driven, static-output microsite generator, with key terminology. | media-image | `haxcms`, `php`, `nodejs` |  |
| HAXsite | `documentation/developers/platforms/haxsite` | Platforms | P | 454 | HAXsite folder anatomy: site.json, pages/, files/, custom/, build.js magic script, SCORM ims files. |  | `haxcms`, `jos`, `staticpub` |  |
| Frontend developers | `documentation/hax-frontend-devs` | Documentation | P | 625 | Front-end dev intro: magic script, CLI quick start, web component workshop, CodePen of h-a-x, HAXSchema pointers. | code-sample | `components`, `cli`, *haxcloud* NEW | links to elmsln/lrnwebcomponents (renamed to haxtheweb/webcomponents); links to elmsln/wc-workshop; links to old haxtheweb.org/documentation-1/... paths; haxapi.vercel.app link may be stale |
| Implementing DDD | `documentation/hax-frontend-devs/implementing-ddd` | Frontend developers | P | 358 | How to install and extend DDD (d-d-d) as a Lit base class with global and local styles. | code-sample | `ddd`, `components` | DDDStyles link points to elmsln/lrnwebcomponents (renamed) |
| Data store | `documentation/developers/haxsite/data-store` | HAXSite | P | 1086 | Documents the HAXsite/HAXeditor MobX stores and their observable/computed properties. | code-sample, simple-icon-lite, stop-note, true-false-question | `haxcms`, `editor`, `themes` | self-described as possibly out of date |
| Classicpress | `documentation/integrations/classicpress` | Integrations | P | 57 | Installing HAX into ClassicPress via the WordPress plugin, with video. | video-player | *cmsintegrations* NEW, `agnostic` |  |
| Outcomes | `ontology/page` | HAX Ontology | P | 53 | Ontology Outcomes branch: course goals and objectives. | video-player | *ontology* NEW, `course` |  |
| WCFactory | `documentation/wcfactory` | Deprecated | P | 163 | Deprecated WCFactory page: former monorepo tooling, superseded by the HAX CLI. | stop-note, video-player | drop (WCFactory deprecated) | deprecated tooling; uses old 'npm init @haxtheweb'; links elmsln/wcfactory, elmsln/lrnwebcomponents, webcomponents.org (retired); mentions Yarn/Lerna |
| Developers | `documentation/developers` | Documentation | P | 224 | Developer hub: contributing to the webcomponents monorepo, CLI for new components, backend repos. |  | `components`, `cli`, `github` | yarn-based contribution steps may be outdated |
| Tools | `documentation/developers/tools` | Developers | P | 10 | Section stub listing developer tools. | site-collection-list | `cli` | near-empty section page |
| @haxtheweb/create | `documentation/developers/tools/create` | Tools | P | 36 | @haxtheweb/create (HAX CLI) intro with repo/npm links. |  | `cli`, `npm` |  |
| WCFactory | `documentation/developers/tools/wcfactory` | Tools | P | 83 | Second WCFactory page under Tools, recommending the HAX CLI instead. |  | drop (WCFactory deprecated) | duplicate of deprecated WCFactory content; links haxtheweb/wcfactory |
| Data formats | `documentation/data-formats` | Developers | P | 437 | Canonical list of authoring/import formats, accepted uploads, and alternate formats generated per save. |  | `importers`, `staticpub`, `haxcms` |  |
| Schema | `documentation/developers/schema` | Developers | P | 0 | Empty Schema section page. |  | `haxschema`, `jos` | empty page (0 words) |
| HAXSchema | `documentation/developers/schema/haxschema` | Schema | P | 1094 | Implementing haxProperties/HAXSchema: booleans, design-system flags, gizmo, settings and demoSchema. | code-sample | `haxschema`, `editor`, `components` |  |
| JSON Outline Schema | `documentation/developers/schema/json-outline-schema` | Schema | P | 24 | JSON Outline Schema page that renders the spec README from GitHub via md-block. | md-block | `jos` | content depends on remote README render |
| OER Schema | `documentation/oer-schema` | Schema | P | 2508 | Long OER Schema explainer: pedagogical vocabulary extending schema.org and how HAX blocks emit it. |  | `oerschema` | many http:// namespace URIs (expected for RDF) |
| OpenAPI | `documentation/developers/schema/openapi` | Schema | P | 28 | Points to the HAXcms OpenAPI spec in the haxcms-nodejs repo. |  | `openapi`, `nodejs` |  |
| HAXEditor | `documentation/developers/hax` | Developers | P | 104 | HAXEditor developer section intro: i18n, haxProperties, hooks, app store. | site-collection-list | `editor`, `haxschema` |  |
| haxHooks | `documentation/developers/hax/haxhooks` | HAXEditor | P | 976 | haxHooks lifecycle callbacks that let elements supply their own editing behavior, with code links. | code-sample | `editor`, `haxschema`, `extensible` |  |
| Internationalization - i18n | `documentation/developers/hax/internationalization-i18n` | HAXEditor | P | 286 | Adding i18n to any web component using I18NMixin and locale JSON files. | code-sample | `languages`, `components` |  |
| App store API | `documentation/developers/hax/app-store-api` | HAXEditor | P | 183 | App Store API overview: apps, stax, blox and autoloader sections. |  | `appstore` |  |
| stax | `documentation/developers/hax/app-store-api/stax` | App store API | P | 718 | Stax templates: sequences of HAXElement schema with a full example lesson. | code-sample | `appstore`, `haxschema` |  |
| autoloader | `documentation/developers/hax/app-store-api/autoloader` | App store API | P | 399 | App store autoloader: how HAX loads element definitions after bootstrap. | code-sample | `appstore`, `editor` |  |
| HAXSite | `documentation/developers/haxsite` | Developers | P | 92 | HAXsite developer section intro: site as a folder, editable when HAXcms is present. | site-collection-list | `haxcms`, `themes` |  |
| Custom theme development | `documentation/developers/haxsite/custom-theme-development` | HAXSite | P | 806 | Custom theme development with the HAX CLI, importmaps, and HAXCMSLitElementTheme. | code-sample | `themes`, `cli` | example links to btopro personal repo and a surge demo |
| Theme blocks | `documentation/developers/theme-blocks` | HAXSite | P | 933 | Catalog of haxcms-elements theme building blocks (active item, menus, regions, query, magic). | code-sample, media-image | `themes`, `components` |  |
| Deprecated | `documentation/developers/legacy-projects` | Developers | P | 0 | Empty 'Deprecated' section parent (holds ELMS:LN and WCFactory). |  | `elmsln` | empty page (0 words) |
| Pedagogy | `ontology/new-item` | HAX Ontology | P | 35 | Ontology Pedagogy branch with intro video. | simple-tags, video-player | *ontology* NEW, `course` |  |
| Documentation | `documentation` |  | P | 70 | Documentation landing page with section listing and request-for-improvements note. | site-collection-list, stop-note | `learnhax` | mentions wcfactory.js.org (deprecated) |
| Integrations | `documentation/haxcms/integrations` | Documentation | P | 493 | Integration methodology via the magic script, unbundled-webcomponents, and a WordPress code sample. | code-sample | *cmsintegrations* NEW, `agnostic`, *haxcloud* NEW | links elmsln/hax-all-the-things (old org) |
| Drupal | `documentation/haxcms/integrations/drupal` | Integrations | P | 269 | Installing HAX in Drupal 6-9 including SimplyTest.me trial. |  | *cmsintegrations* NEW, `agnostic`, `drupalcon` | covers Drupal 6/7/8/9 only (EOL versions; no 10/11) |
| GravCMS | `documentation/integrations/gravcms` | Integrations | P | 77 | Installing HAX in GravCMS via web components and HAX plugins. |  | *cmsintegrations* NEW, `agnostic` | plugins under elmsln org (possibly unmaintained) |
| Wordpress | `documentation/integrations/wordpress` | Integrations | P | 61 | Installing HAX in WordPress with the Classic Editor plugin. |  | *cmsintegrations* NEW, `agnostic` | requires Classic Editor; verify plugin still current |
| HAX Ontology | `ontology` | Documentation | P | 267 | HAX course ontology overview with tour video and Mural board. | media-image, simple-tags, video-player | *ontology* NEW, `course` | Mural board link may require access |
| Structure | `ontology/page-1` | HAX Ontology | P | 39 | Ontology Structure branch: units, lessons, sub-lessons. | simple-tags, video-player | *ontology* NEW, `course` |  |
| Instruction | `ontology/page-3` | HAX Ontology | P | 50 | Ontology Instruction branch: Adler's modes and learning progression. | a11y-media-play-button, a11y-media-player, simple-tags, video-player | *ontology* NEW, `course` |  |
| Content | `ontology/page-2` | HAX Ontology | P | 57 | Ontology Content branch: classifying content by structure and learner progress. | simple-tags, video-player | *ontology* NEW, `course` |  |
| Assessment | `ontology/page-4` | HAX Ontology | P | 34 | Ontology Assessment branch by stakes level. | simple-tags, video-player | *ontology* NEW, `course` |  |
| Text Schema | `documentation/ontology/text-schema` | HAX Ontology | P | 436 | Text hierarchy of the ontology (UbD, WHERETO, six facets) for LLM use. |  | *ontology* NEW, `course`, `ai` |  |

### Solutions (8 pages, 1,154 words)

| title | slug | parent | status | words | summary | elements | mapped nodes | flags |
|---|---|---|---|---|---|---|---|---|
| Desktop | `solutions/desktop` | Solutions | P | 41 | HAX Desktop: Electron packaging of the Node version, currently Ubuntu-oriented. |  | *desktop* NEW, `nodejs` | possibly stale; verify desktop repo is maintained |
| Installing HAXcms | `installation` | HAXcms | P | 118 | How to install HAXcms via npx/CLI for Node and manual PHP or Reclaim Hosting. | code-sample, video-player | `haxcms`, `nodejs`, `php`, `reclaim` |  |
| HAXcms | `documentation/haxcms` | Solutions | P | 91 | HAXcms solution overview: databaseless site.json, themes, HAX editor, portable remixable sites. |  | `haxcms`, `jos`, `remixable` |  |
| Deploying HAXcms | `documentation/deploying-haxcms` | HAXcms | P | 612 | Deploying HAXcms sites: static per save, magic script CDN fallback order, and serving assets locally. |  | `deploy`, `staticpub`, *haxcloud* NEW |  |
| HAXiam | `solutions/haxiam` | Solutions | P | 146 | HAXiam solution overview: multi-user PaaS/SaaS on HAXcms PHP with enterprise login. |  | `haxiam`, `php` | links github.com/elmsln/HAXiam (old org) |
| HAXSite | `solutions/haxsite` | Solutions | P | 68 | HAXsite as a standalone site and a starter repo, publishing via GitHub + StackBlitz. | video-player | `haxcms`, `deploy`, `github` |  |
| Solutions | `solutions` |  | P | 5 | Solutions section landing page. | site-collection-list | `ubiquity` | near-empty section page |
| @haxtheweb/h-a-x | `solutions/h-a-x` | Solutions | P | 73 | h-a-x standalone editor tag and its integrations/storybook. | code-sample | `editor`, `agnostic` |  |

### HAX Lab (12 pages, 1,962 words)

| title | slug | parent | status | words | summary | elements | mapped nodes | flags |
|---|---|---|---|---|---|---|---|---|
| Conversion tools | `stand-alone-tools/conversion-tools` | Stand alone tools | P | 65 | Microservice-based converters: DOCX to HTML/PDF, Markdown to/from HTML, image compression, screenshots, secure feedback. |  | *haxcloud* NEW, `importers`, *standalone* NEW |  |
| Stand alone tools | `stand-alone-tools` | The Future | P | 44 | Section page for stand-alone tools spun off from HAX infrastructure. |  | *standalone* NEW |  |
| Local Save | `the-future/stand-alone-tools/local-save` | Stand alone tools | P | 27 | Stand-alone HAX page that reads/writes a local file (Chrome only). |  | *standalone* NEW, `editor` | links haxtheweb.org/assets/local-save.html, which may disappear when the site is replaced |
| Qualitative Rubric Prototype | `stand-alone-tools/rubrics` | Stand alone tools | P | 53 | Qualitative rubric prototype for faster LMS feedback, derived from ELMS work. |  | *standalone* NEW, `course`, `elmsln` |  |
| Course Model Player | `page` | Stand alone tools | P | 277 | Course Model Player demo showing a 3D Colt 1911 model with info hotspots and video. | course-model, media-image, model-info, video-player | *standalone* NEW, `components`, `eberly` | assets hosted under elmsln/lrnwebcomponents raw URLs (repo renamed); embeds media.ed.science.psu.edu H5P iframe |
| Keycloak authentication | `stand-alone-tools/page` | Stand alone tools | P | 101 | Headless Keycloak authentication service demo built by Andrew Maier. |  | *standalone* NEW, `security`, `andrew` | demo on keycloak-login.vercel.app; repo under btopro personal account |
| HAX YouTube Channel | `hax-lab/hax-youtube-channel` | HAX Lab | P | 38 | Points to the official HAX YouTube channel and an embedded dev playlist. | iframe-loader | `presentations`, `learnhax` |  |
| HAX The Whole Web | `hax-the-whole-web` | HAX Lab | P | 212 | HAX The Whole Web: 5-step process for contributing use-case skeletons via tagged issues. |  | `skeletons`, `issues`, *community* NEW |  |
| Student Innovation Pipeline | `hax-lab/student-innovation-pipeline` | HAX Lab | P | 244 | Student innovation pipeline from IST 256 / HAX The Club into HAX Lab internships and PSU web work. | grid-plate, media-image | `haxlab`, `ist256`, `ist` |  |
| HAX AI | `hax-lab/hax-ai` | HAX Lab | P | 50 | Penn State Data Summit 2025 talk on AI with HAX, including teaching Claude the HAX CLI. | iframe-loader | `ai`, `agents`, `fusco`, `presentations` | Kaltura embed (PSU-hosted) |
| The Future | `the-future` | HAX Lab | P | 180 | HAX Horizon Reports concept and the October 2023 horizon video. | media-image, video-player | `traveler`, `wcstandard`, `presentations` | latest horizon report is Oct 2023 |
| HAX Lab | `hax-lab` |  | P | 671 | HAX Lab: faculty sponsors, how students join, and student contributors. | github-rpg-contributors, grid-plate, rpg-character | `haxlab`, `bryan`, `fusco` |  |

### Gallery of Online Excellence (18 pages, 10,758 words)

| title | slug | parent | status | words | summary | elements | mapped nodes | flags |
|---|---|---|---|---|---|---|---|---|
| Planning the Lecture | `planning-the-lecture` | In Brief: A Sound Process | P | 1558 | Gallery guideline page on planning an educational lecture video: objectives, strategy fit, accessibility, copyright, citation. | block-quote, grid-plate | *gallery* NEW, `course`, `design` | Gallery content imported from iam.hax.psu.edu/bmr1/sites/haxcellence |
| Peter Aeschbacher Exhibit | `peter-aeschbacher-exhibit` | Gallery Exhibits | P | 1117 | Gallery exhibit analyzing Peter Aeschbacher's AA 121 green-screen lecture videos against the guidelines. | a11y-collapse, block-quote, editable-table, grid-plate, media-image, page-anchor, video-player | *gallery* NEW, `aa` | contains 'Content goes here.' placeholder text |
| Effective Educational Video | `effective-educational-video` | Gallery of Online Excellence | P | 382 | Introduction and recommended path through the Effective Educational Video exhibit. | grid-plate, video-player | *gallery* NEW, `course` | internal links point to iam.hax.psu.edu/bmr1/sites/haxcellence (source site), not this site |
| In Brief: Design Guidelines and Principles | `design-guidelines-and-principles` | Effective Educational Video | P | 1110 | Summary of Brame's research on effective educational video: cognitive load, engagement, active learning. | block-quote, grid-plate, media-image | *gallery* NEW, `course` | internal links point to iam.hax.psu.edu/bmr1 source site |
| Follow Cognitive Load Theory | `the-gallery-of-online-excellence/effective-educational-video/in-short-a-sound-process/planning-the-lecture-copy` | In Brief: Design Guidelines and Principles | P | 716 | Video guidelines grounded in cognitive load theory: signaling, segmenting, weeding, matching modalities. | block-quote | *gallery* NEW, `course` | slug '...planning-the-lecture-copy' does not match title |
| Foster Student Engagement | `foster-student-engagement` | In Brief: Design Guidelines and Principles | P | 513 | Video engagement guidelines: keep videos short, conversational, enthusiastic. | block-quote, grid-plate, media-image | *gallery* NEW, `course` | contains 'aaa bbb ccc' placeholder text |
| Design for Active Learning | `the-gallery-of-online-excellence/effective-educational-video/design-guidelines-and-principles/foster-student-engagement-copy` | In Brief: Design Guidelines and Principles | P | 701 | Active-learning guidelines: package video with interactive questions and guiding prompts. | block-quote | *gallery* NEW, `course` | slug '...foster-student-engagement-copy' does not match title |
| In Brief: A Sound Process | `in-short-a-sound-process` | Effective Educational Video | P | 775 | Summary of research guidelines for recording slide-based lectures, linking to planning/content/recording pages. | block-quote, grid-plate, media-image | *gallery* NEW, `course` | internal links point to iam.hax.psu.edu/bmr1 source site |
| Creating Content and Slides | `creating-content-and-slides` | In Brief: A Sound Process | P | 1081 | Guidelines for creating lecture content and slides: compelling intros, visuals, pacing. | block-quote | *gallery* NEW, `course`, `design` |  |
| Recording the Video | `recording-the-video` | In Brief: A Sound Process | P | 695 | Guidelines for recording lecture video: voice, presence, audio quality, delivery. | block-quote | *gallery* NEW, `course` |  |
| Gallery Exhibits | `gallery-exhibits` | Effective Educational Video | P | 180 | Explains what a faculty exhibit contains and links to the three exhibits. | collection-item, grid-plate | *gallery* NEW, `aa` | exhibit links point to iam.hax.psu.edu/bmr1 source site |
| Bonj Szczygiel Exhibit | `bonj-szczygiel-exhibit` | Gallery Exhibits | P | 908 | Exhibit analyzing Bonj Szczygiel's LARCH 60 narrated PowerPoint lectures. | a11y-collapse, editable-table, grid-plate, media-image, page-anchor, stop-note, video-player | *gallery* NEW, `aa` | embeds media.aanda.psu.edu entity_iframe (may require PSU access) |
| Ben Andrew Exhibit | `ben-andrew-exhibit` | Gallery Exhibits | P | 946 | Exhibit analyzing Ben Andrew's DART 100 FigJam-canvas video lectures. | a11y-collapse, grid-plate, media-image, page-anchor, video-player | *gallery* NEW, `aa` |  |
| Providing Quality Feedback | `providing-quality-feedback` | Gallery of Online Excellence | P | 0 | Empty Gallery placeholder for providing quality feedback. |  | *gallery* NEW | empty page (0 words) |
| Study Guide Approaches | `study-guide-approaches` | Gallery of Online Excellence | P | 0 | Empty Gallery placeholder for study guide approaches. |  | *gallery* NEW | empty page (0 words) |
| Guided Practice | `guided-practice` | Gallery of Online Excellence | P | 0 | Empty Gallery placeholder for guided practice. |  | *gallery* NEW | empty page (0 words) |
| ODL Course Showcase | `odl-course-showcase` | Gallery of Online Excellence | P | 0 | Gallery placeholder holding only an ODL course showcase video. | video-player | *gallery* NEW, `course` | no text (0 words) |
| Gallery of Online Excellence | `the-gallery-of-online-excellence` |  | P | 76 | Gallery of Online Excellence landing: research-based faculty resources shown through exemplars. | collection-item, collection-list | *gallery* NEW, `course` |  |

### AI integration (1 pages, 177 words)

| title | slug | parent | status | words | summary | elements | mapped nodes | flags |
|---|---|---|---|---|---|---|---|---|
| AI integration | `ai-integration` |  | ? | 177 | AI agent integration: installing hax skills or the PRAW Claude Code marketplace plugins and the golden path to a running site. |  | `agents`, `ai`, `praw`, `cli` | top-level page with no published metadata (published unset) |

### Site things (4 pages, 114 words)

| title | slug | parent | status | words | summary | elements | mapped nodes | flags |
|---|---|---|---|---|---|---|---|---|
| Header | `site-things/header` | Site things | P | 0 | Site header graphic (PSU logo link); site chrome, not documentation. | media-image | `themes`, `psu` | site chrome, zero words |
| Footer | `site-things/footer` | Site things | P | 101 | Site footer mission statement with PSU college logos; site chrome. | grid-plate | `human`, `psu` | site chrome |
| Footer - bottom | `site-things/footer-bottom` | Site things | P | 13 | Bottom footer with PSU copyright and policy links; site chrome. |  | `psu` | site chrome; copyright 2024; http:// PSU policy links |
| Site things | `site-things` |  | U | 0 | Unpublished container for site chrome pages (header/footer). |  | `themes` | unpublished; empty page (0 words) |


---
Count check: 156 table rows = 156 site.json items.
