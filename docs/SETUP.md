# Setup Guide for Administrators

This guide covers initial setup and configuration for the Slack IP Investigation Tool.

## Prerequisites

Before you begin, ensure you have:

- [ ] Slack Business+ or Enterprise plan
- [ ] Slack admin account
- [ ] GitHub organization
- [ ] Repository admin access

## Step 1: Slack Configuration

### 1.1 Create a Slack App

1. Go to https://api.slack.com/apps
2. Click **Create New App**
3. Choose **From scratch**
4. Name: "IP Investigation Tool"
5. Select your workspace

### 1.2 Configure OAuth & Permissions

1. In your app settings, navigate to **OAuth & Permissions**
2. Scroll to **Scopes** section
3. Add **User Token Scopes**:
   - `admin` (required for team.accessLogs)
   - `users:read` (required for user info)
   - `users:read.email` (optional)
   - `search:read` (optional, for message activity)

### 1.3 Install App to Workspace

1. Scroll to **OAuth Tokens for Your Workspace**
2. Click **Install to Workspace**
3. Review permissions and approve
4. **Copy the User OAuth Token** (starts with `xoxp-`)
   - This is your `SLACK_USER_TOKEN` (repository secret name)
   - Store it securely - you'll need it for GitHub Secrets

**Important Security Notes:**
- This token has admin privileges
- Never commit it to code or share publicly
- Store only in GitHub Secrets
- Rotate every 90 days (recommended)

## Step 2: GitHub Repository Setup

### 2.1 Repository Configuration

1. **Create or use existing repository**
   ```bash
   git init slack-investigation
   cd slack-investigation
   ```

2. **Set repository visibility to Private**
   - Settings → General → Danger Zone
   - Change visibility to **Private**
   - Confirm the change

3. **Enable GitHub Actions**
   - Go to Actions tab
   - Enable workflows if prompted

### 2.2 Configure GitHub Secrets

1. Navigate to **Settings → Secrets and variables → Actions**
2. Click **New repository secret**
3. Add repository secret:
   - Name: `SLACK_USER_TOKEN`
   - Value: The xoxp- token from Step 1.3
4. Click **Add secret**

### 2.3 Set Workflow Permissions

1. Go to **Settings → Actions → General**
2. Scroll to **Workflow permissions**
3. Select **Read and write permissions**
4. Enable **Allow GitHub Actions to create and approve pull requests**
5. Click **Save**

### 2.4 Configure Branch Protection (Optional but Recommended)

1. Go to **Settings → Branches**
2. Click **Add rule**
3. Branch name pattern: `main`
4. Enable:
   - Require a pull request before merging
   - Require approvals (at least 1)
   - Require review from Code Owners
5. Click **Create**

## Step 3: Deploy the Code

### 3.1 Clone This Repository

```bash
git clone <this-repository-url>
cd slack-investigation
```

### 3.2 Push to Your Repository

```bash
git remote add origin <your-repository-url>
git branch -M main
git push -u origin main
```

### 3.3 Verify Deployment

1. Check that all files are present:
   - `.github/workflows/ip-investigation.yml`
   - `.github/ISSUE_TEMPLATE/ip-investigation.yml`
   - `src/` directory with all modules
   - `scripts/run_investigation.py`

2. Verify GitHub Actions workflow appears:
   - Go to Actions tab
   - You should see "IP Investigation" workflow

## Step 4: Test the Setup

### 4.1 Create a Test Issue

1. Go to **Issues** tab
2. Click **New Issue**
3. Select **IP Investigation Request** template
4. Fill in with test data:
   - Your own Slack User ID for both users
   - Choose "Quick (10 pages)"
5. **Submit new issue**
6. **Add label**: `ip-investigation`

### 4.2 Monitor the Workflow

1. Go to **Actions** tab
2. Click on the running workflow
3. Watch the real-time logs
4. Verify each step completes successfully:
   - Checkout repository
   - Set up Python
   - Install dependencies
   - Run investigation

### 4.3 Verify the Results

1. Return to your test issue
2. You should see:
   - "Processing Request" comment
   - Complete report with your IP data
   - Issue automatically closed

If everything works, setup is complete!

## Step 5: User Onboarding

### 5.1 Announce the Tool

Create an announcement with:
- Link to repository
- Brief description of purpose
- Link to USAGE.md documentation
- Instructions to request org membership if needed

### 5.2 Add Users to Organization

Ensure authorized users are GitHub org members:
1. Go to your organization settings
2. Navigate to People
3. Invite users via email
4. Set appropriate permissions

### 5.3 Grant Repository Access

For private repositories:
1. Settings → Collaborators and teams
2. Add teams or individuals
3. Grant "Read" or "Triage" access (minimum needed)

## Ongoing Maintenance

### Security

**Token Rotation (Every 90 Days)**
1. Generate new Slack token
2. Update GitHub Secret
3. Test with a sample issue
4. Revoke old token

**Access Review (Quarterly)**
1. Review GitHub org membership
2. Remove users who no longer need access
3. Audit issue history

**Monitor Usage**
1. Check Actions tab for unusual patterns
2. Review closed issues periodically
3. Monitor for abuse or errors

### Troubleshooting

**Common Issues:**

1. **"missing_scope" Error**
   - Solution: Re-add `admin` scope to Slack app
   - Verify `SLACK_USER_TOKEN` secret has the correct token

2. **"paid_only" Error**
   - Solution: Verify Slack plan is Business+ or higher

3. **Workflow Not Triggering**
   - Check: Label is exactly `ip-investigation`
   - Check: Workflow permissions are correct
   - Check: Actions are enabled

4. **API Rate Limits**
   - Solution: Users should space out requests
   - Consider adding rate limiting to workflow if needed

### Updates and Upgrades

To update the tool:
1. Pull latest changes from upstream
2. Test in a dev branch
3. Create PR to main
4. Review and merge
5. Announce changes to users

## Advanced Configuration

### Custom Rate Limiting

Edit `.github/workflows/ip-investigation.yml`:

```yaml
concurrency:
  group: ip-investigation
  cancel-in-progress: false
```

This ensures only one investigation runs at a time.

### Custom Timeout

Adjust timeout in workflow:

```yaml
jobs:
  investigate:
    timeout-minutes: 15  # Increase from default 10
```

### Email Notifications

Set up GitHub Actions notifications:
1. Personal Settings → Notifications
2. Enable "Actions" notifications
3. Configure email preferences

### Audit Logging

GitHub provides built-in audit logs:
- Settings → Audit log (org level)
- Issues and Actions provide natural audit trail

### Backup and Export

Periodically backup:
- Issue data (export via GitHub API)
- Actions logs (download artifacts)
- Configuration files (git history)

## Security Best Practices

1. **Always use a private repository** for sensitive investigation data
2. **Enable two-factor authentication** for all org members
3. **Review access regularly** and remove unnecessary permissions
4. **Monitor the audit log** for suspicious activity
5. **Rotate secrets regularly** (90-day cycle recommended)
6. **Document investigations** with proper justification
7. **Train users** on proper usage and privacy considerations

## Support and Escalation

For technical issues:
1. Check workflow logs in Actions tab
2. Review documentation (README, USAGE.md, this file)
3. Check Slack API status: https://status.slack.com
4. Contact GitHub support for platform issues

For security concerns:
1. Immediately revoke compromised tokens
2. Review issue history for unauthorized access
3. Notify security team
4. Follow your organization's incident response procedures

## Appendix: Required Scopes Reference

| Scope | Required | Purpose |
|-------|----------|---------|
| `admin` | Yes | Access team.accessLogs API |
| `users:read` | Yes | Fetch user information |
| `users:read.email` | No | Include email addresses |
| `search:read` | No | Check message activity |

## Appendix: GitHub Permissions Reference

| Permission | Required | Purpose |
|------------|----------|---------|
| `issues: write` | Yes | Post comments and close issues |
| `contents: read` | Yes | Read repository code |
| `actions: read` | No | View workflow status (automatic) |

## Appendix: Testing Checklist

Before going live:

- [ ] Slack token configured and working
- [ ] GitHub Secrets set correctly
- [ ] Workflow permissions configured
- [ ] Test issue completes successfully
- [ ] Org membership check works (test with non-member)
- [ ] Invalid input handled gracefully (test with bad user IDs)
- [ ] Reports render correctly in GitHub
- [ ] Issue auto-closes after completion
- [ ] Documentation is accessible to users
- [ ] Users have been onboarded and trained

## Getting Help

If you need assistance with setup:
- Check GitHub Actions logs for error messages
- Review Slack API documentation
- Consult your organization's DevOps team
- File an issue in this repository (if appropriate)
