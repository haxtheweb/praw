---
name: haxcms-prototype
description: "Build a prototype of HAXcms itself (whole-site designs, the editor top bar, edit mode, menus, outline, site or system admin, multipage flows) on the real running system, mark what is proposed, and check the rest against a generated UI inventory. Use for any HAXcms mockup, redesign or flow prototype; single elements use hax-element-demo."
version: 1.0.0
license: Apache-2.0
metadata:
  author: haxtheweb
  depends_on: [hax-design-system, hax-managed-files, hax-element-demo]
  tags: [hax, haxcms, prototype, mockup, design-review, admin, hax-ui, ddd, fidelity, artifact]
---

# HAXcms prototype

A prototype of HAXcms is a claim about what the product does and looks like. When it is drawn from
memory it drifts: labels, menu order, spacing and color end up "in the neighborhood", and sometimes
capabilities appear that do not exist. Reviewed as a standalone page, nothing catches it.

This skill prevents that by building every prototype **on the running system**. Only the change being
proposed is authored by hand, it is always marked as proposed, and everything else is checked against a
generated inventory of the real UI. Rule: `ccca6768-05e0-4d4d-b3a1-4b9895531558` in
<https://github.com/haxtheweb/praw/blob/main/RULES.md>.

Use this skill for: whole-site designs, the editor top bar, edit mode and the tray, Merlin, outline,
add page, the site admin dialog and its sections, system admin, the app-hax dashboard, and any flow
that crosses more than one of them. A single element, alone or in the editor, uses `hax-element-demo`
(and `hax-instructional-element` for instructional elements).

## Inputs

- A **haxcms-nodejs** checkout on latest `main` (<https://github.com/haxtheweb/haxcms-nodejs>),
  dependencies installed, Chrome or Chromium available.
- *(For unreleased element or editor work)* a **webcomponents** checkout
  (<https://github.com/haxtheweb/webcomponents>) on the working branch.
- What is being proposed, and for whom.

Clone into any working directory (`git clone --depth 1` in a cloud workspace). Commands below use
`<haxcms-nodejs>` and `<webcomponents>` for those paths. Never write machine-specific paths into
anything you publish.

## Workflow

1. **Write the brief first** (`references/brief.md`). It names the states the prototype shows, in
   order; exactly what is proposed in each; any new labels, components or tokens; and the fixture.
   Most drift starts as an unstated assumption, and the brief brings it out before anything is drawn.
   If the brief cannot say what exists today for a state, capture it (step 2) before going further.

2. **Capture ground truth.** In `<haxcms-nodejs>`:

   ```bash
   npm run ui:inventory -- --out <dir>/main
   ```

   This boots an isolated runtime, creates a site and walks the real states (dashboard, first visit,
   site view, edit mode, outline, add page, user menu, every site admin section). Per state it writes
   screenshots (desktop and mobile, light and dark), `dom.json` (every visible control and heading:
   tag, host chain, label, text, icon, box, computed styles and the DDD / HAX UI tokens they resolve
   to) and the ordered visible labels; plus `manifest.json`, `README.md` and `tokens.css` (every
   `--ddd-*` / `--hax-ui-*` value as it resolved). Read `README.md` and the `dom.json` of every state
   in the brief before drawing anything. Add `--sub` for admin sub-sections and `--states` to limit
   the run. A state the inventory does not cover yet is captured the same way: add it to
   `scripts/ui-inventory.js` in a haxcms-nodejs PR rather than describing it from memory.

   **Something new on a page** (a new block, a new page layout): put the real page around it instead
   of laying the proposal over unrelated content. Write the page's surrounding content to a file with
   an empty slot where the proposal goes (`<div id="proposal-slot" style="height: 760px"></div>`),
   then capture with `--page-title "<title>" --page-html <file> --measure "#proposal-slot"` and, when
   the slot is below the fold, `--viewport-height <px>` (clean-one scrolls inside its own container,
   so a full-page screenshot would not reach it). `manifest.json` records the fixture and the slot's
   box per variant; position the proposed region from those numbers. Don't give the slot a custom
   element tag: the inventory would record it as a real component.

3. **Pick the mode.** Say which one at the top of the prototype.

   - **Branch prototype** (preferred whenever the change can be built). Make the change on a branch of
     webcomponents, then run the inventory against it:

     ```bash
     NODE_ENV=development HAXCMS_WEBCOMPONENTS_ROOT=<webcomponents> npm run ui:inventory -- --out <dir>/branch
     ```

     Every pixel is real on both sides. Run the comparison
     (`node <skill-dir>/scripts/fidelity-check.mjs compare <dir>/main <dir>/branch`) and put its
     label and structure diff in the prototype; any change it finds that the brief does not list is
     a bug in the branch or the brief.
   - **Overlay prototype** (when the change is not built yet). The base of every state is the main
     inventory's screenshot for that state, copied unchanged into the prototype's `base/` folder. The
     proposal is HTML positioned over the base, inside `data-proposed` regions, styled only with
     variables from the inventory's `tokens.css`: HAX UI (`--hax-ui-*`) for admin surfaces and editor
     chrome, DDD for anything a visitor sees, per the HAX UI rule. Live editor pieces inside a
     proposal come from a `hax-element-demo` bundle, never redrawn.
   - **Concept sketch** (only when the person asks for loose ideas, not how HAXcms would look). Use
     the DDD Design System artifact. Label it "Concept, not the current UI" on the page. It must not
     be presented as, or reviewed as, a HAXcms prototype.

4. **Build the page** from `references/template.html` (it already implements the chrome below and
   renders from the brief), to the contract in `references/artifact.md`: provenance stamp, the states in
   brief order as a stepper, a variant switch (desktop / mobile, light / dark), proposed regions
   always marked plus a **Show proposed** toggle, a **Current / Proposed** flip per state, the brief,
   and a review panel with **Copy feedback**. Multipage and admin flows show each step as its own real
   state, never a storyboard of approximations.

5. **Check fidelity**, then fix and re-run until it passes:

   ```bash
   node <skill-dir>/scripts/fidelity-check.mjs check <prototype-dir> <dir>/main [--registry <wc-registry.json>]
   ```

   It fails when a base image is not byte-identical to an inventory screenshot, the provenance stamp
   is missing or does not match the inventory, a proposed region is not in the brief, visible text
   outside proposed regions is not a real label, a new label or component is not declared in the
   brief, a custom element tag is not in the registry (`src/public/wc-registry.json` in
   haxcms-nodejs) or the brief, or authored CSS uses a raw color or size instead of a token. Paste
   its report into the review panel.

   The check reads the page's HTML. Text and styles a proposed element renders from JavaScript
   (shadow DOM, CSS in the module) are outside its reach, so declare those labels in the brief anyway,
   keep the module's CSS on tokens, and let the independent review (step 6) and an axe run on the
   rendered page cover them.

6. **Independent review** for anything going to a design decision: hand the prototype directory, the
   inventory and the brief to a separate agent that has not seen the build, ask it to list anything
   in the prototype that is not how HAXcms works today, and add its findings to the review panel.

7. **Publish** as an artifact with the inventory screenshots as supporting files (they are part of the
   page, not links). Republish to the same artifact for later rounds so the link people have keeps
   working.

8. **Close the loop.** When a reviewer flags something as inaccurate, fix the prototype and also
   decide why it happened: the inventory was wrong or missing a state (fix `ui-inventory.js`), or the
   agent made a repeatable mistake (add it to `references/deviation-log.md`, and propose a rule when
   the same mistake shows up twice). Read the deviation log before every new prototype.

## Gotchas

- A proposal that uses real HAX parts (DDD block anatomy, rpg-character, simple-icon) imports them
  from the haxcms-nodejs build of main (`src/public/build/es6/node_modules`), copied into the
  prototype as supporting files with their relative paths intact. Copy only what the page loads
  (record the requests while exercising every state), plus every file a random choice could reach,
  such as all of rpg-character's numbered trait art when the page reseeds characters. An artifact
  publish takes at most 255 files.

- Labels carry their shortcut in the top bar ("Edit • Ctrl⇧E"); the inventory records them as users
  see them. Do not shorten them in a base region.
- A first visit opens Merlin's welcome over the page; `site-first-visit` captures it and the other
  states dismiss it. Show it only if the flow really starts on a first visit.
- `prefers-color-scheme` drives the dark captures. Where a surface has its own dark-mode switch that
  does not follow it, the dark capture shows light: say so rather than painting a dark version.
- Live prototypes cannot use jsdelivr or unpkg for HAX code: they serve npm releases, not main.
  Bundle from the checkout and publish the bundle as supporting files.
- Never refresh the e2e visual baselines in haxcms-nodejs as part of prototyping; the inventory
  writes only to its `--out` directory.
- Do not show the running HAX version anywhere in a prototype. The provenance stamp carries commit
  SHAs of the checkouts it was built from, not a release version of any deployed site.
