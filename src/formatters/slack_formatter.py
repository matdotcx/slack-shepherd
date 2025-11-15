"""Slack message formatter for IP analysis results."""
from datetime import datetime
from ..models.ip_analysis import IPAnalysisResult


class SlackFormatter:
    """Format IP analysis results for Slack."""

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
            self._format_verdict(result),
            self._format_user_ips(result),
            self._format_shared_ips(result),
            self._format_locations(result),
            self._format_footer()
        ]

        return "\n\n".join(sections)

    def _format_header(self, result: IPAnalysisResult) -> str:
        """Format report header."""
        return f"""*IP Comparison Analysis Report*
📅 *Analysis Date:* {datetime.now().strftime("%B %d, %Y at %H:%M UTC")}
🔍 *Search Window:* Last {result.days_back} days
📊 *Activity Span:* {result.date_range_days} days (actual data range)
📁 *Total Records:* {result.total_logs_analyzed:,}"""

    def _format_summary(self, result: IPAnalysisResult) -> str:
        """Format executive summary."""
        return f"""*Summary*
👤 *User 1:* {result.user1.real_name} (@{result.user1.name})
👤 *User 2:* {result.user2.real_name} (@{result.user2.name})
🌐 *User 1 Unique IPs:* {len(result.user1_ips)}
🌐 *User 2 Unique IPs:* {len(result.user2_ips)}
⚠️ *Shared IP Addresses:* *{len(result.shared_ips)}*
📍 *Shared Locations:* {len(result.shared_locations)}"""

    def _format_verdict(self, result: IPAnalysisResult) -> str:
        """Format the verdict section."""
        if result.shared_ips:
            return f"""*🚨 SHARED IP ADDRESSES DETECTED*
These users have accessed Slack from *{len(result.shared_ips)} common IP address(es)*.
This could indicate:
• Shared network access (same office/building)
• Same physical location
• Duplicate/shadow accounts (one person with multiple accounts)
• Potential account sharing"""
        else:
            return f"""*✅ NO SHARED IP ADDRESSES*
These users have not accessed Slack from any common IP addresses during the analyzed period."""

    def _format_user_ips(self, result: IPAnalysisResult) -> str:
        """Format detailed IP information for each user."""
        sections = []

        # User 1
        user1_section = f"*{result.user1.real_name} (@{result.user1.name}) - IPs*"
        for ip, logs in sorted(result.user1_ips.items(), key=lambda x: -x[1][0].count):
            geo = result.geolocation_data.get(ip)
            if not geo:
                continue

            is_shared = "🔴 *SHARED*" if ip in result.shared_ips else ""
            first_seen = datetime.fromtimestamp(logs[0].date_first).strftime("%b %d, %Y")
            last_seen = datetime.fromtimestamp(logs[0].date_last).strftime("%b %d, %Y")

            user1_section += f"\n• `{ip}` {is_shared}"
            user1_section += f"\n  📍 {geo.city}, {geo.region}, {geo.country}"
            user1_section += f"\n  🏢 {geo.org}"
            user1_section += f"\n  📅 {first_seen} → {last_seen} ({logs[0].count} accesses)"

        sections.append(user1_section)

        # User 2
        user2_section = f"*{result.user2.real_name} (@{result.user2.name}) - IPs*"
        for ip, logs in sorted(result.user2_ips.items(), key=lambda x: -x[1][0].count):
            geo = result.geolocation_data.get(ip)
            if not geo:
                continue

            is_shared = "🔴 *SHARED*" if ip in result.shared_ips else ""
            first_seen = datetime.fromtimestamp(logs[0].date_first).strftime("%b %d, %Y")
            last_seen = datetime.fromtimestamp(logs[0].date_last).strftime("%b %d, %Y")

            user2_section += f"\n• `{ip}` {is_shared}"
            user2_section += f"\n  📍 {geo.city}, {geo.region}, {geo.country}"
            user2_section += f"\n  🏢 {geo.org}"
            user2_section += f"\n  📅 {first_seen} → {last_seen} ({logs[0].count} accesses)"

        sections.append(user2_section)

        return "\n\n".join(sections)

    def _format_shared_ips(self, result: IPAnalysisResult) -> str:
        """Format shared IP analysis section."""
        if not result.shared_ips:
            return ""

        section = "*🔴 Shared IP Analysis*"

        for ip in result.shared_ips:
            geo = result.geolocation_data.get(ip)
            if not geo:
                continue

            section += f"\n\n*IP: `{ip}`*"
            section += f"\n📍 {geo.city}, {geo.region}, {geo.country}"
            section += f"\n🏢 {geo.org}"
            section += f"\n🌍 Coordinates: {geo.loc}"

            # User 1 access info
            if ip in result.user1_ips:
                logs = result.user1_ips[ip]
                first = datetime.fromtimestamp(logs[0].date_first).strftime("%b %d, %H:%M")
                last = datetime.fromtimestamp(logs[0].date_last).strftime("%b %d, %H:%M")
                section += f"\n• *{result.user1.real_name}:* {logs[0].count} accesses ({first} → {last})"

            # User 2 access info
            if ip in result.user2_ips:
                logs = result.user2_ips[ip]
                first = datetime.fromtimestamp(logs[0].date_first).strftime("%b %d, %H:%M")
                last = datetime.fromtimestamp(logs[0].date_last).strftime("%b %d, %H:%M")
                section += f"\n• *{result.user2.real_name}:* {logs[0].count} accesses ({first} → {last})"

        return section

    def _format_locations(self, result: IPAnalysisResult) -> str:
        """Format geographic analysis section."""
        sections = []

        # User 1 locations
        user1_locs = "\n".join(
            f"• {loc}" + (" 🔴 *SHARED*" if loc in result.shared_locations else "")
            for loc in sorted(result.user1_locations)
        )
        sections.append(f"*📍 {result.user1.real_name} Locations*\n{user1_locs}")

        # User 2 locations
        user2_locs = "\n".join(
            f"• {loc}" + (" 🔴 *SHARED*" if loc in result.shared_locations else "")
            for loc in sorted(result.user2_locations)
        )
        sections.append(f"*📍 {result.user2.real_name} Locations*\n{user2_locs}")

        # Shared locations
        if result.shared_locations:
            shared_locs = "\n".join(f"• {loc}" for loc in sorted(result.shared_locations))
            sections.append(f"*🔴 Shared Locations*\n{shared_locs}")

        return "\n\n".join(sections)

    def _format_footer(self) -> str:
        """Format report footer."""
        return """---
_This report was automatically generated by *slack-shepherd*_
_Watching over your workspace security_ 🐑"""
