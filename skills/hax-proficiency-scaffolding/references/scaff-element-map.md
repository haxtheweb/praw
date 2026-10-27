# SCAFF dials and learning-loop steps → HAX elements

Every tag below exists in `haxtheweb/webcomponents` (https://github.com/haxtheweb/webcomponents)
and is HAX-authorable. Do not substitute tags that are not listed here; check `wc-registry.json`
on the site when in doubt.

The question elements `multiple-choice`, `true-false-question`, `short-answer-question`,
`sorting-question`, `matching-question`, `tagging-question`, `fill-in-the-blanks` and `mark-the-words` share one base
(`QuestionElement`), so they share these controls:

| Control | What it does |
|---|---|
| `max-attempts="N"` | Limits tries; omitted or 0 means unlimited |
| `randomize` | Shuffles answer order on each load |
| `<div slot="feedbackIncorrect">` | Shown after a wrong answer |
| `<div slot="feedbackCorrect">` | Shown after a right answer |
| `<div slot="hint">` | Shown under "Need a hint?" after a wrong answer |
| `<div slot="evidence">` | Shown after a right answer (why it is right, supporting source) |
| `<div slot="content">` | Related content, always available in a collapsed area |

## Stress

| Setting | HAX control |
|---|---|
| None | Questions with no `max-attempts`; `concept-map-game` (explore, nothing to lose) |
| Time awareness | A visible expected time in the page intro or a `stop-note` ("about 5 minutes") |
| Consequences | `max-attempts` 2–3; `concept-quest-game` (wrong answers cost a heart; recap shows tries) |
| Time pressure | `concept-runner-game` (`duration` seconds, default 20, sorting good from bad concepts at speed) |
| High stakes | Graded GRASPS task from `hax-ubd-stage2`; single attempt (`max-attempts="1"`) |

Never add stress on a learner's first exposure to a concept, and keep it out of advanced-beginner checks.

## Complexity (worked example → completion → problem)

| Setting | HAX pattern |
|---|---|
| Worked example | Full solution shown step by step: ordered list or `lrndesign-sidenote` / `stop-note` per step; `video-player` with `start-time` / `end-time` for one demonstration; `code-sample` for code |
| Completion problem | Learner finishes a partly worked example: `fill-in-the-blanks` (missing steps or terms), `sorting-question` (put the steps in order), `fill-in-the-blanks` over a `code-sample`-style snippet for code |
| Conventional problem | Learner solves it unaided: `short-answer-question`, `multiple-choice` on a new case |
| Inverse / ill-defined problem | Case page with symptoms or outcomes; learner works back to causes; answer in `short-answer-question` or a rubric-scored task (`editable-table` rubric) |
| Novel, ambiguous problem | GRASPS performance task from `hax-ubd-grasps`, scored with a rubric; peer or self review |

Fade one step at a time: example → example → completion → completion → problem (Renkl & Atkinson, 2003).

## Assistance

| Setting | HAX control |
|---|---|
| High (orienting) | `lrndesign-imagemap` hotspots on the parts that matter; `stop-note` with "what to look for"; labeled `media-image`; `lrn-vocab` for key terms |
| Medium (on request) | `a11y-collapse` with `heading-button` titled "Show me how" / "Need a refresher?"; `hint` slot |
| Low (strategic) | `hint` slot that names a strategy or a cue to check, never the answer |
| None | No `hint` slot; debrief in an `a11y-collapse` placed after the task |

## Feedback

| Setting | HAX control (see `hax-feedback-design` for wording) |
|---|---|
| Outcome | Default right/wrong message plus `feedbackIncorrect` stating the correct response |
| Elaborative | `feedbackIncorrect` and `feedbackCorrect` explain why; `evidence` cites the source |
| Facilitative | `feedbackIncorrect` gives advice or a suggestion and invites another try |
| Strategy (immediate) | `hint` slot points to a strategy or cue; feedback slots do not give the answer |
| Strategy (delayed) | No in-item feedback; a debrief section or page after the task points out inconsistencies; `self-check` reveals an expert's reasoning to compare against |

## Fidelity (replaces the paper's XR form-factor row)

| Level | HAX media |
|---|---|
| Low | Plain text, a simple diagram, one focused `media-image` |
| Medium | `lrndesign-imagemap` on a real photo, `image-compare-slider` (before/after, normal/fault), short `video-player` segments |
| High | Real-world footage, real documents and data, `h5p-element` interactive simulations, field tasks via `worksheet-download` |

Novices get low fidelity even when high-fidelity media exists: realistic detail they cannot yet filter adds extraneous load.
For physical skills, name where hands-on practice happens; a web page alone is not embodied practice.

## Learning-loop steps

| Step | HAX pattern |
|---|---|
| Situate | Page intro with a short scenario; `media-image` or `video-player` of the real setting |
| Orient | `stop-note` (objective + what to look for); `lrndesign-imagemap` hotspots |
| Observe | Worked example; `video-player` demonstration segment |
| Guide | Modeled steps then `sorting-question` to imitate the order |
| Organize | `matching-question` / `tagging-question` to classify situations; an `editable-table` "if you see / do this" table |
| Give autonomy | `a11y-tabs` offering case choices; help in `a11y-collapse` on request |
| Embody | `h5p-element` simulation, or a `worksheet-download` field or lab task with a follow-up check (for code, link to a sandbox; `code-editor` is not HAX-authorable) |
| Goal-orient | `short-answer-question` or prompt asking the learner to state the goal for the case |
| Generalize | Two or more contrasting cases side by side (`image-compare-slider`, `a11y-tabs`) |
| Challenge / Create | GRASPS task (`hax-ubd-grasps`) |
| Reflect | `self-check` (prompt, then reveal an expert's reflection), `stop-note` prompt, `self-reflective-nudge` (see `hax-reflection-prompts`) |
| Appraise | Question elements at the stage's level (crosswalk) |
| Repeat | `flash-card` / `flash-card-set`, `concept-quest-game`, later retrieval items (see `hax-practice-and-retrieval`) |

## Routing for mixed audiences

```html
<self-reflective-nudge input="grade" prompt="How did you do on the pre-check above?">
  <p data-max-value="1" data-link="{refresher-page-slug}">Start with the refresher page.</p>
  <p data-min-value="2" data-max-value="3">Continue to the next page.</p>
  <p data-min-value="4" data-link="{challenge-page-slug}">Skip ahead to the challenge case.</p>
</self-reflective-nudge>
```

`input` is `grade` (F–A, values 0–4) or `mood` (five faces, values 0–4). Each nudge child takes
`data-min-value` / `data-max-value` and an optional `data-link`, which becomes a plain link:
use the target page's relative path (its slug) or a full URL.
