"""Access log data model."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class AccessLog:
    """Represents a Slack access log entry."""

    user_id: str
    ip: str
    user_agent: str
    date_first: int
    date_last: int
    count: int
    isp: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict) -> 'Access Log':
        """Create AccessLog from Slack API response."""
        return cls(
            user_id=data.get('user_id', ''),
            ip=data.get('ip', ''),
            user_agent=data.get('user_agent', ''),
            date_first=data.get('date_first', 0),
            date_last=data.get('date_last', 0),
            count=data.get('count', 0)
        )
