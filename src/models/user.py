"""User data model."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """Represents a Slack user."""

    id: str
    name: str
    real_name: str
    email: str
    updated: int
    is_bot: bool
    last_message_ts: Optional[float] = None

    @classmethod
    def from_api_response(cls, data: dict) -> 'User':
        """Create User from Slack API response."""
        profile = data.get('profile', {})
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            real_name=profile.get('real_name', ''),
            email=profile.get('email', ''),
            updated=data.get('updated', 0),
            is_bot=data.get('is_bot', False),
            last_message_ts=None
        )
