# Impact data

The numbers behind `WINS.md` and `visuals/`, kept as data so agents and people can refresh them instead of retyping figures.

Refresh everything from public sources:

```bash
GITHUB_TOKEN=<token> node scripts/impact-stats.mjs        # or: npm | velocity | prs | charts
```

A token is optional; without one, GitHub allows 60 requests an hour, which may not be enough. Behind a proxy, add `NODE_USE_ENV_PROXY=1`.

## Files

| File | What it is | Source |
| --- | --- | --- |
| `npm-downloads.json` | Weekly and monthly downloads for every `@haxtheweb` package, with totals | npm registry search, refreshed by the script |
| `release-velocity.csv` / `.svg` | Issues closed per month in `haxtheweb/issues` for each major HAX release window, plus the window from the newest tag to today | GitHub API, refreshed by the script |
| `merged-prs-by-month.csv` / `.svg` | Merged pull requests per month across webcomponents, haxcms-nodejs, haxcms-php, create, praw and issues | GitHub API, refreshed by the script |
| `siip-timeline.csv` | Yearly counts from the SIIP timeline slide (2008–2025) | Transcribed from the talk, legend confirmed by Bryan; update by hand |

## SIIP timeline columns

- `web_components`: web components (bricks) in the ecosystem
- `sites`: sites built with HAX (2021–22 estimated)
- `fulltime_psu_staff`: full-time Penn State staff on HAX
- `student_interns`: student interns
- `contributors_at_large`: all contributors, including staff and interns
- `students_in_bryans_classes`: students taught web components in Bryan's classes
- `students_educated_aa`: students educated that semester through HAX-based systems in Arts and Architecture only; the real reach is far higher
- `faculty_staff_using_hax_est`: faculty and staff who teach with or edit in HAX (estimate)

2025 class and student counts were projections when the slide was made. 2026 isn't charted the same way: at 400+ merged PRs a month the project is enhancing everything at once.

## Reading the numbers

- **Release windows** start at the first tag of each major version in webcomponents (majors 5, 6 and 12–24 have no tags, so some windows span several). The v25→v26 window reproduces the figure in *The Many Mes* exactly (258 issues, 63.8 a month). That talk's v26.0→v26.7 figure (104 a month) used a shorter window than the tags here.
- **Merged PRs** undercount history: for years most work went straight to the main branch without pull requests. The jump in late 2026 is real, but earlier months shouldn't be read as low activity.
- **npm downloads** include automated installs (CI, mirrors) and are a reach signal, not a user count. CDN traffic (jsDelivr, the Penn State CDN) isn't included.
- **No funding figures.** Wins are measured by what got built and who it helped (see `VOICE.md`).
