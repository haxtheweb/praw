---
name: hax-tutorial-site
description: >
  Create a published HAXcms tutorial site from a YouTube video and a DOCX transcript
  (with screenshots and timestamps), then generate LinkedIn / X posts and a
  YouTube SEO description. Use this skill whenever the user says "create a tutorial site
  for this", "run the hax tutorial skill", "hax tutorial skill", "make a tutorial site
  from this docx and youtube", "build a tutorial site from this video", or provides a
  YouTube URL plus a .docx file and wants a single-page tutorial published to surge with
  social copy — even if they do not say "skill" or "tutorial site" explicitly. "hax
  tutorial skill" is an alias for "make a HAXcms site" so the skill is discovered faster.
  Also use it when the user references the `hax-tutorial` skeleton or the
  `ai-single-site-tutorials` directory in the context of turning a video + transcript
  into a site. The skeleton is bundled with the skill (references/hax-tutorial.json)
  and referenced via `--skeleton-file`, so no personal-profile install is required and
  other people can use the skill to create tutorial sites rapidly.
version: 1.4.0
license: Apache-2.0
metadata:
  author: haxtheweb
  tags: [hax, tutorial, youtube, docx, surge, resume-theme, page-anchor, social-copy, provenance, puppeteer, review-mode, transcript, vtt, a11y-media-player, skeleton-file, portable]
---

# Create a Tutorial Site

Turn a YouTube video + a DOCX transcript (screenshots + timestamps) into a published,
single-page HAXcms tutorial site, plus ready-to-post LinkedIn / X copy and a
YouTube SEO description. Trigger phrase: **"create a tutorial site for this"** (also
**"run the hax tutorial skill"** / **"hax tutorial skill"** — an alias for "make a HAXcms
site" so it is discovered faster).

## Inputs

- **YouTube watch URL** — e.g. `https://www.youtube.com/watch?v=XXXXXXXXXXX`. The video
  title (resolved via yt-dlp in step 2) becomes the site title and the page `<h1>`; the
  video is embedded directly below that title.
- **Local `.docx` path** — the transcript with screenshots and timestamps. Screenshots are
  extracted into the site so media lives with the tutorial; timestamps become in-page
  seek links.
- **Puppeteer `.json` path (optional)** — a browser-automation recording artifact. When
  supplied, it is copied into the site `files/` folder and linked as an "Automation
  recording (JSON)" bullet at the bottom of the Tutorial Details block. The converter
  treats it as a linked artifact; it does not parse an unknown JSON shape into page
  content.

## Prerequisites

- `hax` CLI (local copy — never `npx`), `surge`, `node` v22+. mammoth is resolved from the
  `create`/`haxcms-nodejs` `node_modules` (no pandoc required). yt-dlp is used for video
  metadata + VTT and is auto-provisioned via an isolated venv by the skill scripts (no
  manual install or sudo needed).
- The `hax-tutorial` site skeleton is **bundled with this skill** at
  `references/hax-tutorial.json` — it bakes in the `resume-theme`, site settings, and
  platform config, plus one placeholder page (title "Tutorial", slug `tutorial`). The
  skill scaffolds from it via `--skeleton-file` (a direct path), so the skeleton does NOT
  need to be installed in `~/.haxcmsconfig/skeletons/` and the skill is portable to other
  users. It does NOT bake in the author profile (`metadata.author` ships empty `{}`), so
  the skill injects the author from `references/author-profile.json` during step 7. The
  skill does not pass `--theme`.
- All sites live under `~/Documents/git/haxtheweb/ai-single-site-tutorials/` (adjust the
  parent directory if adopting the skill elsewhere).

## Modes

- **Publish mode (default)** — the full workflow runs end to end: scaffold, convert,
  publish to surge, generate social copy, report back. This is what happens unless the
  user signals otherwise.
- **Review mode** — used when the user's request implies oversight before publishing
  (e.g. "review before publishing", "let me review/edit first", "I want to oversee this",
  "draft it first", "don't publish yet", "let me look it over before it goes live").
  Detection is natural-language judgment, not a literal flag. In review mode the skill
  runs steps 1–7, then **stops before the surge publish**: it reports the local site
  directory and the exact page file path so the user can edit by hand, and starts
  `hax serve` from the site directory so the user can open the HAX editor in the browser
  to review/edit. It waits for the user's explicit go-ahead ("publish now", "go ahead and
  publish", "publish it"), then stops the dev server and runs steps 8–10. The
  `--y --no-i --auto --skip --quiet` automation flags still apply to scaffold/convert/
  publish; `hax serve` is the one intentional interactive sub-process, started only here.

## Execution style

Run the whole workflow straight through with minimal narration — no per-step
confirmation or status chatter, just run it. Only report once, at the end (step 10):
the published site URL, the local site path, and the copy blocks. If a step soft-fails
(e.g. no captions available), note it in one line and continue.

## Workflow

1. **Collect inputs** — YouTube watch URL + local `.docx` path. Validate the URL contains an
   11-char video ID and the DOCX exists.
2. **Resolve video metadata** — use the bundled yt-dlp helper (NOT curl/oEmbed, so no
   network call that needs interactive confirmation). It auto-provisions yt-dlp via the
   same isolated venv the VTT step uses and prints `{ title, author, thumbnail }`:
   `node <skill-dir>/scripts/youtube-metadata.cjs <watch-url>`
   The `title` becomes the site title and the page `<h1>`. Extract the video ID from the
   URL with a regex (the 11-char id after `v=`).
3. **Derive machine name** — slugify the video title to kebab-case (lowercase, hyphen-separated,
   no spaces). If `<machine-name>` already exists under `ai-single-site-tutorials/`, append
   `-2`, `-3`, etc. Per ecosystem rule, `metadata.site.name` MUST equal this folder name.
4. **Scaffold the site from the bundled skeleton** — run from the tutorials directory
   with automation flags (never `npx`; the `--y --no-i --auto --skip --quiet` flags prevent
   prompts and sub-process launches). Use `--skeleton-file` pointing at the skeleton that
   ships with the skill (a direct path), NOT `--skeleton-machine-name`, so the skill does
   not depend on a skeleton installed in the user's personal `~/.haxcmsconfig` profile:
   ```
   cd ~/Documents/git/haxtheweb/ai-single-site-tutorials && \
     hax site <machine-name> --skeleton-file <skill-dir>/references/hax-tutorial.json \
       --y --no-i --auto --skip --quiet
   ```
5. **Generate a video-player UUID** — used so timestamp `page-anchor` links can seek the
   embedded video in-page:
   `node -p "crypto.randomUUID()"`
6. **Generate a VTT transcript (automatic)** — run the `youtube-vtt` skill script against
   the watch URL to produce a searchable WebVTT transcript (the video itself is NOT
   downloaded):
   `node <youtube-vtt-skill-dir>/scripts/youtube-to-vtt.cjs <watch-url> <tmp-dir>`
   It auto-provisions `yt-dlp` via an isolated venv if needed (first run only), tries manual
   captions then YouTube auto-captions, normalizes to `<tmp-dir>/transcript.vtt`, and
   cleans the result: strips YouTube's inline karaoke timing tags, de-duplicates the
   2-line rolling auto-caption repetition, and fixes the "HackCMS" speech-to-text typo. On
   success, pass `--transcript-vtt <tmp-dir>/transcript.vtt` to the converter in step 7. On
   failure (no captions available), warn and continue — the converter simply omits the
   transcript track and bullet, and the tutorial is still fully usable. This step is
   automatic (default on); it requires no user input beyond the YouTube URL.
7. **Convert the DOCX, assemble the page, and finalize site.json in one pass** — run the
   bundled converter. It extracts screenshots into `<site>/files/images/` and converts
   each into a `<media-image source=\"files/images/<n>.<ext>\" caption=\"<nearest preceding heading>\" offset=\"narrow\" card box>`, fixes the common speech-to-text typo
   "HackCMS"/"Hack CMS" -> "HAXcms", wraps timestamp tokens in
   `<page-anchor target=\"#<uuid>\" value=\"<seconds>\">`, emits an `<h1>` of the video
   title followed immediately by a `<video-player id=\"<uuid>\" source=\"<watch-url>\">`,
   writes the combined HTML to the
   skeleton's root page (location resolved from `site.json`'s first root item — the
   placeholder page folder is UUID-based), AND finalizes `site.json`: sets `title` to the
   video title, `description` (from `--description` or a default), and injects the author
   profile from `references/author-profile.json` into `metadata.author` (plus the top-level
   `author` string). It never touches `metadata.site.name`.
   ```
   NODE_PATH=~/Documents/git/haxtheweb/create/node_modules \
     node <skill-dir>/scripts/docx-to-content.cjs \
     <docx-path> <site-dir> <uuid> <watch-url> "<video-title>" \
     --description "<optional SEO summary>" [--puppeteer-json "<optional path>"] \
     [--transcript-vtt "<optional path>"]
   ```
   `--author-profile` defaults to `references/author-profile.json` (override only if needed).
   Pass `--puppeteer-json <path>` only when a puppeteer `.json` was attached; it is copied
   into `<site>/files/` and linked in the Details section (see below). Pass
   `--transcript-vtt <path>` with the VTT produced in step 6; it is copied into
   `<site>/files/transcript.vtt`, a `track="files/transcript.vtt"` attribute is added to
   the `<video-player>` (so `a11y-media-player` renders the searchable transcript that
   reads along with the video), and a "Transcript (VTT)" bullet is added to the Details
   section.
   The script resolves mammoth via `require('mammoth')` (honors `NODE_PATH`) with fallbacks
   to the `create` and `haxcms-nodejs` `node_modules`, so it works even without `NODE_PATH`
   on this machine. If the DOCX has no timestamp tokens, no `page-anchor` elements are
   emitted (the video-player is still embedded).
   The author injection matters: the `hax-tutorial` skeleton ships `metadata.author` as
   an empty `{}`, so without this step the resume-theme sidebar renders no presenter. The
   profile keys (name, image, email, phone, location, website, website2, socialLink,
   socialLink2) map directly to what `resume-theme.js` reads from `metadata.author`.
   The converter also appends a **Tutorial Details / provenance section** to the bottom of
   the page: a `<h2>Tutorial Details</h2>` heading and a bulleted list (every link opens in
   a new window via `target=\"_blank\"`). The first bullet is "Video Tutorial Link
   (YouTube)" with a `transcript` link to the VTT right after it (when a transcript was
   supplied); next, "Images in this page:" followed by a comma-separated list of image
   links (one `<li>`, not a nested list); then "Original Content Source (DOCX)"; the
   "Automation recording (JSON)" artifact as a bullet (not a sub-heading) when a puppeteer
   JSON was supplied; then a "Last updated" date and the "HAXcms version" used in
   generation (read from the scaffolded site's `package.json`, falling back to the `create`
   CLI version).

   **Review-mode fork:** in review mode, stop after step 7. Start `hax serve` from
   `<site-dir>` for in-browser editing, report the local site directory and page file path,
   and wait for the user's explicit go-ahead before running step 8. (Publish mode continues
   straight through.)
8. **Publish to surge** — the domain is `<machine-name>.surge.sh`:
   ```
   cd <site-dir> && hax site site:surge --domain <machine-name>.surge.sh \
     --y --no-i --auto --quiet
   ```
   The CLI auto-installs surge if missing, swaps in the static `index.html` for publish,
   and restores it afterward. Record `https://<machine-name>.surge.sh`.
9. **Generate promotional copy** — read `references/social-copy-templates.md` (the author
   profile is already in `site.json` from step 7) and produce three ready-to-post pieces,
   each referencing both the YouTube URL and the tutorial site URL. Use the exact emoji +
   link format from the templates:
   - **LinkedIn post** — one-line hook, then `🎬 Watch:` (YouTube) and `📝 Tutorial:` (site)
     links BEFORE the details/summary, then a 2-3 sentence "what you'll learn" summary, then
     the hashtags `#HAXTheWeb #OER #opensource #edtech #education #pennstate`. Do NOT append
     author name / links / signature after the hashtags.
   - **X post** (also covers Mastodon — one output, not two) — concise (≤280), simplified
     language, `🎬 Watch:` + `📝 Tutorial:` lines, then a single hashtag `#HAXTheWeb`. No other
     hashtags. No personal handle.
   - **YouTube SEO description** — keyword-rich first 1-2 lines, brief summary, a
     chapters/what's-covered list pulled from the DOCX, a Links section, and the SAME
     hashtags as the LinkedIn post: `#HAXTheWeb #OER #opensource #edtech #education #pennstate`.
10. **Report back (concise)** — print only: the published site URL, the local site path,
    and the three copy blocks (LinkedIn, X, YouTube). No per-step recap, no restating what
    each step did. Keep it scannable so the user can copy/paste and post immediately.

## Command reference

- Scaffold: `hax site <name> --skeleton-file <skill-dir>/references/hax-tutorial.json --y --no-i --auto --skip --quiet` (uses the skeleton bundled with the skill via a direct file path; portable, no personal-profile install required)
- VTT transcript: `node <youtube-vtt-skill-dir>/scripts/youtube-to-vtt.cjs <watch-url> <tmp-dir> [--lang en]` (auto-provisions yt-dlp via venv; subtitle-only; normalizes + cleans transcript.vtt [strips inline timing tags, de-duplicates rolling auto-captions, fixes "HackCMS"->"HAXcms"]; soft-fails on no captions)
- Convert + assemble + finalize site.json + Tutorial Details section: `node scripts/docx-to-content.cjs <docx> <site-dir> <uuid> <watch-url> \"<title>\" [--description \"<text>\"] [--puppeteer-json \"<path>\"] [--transcript-vtt \"<path>\"]` (injects author profile into `metadata.author`, sets title/description, builds the page [H1 video title + video-player + media-image screenshots + page-anchor timestamps + HackCMS->HAXcms fix] + Tutorial Details/provenance block with target=\"_blank\" links, optionally links a puppeteer JSON and attaches a VTT transcript via the `video-player` `track` attribute)
- Publish: `hax site site:surge --domain <name>.surge.sh --y --no-i --auto --quiet`
- Review-mode dev server: `cd <site-dir> && hax serve` (in-browser HAX editor for local review; stop it before publishing)
- Video metadata: `node <skill-dir>/scripts/youtube-metadata.cjs <watch-url>` (yt-dlp, auto-provisioned venv; prints {title, author, thumbnail}; no curl/oEmbed, no interactive confirm)
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

- `scripts/docx-to-content.cjs` — mammoth DOCX→HTML converter (image extraction +
  `<media-image>` conversion with heading captions + "HackCMS"->"HAXcms" fix + page-anchor
  timestamps + H1(video-title)+video-player assembly), Tutorial Details/provenance section
  builder (Video Tutorial Link (YouTube) + `transcript` + comma-separated image links +
  Original Content Source (DOCX) + Automation recording bullet; all links `target=\"_blank\"`;
  last-updated date, HAXcms version), AND site.json finalizer (title, description, author
  profile injection into `metadata.author`). Accepts `--puppeteer-json <path>` to attach a
  browser-automation artifact and `--transcript-vtt <path>` to copy a WebVTT into `files/`, add a
  `track=\"files/transcript.vtt\"` attribute to the `<video-player>` (so `a11y-media-player` renders
  the searchable transcript), and link it in Details.
- `scripts/youtube-metadata.cjs` — yt-dlp-based video metadata fetcher used in step 2
  (title, author, thumbnail). Resolves yt-dlp via PATH then the same managed venv as the
  youtube-vtt skill (auto-provisions on first run; no curl/oEmbed, no interactive confirm).
- **`youtube-vtt` skill** (`../youtube-vtt/`) — dependency for step 6. Its
  `scripts/youtube-to-vtt.cjs` turns the YouTube URL into a cleaned `transcript.vtt` via
  yt-dlp subtitle-only extraction (auto-provisions yt-dlp via a venv; strips inline timing
  tags + de-duplicates rolling auto-captions + fixes the "HackCMS" typo; soft-fails on no
  captions).
- `references/hax-tutorial.json` — the `hax-tutorial` site skeleton bundled with
  this skill (resume-theme + site settings + platform config + one placeholder "Tutorial"
  page). Scaffolding uses `--skeleton-file <skill-dir>/references/hax-tutorial.json`, so
  the skill is self-contained and portable (no `~/.haxcmsconfig/skeletons/` install needed).
- `references/author-profile.json` — author profile (Bryan T Ollendyke); written into
  `site.json` `metadata.author` for the resume-theme sidebar and reused for promotional copy.
- `references/social-copy-templates.md` — LinkedIn / X / YouTube copy templates. LinkedIn:
  hook → `🎬 Watch:` / `📝 Tutorial:` links before the details → summary → hashtags
  `#HAXTheWeb #OER #opensource #edtech #education #pennstate` (no author signature after
  hashtags). X (also serves Mastodon): `🎬 Watch:` / `📝 Tutorial:` → only `#HAXTheWeb`.
  YouTube SEO description: same hashtags as LinkedIn.
