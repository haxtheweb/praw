# LinkedIn Posting Automation

This module provides comprehensive LinkedIn posting automation with support for both data-driven and custom content posting.

## Features

- **OAuth 2.0 Integration**: Secure LinkedIn API authentication
- **Multiple Content Modes**: Issues-based automation, custom posts, stdin input
- **Fallback Support**: Manual posting when API is unavailable
- **Content Generation**: Automatic productivity summaries from GitHub issues
- **Cross-platform**: Twitter content generation for cross-posting

## Quick Start

### 1. First-Time Setup
```bash
node setup-linkedin.js
```

Follow the interactive prompts to:
1. Create a LinkedIn Developer App
2. Configure OAuth credentials
3. Authenticate and store access tokens

### 2. Basic Usage

**Post Weekly Issue Summary:**
```bash
./linkedin
# or
node post-to-linkedin.js
```

**Post Custom Content:**
```bash
node post-to-linkedin.js --custom "Excited to share our new web component library! 🚀 #WebComponents"
```

**Pipe Content from Other Sources:**
```bash
echo "Great discussion about accessibility in web development" | node post-to-linkedin.js --stdin
```

## Configuration

### LinkedIn Developer App Setup

1. Go to [LinkedIn Developers](https://www.linkedin.com/developers/apps)
2. Click "Create app"
3. Fill in app details:
   - **App name**: "HAX Productivity Tracker" (or your preferred name)
   - **LinkedIn Page**: Your personal or company page
   - **App use**: "Other"
4. In the Products tab:
   - Request "Sign In with LinkedIn using OpenID Connect"
   - Request "Share on LinkedIn"
5. In the Auth tab:
   - Add redirect URL: `http://localhost:3000/callback`
   - Copy Client ID and Client Secret for setup

### File Locations

- **Config**: `~/.hax-linkedin-config.json` (auto-created, not in version control)
- **Post History**: `./post-history.json` (tracks all posts for analytics)
- **Issue Data**: `../issue-management/issues_data/latest_issues.json` (if available)

## Content Generation

### Automatic Issue Summaries

The script analyzes GitHub issues to create engaging posts featuring:

- **Weekly Statistics**: Issues created, resolved, completion rates
- **Category Breakdown**: Accessibility, performance, UX, etc.
- **Project Health**: Overall resolution rates and active issue counts
- **Relevant Hashtags**: #OpenSource #WebComponents #HAXTheWeb

### Custom Content Features

- **Length Optimization**: Content adjusted for LinkedIn's algorithm
- **Cross-platform**: Generates both LinkedIn and Twitter versions
- **Engagement Elements**: Emojis, bullet points, clear structure

## Advanced Usage

### Command Line Options

```bash
node post-to-linkedin.js [OPTIONS]

Options:
  --custom "text"   Post custom content instead of issue summary
  --stdin           Read content from stdin (pipe mode)  
  --dry-run         Generate content without posting
  --help, -h        Show help message

Examples:
  node post-to-linkedin.js --custom "New release is live!"
  cat content.txt | node post-to-linkedin.js --stdin
  node post-to-linkedin.js --dry-run  # Preview without posting
```

### Integration with Issue Management

```bash
# Update issue data and post
cd ../issue-management && ./fetch_issues.sh
cd ../linkedin && ./linkedin

# Create custom analysis post
cd ../issue-management
./query_issues.sh stats | cd ../linkedin && node post-to-linkedin.js --stdin
```

## API Modes

### 1. API Mode (Preferred)
- **Requirements**: Valid LinkedIn app with API access
- **Features**: Automatic posting, post tracking, full automation
- **Setup**: Run `setup-linkedin.js` once

### 2. Manual Mode (Fallback)
- **Trigger**: When API is unavailable or not configured
- **Features**: Content generation, clipboard copy, browser opening
- **Benefits**: Still provides value without API complexity

## Troubleshooting

### Common Issues

**"LinkedIn API not configured"**
- Run `node setup-linkedin.js`
- Ensure LinkedIn app has correct permissions

**"Access token expired"**
- Re-run `node setup-linkedin.js` to refresh token
- LinkedIn tokens typically expire after 60 days

**"Rate limiting"**
- Wait before retrying
- LinkedIn has generous rate limits for personal posting

**"Permission denied"**
- Verify LinkedIn app has "Share on LinkedIn" product enabled
- Check app review status (some products require approval)

### Token Management

LinkedIn tokens are stored securely in your home directory and include:
- Access token for API calls
- Refresh token for token renewal
- Expiration tracking with automatic warnings
- User profile information for post attribution

### Content Guidelines

**Effective LinkedIn Posts:**
- Use compelling opening lines
- Include relevant emojis and formatting
- Add 3-5 targeted hashtags
- Keep personal while being professional
- Include data/metrics when available

**Hashtag Strategy:**
- `#OpenSource` - For open source projects
- `#WebComponents` - For web component development  
- `#HAXTheWeb` - For HAX-specific content
- `#ProductivityUpdate` - For weekly summaries
- `#Developer` or `#WebDevelopment` - For technical content

## Integration for Agents

When helping users with LinkedIn automation:

### Setup Assistance
1. Guide through LinkedIn Developer Console
2. Help debug OAuth flow issues
3. Verify app permissions and configuration
4. Test with sample content before automation

### Content Strategy
1. Help craft engaging technical narratives
2. Balance automation with personal touch
3. Suggest optimal posting schedules
4. Track engagement patterns for improvement

### Privacy Considerations
1. All credentials stored locally (not in git)
2. User approval required for each post (unless automated)
3. Content preview available before posting
4. Manual fallback preserves user control

---

*This LinkedIn automation respects user privacy while maximizing content engagement and productivity tracking.*