# Deviation log

Mistakes prototypes have made about HAXcms, and what is actually true. Read this before every new
prototype. Each entry says what was wrong, what is real (checked against the UI inventory on the date
given), and where to look. When the same mistake shows up twice, propose a rule in RULES.md.

When the UI changes, update or retire the entry instead of leaving it stale: an entry here is a claim
about the product too.

## Entries

### Outline is part of Site Settings, not its own top bar button

- **Seen**: prototypes drawing Outline as a separate modal or page, or as its own top bar button.
- **Real** (source, webcomponents master `6a933ca7fc`, 2026-11-10): since
  https://github.com/haxtheweb/webcomponents/pull/1149 the top bar has no Outline button. Site
  Settings is a menu (Dashboard, Content, Structure, Files, Appearance, ...) and Structure opens the
  one Site Settings dialog there, with the admin rail on the left. Ctrl⇧6 opens the outline actions.
- **Look at**: inventory states `site-view` and `outline`.

### The site admin is one dialog with a section rail

- **Seen**: Site Settings drawn as a single form, or as separate dialogs per area.
- **Real** (inventory, 2026-11-06): one dialog (`haxcms-site-admin`) with a collapsible rail. Top-level
  sections are discovered at runtime; on this date they were Dashboard, Content, Structure, Files,
  Appearance, then an "Advanced" group with Views (Beta badge), Blocks, Features, Details, Editor, SEO,
  Import / Export and About; several expand to sub-sections and some carry count badges. The titlebar
  is a breadcrumb ("Site Settings / Details"), each section has a page header with a one-line
  description, and the shell's action bar reads "No unsaved changes" with Discard and Save. Sections
  never draw their own titlebar or Save button (HAX UI rule).
- **Look at**: inventory states `site-admin-*` (add `--sub` for sub-sections).

### The top bar is three groups, and its shortcuts have moved

- **Seen**: the pre-#1149 bar ("Outline • Ctrl⇧2", "Site Settings • Ctrl⇧3"), or labels without their
  shortcut.
- **Real** (source, webcomponents master `6a933ca7fc`, 2026-11-10):
  - Left: the account menu (Ctrl⇧1; the way back to your sites lives in it), a thin divider, the Site
    Settings menu (house icon, Ctrl⇧2), "Add page • Ctrl⇧3", another divider and "Edit • Ctrl⇧E".
  - Center: Merlin as a search field ("Filter commands"), not a lone wand button.
  - Right: "Preview • Ctrl⇧8" (eye icon), then the HAX mark (World Traveler). The mark is decorative,
    not a link.
  - Every label carries its shortcut.
- **Phone width** (600px and below): the left group's dividers and the HAX mark are hidden, and the
  right group drops its gaps, so Edit still fits.
- **Shortcuts move**: they were renumbered in #1149. Read them from the capture or the source on the
  day you draw, never from an older prototype.
- **Look at**: inventory state `site-view`, `dom.json` labels and icons.

### Edit mode replaces the top bar's controls

- **Seen**: edit mode drawn as the site-view top bar plus a Save button.
- **Real** (source, webcomponents master `6a933ca7fc`, 2026-11-10): in edit mode Site Settings and
  Add page are hidden. The left group becomes the editing toolbar: "Source • Ctrl⇧2", "Structure •
  Ctrl⇧3" (the page outline), "Blocks • Ctrl⇧4", "Configure • Ctrl⇧5", "Undo • Ctrl Z", "Redo • Ctrl⇧Z",
  "Cancel • Ctrl⇧/", and Edit becomes "Save • Ctrl⇧S". The right group stays, including Preview. The
  Configure panel opens on the left, and the edited page gets a header row with status pills
  (Published, Unlocked, tags, path) and Page settings.
- **Look at**: inventory state `edit-mode`.

### What a visitor sees is its own capture, not a cropped logged-in one

- **Seen**: a visitor view drawn by cutting the top bar off a logged-in capture. The theme
  still drew its logged-in extras (page pencils, unpublished pages) because themes key them on
  `is-logged-in`.
- **Real**: use inventory state `site-view-visitor`, which loads the site in a browser context that
  never logged in. Since https://github.com/haxtheweb/webcomponents/pull/1210 the editor also has
  Preview (Ctrl⇧8). It keeps you logged in but turns `is-logged-in` off for the theme and folds the
  bar into a flag at the top right. A prototype of something seen while previewing starts from that
  state, not from the visitor capture.
- **Look at**: inventory state `site-view-visitor`.

### The DDD block header does not wrap its actions

- **Seen** (2026-11-09): a text action in the block header at phone
  width squeezed the title into a one-word column.
- **Real**: `.ddd-block-header` keeps chip, text and actions on one row. At narrow widths, text
  actions go icon-only (visible text moved to `.sr-only`), as the real players' headers do.
- **Look at**: `d-d-d/lib/DDDBlock.js` in the build.

### clean-one scrolls inside its own container

- **Seen** (2026-11-09): a full-page capture of a long clean-one page was still one
  viewport tall.
- **Real**: clean-one's content area scrolls itself. Use the inventory's `--viewport-height` to get
  content below the fold in frame.

### Switching color scheme makes HAX respond

- **Seen**: dark screenshots taken by flipping `prefers-color-scheme` on a loaded page, which shows a
  toast that a user loading the page in dark mode does not see.
- **Real**: the inventory loads each variant fresh with the scheme already set. Do the same for any
  capture you take yourself.
- **Also**: HAX saves the visitor's choice in localStorage (`app-hax-darkMode`), and a saved choice
  wins over `prefers-color-scheme`. Inventories before https://github.com/haxtheweb/haxcms-nodejs/pull/205
  produced dark `mobile-light` captures because of it; recapture anything made from those.

### Some themes open on a listing, not the page

- **Seen** (2026-11-09): `site-view-visitor` captures of journey-theme and haxor-slevin showed the
  blog / timeline listing and simple-blog showed an empty front page, so the fixture page's content
  was never in frame. A page script that routed by a guessed URL slug then captured "Page not found".
- **Real**: these themes show a listing at the site root. Open the page the way a reader does (click
  its link, or route to the item's real `slug` from the site store) in `--page-script`, and have the
  script throw when the page's content is not visible so a wrong capture fails instead of passing.
- **Look at**: the theme's front page in the inventory screenshots before building on them.

