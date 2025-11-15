"""Configuration management."""
import os
from dataclasses import dataclass


@dataclass
class Config:
    """Application configuration."""

    slack_token: str
    user_id_1: str
    user_id_2: str
    max_pages: int = 30
    days_back: int = 30  # Only analyze logs from last N days
    slack_channel: str = ""  # Optional: Post results to this Slack channel

    @classmethod
    def from_env(cls) -> 'Config':
        """Load configuration from environment variables."""
        slack_token = os.getenv('SLACK_USER_TOKEN')
        user_id_1 = os.getenv('USER_ID_1')
        user_id_2 = os.getenv('USER_ID_2')
        max_pages = int(os.getenv('MAX_PAGES', '30'))
        days_back = int(os.getenv('DAYS_BACK', '30'))
        slack_channel = os.getenv('SLACK_CHANNEL', '')

        if not slack_token:
            raise ValueError("SLACK_USER_TOKEN environment variable is required")
        if not user_id_1:
            raise ValueError("USER_ID_1 environment variable is required")
        if not user_id_2:
            raise ValueError("USER_ID_2 environment variable is required")

        return cls(
            slack_token=slack_token,
            user_id_1=user_id_1,
            user_id_2=user_id_2,
            max_pages=max_pages,
            days_back=days_back,
            slack_channel=slack_channel
        )
