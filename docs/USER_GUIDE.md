# Slack Shepherd - User Guide

## How to Run an IP Investigation

### Step 1: Create a New Issue
1. Go to https://github.com/macadminsdotorg/slack-shepherd/issues/new/choose
2. Click "Get started" next to "IP Investigation Request"

### Step 2: Fill in the User IDs
- **User 1 ID**: Enter the first Slack user ID (e.g., `U1CJTLF8X`)
- **User 2 ID**: Enter the second Slack user ID (e.g., `U09SYLRQW2F`)
- **Data Depth**: Choose how much history to analyze (Standard is recommended)
- **Purpose**: Optionally describe why you're running this investigation

### Step 3: Add the Label
1. After creating the issue, add the `ip-investigation` label
2. The workflow will start automatically

### Step 4: Wait!
- The investigation takes 2-5 minutes to complete
- You'll see a "Processing Request" comment appear
- When done, the full report will be posted as a comment
- The report is also sent to the configured Slack channel

## Finding Slack User IDs

**From Slack Desktop/Web:**
1. Right-click on the user's name or avatar
2. Select "View profile"
3. Click the three dots (...)
4. Select "Copy member ID"

**From a user's message:**
1. Click on their avatar in any message
2. Click "View full profile"
3. Look at the URL: the part after `/team/` is the User ID

## What the Report Shows

- **Shared IP Addresses**: IPs that both users accessed Slack from
- **Unique IPs**: IPs used by only one user
- **Location Data**: Geographic location and ISP for each IP
- **Access Patterns**: When and how many times each IP was used

## Interpreting Results

If shared IPs are found, this could indicate:
- Shared network access (same office/building)
- Same physical location
- Duplicate/shadow accounts (one person with multiple accounts)

---

That's it! Create issue → Add user IDs → Add label → Wait for results.
