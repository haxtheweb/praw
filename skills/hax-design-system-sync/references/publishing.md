# Publishing the DDD design system

`yarn design-system:sync` (in webcomponents) writes the complete design system to `elements/d-d-d/design-system/dist/`. That folder is gitignored and regenerated on every run.

## Who can publish

Publishing writes to a claude.ai **Design System** artifact, so it needs a Claude session with the Artifact tool, run by someone with edit access to that artifact. Other agents should stop after the sync and hand `dist/` to a maintainer who has that access.

## How

1. Publish only from `master` after the PRs merge, so the design system never shows values that aren't merged.
2. Read the existing artifact first, using the Artifact tool's `read` action with its URL. Ask the maintainer for the URL if you don't have it.
3. Publish the files under `dist/` to that URL as the artifact's data files (`project/…`).
   - **At most 255 files per call.** The sync output is about 350, so split it across calls to the same URL.
   - **`design-system.json` (the index) goes last**, after you read the artifact again, and in a call of its own.
4. Say what changed in one line: the token values, the cards added, and the bundle version (`globalThis.DDD.version`).

## Limits the sync already checks

| Limit | Value |
|---|---|
| `components/bundle.js` | 6 MB |
| `components/lib/*.js` (sheet-music, slide-deck) | 2 MB each |
| Every other file | 512 KB |
| Files per version / per publish call | 511 / 255 |
| Colours in `tokens.json` | 600 |
| Extra token families | 12 (it is at 12: adding one means merging two) |
| Paths | No `node_modules` segment (runtime files live in `runtime/nm/`) |
| Types | No `.pptx`, `.docx` or `.zip`; XML must not contain a DOCTYPE |
| Component names | `^[A-Za-z_$][A-Za-z0-9_$]{0,63}$` (cards are PascalCase; themes are `HaxTheme_<Name>`) |
