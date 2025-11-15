"""Slack API client."""
import requests
from typing import List, Optional, Dict, Any
from ..models.user import User
from ..models.access_log import AccessLog


class SlackClient:
    """Handles all Slack API communication."""

    def __init__(self, token: str):
        """Initialize Slack client with API token."""
        self.token = token
        self.base_url = "https://slack.com/api"

    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict]:
        """Make a request to Slack API with error handling."""
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            data = response.json()

            if not data.get('ok'):
                error = data.get('error', 'Unknown error')
                print(f"  API Error: {error}")
                if error == 'missing_scope':
                    print(f"  Required scope: admin (your token needs admin privileges)")
                elif error == 'paid_only':
                    print(f"  This endpoint requires a paid Slack plan")
                return None

            return data

        except Exception as e:
            print(f"  Exception making API request: {e}")
            return None

    def get_user_info(self, user_id: str) -> Optional[User]:
        """Fetch user information."""
        data = self._make_request("users.info", {"user": user_id})

        if data and data.get('user'):
            return User.from_api_response(data['user'])

        # Return a minimal user object if fetch fails
        return User(
            id=user_id,
            name=user_id,
            real_name='Unknown',
            email='Unknown',
            updated=0,
            is_bot=False
        )

    def get_access_logs(self, max_pages: int = 30, days_back: int = 30) -> Optional[List[AccessLog]]:
        """
        Fetch access logs with pagination.

        Args:
            max_pages: Maximum number of pages to fetch (each page = 1000 records)
            days_back: Only include logs from the last N days (default: 30)

        Returns:
            List of AccessLog objects or None if error on first page
        """
        import time

        all_logs = []
        page = 1
        cutoff_timestamp = int(time.time()) - (days_back * 86400)  # 86400 seconds per day

        print(f"  Fetching access logs (up to {max_pages} pages, last {days_back} days)...")

        while page <= max_pages:
            params = {
                "count": 1000,  # Maximum per page
                "page": page
            }

            data = self._make_request("team.accessLogs", params)

            if data is None:
                return None if page == 1 else all_logs

            logins = data.get('logins', [])
            paging = data.get('paging', {})
            total_pages = paging.get('pages', 1)

            if not logins:
                print(f"  No more data on page {page}")
                break

            # Convert to AccessLog objects and filter by date
            logs_added = 0
            oldest_in_page = None
            for login in logins:
                log = AccessLog.from_api_response(login)

                # Track oldest timestamp in this page
                if oldest_in_page is None or log.date_last < oldest_in_page:
                    oldest_in_page = log.date_last

                # Only add logs within the date range
                if log.date_last >= cutoff_timestamp:
                    all_logs.append(log)
                    logs_added += 1

            print(f"  Page {page}/{total_pages}: {logs_added}/{len(logins)} entries within date range (total: {len(all_logs)})")

            # Stop if the oldest log in this page is before our cutoff
            if oldest_in_page and oldest_in_page < cutoff_timestamp:
                print(f"  Reached date cutoff (oldest entry in page: {oldest_in_page}, cutoff: {cutoff_timestamp})")
                break

            # Check if we've reached the last page
            if total_pages <= page:
                print(f"  Reached last page ({page}/{total_pages})")
                break

            page += 1

        return all_logs

    def search_user_messages(self, user_id: str, days_back: int = 7) -> Optional[List[Dict]]:
        """
        Search for recent messages from a user.
        Optional feature to verify user activity.

        Args:
            user_id: Slack user ID
            days_back: Number of days to search back

        Returns:
            List of message matches or None if error/not available
        """
        query = f"from:<@{user_id}>"
        params = {
            "query": query,
            "sort": "timestamp",
            "sort_dir": "desc",
            "count": 10
        }

        data = self._make_request("search.messages", params)

        if data and data.get('messages'):
            return data['messages'].get('matches', [])

        return None
