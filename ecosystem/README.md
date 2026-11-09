# Ecosystem maps

Data that ties the HAX ecosystem web to the evidence and skills behind it. Each file uses the ecosystem web's node keys (`human`, `praw`, `oerschema`, `accessible` and so on), so the web can draw these links and a node's detail page can list them. The web itself is tracked in [haxtheweb/issues#3173](https://github.com/haxtheweb/issues/issues/3173).

| File | What it maps |
| --- | --- |
| [`heosat-evidence-map.json`](heosat-evidence-map.json) | Every HEOSAT question to the nodes and public files that answer it, with a status: evidenced, partial or gap. |
| [`id-skills-map.json`](id-skills-map.json) | Each instructional design skill in `skills/` to the elements it recommends or checks, the pillars it upholds and its nodes. |

The JSON files are the source; this page summarizes them. Statuses and pillar links are a self-assessment for maintainer review, not a HEOSAT score.

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

- `course-model`: Course structure modeling; no skill recommends it.
- `vocab-term`: Overlaps lrn-vocab, which skills do cite; decide which one skills should recommend.
- `micro-game-base`: Base for learning games; no skill covers game-based practice.
- `bullet-check-list`: Checklist activity; could serve practice or reflection skills.

Skills that reference no element: `haxcms-lrs-rater` (it rates content rather than authoring it, so this is expected).
