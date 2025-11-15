# Usage Guide

## For End Users

### Step 1: Create an Investigation Request

1. Navigate to the **Issues** tab in the repository
2. Click **New Issue**
3. Select the **IP Investigation Request** template

### Step 2: Fill Out the Form

#### User IDs
Enter the Slack user IDs you want to compare:
- **User 1 ID**: e.g., `U09H7SDJCB1`
- **User 2 ID**: e.g., `U09N8R0AB0W`

**How to find user IDs:** See the instructions in the issue template or the main README.

#### Data Depth
Choose how much historical data to analyze:
- **Quick (10 pages)**: ~10,000 records, ~1 minute processing
- **Standard (30 pages)**: ~30,000 records, ~3 minutes processing (recommended)
- **Deep (50 pages)**: ~50,000 records, ~5 minutes processing

#### Purpose (Optional)
Briefly explain why you're running this investigation for audit purposes.

### Step 3: Submit and Label

1. Click **Submit new issue**
2. **Important:** Add the label `ip-investigation` to trigger the workflow
3. Wait for processing to complete

### Step 4: Review Results

Within 2-5 minutes, you'll receive:
- A "Processing" comment confirming the request was received
- A detailed report posted as a comment with:
  - Executive summary
  - Verdict (shared IPs or not)
  - Detailed IP information for each user
  - Shared IP analysis
  - Geographic comparison

The issue will automatically close once complete.

## Understanding the Report

### Summary Section
Quick overview of key metrics:
- Total records analyzed
- Number of unique IPs per user
- Count of shared IPs and locations

### Verdict
Clear statement about whether shared IP addresses were detected and what this might indicate.

### User Details
Complete table of all IP addresses used by each user with:
- IP address (shared IPs are marked in bold)
- Geographic location
- ISP/Organization
- First and last seen timestamps
- Total access count

### Shared IP Analysis
Detailed breakdown of any IP addresses used by both users, including:
- Complete geolocation data
- Usage timeline for each user
- Access counts and patterns

### Geographic Analysis
Location-based comparison showing:
- All locations for each user
- Shared locations marked clearly
- Easy to spot geographic overlaps

## Common Use Cases

### Investigating Account Sharing
1. Create investigation for two suspected accounts
2. Review report for shared IPs
3. Check if IPs are residential or corporate
4. Verify timing of accesses

### Security Audit
1. Run investigations for key personnel
2. Look for unexpected locations
3. Verify expected vs. actual access patterns
4. Document findings in issue comments

### Compliance Reporting
1. Generate reports on schedule
2. Export markdown for documentation
3. Track historical access patterns
4. Maintain audit trail via GitHub Issues

## Best Practices

### Choosing Data Depth
- **Quick**: For recent activity or quick checks
- **Standard**: Best balance for most investigations
- **Deep**: When you need complete historical data

### Interpreting Results
- **Shared residential IP**: Could indicate same household
- **Shared corporate IP**: Likely same office/network
- **Shared public WiFi**: Coffee shop, airport, etc.
- **Multiple shared IPs**: Stronger indicator of relationship

### Privacy Considerations
- Only request investigations when justified
- Handle results securely
- Don't share reports publicly
- Document business justification

## Rate Limits and Restrictions

### GitHub Actions
- Maximum 10 minutes per workflow run
- Automatic timeout protection

### Slack API
- Rate limits handled automatically
- Pagination limits: 1000 entries per page, max 50 pages

### Geolocation API
- Rate limits: ~50,000 requests/month (free tier)
- Automatic caching to minimize lookups

## Troubleshooting

### Investigation Doesn't Start
**Problem**: No processing comment appears
**Solutions**:
- Verify you added the `ip-investigation` label
- Check GitHub Actions tab for errors
- Ensure you're an org member

### Invalid User ID Error
**Problem**: "Could not parse user IDs"
**Solutions**:
- Verify IDs start with 'U'
- Check ID is exactly 11 characters
- Copy directly from Slack (don't type manually)

### Access Denied
**Problem**: "User is not a member of organization"
**Solutions**:
- Verify GitHub account is in the organization
- Contact admin to add you to org
- Check repository permissions

### No Data Found
**Problem**: "0 access logs found"
**Solutions**:
- Users may be newly created
- No activity in data retention period
- Check Slack plan supports access logs (Business+ required)

### Timeout Error
**Problem**: Workflow times out after 10 minutes
**Solutions**:
- Try "Quick" data depth instead of "Deep"
- Report issue to admins (may need infrastructure scaling)

## FAQ

**Q: How far back does the data go?**
A: Typically 30-90 days, depending on your Slack plan and data retention settings.

**Q: Can I compare more than 2 users?**
A: Currently limited to 2 users per investigation. Run multiple investigations for more users.

**Q: Are the reports private?**
A: Yes, if the repository is private (recommended). Reports are visible to anyone with repo access.

**Q: Can I delete a report?**
A: Yes, you can delete issue comments. Consider closing/locking issues instead.

**Q: How often can I run investigations?**
A: No hard limits, but be mindful of API rate limits and GitHub Actions minutes.

**Q: What if users are in different Slack workspaces?**
A: This tool only works within a single Slack workspace. User IDs from different workspaces won't match.

## Advanced Usage

### Running Locally
For testing or development, you can run investigations locally:

```bash
export SLACK_USER_TOKEN="xoxp-..."
export USER_ID_1="U09H7SDJCB1"
export USER_ID_2="U09N8R0AB0W"
export MAX_PAGES="30"

python3 -m src.main
```

### Exporting Reports
Reports are in markdown format and can be easily exported:
1. Copy the report comment text
2. Save as `.md` file
3. Convert to PDF using tools like pandoc

### Batch Analysis
To analyze multiple user pairs:
1. Create multiple issues
2. Label them all at once
3. GitHub Actions will queue and process them
4. Review results as they complete

## Getting Help

If you encounter issues:
1. Check the workflow logs in the Actions tab
2. Review this documentation
3. Check the main README
4. Contact your security team or repository administrators
