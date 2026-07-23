---
name: create-tutorial-site
description: >
  Create a published HAXcms tutorial site from a YouTube video and a DOCX transcript
  (with screenshots and timestamps), then generate LinkedIn / X / Mastodon posts and a
  YouTube SEO description. Use this skill whenever the user says "create a tutorial site
  for this", "turn this video into a tutorial site", "make a tutorial site from this docx
  and youtube", "build a tutorial site from this video", or provides a YouTube URL plus a
  .docx file and wants a single-page tutorial published to surge with social copy — even
  if they do not say "skill" or "tutorial site" explicitly. Also use it when the user
  references the `btopro-tutorial` skeleton or the `ai-single-site-tutorials` directory
  in the context of turning a video + transcript into a site.
version: 1.1.0
license: Apache-2.0
metadata:
  author: haxtheweb
  tags: [hax, tutorial, youtube, docx, surge, resume-theme, page-anchor, social-copy, provenance, puppeteer, review-mode]
---

# Create a Tutorial Site

Turn a YouTube video + a DOCX transcript (screenshots + timestamps) into a published,
single-page HAXcms tutorial site, plus ready-to-post LinkedIn / X / Mastodon copy and a
YouTube SEO description. Trigger phrase: **"create a tutorial site for this"**.

## Inputs

- **YouTube watch URL** — e.g. `https://www.youtube.com/watch?v=XXXXXXXXXXX`. The video
  title (via oEmbed) becomes the site title; the video is embedded at the top of the page.
- **Local `.docx` path** — the transcript with screenshots and timestamps. Screenshots are
  extracted into the site so media lives with the tutorial; timestamps become in-page
  seek links.
- **Puppeteer `.json` path (optional)** — a browser-automation recording artifact. When
  supplied, it is copied into the site `files/` folder and linked in an "Automation
  recording" sub-section at the bottom of the Details block. The converter treats it as a
  linked artifact; it does not parse an unknown JSON shape into page content.

## Prerequisites (verified on this machine)

- `hax` CLI (local copy — never `npx`), `surge`, `node` v22+. mammoth is resolved from the
  `create`/`haxcms-nodejs` `node_modules` (no pandoc/yt-dlp required).
- The `btopro-tutorial` site skeleton installed at `~/.haxcmsconfig/skeletons/btopro-tutorial.json`
  — it bakes in the `resume-theme`, site settings, and platform config, plus one placeholder
  page (title "Tutorial", slug `tutorial`). It does NOT bake in the author profile
  (`metadata.author` ships empty `{}`), so the skill injects the author from
  `references/author-profile.json` during step 6. The skill does not pass `--theme`.
- All sites live under `~/Documents/git/haxtheweb/ai-single-site-tutorials/`.

## Modes

- **Publish mode (default)** — the full workflow runs end to end: scaffold, convert,
  publish to surge, generate social copy, report back. This is what happens unless the
  user signals otherwise.
- **Review mode** — used when the user's request implies oversight before publishing
  (e.g. "review before publishing", "let me review/edit first", "I want to oversee this",
  "draft it first", "don't publish yet", "let me look it over before it goes live").
  Detection is natural-language judgment, not a literal flag. In review mode the skill
  runs steps 1–6, then **stops before the surge publish**: it reports the local site
  directory and the exact page file path so the user can edit by hand, and starts
  `hax serve` from the site directory so the user can open the HAX editor in the browser
  to review/edit. It waits for the user's explicit go-ahead ("publish now", "go ahead and
  publish", "publish it"), then stops the dev server and runs steps 7–9. The
  `--y --no-i --auto --skip --quiet` automation flags still apply to scaffold/convert/
  publish; `hax serve` is the one intentional interactive sub-process, started only here.

## Workflow

1. **Collect inputs** — YouTube watch URL + local `.docx` path. Validate the URL contains an
   11-char video ID and the DOCX exists.
2. **Resolve video metadata** — fetch the YouTube oEmbed endpoint to get `title`,
   `author_name`, and `thumbnail_url`:
   `curl -s "https://www.youtube.com/oembed?url=<watch-url>&format=json"`
   Extract the video ID from the URL. The oEmbed `title` becomes the site title.
3. **Derive machine name** — slugify the video title to kebab-case (lowercase, hyphen-separated,
   no spaces). If `<machine-name>` already exists under `ai-single-site-tutorials/`, append
   `-2`, `-3`, etc. Per ecosystem rule, `metadata.site.name` MUST equal this folder name.
4. **Scaffold the site from the skeleton** — run from the tutorials directory with automation
   flags (never `npx`; the `--y --no-i --auto --skip --quiet` flags prevent prompts and
   sub-process launches):
   ```
   cd ~/Documents/git/haxtheweb/ai-single-site-tutorials && \
     hax site <machine-name> --skeleton-machine-name btopro-tutorial \
       --y --no-i --auto --skip --quiet
   ```
5. **Generate a video-player UUID** — used so timestamp `page-anchor` links can seek the
   embedded video in-page:
   `node -p "crypto.randomUUID()"`
6. **Convert the DOCX, assemble the page, and finalize site.json in one pass** — run the
   bundled converter. It extracts screenshots into `<site>/files/images/`, rewrites
   `<img src>` to site-relative paths, wraps timestamp tokens in
   `<page-anchor target="#<uuid>" value="<seconds>">`, prepends a
   `<video-player id="<uuid>" source="<watch-url>">`, writes the combined HTML to the
   skeleton's root page (location resolved from `site.json`'s first root item — the
   placeholder page folder is UUID-based), AND finalizes `site.json`: sets `title` to the
   video title, `description` (from `--description` or a default), and injects the author
   profile from `references/author-profile.json` into `metadata.author` (plus the top-level
   `author` string). It never touches `metadata.site.name`.
   ```
   NODE_PATH=~/Documents/git/haxtheweb/create/node_modules \
     node <skill-dir>/scripts/docx-to-content.cjs \
     <docx-path> <site-dir> <uuid> <watch-url> "<video-title>" \
     --description "<optional SEO summary>" [--puppeteer-json "<optional path>"]
   ```
   `--author-profile` defaults to `references/author-profile.json` (override only if needed).
   Pass `--puppeteer-json <path>` only when a puppeteer `.json` was attached; it is copied
   into `<site>/files/` and linked in the Details section (see below).
   The script resolves mammoth via `require('mammoth')` (honors `NODE_PATH`) with fallbacks
   to the `create` and `haxcms-nodejs` `node_modules`, so it works even without `NODE_PATH`
   on this machine. If the DOCX has no timestamp tokens, no `page-anchor` elements are
   emitted (the video-player is still embedded).
   The author injection matters: the `btopro-tutorial` skeleton ships `metadata.author` as
   an empty `{}`, so without this step the resume-theme sidebar renders no presenter. The
   profile keys (name, image, email, phone, location, website, website2, socialLink,
   socialLink2) map directly to what `resume-theme.js` reads from `metadata.author`.
   The converter also appends a **Details / provenance section** to the bottom of the page:
   a `<h2>Details</h2>` heading and a bulleted list linking the YouTube video, every
   screenshot in the page, and the source DOCX (copied into `files/`), followed by a
   "Last updated" date and the "HAXcms version" used in generation (read from the
   scaffolded site's `package.json`, falling back to the `create` CLI version). When
   `--puppeteer-json` is supplied, an "Automation recording" sub-section is appended at the
   very bottom of the Details section linking the copied JSON file.

   **Review-mode fork:** in review mode, stop after step 6. Start `hax serve` from
   `<site-dir>` for in-browser editing, report the local site directory and page file path,
   and wait for the user's explicit go-ahead before running step 7. (Publish mode continues
   straight through.)
7. **Publish to surge** — the domain is `<machine-name>.surge.sh`:
   ```
   cd <site-dir> && hax site site:surge --domain <machine-name>.surge.sh \
     --y --no-i --auto --quiet
   ```
   The CLI auto-installs surge if missing, swaps in the static `index.html` for publish,
   and restores it afterward. Record `https://<machine-name>.surge.sh`.
8. **Generate promotional copy** — read `references/author-profile.json` and
   `references/social-copy-templates.md` and produce three ready-to-post pieces, each
   referencing both the tutorial site URL and the YouTube URL:
   - **LinkedIn post** — hook + what you'll learn + CTA + both links + hashtags.
   - **X / Mastodon post** — concise (≤280 for X), punchy, tutorial site link (+ YouTube link
     if space). If `twitter`/`mastodon` in the profile are blank, link haxtheweb.org instead
     of a personal handle.
   - **YouTube SEO description** — keyword-rich first 1-2 lines, brief summary, a
     timestamps/chapters list pulled from the DOCX, links to the tutorial site + author
     profiles, and relevant hashtags.
9. **Report back** — print the published site URL, the local site path, and the three copy
    blocks so the user can post them immediately.

## Command reference

- Scaffold: `hax site <name> --skeleton-machine-name btopro-tutorial --y --no-i --auto --skip --quiet`
- Convert + assemble + finalize site.json + Details section: `node scripts/docx-to-content.cjs <docx> <site-dir> <uuid> <watch-url> "<title>" [--description "<text>"] [--puppeteer-json "<path>"]` (injects author profile into `metadata.author`, sets title/description, builds the page + Details/provenance block, optionally links a puppeteer JSON)
- Publish: `hax site site:surge --domain <name>.surge.sh --y --no-i --auto --quiet`
- Review-mode dev server: `cd <site-dir> && hax serve` (in-browser HAX editor for local review; stop it before publishing)
- Video metadata: `curl -s "https://www.youtube.com/oembed?url=<watch-url>&format=json"`
- UUID: `node -p "crypto.randomUUID()"`

## How the in-page seeking works

`<video-player id="<uuid>">` exposes a `seek(seconds)` method. `<page-anchor target="#<uuid>"
value="<seconds>">` (from `page-break/lib/page-anchor.js`) scrolls the video into view and
calls `video-player.seek(parseInt(value))` on click — true in-page seeking, not a YouTube
deep-link. `value` is total seconds (`1:30` → `90`). The converter handles this mapping.

## Guardrails (ecosystem rules)

- Use the **local** `hax` command, never `npx`.
- Always pass `--y --no-i --auto --skip --quiet` when scripting `hax` so no prompts or
  sub-processes launch.
- Keep `metadata.site.name` equal to the site folder name; do not modify it.
- Do not create `x/` routes (reserved for internal HAXcms paths).
- Do not run the monorepo build or the ubiquity script.
- Inject the author profile from `references/author-profile.json` into `site.json`
  `metadata.author` (the skeleton ships it empty). Never modify `metadata.site.name`.
  The same profile also feeds the promotional copy.
- Avoid optional chaining (`?.`) in any generated code (the Polymer parser has issues with it).
- Use `globalThis` instead of `window` in generated JavaScript.

## References

- `scripts/docx-to-content.cjs` — mammoth DOCX→HTML converter (image extraction + page-anchor
  timestamps + video-player prepend), Details/provenance section builder (YouTube + screenshot
  + DOCX links, last-updated date, HAXcms version; optional puppeteer-JSON "Automation recording"
  sub-section), AND site.json finalizer (title, description, author profile injection into
  `metadata.author`). Accepts `--puppeteer-json <path>` to attach a browser-automation artifact.
- `references/author-profile.json` — author profile (Bryan T Ollendyke); written into
  `site.json` `metadata.author` for the resume-theme sidebar and reused for promotional copy.
- `references/social-copy-templates.md` — LinkedIn / X / YouTube copy templates.
