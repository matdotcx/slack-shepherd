"""Slack message formatter for IP analysis results."""
from datetime import datetime
from ..models.ip_analysis import IPAnalysisResult


class SlackFormatter:
    """Format IP analysis results for Slack."""

    def __init__(self, issue_url: str = "", issue_creator: str = ""):
        """Initialize with optional GitHub issue info."""
        self.issue_url = issue_url
        self.issue_creator = issue_creator

    def format(self, result: IPAnalysisResult) -> str:
        """
        Format analysis results as a Slack message.

        Args:
            result: IPAnalysisResult object

        Returns:
            Formatted Slack message string
        """
        sections = [
            self._format_header(result),
            self._format_summary(result),
            self._format_verdict(result)
        ]

        # Add shared IPs section if there are any
        shared_section = self._format_shared_ips(result)
        if shared_section:
            sections.append(shared_section)

        # Add unique IPs section
        sections.append("*Unique IPs*\n\n" + self._format_user_ips(result))

        sections.append(self._format_footer())

        return "\n\n---\n\n".join(sections)

    def _format_header(self, result: IPAnalysisResult) -> str:
        """Format report header."""
        date_str = datetime.now().strftime("%B %d, %Y at %H:%M UTC")

        # Add link and creator if available
        if self.issue_url and self.issue_creator:
            date_line = f"*Analysis Date:* <{self.issue_url}|{date_str}> (requested by @{self.issue_creator})"
        else:
            date_line = f"*Analysis Date:* {date_str}"

        return f"""*IP Comparison Analysis Report*
{date_line}
*Search Window:* Last {result.days_back} days | *Activity Span:* {result.date_range_days} days | *Records:* {result.total_logs_analyzed:,}"""

    def _format_summary(self, result: IPAnalysisResult) -> str:
        """Format executive summary."""
        return f"""*Summary*
*User 1:* {result.user1.real_name} (@{result.user1.name})
*User 2:* {result.user2.real_name} (@{result.user2.name})
*User 1 Unique IPs:* {len(result.user1_ips)}
*User 2 Unique IPs:* {len(result.user2_ips)}
*Shared IP Addresses:* *{len(result.shared_ips)}*
*Shared Locations:* {len(result.shared_locations)}"""

    def _format_verdict(self, result: IPAnalysisResult) -> str:
        """Format the verdict section."""
        if result.shared_ips:
            ip_word = "address" if len(result.shared_ips) == 1 else "addresses"
            return f"""*Shared IP Addresses Found*
These users have accessed Slack from *{len(result.shared_ips)} common IP {ip_word}*.

This could indicate shared network access (same office/building), the same physical location, or duplicate/shadow accounts (one person with multiple accounts)."""
        else:
            return f"""*No Shared IP Addresses*
These users have not accessed Slack from any common IP addresses during the analyzed period."""

    def _format_user_ips(self, result: IPAnalysisResult) -> str:
        """Format unique IPs section only."""
        sections = []

        # User 1 unique IPs
        user1_unique = {ip: logs for ip, logs in result.user1_ips.items() if ip not in result.shared_ips}
        user1_section = f"*{result.user1.real_name} (@{result.user1.name}) only:*"

        if user1_unique:
            for ip, logs in sorted(user1_unique.items(), key=lambda x: -x[1][0].count):
                geo = result.geolocation_data.get(ip)
                if not geo:
                    continue

                first_seen = datetime.fromtimestamp(logs[0].date_first).strftime("%b %d, %Y")
                last_seen = datetime.fromtimestamp(logs[0].date_last).strftime("%b %d, %Y")
                access_word = "access" if logs[0].count == 1 else "accesses"

                user1_section += f"\n`{ip}` - {geo.city}, {geo.region}, {geo.country}"
                user1_section += f"\n  ISP: {geo.org}"
                user1_section += f"\n  Activity: {first_seen} → {last_seen} ({logs[0].count} {access_word})"
        else:
            user1_section += "\nNo unique IPs"

        sections.append(user1_section)

        # User 2 unique IPs
        user2_unique = {ip: logs for ip, logs in result.user2_ips.items() if ip not in result.shared_ips}
        user2_section = f"*{result.user2.real_name} (@{result.user2.name}) only:*"

        if user2_unique:
            for ip, logs in sorted(user2_unique.items(), key=lambda x: -x[1][0].count):
                geo = result.geolocation_data.get(ip)
                if not geo:
                    continue

                first_seen = datetime.fromtimestamp(logs[0].date_first).strftime("%b %d, %Y")
                last_seen = datetime.fromtimestamp(logs[0].date_last).strftime("%b %d, %Y")
                access_word = "access" if logs[0].count == 1 else "accesses"

                user2_section += f"\n`{ip}` - {geo.city}, {geo.region}, {geo.country}"
                user2_section += f"\n  ISP: {geo.org}"
                user2_section += f"\n  Activity: {first_seen} → {last_seen} ({logs[0].count} {access_word})"
        else:
            user2_section += "\nNo unique IPs"

        sections.append(user2_section)

        return "\n\n".join(sections)

    def _format_shared_ips(self, result: IPAnalysisResult) -> str:
        """Format shared IP analysis section."""
        if not result.shared_ips:
            return ""

        sections = []

        for ip in sorted(result.shared_ips):
            geo = result.geolocation_data.get(ip)
            if not geo:
                continue

            ip_section = f"*Shared IP: `{ip}`*"
            ip_section += f"\nLocation: {geo.city}, {geo.region}, {geo.country}"
            ip_section += f"\nISP: {geo.org}"
            ip_section += f"\nCoordinates: {geo.loc}"
            ip_section += f"\n\n*Access by both users:*"

            # User 1 access info
            if ip in result.user1_ips:
                logs = result.user1_ips[ip]
                first = datetime.fromtimestamp(logs[0].date_first).strftime("%b %d %H:%M")
                last = datetime.fromtimestamp(logs[0].date_last).strftime("%b %d %H:%M")
                access_word = "access" if logs[0].count == 1 else "accesses"
                ip_section += f"\n• {result.user1.real_name} (@{result.user1.name}): {logs[0].count} {access_word} ({first} → {last})"

            # User 2 access info
            if ip in result.user2_ips:
                logs = result.user2_ips[ip]
                first = datetime.fromtimestamp(logs[0].date_first).strftime("%b %d %H:%M")
                last = datetime.fromtimestamp(logs[0].date_last).strftime("%b %d %H:%M")
                access_word = "access" if logs[0].count == 1 else "accesses"
                ip_section += f"\n• {result.user2.real_name} (@{result.user2.name}): {logs[0].count} {access_word} ({first})"

            sections.append(ip_section)

        return "\n\n---\n\n".join(sections)

    def _format_footer(self) -> str:
        """Format report footer."""
        return """---
_This report was automatically generated by *slack-shepherd*_
_Watching over your workspace security_"""
