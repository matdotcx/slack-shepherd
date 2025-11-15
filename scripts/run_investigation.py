#!/usr/bin/env python3
"""
slack-shepherd - GitHub Actions Entry Point

A professional Slack workspace security tool for monitoring user access patterns.
Named after the biblical shepherd who watches over and protects their flock.

This script parses GitHub issue bodies, runs IP investigations, and posts results.
"""
import os
import sys
import re
import json
import requests
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import Config
from src.main import InvestigationOrchestrator


def parse_issue_body(body: str) -> dict:
    """
    Parse user IDs and options from GitHub issue body.

    Args:
        body: GitHub issue body text

    Returns:
        Dictionary with 'user_id_1', 'user_id_2', 'max_pages'
    """
    # Try parsing the issue template format first
    user1_match = re.search(r'User 1 ID\s*.*?\n\s*([A-Z0-9]+)', body, re.DOTALL)
    user2_match = re.search(r'User 2 ID\s*.*?\n\s*([A-Z0-9]+)', body, re.DOTALL)

    if user1_match and user2_match:
        user_id_1 = user1_match.group(1).strip()
        user_id_2 = user2_match.group(1).strip()
    else:
        # Fallback: Try parsing comma-separated user IDs
        user_ids_match = re.search(r'User IDs to Investigate\s*.*?\n\s*([A-Z0-9,\s]+)', body, re.DOTALL)
        if not user_ids_match:
            raise ValueError("Could not parse user IDs from issue body")

        user_ids = [uid.strip() for uid in user_ids_match.group(1).split(',')]
        if len(user_ids) < 2:
            raise ValueError("At least two user IDs are required")

        user_id_1 = user_ids[0]
        user_id_2 = user_ids[1]

    # Parse max pages from Data Depth selection
    max_pages = 30  # default
    if "Quick (10 pages)" in body:
        max_pages = 10
    elif "Deep (50 pages)" in body:
        max_pages = 50

    return {
        'user_id_1': user_id_1,
        'user_id_2': user_id_2,
        'max_pages': max_pages
    }


def validate_user_id(user_id: str) -> bool:
    """Validate Slack user ID format."""
    # Slack user IDs: U followed by 8-11 alphanumeric characters
    pattern = re.compile(r'^U[A-Z0-9]{8,11}$')
    return bool(pattern.match(user_id))


def check_org_membership(username: str, org: str, github_token: str) -> bool:
    """
    Check if user is a member of the GitHub organization.

    Args:
        username: GitHub username
        org: Organization name
        github_token: GitHub token

    Returns:
        True if user is member, False otherwise
    """
    url = f"https://api.github.com/orgs/{org}/members/{username}"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.status_code == 204
    except Exception as e:
        print(f"Error checking org membership: {e}")
        return False


def post_comment(repo: str, issue_number: int, body: str, github_token: str):
    """Post a comment to the GitHub issue."""
    owner, repo_name = repo.split('/')
    url = f"https://api.github.com/repos/{owner}/{repo_name}/issues/{issue_number}/comments"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json"
    }
    data = {"body": body}

    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error posting comment: {e}")


def close_issue(repo: str, issue_number: int, github_token: str):
    """Close the GitHub issue."""
    owner, repo_name = repo.split('/')
    url = f"https://api.github.com/repos/{owner}/{repo_name}/issues/{issue_number}"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json"
    }
    data = {"state": "closed"}

    try:
        response = requests.patch(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error closing issue: {e}")


def main():
    """Main entry point for GitHub Actions."""
    # Get environment variables
    issue_body = os.getenv('ISSUE_BODY', '')
    issue_number = os.getenv('ISSUE_NUMBER', '')
    repository = os.getenv('GITHUB_REPOSITORY', '')
    github_token = os.getenv('GITHUB_TOKEN', '')
    github_actor = os.getenv('GITHUB_ACTOR', '')
    slack_token = os.getenv('SLACK_USER_TOKEN', '')

    if not all([issue_body, issue_number, repository, github_token, slack_token]):
        print("Error: Missing required environment variables")
        return 1

    # Check org membership
    org = repository.split('/')[0]
    print(f"Checking if {github_actor} is a member of {org}...")
    if not check_org_membership(github_actor, org, github_token):
        error_msg = f"Access denied: {github_actor} is not a member of the {org} organization."
        post_comment(repository, int(issue_number), f"## Error\n\n{error_msg}", github_token)
        close_issue(repository, int(issue_number), github_token)
        return 1

    print(f"  Verified: {github_actor} is an org member")

    # Post processing message
    post_comment(
        repository,
        int(issue_number),
        "## Processing Request\n\nYour IP investigation is in progress. This may take 2-5 minutes...",
        github_token
    )

    try:
        # Parse issue body
        print("Parsing issue body...")
        params = parse_issue_body(issue_body)
        user_id_1 = params['user_id_1']
        user_id_2 = params['user_id_2']
        max_pages = params['max_pages']

        print(f"  User ID 1: {user_id_1}")
        print(f"  User ID 2: {user_id_2}")
        print(f"  Max pages: {max_pages}")

        # Validate user IDs
        if not validate_user_id(user_id_1):
            raise ValueError(f"Invalid User ID 1 format: {user_id_1}")
        if not validate_user_id(user_id_2):
            raise ValueError(f"Invalid User ID 2 format: {user_id_2}")

        # Set environment variables for config
        os.environ['SLACK_USER_TOKEN'] = slack_token
        os.environ['USER_ID_1'] = user_id_1
        os.environ['USER_ID_2'] = user_id_2
        os.environ['MAX_PAGES'] = str(max_pages)

        # Run investigation
        print("\nRunning investigation...")
        config = Config.from_env()
        orchestrator = InvestigationOrchestrator(config)
        report = orchestrator.run()

        if report:
            # Post report as comment
            print("\nPosting report to issue...")
            post_comment(repository, int(issue_number), report, github_token)

            # Close issue
            print("Closing issue...")
            close_issue(repository, int(issue_number), github_token)

            print("\nInvestigation completed successfully")
            return 0
        else:
            error_msg = "## Error\n\nInvestigation failed. Please check the workflow logs for details."
            post_comment(repository, int(issue_number), error_msg, github_token)
            return 1

    except Exception as e:
        error_msg = f"## Error\n\n{str(e)}\n\nPlease verify your inputs and try again."
        post_comment(repository, int(issue_number), error_msg, github_token)
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
