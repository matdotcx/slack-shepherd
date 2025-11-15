"""IP analysis logic."""
from typing import Dict, List, Set
from collections import defaultdict
from datetime import datetime
from ..models.user import User
from ..models.access_log import AccessLog
from ..models.ip_analysis import IPAnalysisResult, GeoLocation


class IPAnalyzer:
    """Analyzes access logs to find IP overlaps between users."""

    @staticmethod
    def group_by_ip(logs: List[AccessLog]) -> Dict[str, List[AccessLog]]:
        """
        Group access logs by IP address.

        Args:
            logs: List of AccessLog objects

        Returns:
            Dictionary mapping IP address to list of AccessLog entries
        """
        ip_map = defaultdict(list)
        for log in logs:
            ip_map[log.ip].append(log)
        return dict(ip_map)

    @staticmethod
    def filter_by_user(logs: List[AccessLog], user_id: str) -> List[AccessLog]:
        """Filter access logs for a specific user."""
        return [log for log in logs if log.user_id == user_id]

    @staticmethod
    def extract_locations(
        ip_map: Dict[str, List[AccessLog]],
        geo_data: Dict[str, GeoLocation]
    ) -> Set[str]:
        """
        Extract unique location strings from IP map.

        Args:
            ip_map: Dictionary mapping IP to access logs
            geo_data: Dictionary mapping IP to GeoLocation

        Returns:
            Set of location strings in format "City, Region, Country"
        """
        locations = set()
        for ip in ip_map.keys():
            if ip in geo_data:
                geo = geo_data[ip]
                location = f"{geo.city}, {geo.region}, {geo.country}"
                locations.add(location)
        return locations

    @staticmethod
    def calculate_date_range(logs: List[AccessLog]) -> int:
        """
        Calculate the date range covered by the logs in days.

        Args:
            logs: List of AccessLog objects

        Returns:
            Number of days between earliest and latest access
        """
        if not logs:
            return 0

        min_date = min(log.date_first for log in logs)
        max_date = max(log.date_last for log in logs)

        # Convert timestamps to days
        days = (max_date - min_date) / (24 * 60 * 60)
        return int(days)

    def analyze(
        self,
        user1: User,
        user2: User,
        all_logs: List[AccessLog],
        geo_data: Dict[str, GeoLocation],
        days_back: int = 30
    ) -> IPAnalysisResult:
        """
        Perform complete IP analysis for two users.

        Args:
            user1: First user
            user2: Second user
            all_logs: All access logs
            geo_data: Geolocation data for IPs

        Returns:
            IPAnalysisResult with complete analysis
        """
        # Filter logs by user
        user1_logs = self.filter_by_user(all_logs, user1.id)
        user2_logs = self.filter_by_user(all_logs, user2.id)

        # Group by IP
        user1_ips = self.group_by_ip(user1_logs)
        user2_ips = self.group_by_ip(user2_logs)

        # Find shared IPs
        user1_ip_set = set(user1_ips.keys())
        user2_ip_set = set(user2_ips.keys())
        shared_ips = user1_ip_set & user2_ip_set

        # Extract locations
        user1_locations = self.extract_locations(user1_ips, geo_data)
        user2_locations = self.extract_locations(user2_ips, geo_data)
        shared_locations = user1_locations & user2_locations

        # Calculate date range
        date_range_days = self.calculate_date_range(all_logs)

        return IPAnalysisResult(
            user1=user1,
            user2=user2,
            user1_ips=user1_ips,
            user2_ips=user2_ips,
            shared_ips=shared_ips,
            user1_locations=user1_locations,
            user2_locations=user2_locations,
            shared_locations=shared_locations,
            geolocation_data=geo_data,
            total_logs_analyzed=len(all_logs),
            date_range_days=date_range_days,
            days_back=days_back
        )
