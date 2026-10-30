---
name: siip-course-alignment
description: "Align a course with an open source project using the Sustainable Impact and Innovation Pipeline (SIIP): map course objectives to real contribution paths, shape a 40/20/20/20 term, and plan the lab, club and onboarding loop. Use for \"align my course with an open source project\", \"students contributing to OSS\", \"SIIP\" or \"turn class projects into real contributions\"."
version: 1.0.0
license: Apache-2.0
metadata:
  author: PRAW
  tags: [siip, open-source, course-design, cognitive-apprenticeship, experiential-learning, community, hax]
  requirements: "A course (syllabus, objectives or outline) and an open source project (repo URL or description). Produces a plan; does not edit the course or the project."
---

# SIIP Course Alignment

The Sustainable Impact and Innovation Pipeline (SIIP) turns a course into a contributor pipeline for an open source project without turning the course into "the project class." Students learn the discipline; the project supplies real problems. HAX used it to keep shipping with a single full-time developer ([recording](https://www.youtube.com/watch?v=TNF0uzYi9Kk)). The method and its evidence are summarized in https://github.com/haxtheweb/praw/blob/main/WORLDVIEW.md (pillar 8).

## When to use

- A faculty member wants course projects that count in the real world.
- An open source project (HAX or any other) needs a sustainable stream of contributors.
- Designing an independent study, internship track or student-club partnership around a project.

## When not to use

- Designing a unit's learning outcomes from scratch: use `hax-ubd-backward-design` first, then align it here.
- The project has no public issue queue or can't accept outside contributions yet: fix onboarding first (step 2).

## Inputs

1. The course: level, objectives, length, current projects and assessments.
2. The project: repo or issue queue URL, tech stack, where newcomers struggle.
3. The people: who teaches, who maintains, and any clubs, labs or internship requirements available.

Ask for whatever is missing in one short round of questions, then proceed.

## Method

1. **Find the overlap.** List the course objectives and the project's open needs side by side (issues, docs gaps, design, accessibility, security, tests). Mark each need with the objective it exercises. Keep only needs that genuinely teach an objective; the course's own goals come first.
2. **Check onboarding.** Can someone with no context install the project and make a first change from the docs alone? Try it, or have an agent try it. List every stumble; fixing those docs is itself a first contribution. Label beginner issues (`good first issue`, `student`).
3. **Shape the term (40/20/20/20).**
   - ~40%: skill up to contributor level while meeting the course objectives. Heavy scaffolding, modeling and live demos on the real codebase.
   - ~20%: a simple project that isn't community-related, to practice the full workflow safely.
   - ~20%: a larger project tied to the project's needs, with less scaffolding.
   - ~20%: an unscaffolded, internship-like contribution chosen from the overlap list.
4. **Make thinking visible (cognitive apprenticeship).** For each phase, say how the instructor will *model* (narrate decisions, not just steps), *scaffold*, *fade* support, and *coach* (task choice, hints, feedback, rising challenge). Plan collaboration and whiteboard time.
5. **Build the loop beyond the course.** Name the paths for students who want more: independent study, internship (with hours), lab, and clubs whose interests match (security, UX, design). Plan regular open office hours. Plan how this term's best contributions become next term's examples and tooling.
6. **Incentives and credit.** Real work experience, public credit (posts that tag students, with permission), course credit, internship hours, community roles. Never make contribution to a specific project a grading requirement students can't opt out of; offer an equivalent path.
7. **Measure.** Track contributions merged, students continuing to the lab or club, onboarding stumbles fixed, and where students go next. Expect the biggest gains 6–12 months after the course, and the top 5–10% of a class to go further.

## Output

A plan with these sections:

- **Overlap map**: table of course objective → project need → issue or area → difficulty.
- **Onboarding fixes**: stumbles found and the first-contribution issues they become.
- **Term outline**: the four phases with weeks, deliverables and scaffolding level, plus modeling, scaffolding, fading and coaching notes for each.
- **Beyond the course**: lab, internship, club and office-hour paths, and how contributions feed back into the next term.
- **Credit and incentives**, including the opt-out path.
- **Measures** to track.

## Gotchas

- The project is the backdrop, not the subject. If the syllabus starts reading like project documentation, pull back to the discipline.
- Don't promise maintainers' review time that doesn't exist; agree on review capacity before the term starts.
- Student work goes public. Confirm license, contributor agreement (CLA or DCO) and students' consent to be named before anything is posted.
- Early cohorts see small returns; the spiral grows over several semesters. Plan for at least a year.

## References

- Pillar 8 and the cognitive apprenticeship table: https://github.com/haxtheweb/praw/blob/main/WORLDVIEW.md
- Evidence and stories: https://github.com/haxtheweb/praw/blob/main/WINS.md
- Talk notes: https://github.com/haxtheweb/praw/blob/main/talks/README.md
- Related skills: `hax-ubd-backward-design` (outcomes), `hax-proficiency-scaffolding` (learner stage), `hax-reflection-prompts` (reflection on contributions)
