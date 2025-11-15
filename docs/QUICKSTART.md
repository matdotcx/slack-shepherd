# Quick Start Guide

## For Administrators: 5-Minute Setup

1. **Configure Slack App**
   - Go to https://api.slack.com/apps → Create New App
   - Add scopes: `admin`, `users:read`
   - Install to workspace
   - Copy the User OAuth Token (xoxp-...)

2. **Configure GitHub**
   - Make repository private
   - Add repository secret `SLACK_BOT_TOKEN` in Settings → Secrets
   - Enable GitHub Actions

3. **Test**
   - Create an issue using the IP Investigation template
   - Add label `ip-investigation`
   - Wait 2-5 minutes for results

Done! See [SETUP.md](SETUP.md) for detailed instructions.

## For Users: Running an Investigation

1. **Create Issue**
   - Issues tab → New Issue → IP Investigation Request

2. **Fill Form**
   - User 1 ID: `U09H7SDJCB1` (example)
   - User 2 ID: `U09N8R0AB0W` (example)
   - Data Depth: Standard

3. **Submit & Label**
   - Submit the issue
   - Add label: `ip-investigation`

4. **Review Results**
   - Wait 2-5 minutes
   - Report posted as comment
   - Issue auto-closes

**Need help finding User IDs?**
Slack → Right-click user → View profile → ... → Copy member ID

## Common Issues

| Problem | Solution |
|---------|----------|
| Workflow doesn't start | Add the `ip-investigation` label |
| Access denied | Verify you're a GitHub org member |
| Invalid user ID | Check format: U + 10 characters |
| API error | Check Slack token has `admin` scope |

See [USAGE.md](USAGE.md) for complete documentation.
