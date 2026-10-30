# PACE: issue-closure velocity by major release (1 → 26.10)

## Scope and method
- Major-version boundaries were taken from `haxtheweb/haxcms-php` tags so the `1..10` baseline could be included.
- For each major, the boundary uses the **first available tag in that major**.
  - Example: major `5` uses `5.1.0` because no `5.0.0` tag exists.
- Closed-issue counts are from the unified queue `haxtheweb/issues` using:
  - `repo:haxtheweb/issues is:issue is:closed closed:<start>..<end>`
- Time normalization:
  - `months = days / 30.4375`
  - `issues_per_month = closed_issues / months`
- Missing major tags: `12..24` (so there is a direct jump interval `11 -> 25`).
- Minor tag `26.7.0` was never created; the `26.x` series jumped from `26.0.0` to `26.8.x`. The interval formerly measured against a running `26.7.0` end date has been **re-anchored to `26.8.2`**, so every interval again starts and ends on a real tag.
- Release `26.10.0` is **not yet tagged**; the interval `26.8.2 -> 26.10` counts every issue closed since `26.8.2` up to a running end date (`2026-10-30T18:31:34Z`). Counts and rates will keep changing until the tag is cut.

## Interval data
| Interval | Start tag | Start date (UTC) | End tag | End date (UTC) | Days | Months | Closed issues | Issues / month |
|---|---|---|---|---|---:|---:|---:|---:|
| 1 -> 2 | 1.0.0 | 2020-01-29T05:34:52Z | 2.0.0 | 2021-01-07T21:21:38Z | 344.66 | 11.32 | 324 | 28.61 |
| 2 -> 3 | 2.0.0 | 2021-01-07T21:21:38Z | 3.0.0 | 2021-08-16T20:08:59Z | 220.95 | 7.26 | 275 | 37.88 |
| 3 -> 4 | 3.0.0 | 2021-08-16T20:08:59Z | 4.0.0 | 2022-03-11T14:23:47Z | 206.76 | 6.79 | 149 | 21.93 |
| 4 -> 5 | 4.0.0 | 2022-03-11T14:23:47Z | 5.1.0 | 2022-08-18T18:54:10Z | 160.19 | 5.26 | 42 | 7.98 |
| 5 -> 6 | 5.1.0 | 2022-08-18T18:54:10Z | 6.0.1 | 2023-01-06T20:39:31Z | 141.07 | 4.63 | 191 | 41.21 |
| 6 -> 7 | 6.0.1 | 2023-01-06T20:39:31Z | 7.0.1 | 2023-06-01T20:35:17Z | 146.00 | 4.80 | 294 | 61.29 |
| 7 -> 8 | 7.0.1 | 2023-06-01T20:35:17Z | 8.0.0 | 2023-12-21T17:44:27Z | 202.88 | 6.67 | 289 | 43.36 |
| 8 -> 9 | 8.0.0 | 2023-12-21T17:44:27Z | v9.0.0 | 2024-07-12T21:18:57Z | 204.15 | 6.71 | 200 | 29.82 |
| 9 -> 10 | v9.0.0 | 2024-07-12T21:18:57Z | 10.0.0 | 2024-12-20T19:33:04Z | 160.93 | 5.29 | 175 | 33.10 |
| 10 -> 11 | 10.0.0 | 2024-12-20T19:33:04Z | 11.0.0 | 2025-06-06T14:43:43Z | 167.80 | 5.51 | 167 | 30.29 |
| 11 -> 25 | 11.0.0 | 2025-06-06T14:43:43Z | v25.0.0 | 2026-01-09T18:10:25Z | 217.14 | 7.13 | 233 | 32.66 |
| 25 -> 26 | v25.0.0 | 2026-01-09T18:10:25Z | 26.0.0 | 2026-05-12T19:55:56Z | 123.07 | 4.04 | 258 | 63.81 |
| 26 -> 26.8.2 | 26.0.0 | 2026-05-12T19:55:56Z | 26.8.2 | 2026-09-17T19:24:23Z | 127.98 | 4.20 | 329 | 78.25 |
| 26.8.2 -> 26.10 | 26.8.2 | 2026-09-17T19:24:23Z | 26.10.0 | 2026-10-30T18:31:34Z (running) | 42.96 | 1.41 | 125 | 88.56 |

## Rate-change summary
- Baseline from `1 -> 10` (average of `1->2` through `9->10`): **33.91 issues/month**
- Last two release intervals:
  - `26 -> 26.8.2`: **78.25 issues/month** (**+130.75%** vs `1->10` baseline)
  - `26.8.2 -> 26.10`: **88.56 issues/month** (**+161.17%** vs `1->10` baseline, provisional)
- Increase from `26 -> 26.8.2` to `26.8.2 -> 26.10`: **+13.19%** issues/month
- Average of last two intervals vs `1->10` baseline: **+145.96%**

## Exponential fits
### Full-series fit (all measured intervals)
- Model: `rate(i) = a * e^(b*i)`
- Coefficients:
  - `a = 19.6478`
  - `b = 0.08435`
- Equation:
  - `rate(i) = 19.6478 * e^(0.08435*i)`
- Fit quality:
  - `R² (log-space) = 0.3430`
- Interpretation:
  - Implied multiplicative growth per interval: `e^b = 1.0880` (~`+8.80%` per interval); the re-anchored `26.x` intervals sit above the trend but no longer spike as sharply as the short running `26.7.0` window did.

### Recent-trend fit (25 -> 26, 26 -> 26.8.2, 26.8.2 -> 26.10)
- Model: `rate(j) = a * e^(b*j)` where `j=1` for `25->26`.
- Coefficients:
  - `a = 54.8891`
  - `b = 0.16392`
- Equation:
  - `rate(j) = 54.8891 * e^(0.16392*j)`
- Fit quality:
  - `R² (log-space) = 0.9805`
- Interpretation:
  - Implied multiplicative growth per interval: `e^b = 1.1781` (~`+17.81%` per interval) in the recent regime. Re-anchoring to the real `26.8.2` tag flattens the trend: the earlier `+78.80%` per-interval figure was inflated by the short, untagged `26.7.0` window. The `26.8.2 -> 26.10` point is provisional until the tag is cut.
