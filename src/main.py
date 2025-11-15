"""
slack-shepherd - Main Orchestrator

A professional Slack workspace security tool for monitoring user access patterns.
Orchestrates the complete IP investigation workflow.
"""
from typing import Optional
from .config import Config
from .clients.slack_client import SlackClient
from .clients.geolocation_client import GeolocationClient
from .analyzers.ip_analyzer import IPAnalyzer
from .formatters.markdown_formatter import MarkdownFormatter
from .models.ip_analysis import IPAnalysisResult


class InvestigationOrchestrator:
    """Orchestrates the complete IP investigation workflow."""

    def __init__(self, config: Config):
        """Initialize orchestrator with configuration."""
        self.config = config
        self.slack_client = SlackClient(config.slack_token)
        self.geo_client = GeolocationClient()
        self.analyzer = IPAnalyzer()
        self.formatter = MarkdownFormatter()

    def run(self) -> Optional[str]:
        """
        Execute the complete investigation workflow.

        Returns:
            Markdown report string or None if error
        """
        print("=" * 80)
        print("slack-shepherd - Slack IP Investigation Tool")
        print("Watching over your workspace security")
        print("=" * 80)
        print()

        # Step 1: Fetch user information
        print("Fetching user information...")
        user1 = self.slack_client.get_user_info(self.config.user_id_1)
        user2 = self.slack_client.get_user_info(self.config.user_id_2)

        if not user1 or not user2:
            print("Error: Could not fetch user information")
            return None

        print(f"  User 1: {user1.real_name} (@{user1.name}) - {user1.id}")
        print(f"  User 2: {user2.real_name} (@{user2.name}) - {user2.id}")
        print()

        # Step 2: Fetch access logs
        print("Fetching access logs...")
        all_logs = self.slack_client.get_access_logs(self.config.max_pages, self.config.days_back)

        if not all_logs:
            print("Error: Could not fetch access logs")
            return None

        print(f"  Total logs fetched: {len(all_logs)}")
        print()

        # Step 3: Fetch geolocation data
        print("Fetching geolocation data...")
        # Get all unique IPs
        all_ips = set(log.ip for log in all_logs)
        geo_data = self.geo_client.lookup_batch(all_ips)
        print()

        # Step 4: Perform analysis
        print("Analyzing IP addresses...")
        result = self.analyzer.analyze(user1, user2, all_logs, geo_data)
        print(f"  User 1 unique IPs: {len(result.user1_ips)}")
        print(f"  User 2 unique IPs: {len(result.user2_ips)}")
        print(f"  Shared IPs: {len(result.shared_ips)}")
        print()

        # Step 5: Generate report
        print("Generating report...")
        report = self.formatter.format(result)
        print("  Report generated successfully")
        print()

        return report


def main():
    """Main entry point."""
    try:
        config = Config.from_env()
        orchestrator = InvestigationOrchestrator(config)
        report = orchestrator.run()

        if report:
            print("=" * 80)
            print("REPORT")
            print("=" * 80)
            print()
            print(report)
            return 0
        else:
            print("Investigation failed")
            return 1

    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
