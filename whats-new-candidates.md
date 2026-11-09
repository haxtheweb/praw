# What's New / HAX Tips candidates

Draft entries for the What's New / HAX Tips system ([haxtheweb/issues#3172](https://github.com/haxtheweb/issues/issues/3172), tracking [haxtheweb/issues#3262](https://github.com/haxtheweb/issues/issues/3262)). These are candidates for a person to pick from, trim and give visuals before they become real entries. Nothing here is published.

Each entry has a tag (Idea, Feature, Block, Theme, Template or Improvement), a label, one plain-language line and the pull request(s) it came from.

## Merged 2026-11-02 to 2026-11-09

### Feature

- **Feature: My learning, for learners** — Learners open *My learning* from the user menu and see what they've done across a course, with a Map view that puts them at the centre and their pages done around them. Links: https://github.com/haxtheweb/webcomponents/pull/1110, https://github.com/haxtheweb/webcomponents/pull/1148
- **Feature: Learning activity report** — Site settings › Reports › Learning activity shows which elements on your site can record learner progress, page by page or for the whole site. Links: https://github.com/haxtheweb/webcomponents/pull/1115
- **Feature: Learner progress from the elements you already use** — Videos, slide decks, collapsed sections, image maps, questions and H5P now report meaningful learner moments (started, halfway, finished, opened) without flooding your data. Links: https://github.com/haxtheweb/webcomponents/pull/1099, https://github.com/haxtheweb/webcomponents/pull/1124, https://github.com/haxtheweb/webcomponents/pull/1126, https://github.com/haxtheweb/webcomponents/pull/1129, https://github.com/haxtheweb/webcomponents/pull/1130, https://github.com/haxtheweb/webcomponents/pull/1121, https://github.com/haxtheweb/webcomponents/pull/1120
- **Feature: Hear your course's pacing** — The new Cadence screen in Reports plays each lesson as a bar of music, so you can listen for a slow start, a clear peak and a calm finish. Links: https://github.com/haxtheweb/webcomponents/pull/1131
- **Feature: Check outside links and see edit history in Reports** — "Check outside links" finds broken and redirected links, and Freshness now shows each page's edit history instead of "Coming soon". Links: https://github.com/haxtheweb/webcomponents/pull/1146, https://github.com/haxtheweb/haxcms-nodejs/pull/183, https://github.com/haxtheweb/haxcms-php/pull/740
- **Feature: Compare two versions of a page** — Page history can now compare any two saved versions side by side and adds a note when you restore one. Links: https://github.com/haxtheweb/haxcms-nodejs/pull/166, https://github.com/haxtheweb/haxcms-php/pull/725
- **Feature: Pick icons by searching** — Icon fields in the HAX editor now have a searchable list that shows each icon next to its name. Links: https://github.com/haxtheweb/webcomponents/pull/1091
- **Feature: New site commands in the hax CLI** — `hax site site:validate` finds broken links, missing pages and unknown elements; `site:rebuild`, `site:archive` / `site:restore`, `site:logs`, `site:list`, `hax list` and shell completion join it. Links: https://github.com/haxtheweb/create/pull/106
- **Feature: Agents announce themselves to HAXcms** — The HAXcms MCP server follows each site's MCP policy and marks its calls as agent actions, and HAXcms now ships with MCP turned off until an admin turns it on. Links: https://github.com/haxtheweb/haxcms-mcp/pull/22, https://github.com/haxtheweb/haxcms-mcp/pull/23, https://github.com/haxtheweb/haxcms-nodejs/pull/173, https://github.com/haxtheweb/haxcms-php/pull/734

### Block

- **Block: Reading analysis** — A new learning activity: learners flag the sentences that are evidence for an idea, or select the passage that answers a question. Links: https://github.com/haxtheweb/webcomponents/pull/1112
- **Block: Compact learning blocks** — Questions, self-checks, stop notes, sidenotes and figure labels share one tidy frame, and answers show an icon and a word, not colour alone. Existing content keeps working. Links: https://github.com/haxtheweb/webcomponents/pull/1049, https://github.com/haxtheweb/webcomponents/pull/1119, https://github.com/haxtheweb/webcomponents/pull/1113
- **Block: Wide, narrow, wide layout** — Grid plate has a new 2-1-2 layout for a narrow column between two wide ones. Links: https://github.com/haxtheweb/webcomponents/pull/1123

### Theme

- **Theme: Easier long reads** — Clean One, Clean Two, Learn Two and Polaris Invent got a reading pass: comfortable line length, more line spacing and clearer links. Links: https://github.com/haxtheweb/webcomponents/pull/1053
- **Theme: Training theme scrolls on phones** — Pages in the training theme now scroll normally on phones. Links: https://github.com/haxtheweb/webcomponents/pull/1086
- **Theme: Start a custom theme from a complete starter** — `hax` can create a custom theme from a starter that already has the menu, breadcrumbs, regions, skip link and dark mode wired up, and `hax audit theme` checks your theme against that list. Links: https://github.com/haxtheweb/create/pull/107

### Template

- **Template: Site starters say what they're for** — Starter sites now have plain names (blog, portfolio, online course, club website, resume journey) and a description of what each one gives you. Links: https://github.com/haxtheweb/haxcms-nodejs/pull/186, https://github.com/haxtheweb/haxcms-php/pull/742, https://github.com/haxtheweb/haxcms-nodejs/pull/184, https://github.com/haxtheweb/haxcms-php/pull/741

### Improvement

- **Improvement: Pages appear faster, without jumping** — Sites show their first page sooner and stop shifting while HAXcms loads, and published pages download less. Links: https://github.com/haxtheweb/webcomponents/pull/1134, https://github.com/haxtheweb/webcomponents/pull/1136, https://github.com/haxtheweb/webcomponents/pull/1141, https://github.com/haxtheweb/webcomponents/pull/1074, https://github.com/haxtheweb/haxcms-nodejs/pull/178, https://github.com/haxtheweb/haxcms-nodejs/pull/179, https://github.com/haxtheweb/haxcms-php/pull/735, https://github.com/haxtheweb/haxcms-php/pull/736
- **Improvement: One look for HAX dialogs and the dashboard** — Editor dialogs, admin dialogs, image pop-ups, the site dashboard and its cards now share one consistent HAX UI. Links: https://github.com/haxtheweb/webcomponents/pull/1042, https://github.com/haxtheweb/webcomponents/pull/1095, https://github.com/haxtheweb/webcomponents/pull/1101, https://github.com/haxtheweb/webcomponents/pull/1103, https://github.com/haxtheweb/webcomponents/pull/1140, https://github.com/haxtheweb/webcomponents/pull/1114
- **Improvement: Clear choices when leaving unsaved work** — Buttons now say "Discard changes" or "Keep editing", read apart without colour, and saving an outline no longer asks you to discard it. Links: https://github.com/haxtheweb/webcomponents/pull/1105, https://github.com/haxtheweb/webcomponents/pull/1116, https://github.com/haxtheweb/webcomponents/pull/1154, https://github.com/haxtheweb/webcomponents/pull/1096
- **Improvement: Editors can search unpublished pages** — When you're logged in, site search includes pages that aren't published yet. Links: https://github.com/haxtheweb/haxcms-nodejs/pull/169, https://github.com/haxtheweb/haxcms-php/pull/728
- **Improvement: Fewer surprise logouts** — HAX no longer logs you out over errors a fresh login wouldn't fix, and logging out waits for the server to finish. Links: https://github.com/haxtheweb/webcomponents/pull/1064, https://github.com/haxtheweb/webcomponents/pull/1065, https://github.com/haxtheweb/webcomponents/pull/1093
- **Improvement: Cleaner saves** — Saving a page no longer adds another hidden fallback copy to elements each time. Links: https://github.com/haxtheweb/webcomponents/pull/1142
- **Improvement: Structure scrolls once** — The Structure screen has one scroll area, settings use the name System Settings and breadcrumbs are quieter. Links: https://github.com/haxtheweb/webcomponents/pull/1109
- **Improvement: Every create option on mobile** — The HAX dashboard shows all the ways to create a site on small screens. Links: https://github.com/haxtheweb/webcomponents/pull/1111
- **Improvement: Media you can pause and caption** — The video hero has an accessible pause button, GIF players show a visible title and caption, and image maps work from the keyboard. Links: https://github.com/haxtheweb/webcomponents/pull/1068, https://github.com/haxtheweb/webcomponents/pull/1125, https://github.com/haxtheweb/webcomponents/pull/1128
- **Improvement: Calmer motion** — Pulse animations play twice instead of forever, and not at all when you've asked for reduced motion. Links: https://github.com/haxtheweb/webcomponents/pull/1138
- **Improvement: Tables look the same everywhere** — Tables share one design, including inside apps. Links: https://github.com/haxtheweb/webcomponents/pull/1088
- **Improvement: Grade book fixes** — The grade book has a tidier toolbar and roster grid, plus bug fixes shared with grade book lite. Links: https://github.com/haxtheweb/webcomponents/pull/1098
- **Improvement: Small editor fixes** — The page-break colour picker is no longer empty, long page titles fit in the editing band, and toasts show your own character. Links: https://github.com/haxtheweb/webcomponents/pull/1107, https://github.com/haxtheweb/webcomponents/pull/1084, https://github.com/haxtheweb/webcomponents/pull/1090
- **Improvement: New admin words in 102 languages** — The new HAX UI admin text is translated into all 102 supported languages. Links: https://github.com/haxtheweb/webcomponents/pull/1102
- **Improvement: Security hardening** — Closed several cross-site scripting paths in elements, blocked `.git` exposure and required the install token for every installer step. Links: https://github.com/haxtheweb/webcomponents/pull/1143, https://github.com/haxtheweb/haxcms-nodejs/pull/180, https://github.com/haxtheweb/haxcms-php/pull/737

### Idea

- **Idea: New skills for agents that build with HAX** — PRAW gained skills for building learning-activity elements, building HAXcms prototypes on the real system, and turning a reading into paragraph-level notes. Links: https://github.com/haxtheweb/praw/pull/59, https://github.com/haxtheweb/praw/pull/62, https://github.com/haxtheweb/praw/pull/55
