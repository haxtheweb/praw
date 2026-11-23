# Ecosystem maps

Data that ties the HAX ecosystem web to the evidence and skills behind it. Each file uses the ecosystem web's node keys (`human`, `praw`, `oerschema`, `accessible` and so on), so the web can draw these links and a node's detail page can list them. The web itself is tracked in [haxtheweb/issues#3173](https://github.com/haxtheweb/issues/issues/3173).

| File | What it maps |
| --- | --- |
| [`heosat-evidence-map.json`](heosat-evidence-map.json) | Every HEOSAT question to the nodes and public files that answer it, with a status: evidenced, partial or gap. |
| [`id-skills-map.json`](id-skills-map.json) | Each instructional design skill in `skills/` to the elements it recommends or checks, the pillars it upholds and its nodes. |
| [`docs-inventory.json`](docs-inventory.json) · [`.md`](docs-inventory.md) | All 156 pages of haxtheweb/docs, each with a summary, its elements, stale-link flags and the web nodes it maps to, so nothing is lost when the ecosystem web replaces haxtheweb.org. |

The JSON files are the source; this page summarizes them. Statuses and pillar links are a self-assessment for maintainer review, not a HEOSAT score.

## The web

The ecosystem web itself lives here too: every sub-web's structure and details, the generators that build them from source, and the player that turns them into one page.

| Folder | What's in it |
| --- | --- |
| [`web/`](web) | One `.mmd` and `.json` pair per sub-web (`hax-ecosystem` is the main web), plus `gap-answers.json`, the answers that filled the main web's gaps. These are the source of truth. |
| [`build/`](build) | The generators (`build_*.py`), `drift.py`, `graph-drift.mjs`, `assemble.py`, `sources.sh` and `run.sh`. `site.sh` builds hax.cloud from them: `build_site.py` writes the pages and `build_recent.py` adds recent activity. |
| [`build/data/`](build/data) | Extracts the generators read that don't come from a repo checkout: where a tile's code lives (`concept-code.json`), MCP tools, xAPI verbs, field and Merlin usage, OER Schema, the release script, the HAX Lab README, layer data and a hax.psu.edu snapshot with site owners removed. |
| [`player/`](player) | The page template and the icons, image and mascot it embeds. |
| [`test/`](test) | `integrity-check.py` (the rules below; standard library Python), `parse-check.js` (every web parses with no errors and every icon is in the inlined set) and `layout-check.js` (no overflow at desktop and phone widths). The last two need Playwright (`npm ci` in `test/`). `recent-check.py` checks the recent activity step with no network, and `tutorial-review-check.py` the tutorials-to-review list. |

### Data format

- **Structure (`.mmd`)**: a plain Mermaid flowchart that renders on GitHub, plus `%%@` lines the player reads: `layout rings=… sizes=…`, `group <subgraph> tier=N`, `node <id> icon=<set:name> color=<DDD color> motion=<name>`, `node <id> portal` (the same node in another web; `portal=<web>` when that web isn't the main one) and `web=<id>` (the tile opens that sub-web).
- **Details (`.json`)**: `{meta, nodes, evidence, tours}`. `meta.parent` names the web a sub-web opens from, for the breadcrumbs. A node holds `desc`, `status`, `kind`, `links` and `release` (`npm:@haxtheweb/…` or `git:haxtheweb/…`, read by `graph-drift.mjs`). Statuses: released, prerelease, in-progress, planned, legacy, living, deployed and gap. Planned tiles render ghosted with dashed lines and link to their issue; gap tiles (something an evidence or coverage map says is missing) render ghosted with a dotted line and a "Gap" label. A tour is `{id, label, message, scenes: [{caption, nodes}]}`.

### Checks

Three checks run on pull requests and fail them when a web breaks:

- **Integrity** (`python3 -I ecosystem/test/integrity-check.py`, on every pull request): every tile has a title and sits in a subgraph, which is its type; connections, annotations, details, evidence and tours name tiles that exist; a portal's tile exists in the web it comes from and a `web=` tile opens a web that exists; the main web's pillars are the seven in [`build/data/pillars.json`](build/data/pillars.json) with their icon and color; every tile in the main web reaches a pillar along its connections without passing through the center; every sub-web is opened by a tile and its `meta.parent` chain leads back to the main web; and no tile is an orphan. In a sub-web a tile may stand alone only as a gap (`status: "gap"`), as a portal, or when [`test/integrity-allow.json`](test/integrity-allow.json) names it with a reason.
- **Parse and layout** (`parse-check.js`, `layout-check.js`, on pull requests that touch `ecosystem/`): the assembled page read by the player itself, in a browser.
- **hax.cloud** (on pull requests that touch `ecosystem/`): the site still builds with `build/site.sh`.

Once a week `run.sh` runs in full on GitHub and reports what the generators changed in the run's summary ([`build/drift_report.py`](build/drift_report.py)). It is report only: it writes nothing to the repository. The changed files are kept for a week as the run's `ecosystem-drift` artifact; to take them, run `run.sh` locally and open a pull request.

### Addresses

On hax.cloud, webs and tours have readable paths (`/penn-state/strategic-plan`, `/tours/follow-one-piece-of-content`) and every tile's page is at `/stories/<address>`, for example `/stories/ee450a19`. This is the link to share or embed: the address comes from the tile's key (its web and node id), not its label, so it holds when a tile, or the person it names, is renamed. The interactive web puts the same path in the address bar as the viewer moves around.

- The path a tile's label gives it (`/ecosystem/james-kane-iv`) still answers, as a page that forwards to the address. It follows the current label, so after a rename the old name's path is gone and nothing stores it.
- When a node id or the web that owns a tile has to change, keep its address by adding the new key to [`site/addresses.json`](site/addresses.json): `{"tile:<web>:<new id>": "<address>"}`. `slugs.json` on the live site lists every key and its path.
- Two tiles can't share an address: the build stops and asks for a pin.
- Where a page sits in the site outline (Organizations > Penn State, Courses > IST > IST 256) is set in [`site/categories.json`](site/categories.json) and never changes its address; see [`site/pages/README.md`](site/pages/README.md).

### Recent activity

hax.cloud/recent lists the latest merged pull requests, releases and new issues across the HAX repositories, and a repository's own tile page (HAXcms PHP, PRAW, the CLI) lists its own merges and releases. [`build/build_recent.py`](build/build_recent.py) reads them from the public GitHub REST API while the site builds and publishes the snapshot as `recent.json`; nothing on the site calls GitHub.

- The repositories are the ones the webs name (a tile's `repo` link or `release: git:…`) plus each property's `repo` in `network.json`. A new tile with a `repo` link gets its activity with no other change.
- The build needs no account. Without one GitHub allows 60 requests an hour from one address, and a build makes about two per repository; a `GITHUB_TOKEN` in the build's environment raises that and is never written to the site.
- When GitHub can't be read, each list it would not give is kept from the last published snapshot (hax.cloud/recent.json). With no snapshot either, the page says there is nothing to show. The step never fails the build.
- The lists are as fresh as the last build: the site builds when PRAW's `main` changes.

### Tutorials to review when code changes

The tutorials web says what each Learn HAX tutorial teaches, and a tile says where its code lives: its repo, code, source or docs link on GitHub, or its entry in [`build/data/concept-code.json`](build/data/concept-code.json) when its links point at npm or a site. [`build/tutorial_review.py`](build/tutorial_review.py) joins the two, so a change to code names the tutorials, and screencasts, to look at again ([haxtheweb/issues#2946](https://github.com/haxtheweb/issues/issues/2946)):

```bash
python3 -I ecosystem/build/tutorial_review.py webcomponents:elements/super-daemon/super-daemon.js   # Slash Commands, and its screencast
python3 -I ecosystem/build/tutorial_review.py --since "7 days ago"   # everything changed in the clones in ecosystem/.work
python3 -I ecosystem/build/tutorial_review.py --map                  # every taught tile, its code and its tutorials
```

It also lists the taught tiles with no code on record, which is where to add a link or an entry. `python3 -I ecosystem/test/tutorial-review-check.py` checks it.

### Build it

```bash
ecosystem/build/run.sh                  # fetch sources, rerun every generator, report drift, assemble the page
ecosystem/build/run.sh build_json.py    # rerun one generator (the main web), then assemble
ecosystem/build/run.sh --assemble       # assemble only, from web/ as it stands
python3 -I ecosystem/test/integrity-check.py   # the integrity rules, no browser needed
node ecosystem/test/parse-check.js ecosystem/.work/hax-area-icons.html
node ecosystem/test/layout-check.js ecosystem/.work/hax-area-icons.html
```

Everything runs in `ecosystem/.work` (ignored), where `sources.sh` clones the repos the generators read and unpacks the published packages they need. Generators write straight back into `web/` and `build/data/`, so `git diff` after a run is the drift. `drift.py` also writes a report listing tiles that appeared or disappeared (CLI commands, API endpoints, MCP tools, field types, skeletons, importers, tutorials, languages, release steps) and every released part's version against npm and GitHub tags. `drift.py --accept` takes new versions and MCP tools into the saved data, and `--strict` exits non-zero when anything drifted.

Which webs are generated from source and which are curated by hand is in each `.mmd` header; the generated ones are listed in `drift.py`. Edit a curated web through its generator (`build_<web>.py`), not the `.mmd`/`.json` directly, or the next run will put it back.

## The network

The sites people meet HAX through are one network, and [`network.json`](network.json) is its record: what each property is called, where it lives, the color and icon that stand for it, the one sentence that says what it is for, and how it relates to the rest. Anything that names a property, on any site or in any post, uses this label and this sentence.

| Property | Where | Color | What it is for | How it relates |
| --- | --- | --- | --- | --- |
| **HAXTheWeb** | [haxtheweb.org](https://haxtheweb.org) | keystoneYellow | Why HAX is for you, and every way to get it. | The front door. It sends people to try, learn and install. |
| **PRAW** | [hax.cloud](https://hax.cloud) | original87Pink | The brain of the HAX ecosystem: every person, pillar and project, and how they connect. | PRAW, at hax.cloud, drawn as a web. Every other property takes its stories from here. |
| **Build now** | [browser.hax.cloud](https://browser.hax.cloud) | futureLime | Use HAX right now in this browser tab. Nothing to install. | The platform itself, live. Install HAX is how you take it with you. |
| **Learn** | [learn.hax.cloud](https://learn.hax.cloud) | skyBlue | Tutorials that teach HAX one flow at a time. | Where people go after trying it, as users and as contributors. |
| **Web components** | [webcomponents.hax.cloud](https://webcomponents.hax.cloud) | inventOrange | Every HAX element, with live demos and walkthroughs. | The parts every HAX site and editor is built from. |
| **Art** | [art.hax.cloud](https://art.hax.cloud/) | discoveryCoral | The HAX art movement: posters, the Future Traveler across time, and playful tools like RPG me. | Where HAX's creative side lives. RPG me is one of the tools in it. |
| **RPG me** | [rpg.art.hax.cloud](https://rpg.art.hax.cloud) | athertonViolet | Make the character that is you across HAX. | One of HAX Art's tools, linked from the Art site's menu rather than the network bar. On RPG me the bar lights up Art. |

The first six, in that order, are the network bar's list. PRAW feeds all of them and is named in the list as itself: its label is PRAW and its address is hax.cloud. RPG me is one of HAX Art's tools (`within: "art"` in the record), so it is not in the network bar at all: it is a stand-alone service at its own address, rpg.art.hax.cloud (rpg-me.hax.cloud redirects there), linked from the Art site's menu, and on RPG me the bar lights up Art.

Each property's `repo` is the haxtheweb repository it is built and deployed from. A release (ubiquity, in webcomponents) has to account for every one of them: [`scripts/ubiquity-network.json`](https://github.com/haxtheweb/webcomponents/blob/master/scripts/ubiquity-network.json) says what ubiquity does with each repo, and its coverage check fails when a repo named here has no entry there.

### Who draws what

Every site in the network carries the same bar, [`hax-network-bar`](https://github.com/haxtheweb/webcomponents/tree/master/elements/hax-network-bar), and the split is the same everywhere:

- **The network bar owns** moving between properties, Merlin, Install HAX, Discord, GitHub, your character and the Future Traveler. Each property is its icon in its color; the one you are on opens into its name. The Future Traveler at its right end remixes through every era he has been to: see [`FUTURE-TRAVELER.md`](../FUTURE-TRAVELER.md).
- **The site owns** everything under the bar: its header, its links and its controls. It does not repeat the network's links or its own name from the bar.
- **A full platform** (HAXcms in the browser) uses the bar's compact form and puts its own status and functions in it, because the editor under it already has a character, Merlin and the Future Traveler.
- **Install HAX opens in place** on every site, with a tab per way and its quick steps, and links to haxtheweb.org for the full details.

### Changing it

Change `network.json` first, in a pull request here, so the reason is on record. Then make the same change in the copy the elements ship, [`elements/hax-network-bar/lib/hax-network.js`](https://github.com/haxtheweb/webcomponents/blob/master/elements/hax-network-bar/lib/hax-network.js) (and the bar's English strings, which its tests hold to the record). Sites that build from webcomponents pick it up on their next deploy. A new property also needs its own network icon drawn in that file.

## HEOSAT evidence

The [heosat skill](../skills/heosat/SKILL.md) scores **47 questions in 9 sections** (rubric 2026.07 enhanced guidance edition). Apereo's sources disagree on how many criteria HEOSAT has: the HEOSAT README lists 7 assessment areas, the Apereo incubation page lists 8, and the assessment tool's rubric (used here and by the heosat skill) scores 47 questions in 9 sections. This map follows the tool's 9 sections.

Overall: 33 evidenced, 12 partial, 2 gaps.

| Section | Pillars | Evidenced | Partial | Gap |
| --- | --- | --- | --- | --- |
| Legal & Licensing | open | 4 | 1 | 0 |
| Governance & Decision-Making | sustainable, open | 4 | 1 | 2 |
| Community Engagement | accessible, sustainable | 4 | 1 | 0 |
| Documentation & Onboarding | accessible, efficient | 2 | 3 | 0 |
| Project Operations & Roadmap | sustainable, efficient | 3 | 2 | 0 |
| Security & Risk Management | sustainable | 5 | 0 | 0 |
| Accessibility, Standards & Interoperability | accessible, agnostic, remixable, open | 5 | 0 | 0 |
| Adoption, Impact & Institutional Fit | agnostic, sustainable | 2 | 3 | 0 |
| Financial & Organizational Sustainability | sustainable | 4 | 1 | 0 |

### Gaps and partial answers

| Question | Status | What's missing |
| --- | --- | --- |
| LL2: Every repository and distributed artifact includes license and copyright notices. | partial | License files ship in every core repo. Per-file headers are not checked yet; a weekly license compliance job that would check them is planned. |
| GV5: The project periodically reviews governance effectiveness and updates policies. | partial | The annual review is documented; no completed review is recorded yet. |
| GV6: The project documents and practices a standard voting procedure for decisions requiring formal approval. | gap | No documented voting procedure for decisions that need formal approval. |
| GV7: The project has an adopted, documented process for resolving community or governance disputes. | gap | The Code of Conduct covers conduct, but there is no process for resolving technical or governance disputes. |
| CE5: The project measures and responds to community health indicators. | partial | Activity is measured (merged PRs, npm downloads, release velocity). Community health indicators such as response times and contributor retention are not, and weekly issue triage is still planned. |
| DO1: The project has clear installation, configuration, and upgrade documentation. | partial | Install and setup are documented; upgrade documentation is thin while the docs site is being rebuilt. |
| DO2: The project provides end-user documentation appropriate to its primary audiences. | partial | End-user docs exist but are mid-rebuild; the ecosystem doc site and Learn HAX are the planned replacement. |
| DO5: Documentation is maintained as part of the release and contribution process. | partial | A weekly docs drift pass is planned but not running yet. |
| PO1: The project publishes a roadmap or planning process that communicates priorities and timelines. | partial | The roadmap names directions but not timelines. |
| PO5: The project tracks maintainership capacity and bus factor risks. | partial | Succession is documented; maintainer capacity and bus factor are not tracked over time. |
| AI3: The project supports evaluation, pilots, and procurement due diligence. | partial | hax.cloud offers a no-install demo, but there are no HECVAT-style procurement answers or a pilot guide. |
| AI4: The project documents implementation services, hosting options, or support partners when available. | partial | Hosting options exist (HAXiam, Reclaim Hosting, Docker images) but no single page lists hosting and support partners. |
| AI5: The project collects user feedback and uses it to improve product direction. | partial | Feedback arrives through issues and Merlin; a structured user study is planned. |
| FS5: The project periodically assesses sustainability risks and publishes improvement priorities. | partial | One assessment has been run (haxcms-php). There is no recurring reassessment or published improvement priority list yet. |

### Proposed nodes

- `heosat` (HEOSAT), linked to `apereo`, `praw`, `traveler`, `wins`. Hub for this map; each section and question hangs under it.
- `booklooky` (BookLooky), linked to `apereo`, `heosat`, `wins`. Win: HAX's AI-run HEOSAT process helped BookLooky go through Apereo incubation more accurately. PRAW's haxcms-lrs-rater skill also runs BookLooky's Looky Rating System.

## Instructional design skills

24 skills, grouped by family. Elements are the ones each skill's files reference most.

| Skill | Family | Pillars | Top elements |
| --- | --- | --- | --- |
| [`hax-ubd-backward-design`](../skills/hax-ubd-backward-design/SKILL.md) | Understanding by Design | efficient, remixable | `editable-table`, `simple-fields`, `stop-note`, `self-check`, `a11y-collapse` |
| [`hax-ubd-stage1`](../skills/hax-ubd-stage1/SKILL.md) | Understanding by Design | efficient, remixable | `stop-note`, `self-check`, `oer-schema`, `multiple-choice`, `editable-table` |
| [`hax-ubd-stage2`](../skills/hax-ubd-stage2/SKILL.md) | Understanding by Design | efficient, remixable | `editable-table`, `simple-fields`, `stop-note`, `progress-donut`, `simple-progress` |
| [`hax-ubd-stage3`](../skills/hax-ubd-stage3/SKILL.md) | Understanding by Design | efficient, remixable | `a11y-collapse`, `self-check`, `a11y-tabs`, `stop-note`, `map-menu` |
| [`hax-ubd-essential-questions`](../skills/hax-ubd-essential-questions/SKILL.md) | Understanding by Design | efficient, remixable | `stop-note` |
| [`hax-ubd-grasps`](../skills/hax-ubd-grasps/SKILL.md) | Understanding by Design | efficient, remixable | `simple-fields`, `editable-table`, `audio-player`, `media-playlist`, `video-player` |
| [`hax-ubd-six-facets`](../skills/hax-ubd-six-facets/SKILL.md) | Understanding by Design | efficient, remixable | `editable-table`, `simple-fields`, `stop-note`, `image-compare-slider`, `a11y-compare-image` |
| [`hax-ubd-unit-audit`](../skills/hax-ubd-unit-audit/SKILL.md) | Understanding by Design | efficient, remixable | `multiple-choice`, `stop-note`, `oer-schema`, `simple-fields`, `editable-table` |
| [`grad-blooms`](../skills/grad-blooms/SKILL.md) | Course alignment and cognitive level | efficient, remixable | `multiple-choice`, `matching-question`, `sorting-question`, `self-check`, `editable-table` |
| [`siip-course-alignment`](../skills/siip-course-alignment/SKILL.md) | Course alignment and cognitive level | efficient, remixable | `course-design` |
| [`hax-instructional-events-audit`](../skills/hax-instructional-events-audit/SKILL.md) | Course alignment and cognitive level | efficient, remixable | `stop-note`, `self-check`, `media-image`, `video-player`, `oer-schema` |
| [`hax-udl-audit`](../skills/hax-udl-audit/SKILL.md) | Universal design, accessibility and cognitive load | accessible | `stop-note`, `self-check`, `simple-fields`, `multiple-choice`, `oer-schema` |
| [`hax-a11y-audit`](../skills/hax-a11y-audit/SKILL.md) | Universal design, accessibility and cognitive load | accessible | `media-image`, `video-player`, `simple-fields`, `a11y-figure`, `audio-player` |
| [`hax-content-chunking-audit`](../skills/hax-content-chunking-audit/SKILL.md) | Universal design, accessibility and cognitive load | accessible | `a11y-collapse`, `stop-note`, `self-check`, `multiple-choice`, `media-playlist` |
| [`hax-multimedia-principles-audit`](../skills/hax-multimedia-principles-audit/SKILL.md) | Universal design, accessibility and cognitive load | accessible | `lrndesign-imagemap`, `media-image`, `video-player`, `lrn-vocab`, `audio-player` |
| [`hax-feedback-design`](../skills/hax-feedback-design/SKILL.md) | Learning science | accessible, efficient | `multiple-choice`, `tagging-question`, `mark-the-words`, `sorting-question`, `matching-question` |
| [`hax-practice-and-retrieval`](../skills/hax-practice-and-retrieval/SKILL.md) | Learning science | accessible, efficient | `multiple-choice`, `flash-card`, `fill-in-the-blanks`, `self-check`, `self-reflective-nudge` |
| [`hax-proficiency-scaffolding`](../skills/hax-proficiency-scaffolding/SKILL.md) | Learning science | accessible, efficient | `a11y-collapse`, `stop-note`, `self-check`, `video-player`, `self-reflective-nudge` |
| [`hax-reflection-prompts`](../skills/hax-reflection-prompts/SKILL.md) | Learning science | accessible, efficient | `self-check`, `stop-note`, `self-reflective-nudge`, `a11y-collapse`, `editable-table` |
| [`oerschema-audit`](../skills/oerschema-audit/SKILL.md) | Open educational resources | remixable, open | `oer-schema` |
| [`oerschema-integration-finder`](../skills/oerschema-integration-finder/SKILL.md) | Open educational resources | remixable, open | `oer-schema` |
| [`reading-notes`](../skills/reading-notes/SKILL.md) | Reading and content rating | accessible | `self-check` |
| [`haxcms-lrs-rater`](../skills/haxcms-lrs-rater/SKILL.md) | Reading and content rating | accessible | none |
| [`hax-instructional-element`](../skills/hax-instructional-element/SKILL.md) | Building new instructional elements | extensible, accessible | `reading-analysis`, `multiple-choice`, `sorting-question`, `a11y-gif-player`, `h-a-x` |

### Coverage gaps

Instructional elements no skill recommends yet:

- `course-model`: Shows a 3D model learners can turn and view from several angles; no skill recommends it.
- `vocab-term`: Overlaps lrn-vocab, which skills do cite; decide which one skills should recommend.
- `micro-game-base`: Base for learning games; no skill covers game-based practice.
- `bullet-check-list`: Checklist activity; could serve practice or reflection skills.

Skills that reference no element: `haxcms-lrs-rater` (it rates content rather than authoring it, so this is expected).
