# Deviation log

Mistakes prototypes have made about HAXcms, and what is actually true. Read this before every new
prototype. Each entry says what was wrong, what is real (checked against the UI inventory on the date
given), and where to look. When the same mistake shows up twice, propose a rule in RULES.md.

When the UI changes, update or retire the entry instead of leaving it stale: an entry here is a claim
about the product too.

## Entries

### Outline opens inside Site Settings, not as its own dialog

- **Seen**: prototypes drawing Outline as a separate modal or page.
- **Real** (inventory, 2026-11-06): the top bar's Outline control opens the one Site Settings dialog
  at **Structure** (breadcrumb "Site Settings / Structure"), with the admin rail on the left.
- **Look at**: inventory state `outline`.

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

### Top bar labels include their shortcut

- **Seen**: "Edit", "Outline", "Site Settings" as bare labels.
- **Real** (inventory, 2026-11-06): "Edit • Ctrl⇧E", "Add page • Ctrl⇧1", "Outline • Ctrl⇧2",
  "Site Settings • Ctrl⇧3"; Merlin uses the `hax:wand` icon.
- **Look at**: inventory state `site-view`, `dom.json` labels and icons.

### Edit mode replaces the top bar's controls

- **Seen**: edit mode drawn as the site-view top bar plus a Save button.
- **Real** (inventory, 2026-11-06): in edit mode the left of the bar becomes the editing toolbar:
  "Source • Ctrl⇧1", "Structure • Ctrl⇧2", "Blocks • Ctrl⇧3", "Configure • Ctrl⇧4", "Undo • Ctrl Z",
  "Redo • Ctrl⇧Z", "Cancel • Ctrl⇧/", "Save • Ctrl⇧S" (Edit becomes Save). Add page, Outline and Site
  Settings stay on the right but are dimmed. The Configure panel opens on the left, and the edited page
  gets a header row with status pills (Published, Unlocked, tags, path) and Page settings.
- **Look at**: inventory state `edit-mode`.

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
