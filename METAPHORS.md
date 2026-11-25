# Metaphors and refrains

How HAX explains itself in pictures and in lines worth repeating. Talks, posts, docs, release notes and agents writing public copy should reach here before inventing a new image. `VOICE.md` has the short table of recurring metaphors and Bryan's signature lines; this file holds the ones that carry a whole talk, written out so they can be told accurately and the same way every time.

Two kinds of entry live here:

- **Refrains**: one-liners that should keep showing up, the way a chorus does. They close talks, sit under logos, end READMEs. Repetition is the point.
- **Metaphors**: an image that explains how HAX works. Each entry says what the image carries, how to say it, and what to avoid so the picture stays true.

## Refrains

### "With the right tools you can build anything."

A family saying from Bryan's grandfather, William "Poppo" Ollendyke, and his father, Todd (see `WHY.md`). It is the closing line of the *With the right tools* talk (`talks/README.md`) and the last line of `FUTURE-TRAVELER.md`.

- **Say it as written:** *build* anything, not *do* anything. Building is the point: things made out of imagination that someone else can open, use and change.
- **Where it goes:** the end of a talk, the end of an onboarding path, the bottom of a landing page, the moment a demo produces something real. It works best right after the audience has watched something get built.
- **Talk variant:** "With the right tools and determination, YOU can build anything." Hands the line to the audience.

### "Break it down, mix it up, make it new."

The Remixable pillar's phrase. It is also the shortest form of the talk metaphors below: break it down (decomposition), mix it up (remix), make it new (a new, still-editable whole). Use it as the bridge line whenever the fractal or blur metaphors come up.

### Other refrains

The signature lines in `VOICE.md` are the pool. The ones meant to recur, not just be quoted once: "Let's make the web ubiquitous.", "Nothing is intentional, until it is.", "Enable creativity to flow like water." Add a line here when it has been used in more than one talk or post and should keep travelling.

## How HAX and PRAW work, as pictures

Built for talks about PRAW and what it has made possible (2026 onward). Told in order, they make one arc: **the blur, the zoom, the grammar.**

### Coarse to fine (the zoom)

**The image:** an idea starts fuzzy. Zoom in and it gets clearer: a sketch becomes an outline, the outline becomes pages, pages become blocks, blocks become tokens. You always get the big shape first and the detail last.

**What it carries:** how HAX work actually moves. "Napkin 2 PR" is this metaphor as a workflow: idea → drawing → photo → AI breaks it into data → context → constraints, design system, accessibility → a pull request. Every stage is a sharper version of the same picture.

**Why it's accurate:** AI image models (diffusion models) generate the same way. They start from noise; the early steps decide the composition and the later steps add the detail. HAX authoring and AI generation share a direction of travel, coarse to fine.

**How to say it:** "You get the shape first and the detail last. That's true of how we plan, how we build, and how the AI draws."

**Avoid:** saying zooming in reaches a final, complete picture. Every zoom level is still a piece of something larger (see the fractal below).

### The blur and the grid (the headline)

**The image:** two ways to take a book apart. AI takes it apart by blurring it: the book becomes noise, then statistics spread across a model's weights. The original structure is gone; so is who made what. HAX takes the same book apart and keeps the structure: book → `site.json` outline → pages → elements (image, caption, quote) → DDD tokens. Every piece keeps a name and an address.

**What it carries:** the thesis of the talk. Both paths end in remixing. AI remixes by guessing the pieces back. HAX remixes pieces you can still point to, credit and edit, by hand or by agent. And AI's output can land in HAX's structure, so the cycle repeats: AI breaks things down, HAX gives them shape again, people edit the shape, and that becomes the next thing to remix.

**How it was trained, accurately:** diffusion models learn by adding noise to real images until they are static, then learning to undo the noise. The model never stores the images; it stores what it learned about how images are put together. That is why the result can't tell you where a piece came from.

**How to say it:** "AI breaks things down by blurring them. HAX breaks things down and keeps the labels on. Both of them can remix; only one of them can tell you what it's holding."

**Avoid:** "HAX does what AI does." It undersells the difference, which is the whole point. Also avoid framing AI as the villain: AI is the fuse ("AI is the fuse to enable what's always been brewing"); HAX is what keeps the output human-editable.

### Every piece carries the whole (the fractal)

**The image:** zoom into a fractal and you find the shape of the whole again, at every scale.

**What it carries:** every HAX piece should carry the DNA of the larger vision. A single element is accessible, dark-mode ready, translatable and editable, the same promises the whole platform makes. A single PRAW rule carries a pillar. A single page is a whole, portable thing. This is the same idea as the Russian nesting dolls in `VOICE.md`, seen from the inside.

**How to say it:** "Zoom into HAX anywhere, a site, a page, a button, and you should find the same promises."

**Avoid:** using "fractal" to mean "it gets clearer as you zoom". In a fractal, zooming shows you *more of the same pattern*, not more clarity. Clarity is the coarse-to-fine metaphor; the fractal is about consistency at every scale.

### Grammar (what PRAW is)

**The image:** HAX elements are the words. PRAW is the grammar, the written rules for how the pieces combine.

**What it carries:** a diffusion model has to infer the rules of images from millions of examples, and it never writes them down. PRAW writes them down, in plain language, so a person or an agent can learn them from a handful of files instead of a mountain of data. Rules, patterns, worldview and voice are all grammar at different scales.

**How to say it:** "The components are the vocabulary. PRAW is the grammar. Learn both and you can say anything in HAX."

### A shared language

**The image:** people and agents working from the same vocabulary and grammar, so meaning survives the handoff in both directions.

**What it carries:** why PRAW exists. Codifying the rules isn't about making a machine think for us; it's about people, agents and the platform understanding each other.

**How to say it:** "PRAW gives people and tools a shared language."

**Avoid:** "plug your brain into the HAX brain." To a general audience it reads as brain–computer interfaces or giving up your thinking. Bryan's own shorthand for PRAW as HAX's networked brain is fine inside the project; in talks, lead with shared language.

## Adding to this file

- A new metaphor needs a source: a talk, a post or Bryan's own words. Link it.
- Write the accuracy note. If the image borrows from science or tech (diffusion, fractals, networks), check that the borrowed part is true.
- Keep `VOICE.md`'s table in sync with one row per metaphor that points back here.
