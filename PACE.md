# PACE: issue-closure velocity by major release (1 → 26)

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

## Rate-change summary
- Baseline from `1 -> 10` (average of `1->2` through `9->10`): **33.91 issues/month**
- Last two release intervals:
  - `11 -> 25`: **32.66 issues/month** (**-3.69%** vs `1->10` baseline)
  - `25 -> 26`: **63.81 issues/month** (**+88.16%** vs `1->10` baseline)
- Increase from `11 -> 25` to `25 -> 26`: **+95.37%** issues/month
- Average of last two intervals vs `1->10` baseline: **+42.24%**

## Exponential fits
### Full-series fit (all measured intervals)
- Model: `rate(i) = a * e^(b*i)`
- Coefficients:
  - `a = 22.6955`
  - `b = 0.05434`
- Equation:
  - `rate(i) = 22.6955 * e^(0.05434*i)`
- Fit quality:
  - `R² (log-space) = 0.1330`
- Interpretation:
  - Implied multiplicative growth per interval: `e^b = 1.0558` (~`+5.58%` per interval), but weak overall fit due nonlinear jumps.

### Recent-trend fit (10 -> 11, 11 -> 25, 25 -> 26)
- Model: `rate(j) = a * e^(b*j)` where `j=1` for `10->11`.
- Coefficients:
  - `a = 18.9007`
  - `b = 0.37255`
- Equation:
  - `rate(j) = 18.9007 * e^(0.37255*j)`
- Fit quality:
  - `R² (log-space) = 0.8250`
- Interpretation:
  - Implied multiplicative growth per interval: `e^b = 1.4514` (~`+45.14%` per interval) in the recent regime.
