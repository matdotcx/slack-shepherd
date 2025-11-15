# slack-shepherd

*A professional Slack workspace security tool for monitoring user access patterns and detecting shared accounts. Named after the biblical shepherd who watches over and protects their flock - this tool watches over your users to ensure account security and proper access.*

Analyze and compare IP addresses between Slack users to identify shared access patterns.

## Overview

This tool helps investigate potential account sharing, security incidents, or compliance issues by comparing the IP addresses two Slack users have logged in from. It fetches historical access logs from Slack, performs geolocation lookups, and generates comprehensive markdown reports.

**Perfect for:**
- Security audits
- Account sharing investigations
- Compliance reporting
- Geographic access pattern analysis

## Quick Start

### For End Users (GitHub Issues Workflow)

1. **Create a new issue** using the "IP Investigation Request" template
2. **Fill in the form:**
   - User 1 ID (Slack user ID, e.g., U09H7SDJCB1)
   - User 2 ID (Slack user ID, e.g., U09N8R0AB0W)
   - Data depth (Quick/Standard/Deep)
3. **Add the label** `ip-investigation` to trigger the workflow
4. **Wait 2-5 minutes** - Results will be posted as a comment

### For Administrators (Setup)

1. **Repository setup:**
   ```bash
   # Clone or initialize this repository
   git clone <repository-url>
   cd slack-investigation
   ```

2. **Configure GitHub Secrets:**
   - Go to Settings → Secrets and variables → Actions
   - Add repository secret: `SLACK_BOT_TOKEN`
     - Value: Your Slack admin token (xoxp-...)
     - Required scopes: `admin`, `users:read`

3. **Set repository to Private:**
   - Go to Settings → General → Danger Zone
   - Change visibility to Private (recommended for security)

4. **Enable GitHub Actions:**
   - Go to Actions tab
   - Click "I understand my workflows, go ahead and enable them"

## Features

- **Automated workflow** triggered by GitHub Issues
- **Org-only access** - automatically verifies GitHub organization membership
- **Comprehensive reports** with geolocation data, ISP information, and timeline analysis
- **Clean markdown output** - easy to read directly in GitHub Issues
- **Secure** - tokens stored as encrypted GitHub Secrets, private repo recommended

## How It Works

1. User creates a GitHub Issue with two Slack user IDs
2. Issue is labeled with `ip-investigation`
3. GitHub Actions workflow automatically:
   - Verifies the requester is an org member
   - Fetches Slack access logs (up to 50,000 entries)
   - Performs IP geolocation lookups
   - Analyzes shared IPs and locations
   - Posts a detailed report as a comment
   - Closes the issue

## Finding Slack User IDs

**Method 1: From Slack Desktop/Web**
1. Right-click on the user's name or avatar
2. Select "View profile"
3. Click the three dots (...)
4. Select "Copy member ID"

**Method 2: From a URL**
1. Open the user's profile
2. Look at the URL: `slack.com/team/U09H7SDJCB1`
3. The part after `/team/` is the User ID

## Report Contents

Each report includes:

- **Summary** - Key metrics (unique IPs, shared IPs, locations)
- **Verdict** - Whether shared IPs were detected
- **User Details** - Complete IP history for each user with ISP and location
- **Shared IP Analysis** - Detailed breakdown of any common access points
- **Geographic Analysis** - Location-based comparison

## Requirements

- Slack Business+ or Enterprise plan (for `team.accessLogs` API)
- Slack admin token with required scopes
- GitHub repository (private recommended)
- GitHub Actions enabled

## Architecture

The tool uses a modular architecture:

```
src/
├── clients/          # Slack API and geolocation clients
│   ├── slack_client.py
│   └── geolocation_client.py
├── models/           # Data models
│   ├── user.py
│   ├── access_log.py
│   └── ip_analysis.py
├── analyzers/        # Analysis logic
│   └── ip_analyzer.py
├── formatters/       # Report generation
│   └── markdown_formatter.py
├── config.py         # Configuration management
└── main.py           # Main orchestrator

scripts/
└── run_investigation.py  # GitHub Actions entry point

.github/
├── workflows/
│   └── ip-investigation.yml  # Workflow definition
└── ISSUE_TEMPLATE/
    └── ip-investigation.yml  # Issue form template
```

## Local Development

You can also run the tool locally for testing:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables:**
   ```bash
   export SLACK_USER_TOKEN="xoxp-..."
   export USER_ID_1="U09H7SDJCB1"
   export USER_ID_2="U09N8R0AB0W"
   export MAX_PAGES="30"
   ```

3. **Run the investigation:**
   ```bash
   python3 -m src.main
   ```

## Security Considerations

- **Private repository** - Keep this repository private to protect sensitive access logs
- **Org-only access** - The workflow automatically verifies GitHub org membership
- **Token security** - Slack tokens are stored as encrypted GitHub Secrets
- **Audit trail** - All investigations are logged via GitHub Issues and Actions
- **Input validation** - User IDs are validated to prevent injection attacks

## Troubleshooting

### "Access Denied" Error
- Verify you are a member of the GitHub organization
- Check that the repository is configured correctly

### "Invalid User ID" Error
- Ensure Slack user IDs start with 'U' and are 11 characters long
- Copy the ID directly from Slack using the instructions above

### "API Error: missing_scope"
- Your Slack token needs the `admin` scope
- Regenerate the token with proper permissions

### Workflow Doesn't Start
- Did you add the `ip-investigation` label?
- Check that GitHub Actions are enabled
- Verify the `SLACK_USER_TOKEN` secret is configured

## Migration from Original Script

The original `check_user_ips.py` script is preserved for reference. The new modular architecture provides:

- Better separation of concerns
- Easier testing and maintenance
- GitHub Actions integration
- More flexible configuration

To migrate, simply use the GitHub Issues workflow instead of running the script locally.

## License

Internal use only. Do not distribute.

## Support

For issues or questions:
- Check the [Actions logs](../../actions) for error details
- Review the documentation in the `docs/` directory
- Contact your security team
