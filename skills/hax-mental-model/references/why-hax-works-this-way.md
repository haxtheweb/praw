# Why HAX works this way

The structure of HAX follows a small set of values (summarized from `WORLDVIEW.md` in this repo).
Knowing them lets you predict the right answer to a question the skills do not cover.

| Value | What it looks like in the platform |
|---|---|
| The web should stay open, ownable, and portable | Sites are plain files; content moves into and out of HAX; no vendor is required. |
| Authoring is decoupled from storage and backend | The editor and content model work across CMS, LMS, and static workflows. |
| Accessibility and OER are defaults | Components carry accessible structure so authors get it without extra effort. |
| Sustainable beats novel | Prefer standards (web components, JSON, HTML) over frameworks that may disappear. |
| Community is part of the architecture | Work happens in public issue queues; students and faculty contribute to real systems. |
| Education-led, not technology-led | Tools serve teaching and learning goals, and give educators agency. |

## How to use this when deciding

- Two options, one portable and one convenient but locked in: choose portable.
- A feature needs a server: check whether static files or a component can do it first.
- A shortcut skips accessibility: it is not a shortcut.
- A change helps one site: ask whether it belongs in a shared component instead.

## Further reading

- `WORLDVIEW.md` and `what-is-hax.md` at the repo root.
- Bryan Ollendyke's thesis on information altruism (PDF at the repo root).
