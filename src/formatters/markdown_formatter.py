"""Markdown report formatter."""
from datetime import datetime
from ..models.ip_analysis import IPAnalysisResult


class MarkdownFormatter:
    """Formats IP analysis results as markdown for GitHub Issues."""

    def format(self, result: IPAnalysisResult) -> str:
        """
        Generate a complete markdown report.

        Args:
            result: IPAnalysisResult object

        Returns:
            Formatted markdown string
        """
        sections = [
            self._format_header(result),
            self._format_summary(result),
            self._format_verdict(result),
            self._format_user_details(result),
            self._format_shared_ips(result),
            self._format_geographic_analysis(result),
            self._format_footer()
        ]

        return "\n\n".join(sections)

    def _format_header(self, result: IPAnalysisResult) -> str:
        """Format report header."""
        return f"""# IP Comparison Analysis Report

**Analysis Date:** {datetime.now().strftime("%B %d, %Y at %H:%M UTC")}
**Search Window:** Last {result.days_back} days
**Activity Span:** {result.date_range_days} days (actual data range)
**Total Records Analyzed:** {result.total_logs_analyzed:,}"""

    def _format_summary(self, result: IPAnalysisResult) -> str:
        """Format executive summary table."""
        return f"""## Summary

| Metric | Value |
|--------|-------|
| **User 1** | {result.user1.real_name} (@{result.user1.name}) |
| **User 2** | {result.user2.real_name} (@{result.user2.name}) |
| **User 1 Unique IPs** | {len(result.user1_ips)} |
| **User 2 Unique IPs** | {len(result.user2_ips)} |
| **Shared IP Addresses** | **{len(result.shared_ips)}** |
| **Shared Locations** | **{len(result.shared_locations)}** |"""

    def _format_verdict(self, result: IPAnalysisResult) -> str:
        """Format verdict section."""
        if len(result.shared_ips) > 0:
            return f"""## Verdict

> ### SHARED IP ADDRESSES DETECTED
>
> These users have accessed Slack from **{len(result.shared_ips)} common IP address(es)**.
>
> This could indicate:
> - Shared network access (same office/building)
> - Same physical location
> - Duplicate/shadow accounts (one person with multiple accounts)
> - Potential account sharing"""
        else:
            return """## Verdict

> ### NO SHARED IP ADDRESSES
>
> These users have not accessed Slack from any common IP addresses during the analyzed period."""

    def _format_user_details(self, result: IPAnalysisResult) -> str:
        """Format detailed IP information for both users."""
        user1_section = self._format_user_ip_table(
            result.user1,
            result.user1_ips,
            result.geolocation_data,
            result.shared_ips
        )

        user2_section = self._format_user_ip_table(
            result.user2,
            result.user2_ips,
            result.geolocation_data,
            result.shared_ips
        )

        return f"""## Detailed IP Information

### User 1: {result.user1.real_name} (@{result.user1.name})

{user1_section}

### User 2: {result.user2.real_name} (@{result.user2.name})

{user2_section}"""

    def _format_user_ip_table(self, user, ip_map, geo_data, shared_ips) -> str:
        """Format IP table for a single user."""
        if not ip_map:
            return "*No IP data available*"

        lines = ["| IP Address | Location | ISP | First Seen | Last Seen | Access Count |",
                 "|------------|----------|-----|------------|-----------|--------------|"]

        for ip, logs in ip_map.items():
            # Mark shared IPs
            ip_display = f"**{ip}** (SHARED)" if ip in shared_ips else ip

            # Get geolocation
            if ip in geo_data:
                geo = geo_data[ip]
                location = f"{geo.city}, {geo.region}, {geo.country}"
                isp = geo.org
            else:
                location = "Unknown"
                isp = "Unknown"

            # Get timestamps
            first_seen = datetime.fromtimestamp(logs[0].date_first).strftime("%b %d, %Y")
            last_seen = datetime.fromtimestamp(logs[0].date_last).strftime("%b %d, %Y")
            count = sum(log.count for log in logs)

            lines.append(f"| {ip_display} | {location} | {isp} | {first_seen} | {last_seen} | {count} |")

        return "\n".join(lines)

    def _format_shared_ips(self, result: IPAnalysisResult) -> str:
        """Format detailed analysis of shared IPs."""
        if not result.shared_ips:
            return ""

        lines = ["## Shared IP Analysis\n"]

        for ip in result.shared_ips:
            lines.append(f"### IP: {ip}\n")

            # Geolocation
            if ip in result.geolocation_data:
                geo = result.geolocation_data[ip]
                lines.append(f"**Location:** {geo.city}, {geo.region}, {geo.country}")
                lines.append(f"**ISP:** {geo.org}")
                lines.append(f"**Coordinates:** {geo.loc}\n")

            # User 1 activity
            if ip in result.user1_ips:
                logs = result.user1_ips[ip]
                first = datetime.fromtimestamp(logs[0].date_first).strftime("%b %d, %Y %H:%M")
                last = datetime.fromtimestamp(logs[0].date_last).strftime("%b %d, %Y %H:%M")
                count = sum(log.count for log in logs)
                lines.append(f"**{result.user1.real_name}:** {count} accesses from {first} to {last}")

            # User 2 activity
            if ip in result.user2_ips:
                logs = result.user2_ips[ip]
                first = datetime.fromtimestamp(logs[0].date_first).strftime("%b %d, %Y %H:%M")
                last = datetime.fromtimestamp(logs[0].date_last).strftime("%b %d, %Y %H:%M")
                count = sum(log.count for log in logs)
                lines.append(f"**{result.user2.real_name}:** {count} accesses from {first} to {last}")

            lines.append("\n---\n")

        return "\n".join(lines)

    def _format_geographic_analysis(self, result: IPAnalysisResult) -> str:
        """Format geographic analysis section."""
        lines = ["## Geographic Analysis\n"]

        lines.append(f"### {result.user1.real_name} Locations")
        if result.user1_locations:
            for loc in sorted(result.user1_locations):
                marker = " (SHARED)" if loc in result.shared_locations else ""
                lines.append(f"- {loc}{marker}")
        else:
            lines.append("*No location data*")

        lines.append(f"\n### {result.user2.real_name} Locations")
        if result.user2_locations:
            for loc in sorted(result.user2_locations):
                marker = " (SHARED)" if loc in result.shared_locations else ""
                lines.append(f"- {loc}{marker}")
        else:
            lines.append("*No location data*")

        if result.shared_locations:
            lines.append("\n### Shared Locations")
            for loc in sorted(result.shared_locations):
                lines.append(f"- {loc}")

        return "\n".join(lines)

    def _format_footer(self) -> str:
        """Format report footer."""
        return """---

*This report was automatically generated by **slack-shepherd***
*Watching over your workspace security*"""
