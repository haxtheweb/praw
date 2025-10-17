# GitHub Issue Management & Analysis

This module provides comprehensive GitHub issue tracking, analysis, and automation capabilities designed to help maintain visibility into project health and productivity.

## Features

- **Bulk Issue Fetching**: Download and cache all GitHub issues locally
- **Advanced Querying**: Search, filter, and analyze issues with rich CLI tools
- **Analytics**: Generate statistics, trends, and productivity reports
- **Automation Ready**: Designed for integration with posting and notification systems
- **Offline Capability**: Work with cached data without API rate limit concerns

## Quick Start

### 1. Fetch Issue Data
```bash
./fetch_issues.sh
```

This downloads all issues from the configured GitHub repository and saves them locally with full metadata.

### 2. Explore Your Data
```bash
# View overall statistics
./query_issues.sh stats

# Search for specific topics
./query_issues.sh search "accessibility"

# View recent activity
./query_issues.sh recent 10
```

### 3. Automated Workflow
```bash
./weekly-post.sh
```

This runs a complete workflow: fetch data → analyze → generate content → post to social media.

## Core Scripts

### `fetch_issues.sh` - Data Collection

Downloads all GitHub issues with complete metadata including:
- Issue numbers, titles, descriptions
- States (open/closed), labels, assignees
- Creation and update timestamps  
- Author information and URLs

**Usage:**
```bash
./fetch_issues.sh
```

**Output Files:**
- `issues_data/all_issues_TIMESTAMP.json` - Complete issue dump
- `issues_data/latest_issues.json` - Symlink to most recent data
- `issues_data/issues_summary_TIMESTAMP.md` - Human-readable summary

### `query_issues.sh` - Interactive Analysis

Provides comprehensive issue exploration and filtering capabilities.

**Commands:**
```bash
./query_issues.sh stats           # Show comprehensive statistics
./query_issues.sh search "term"   # Search titles and descriptions
./query_issues.sh number 123      # Get specific issue details
./query_issues.sh state open      # Filter by state (open/closed)
./query_issues.sh author username # Filter by author
./query_issues.sh recent [N]      # Show N most recent issues
./query_issues.sh labels          # List all unique labels
./query_issues.sh label "bug"     # Filter by specific label
```

**Example Analytics Output:**
```
📊 GitHub Issues Statistics

Total Issues: 2,847
Open Issues: 234
Closed Issues: 2,613

📈 Top 10 Authors:
  btopro: 1,847
  agent-contributions: 456
  community-user: 127

🏷️ Top 10 Labels:
  enhancement: 534
  bug: 423
  pillar: accessibility: 234
```

### `weekly-post.sh` - Automation Workflow

Complete automation pipeline that:
1. Fetches latest issue data
2. Checks LinkedIn configuration
3. Generates productivity summaries
4. Posts to social media (with approval)

**Features:**
- Dependency checking (Node.js, jq, GitHub CLI)
- Token expiry management
- Interactive LinkedIn setup if needed
- Final activity summary and statistics

## Configuration

### GitHub Repository Setup

By default, the scripts target the `haxtheweb/issues` repository. To modify:

1. Edit `REPO` variable in `fetch_issues.sh`:
   ```bash
   REPO="your-org/your-repo"
   ```

2. Ensure GitHub CLI (`gh`) is authenticated:
   ```bash
   gh auth login
   ```

### Data Storage

All issue data is stored locally in `issues_data/`:
```
issues_data/
├── all_issues_20240315_143022.json    # Timestamped snapshots
├── all_issues_20240316_091544.json
├── latest_issues.json -> all_issues_20240316_091544.json
└── issues_summary_20240316_091544.md  # Human-readable summary
```

## Advanced Usage

### Custom Analysis Scripts

The JSON data structure allows for powerful custom analysis:

```bash
# Issues created in the last 7 days
jq '[.[] | select(.createdAt > (now - 7*24*3600 | strftime("%Y-%m-%dT%H:%M:%SZ")))]' issues_data/latest_issues.json

# Resolution time analysis
jq '[.[] | select(.state == "CLOSED") | {number, created: .createdAt, closed: .updatedAt}]' issues_data/latest_issues.json

# Label popularity over time
jq '[.[] | .labels[]?.name] | group_by(.) | map({label: .[0], count: length}) | sort_by(.count) | reverse' issues_data/latest_issues.json
```

### Integration with External Tools

**Export for Spreadsheet Analysis:**
```bash
# CSV export of key metrics
jq -r '["Number","Title","State","Author","Created","Labels"], (.[] | [.number, .title, .state, .author.login, .createdAt, ([.labels[]?.name // empty] | join(";"))]) | @csv' issues_data/latest_issues.json > issues_export.csv
```

**Generate Reports:**
```bash
# Monthly productivity report
./query_issues.sh recent 100 | grep "$(date +%Y-%m)" > monthly_report.txt
```

## Data Analysis Capabilities

### Productivity Metrics

The scripts automatically calculate:
- **Issue Velocity**: Creation vs. resolution rates
- **Completion Rates**: Percentage of issues resolved
- **Category Distribution**: Types of work being done
- **Author Contributions**: Individual and team productivity
- **Trend Analysis**: Week-over-week changes

### Content Generation

Designed for integration with social media posting:
- **Weekly Summaries**: Automated productivity reports
- **Milestone Celebrations**: Achievement highlighting
- **Project Health**: Overall status communication
- **Community Recognition**: Contributor acknowledgments

## Automation Integration

### Cron Job Setup

For automated weekly reports:
```bash
# Edit crontab
crontab -e

# Add weekly execution (Mondays at 9 AM)
0 9 * * 1 /path/to/praw/programs/issue-management/weekly-post.sh

# Or daily data updates (6 AM daily)
0 6 * * * /path/to/praw/programs/issue-management/fetch_issues.sh
```

### Integration with LinkedIn Module

```bash
# Manual workflow
./fetch_issues.sh
cd ../linkedin
./linkedin  # Uses fresh issue data

# Automated workflow  
./weekly-post.sh  # Handles everything
```

### Custom Notifications

Example Slack integration:
```bash
# After running analysis
STATS=$(./query_issues.sh stats)
curl -X POST -H 'Content-type: application/json' \
  --data "{\"text\":\"Weekly Issue Report:\n$STATS\"}" \
  YOUR_SLACK_WEBHOOK_URL
```

## Troubleshooting

### Common Issues

**"Command not found: gh"**
- Install GitHub CLI: Follow [official instructions](https://cli.github.com/)
- Authenticate: `gh auth login`

**"Permission denied" errors**
- Verify repository access with current GitHub token
- Check if repository is public or if you have access

**"Rate limit exceeded"**
- GitHub CLI handles rate limits automatically
- For heavy usage, consider GitHub Apps for higher limits

**Empty or incomplete data**
- Check network connectivity
- Verify repository name and permissions
- Review GitHub API status

### Performance Considerations

- **Large Repositories**: First fetch may take several minutes
- **Storage**: Each snapshot is ~1-10MB depending on issue count
- **API Limits**: GitHub CLI manages rate limits automatically
- **Update Frequency**: Daily updates are usually sufficient

### Data Integrity

The scripts include:
- **Validation**: JSON syntax checking on all outputs
- **Backup**: Timestamped snapshots prevent data loss
- **Recovery**: Manual cleanup commands for corrupted data

```bash
# Clean up corrupted files
rm issues_data/latest_issues.json
./fetch_issues.sh  # Re-fetch clean data
```

## Agent Integration Guidelines

When helping users with issue management:

### Setup Assistance
1. Verify GitHub CLI installation and authentication
2. Test repository access and permissions
3. Run initial data fetch and verify results
4. Explain data storage and privacy implications

### Analysis Support
1. Help interpret statistics and trends
2. Create custom queries for specific insights
3. Generate reports for stakeholder communication
4. Identify productivity improvement opportunities

### Automation Guidance
1. Set up appropriate cron schedules
2. Configure notification integrations
3. Design custom analysis workflows
4. Balance automation with manual oversight

---

*This issue management system provides comprehensive project visibility while respecting GitHub API limits and user privacy.*