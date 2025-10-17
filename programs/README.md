# PRAW Programs Directory

This directory contains utility programs for agent automation and productivity enhancement. These tools are designed to help future agents assist users with various tasks including social media posting and project management.

## Overview

The programs directory is organized into specialized modules:

- **`linkedin/`** - LinkedIn posting automation
- **`issue-management/`** - GitHub issue tracking and analysis

## Quick Start Guide for Agents

### 1. LinkedIn Posting Automation

The LinkedIn module allows agents to help users automate content posting to LinkedIn, with both automatic issue-based and custom content modes.

#### Setup Process
1. **Navigate to LinkedIn directory:**
   ```bash
   cd programs/linkedin/
   ```

2. **Configure LinkedIn API (one-time setup):**
   ```bash
   node setup-linkedin.js
   ```
   
   This will guide the user through:
   - Creating a LinkedIn Developer App
   - Setting up API credentials
   - OAuth authentication flow
   - Storing secure tokens

#### Usage Scenarios

**A) Automatic Issue-Based Posts**
```bash
# Simple weekly productivity update
./linkedin

# Or directly call the script
node post-to-linkedin.js
```

**B) Custom Content Posts**
```bash
# Post custom content
node post-to-linkedin.js --custom "Just shipped a new web component! 🚀"

# Pipe content from conversations
echo "Summary of our accessibility discussion" | node post-to-linkedin.js --stdin
```

**C) Dry Run Mode**
```bash
# Generate content without posting (useful for review)
node post-to-linkedin.js --dry-run
```

#### For Agents: LinkedIn Integration Tips

1. **Help users with setup:**
   - Guide them through LinkedIn Developer App creation
   - Explain the OAuth flow clearly
   - Troubleshoot common API configuration issues

2. **Content assistance:**
   - Help craft engaging technical posts
   - Suggest relevant hashtags (#WebComponents #OpenSource #HAXTheWeb)
   - Optimize content length for LinkedIn's algorithm

3. **Automation recommendations:**
   - Weekly productivity posts work well for maintaining visibility
   - Custom posts for major milestones, releases, or insights
   - Combine with issue management for data-driven content

### 2. Issue Management System

The issue management module provides comprehensive GitHub issue tracking and analysis capabilities.

#### Core Scripts

**`fetch_issues.sh`** - Downloads and caches GitHub issues
```bash
cd programs/issue-management/
./fetch_issues.sh
```

**`query_issues.sh`** - Interactive issue exploration
```bash
# View statistics
./query_issues.sh stats

# Search issues
./query_issues.sh search "web component"

# Filter by author, state, labels, etc.
./query_issues.sh author btopro
./query_issues.sh state open
./query_issues.sh recent 20
```

**`weekly-post.sh`** - Automated weekly productivity posting
```bash
./weekly-post.sh
```

#### For Agents: Issue Management Assistance

1. **Data Collection:**
   - Help users understand their project metrics
   - Identify trends in issue creation and resolution
   - Highlight productivity patterns

2. **Content Generation:**
   - Transform issue data into engaging social posts
   - Create weekly/monthly progress summaries
   - Generate project health reports

3. **Automation Setup:**
   - Help configure cron jobs for regular posting
   - Set up monitoring for issue patterns
   - Create custom analysis scripts for specific needs

## Integration Patterns

### Cross-Module Integration

The LinkedIn and issue management modules are designed to work together:

1. **Automated Workflow:**
   ```bash
   cd programs/issue-management/
   ./fetch_issues.sh
   cd ../linkedin/
   ./linkedin  # Will use fresh issue data
   ```

2. **Custom Analysis + Posting:**
   ```bash
   # Generate custom analysis
   cd issue-management/
   ./query_issues.sh stats > weekly_stats.txt
   
   # Post the analysis
   cd ../linkedin/
   cat ../issue-management/weekly_stats.txt | node post-to-linkedin.js --stdin
   ```

## Agent Best Practices

### 1. User Onboarding
- Always start with `setup-linkedin.js` for new users
- Explain the LinkedIn Developer App requirements clearly
- Test with custom content before automated posting

### 2. Content Strategy
- Mix automated issue summaries with custom insights
- Use data to tell compelling stories about productivity
- Maintain consistent posting schedules

### 3. Privacy & Security
- Credentials are stored in user's home directory (not version controlled)
- Always respect user's content approval preferences
- Provide manual fallbacks when API fails

### 4. Troubleshooting Common Issues

**LinkedIn API Issues:**
- Token expiration: Re-run `setup-linkedin.js`
- Rate limiting: Implement delays between posts
- Permissions: Verify app has "Share on LinkedIn" product

**Issue Data Problems:**
- Missing data: Run `fetch_issues.sh` first
- Stale data: Check GitHub API rate limits
- Permission errors: Verify repository access

### 5. Extensibility

The programs are designed for easy extension:

**Adding New Social Platforms:**
- Follow the LinkedIn module pattern
- Implement setup, posting, and fallback modes
- Integrate with issue management data

**Custom Analysis:**
- Extend `query_issues.sh` with new filters
- Add custom data visualizations
- Create domain-specific metrics

## File Structure

```
programs/
├── README.md                    # This file
├── linkedin/                    # LinkedIn automation module
│   ├── linkedin                 # Main CLI wrapper
│   ├── setup-linkedin.js        # OAuth setup and configuration
│   └── post-to-linkedin.js      # Content generation and posting
└── issue-management/            # GitHub issue management module
    ├── fetch_issues.sh           # Issue data collection
    ├── query_issues.sh           # Issue analysis and search
    └── weekly-post.sh            # Automated posting workflow
```

## Dependencies

### System Requirements
- Node.js (for LinkedIn scripts)
- GitHub CLI (`gh` command)
- `jq` (for JSON processing)
- `curl` (for API calls)

### Installation Commands
```bash
# Ubuntu/Debian
sudo apt install nodejs npm jq curl

# Install GitHub CLI
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update && sudo apt install gh
```

## Future Development

These programs serve as a foundation for expanded automation capabilities:

1. **Additional Social Platforms** (Twitter, Mastodon, etc.)
2. **Advanced Analytics** (trend analysis, prediction)
3. **Integration APIs** (webhooks, Slack notifications)
4. **AI-Enhanced Content** (GPT integration for content generation)

## Support

For agents helping users with these tools:

1. **Documentation**: Always refer to individual script `--help` flags
2. **Logs**: Check `post-history.json` for posting records
3. **Debugging**: Use `--dry-run` mode for testing
4. **Updates**: Scripts are version-controlled and should be kept current

---

*This documentation is designed to help AI agents effectively assist users with LinkedIn posting and project management automation. Always prioritize user privacy and content approval in automated workflows.*