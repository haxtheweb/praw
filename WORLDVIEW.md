# WORLDVIEW
This document captures a normalized worldview profile derived from two aligned sources: Bryan Ollendyke's `btopro/blog` writing corpus (spanning roughly two decades of life, work, research, and philosophy) and his 2015 thesis, *Information Altruism*. The blog captures long-run practice in public; the thesis provides explicit theory for how those practices reshape institutions.
## Source scope
- Primary corpus (served): `https://btopro.com`
- Primary corpus (source mirror): `https://github.com/btopro/blog`
- Thesis corpus: `https://github.com/haxtheweb/praw/blob/main/thesis-bryan-ollendyke-information-altruism.pdf`
- Current corpus snapshot: `site.json` with 83 indexed items
- Inclusion focus: HAX, HAXcms, ELMS:LN, open web, instructional design, educational transformation, community development, sustainability, faculty/student empowerment
- Thesis inclusion focus: Information Altruism, Actor-Network Theory, tempered radicalism, diffusion of innovation, do-ocracy, and institution change from within
- Explicit exclusion focus for this synthesis: hockey and family-centric material unless directly tied to educational technology strategy
## People who shaped it

- **Keith Bailey** (1970–2020): mentor who hired Bryan into online learning at Penn State and championed the work that became ELMS (see `WHY.md`).
- **Mike Potter**: one of Bryan's best friends; pointed him to the web component *standard* in 2016, which made HAX possible. Still works on web components, though not on HAX at present.
- **Michael Collins**: faculty member who teaches with HAX tools and now develops his own flavor on top of HAX; recent admin dashboard UI and the updated outline designer come from him.
- **Bill Rose**: HAX product owner; the course ontology, cognitive apprenticeship framing and partner-facing voice.

## Core worldview pillars
### 1) The web should remain open, ownable, and portable
- Content and tooling should resist platform lock-in.
- Publishing should preserve long-term ownership and portability across platforms.
- Open standards are preferred over closed vendor dependency.
### 2) Authoring must be decoupled from storage and backend politics
- HAX as Headless Authoring eXperience is a strategic pattern, not just a product feature.
- Authoring UX should be reusable across CMS/LMS/static workflows.
- The same content model should travel across systems without rewriting pedagogy.
### 3) Education technology should be education-led, not profit-led
- Critical stance toward techno-centrism and edtech commodification.
- Institutions should build and steer solutions grounded in learning science, instructional practice, and public-good values.
- Technology is a means to educational outcomes, not the outcome itself.
### 4) Move beyond LMS monoculture toward distributed learning ecosystems
- Faculty autonomy and academic freedom are central.
- Systems should meet educators where they are instead of forcing one toolchain.
- Interoperability between LMS/CMS/static and desktop/local workflows is a core requirement.
### 5) Accessibility and OER are default constraints, not optional add-ons
- Non-technical educators should be able to produce high-quality, accessible learning experiences.
- Open Educational Resources and reusable content patterns are essential to scale impact.
- Better authoring interfaces reduce accessibility debt and improve pedagogical reach.
### 6) Community-building is part of the architecture
- Build in public with faculty, designers, technologists, students, and open-source contributors.
- Progress is amplified through shared issue queues, demos, and collaborative refinement.
- Institutional and open-source communities should co-evolve.
### 7) Sustainable systems matter technically, economically, and socially
- "Open but unmaintainable" is treated as a failure mode.
- Preferred solutions are understandable, maintainable, and deployable by regular practitioners.
- Long-term sustainability (including resource use and organizational resilience) is a design requirement.
### 8) Learning by building in real systems (SIIP pattern)
- Coursework can be aligned to real project contribution pathways.
- Student and faculty contributions can compound project velocity and educational outcomes simultaneously.
- Real-world contribution loops create durable innovation pipelines for institutions.
## Information Altruism thesis lens (explicit additions)
### A) Information altruism is a practical strategy, not just an ethic
- The donation of code, time, support, and knowledge can change institutional decision-making by changing the cost structure of innovation.
- Giving away working capability can outperform arguments alone when organizations are stuck in gatekeeper models.
### B) Technology artifacts carry worldview
- Systems are political artifacts: they encode assumptions about agency, ownership, collaboration, and control.
- The goal is to imprint empowering values into tools so adoption shifts norms organically.
### C) Durable change is usually constraint-based
- Lasting institutional change often comes from inside existing systems, not only from outside protest.
- Tempered radical methods (build, seed, support, iterate) are preferred over purely oppositional postures.
### D) Four-factor diagnostic before intervention
- **Currency**: what exchange model dominates (money, control, service), and what is the non-dominant counter?
- **Power flow**: where decisions originate and who is excluded from shaping them?
- **Value system**: which beliefs are in conflict between institution and change agents?
- **Flag in the ground**: what visible artifact/community can serve as a rally point for aligned actors?
### E) Organizational implications
- Favor smaller, flatter, contributor-empowered teams where ideas can bubble up.
- Treat central IT gatekeeping as a risk pattern in rapidly changing technology contexts.
## Agent-use implications
When generating recommendations aligned to this worldview:
- Prefer open standards, portability, and low lock-in architecture.
- Favor workflows that increase educator agency and reduce technical overhead.
- Treat accessibility and OER compatibility as default design constraints.
- Encourage community contribution models and transparent iteration.
- Prioritize sustainable, maintainable delivery over novelty theater.
- Apply the Information Altruism four-factor diagnostic (currency, power flow, value system, flag) when proposing organizational or platform strategy.
- Recommend approaches that encode values into tooling and service design, not just policy statements.
- Prefer change strategies that are empowering and non-coercive while still structurally transformative.
## Community pillars (canonical)

The HAX community's own pillars, published on haxtheweb.org and summarized in `WARP.md`, are the public names for what this worldview protects. Everything must be, at all times, as much as possible:

**Accessible · Efficient · Extensible · Free and open · Platform agnostic · Remixable · Sustainable**

The worldview pillars above explain *why*; the community pillars are *what we call it* in public. When writing for others, use the community pillar names (see `VOICE.md`).

## Course ontology (the model under the authoring)

HAX is general web authoring, but it was built in an instructional design shop, and its educational features follow a course ontology developed by Bill Rose (HAX product owner) in 2023 ([recording](https://www.youtube.com/watch?v=iF4UZKcAWmw)). It is *a* valid ontology, not *the* definitive one ("10 instructional designers would generate 10 ontologies with significant overlap"), and is expected to grow with the community.

HAX's capabilities have moved well beyond this model, but it remains the pedagogical foundation of the worldview. As Bryan puts it: technology changes what is possible and how you teach, but the methodology of effective teaching is eternal. The same qualities apply to a web platform and to a lesson: multiple formats, accessible, fast. A good lesson is never only text, only video, only a game or only questions; it is a healthy chunking and mixing of all of them, so students learn and stay engaged. HAX's blocks exist to make that mix easy.

At its core, a course has six branches:

| Branch | What it holds | Notes |
| --- | --- | --- |
| **Outcomes** | Course goals (broad) and learning objectives (observable, usually per lesson) | UbD Stage 1 "desired results" generate outcomes |
| **Pedagogy** | The beliefs and method driving the course, stated or not | The Office of Digital Learning adopted Understanding by Design (backward design) |
| **Structure** | Optional units/modules → required lessons or weeks → optional sub-lessons → pages | Pages are built from HAX blocks (paragraph, image, video player, self-check, table…) |
| **Instruction** | Teaching in Adler's three modes: direct instruction, facilitation, coaching; and learning activities that culminate in performance with understanding | Facilitation suits pedagogical templates in HAX; UbD Stage 3 plans the sequence (WHERETO) |
| **Content** | Pre-instructional (overviews, objectives), instructional (built from HAX blocks), checks for understanding, metacognitive tips, summaries | Concept maps are high-value and underused |
| **Assessment** | High stakes (summative), low stakes, no stakes (formative) | Formative assessment is underused and a big opportunity; UbD Stage 2 evidence, GRASPS tasks, six facets of understanding |

UbD crosses the branches at three points: desired results (pedagogy → outcomes), acceptable evidence (pedagogy → assessment) and learning experiences (pedagogy → instruction). PRAW's `hax-ubd-*`, `grad-blooms` and audit skills implement this ontology; new instructional features should say which branch they serve.

## Pillar checks
> **Rough draft.** Each pillar above as yes/no questions an agent or reviewer can actually answer for a change. Refine with real failures as they happen.

Run these for any new feature, skill, plugin, integration or architectural decision. A "no" is not an automatic block; it must be named in the PR description with the reason and a follow-up issue in https://github.com/haxtheweb/issues.

| # | Pillar | Community pillar | Check (all should be "yes") |
| --- | --- | --- | --- |
| 1 | Open, ownable, portable | Platform agnostic, Remixable | Can a user export everything they made in an open format (HTML, JSON Outline Schema, files) and run it somewhere else without us? Does it avoid a new required proprietary service or account? |
| 2 | Authoring decoupled from storage | Platform agnostic, Extensible | Does the authoring experience work the same across backends (haxcms-nodejs, haxcms-php, static, desktop) or degrade gracefully? Is content stored as portable HAX-valid HTML rather than backend-specific markup? |
| 3 | Education-led, not profit-led | Free and open | Can you name the learner or educator outcome it improves? Does it avoid paywalls, upsells or tracking that serves someone other than the user? |
| 4 | Distributed, not monoculture | Platform agnostic, Extensible | Does it interoperate (standards, LTI, embeds, exports) rather than require people to move everything into HAX? Can an educator keep using the tools they already rely on? |
| 5 | Accessibility and OER by default | Accessible, Free and open | Does it meet WCAG 2.0 AA without author effort (labels, contrast, keyboard, headings)? Is OER Schema / licensing metadata preserved? Did `hax-a11y-audit` or an equivalent check run? |
| 6 | Community is architecture | Sustainable (community) | Is the work tracked in the unified issue queue, documented, and approachable for a first-time contributor (clear README, "good first issue" where possible)? |
| 7 | Sustainable | Sustainable, Efficient | Could a regular practitioner (not the author) understand, maintain and deploy it? Does it remove or avoid complexity rather than add a new dependency or build step without reason? |
| 8 | Learning by building | Sustainable (community) | Could a student contribute to or learn from this (SIIP)? Is there a path from a course assignment to this code? |
| A | Information altruism | Free and open | Does it give capability away freely (open license, public docs, no lock-in) so others can build on it? |
| B | Values encoded in tools | All | Does the default behavior embody the value, rather than relying on a policy or a setting people must find? |
| C | Human creativity first | Free and open, Remixable | Does AI speed the work while people keep the creative and editorial decisions? Does the output stay open and portable rather than depending on a single AI service ("supplemented by AI, not forever powered by it")? |
| D | Meet people where they are | Accessible, Efficient | Does it start from what people already have (a Word file, an existing site, Markdown, a URL) and ask them to know nothing about the web? Would a newcomer get what it is in about three seconds, without digging through layers of menus? (A guideline, not a blocker.) |
| E | Works forever | Sustainable, Platform agnostic | Will content made today still render and edit years from now because it is saved as HTML whose tag definitions can be upgraded later? (Every HAX site made since about 2020 still works.) |

Agents should report the result as a short table or list in PR descriptions for non-trivial changes, alongside lint and test results.

## Representative source posts
- `open-community-pedagogy-2` — `https://btopro.com/open-community-pedagogy-2` | `https://github.com/btopro/blog/blob/gh-pages/pages/item-e3d7d519-9549-4e44-9ab8-b9df805a3531/index.html`
- `hax-apereo-piece-2` — `https://btopro.com/hax-apereo-piece-2` | `https://github.com/btopro/blog/blob/gh-pages/pages/item-79649f12-a6d2-98f5-3c0b-8b88f2a24457/index.html`
- `when-educators-left-the-lms-2` — `https://btopro.com/when-educators-left-the-lms-2` | `https://github.com/btopro/blog/blob/gh-pages/pages/item-46aa6443-ebf1-62b2-6523-760490d5ce9b/index.html`
- `reclaim-the-web-2` — `https://btopro.com/reclaim-the-web-2` | `https://github.com/btopro/blog/blob/gh-pages/pages/item-7502f3ce-134f-4c88-beaf-85e539c0e801/index.html`
- `open-source-cms---the-4th-turning` — `https://btopro.com/open-source-cms---the-4th-turning` | `https://github.com/btopro/blog/blob/gh-pages/pages/item-802d3c36-cd68-4eb7-b45c-761a779c08d5/index.html`
- `actually-curing-edtech-2` — `https://btopro.com/actually-curing-edtech-2` | `https://github.com/btopro/blog/blob/gh-pages/pages/item-4080a73d-360e-7a65-131b-705b8c6169e7/index.html`
- `creating-the-decentralized-instructional-experience-app-2` — `https://btopro.com/creating-the-decentralized-instructional-experience-app-2` | `https://github.com/btopro/blog/blob/gh-pages/pages/item-70c61ad7-f543-9af8-dd1b-1b65f0f453b2/index.html`
- `hax/sustainable-impact-and-innovation-pipeline` — `https://btopro.com/hax/sustainable-impact-and-innovation-pipeline` | `https://github.com/btopro/blog/blob/gh-pages/pages/item-d21d217e-bead-408f-bd0d-4459cb918914/index.html`
