---
name: hax-issue-analysis
description: >
  Fetch, analyze, and summarize GitHub issues across the HAX ecosystem using the unified
  issue queue. Use when tracking bugs, planning sprints, generating weekly productivity
  reports, or creating social media content from project activity.
version: 1.0.0
license: Apache-2.0
metadata:
  author: haxtheweb
  tags: [hax, issues, github, analysis, automation, reporting]
---

# HAX Issue Analysis

Fetch, analyze, and summarize GitHub issues across the HAX ecosystem using the unified issue queue.

## When to Use

- Fetching and caching all issues from the HAX ecosystem
- Analyzing project statistics and issue trends
- Generating weekly productivity reports
- Creating social media content from project activity
- Searching for specific issues by keyword, author, state, or label
- Planning sprints based on open issue backlog

## How It Works

1. **Fetch Issues**: Run `cd programs/issue-management/ && ./fetch_issues.sh` to download and cache GitHub issues from the unified issue queue at `~/Documents/git/haxtheweb/issues`.
2. **Query Issues**: Use `./query_issues.sh` with subcommands:
   - `stats` — View project statistics and issue counts
   - `search <term>` — Search issues by keyword
   - `author <name>` — Filter by author
   - `state <open|closed>` — Filter by issue state
   - `recent <n>` — Show last N issues
3. **Generate Reports**: Use `./weekly-post.sh` for automated weekly productivity summaries.
4. **LinkedIn Integration**: Pipe issue stats into LinkedIn posting automation:
   ```bash
   cd programs/issue-management/
   ./query_issues.sh stats > weekly_stats.txt
   cd ../linkedin/
   cat ../issue-management/weekly_stats.txt | node post-to-linkedin.js --stdin
   ```

## Data Collection

When analyzing issues:
- Identify trends in issue creation and resolution
- Highlight productivity patterns over time
- Flag high-priority or security-related issues
- Group issues by repository, label, or category

## Content Generation

Transform issue data into engaging outputs:
- Weekly progress summaries for social media
- Project health reports for stakeholders
- Sprint planning insights for team meetings
- Data-driven blog posts about ecosystem development

## Automation Setup

For recurring analysis:
- Configure cron jobs for regular issue fetching
- Set up monitoring for issue pattern changes
- Create custom analysis scripts for domain-specific metrics
- Integrate with LinkedIn posting for automated updates

## Privacy & Security

- Credentials are stored in the user's home directory (not version controlled)
- Respect user content approval preferences before posting
- Provide manual fallbacks when API calls fail
- Never include sensitive issue details in public posts without review

## Dependencies

- Node.js (for LinkedIn scripts)
- GitHub CLI (`gh` command)
- `jq` (for JSON processing)
- `curl` (for API calls)

## Scripts

- `programs/issue-management/fetch_issues.sh` — Issue data collection
- `programs/issue-management/query_issues.sh` — Issue analysis and search
- `programs/issue-management/weekly-post.sh` — Automated weekly posting
- `programs/linkedin/post-to-linkedin.js` — Social media posting
- `programs/linkedin/setup-linkedin.js` — LinkedIn API configuration

## References

- For issue query syntax: `references/issue-query-syntax.md`
- For LinkedIn posting templates: `references/linkedin-templates.md`
