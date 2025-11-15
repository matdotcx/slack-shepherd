"""IP analysis result models."""
from dataclasses import dataclass
from typing import Dict, List, Set
from .user import User
from .access_log import AccessLog


@dataclass
class GeoLocation:
    """Represents geolocation data for an IP address."""

    ip: str
    city: str
    region: str
    country: str
    loc: str  # "latitude,longitude"
    org: str  # ISP/Organization
    postal: str = ""
    timezone: str = ""

    @classmethod
    def from_ipinfo_response(cls, ip: str, data: dict) -> 'GeoLocation':
        """Create GeoLocation from ipinfo.io API response."""
        return cls(
            ip=ip,
            city=data.get('city', 'Unknown'),
            region=data.get('region', 'Unknown'),
            country=data.get('country', 'Unknown'),
            loc=data.get('loc', '0,0'),
            org=data.get('org', 'Unknown'),
            postal=data.get('postal', ''),
            timezone=data.get('timezone', '')
        )


@dataclass
class IPAnalysisResult:
    """Complete IP analysis results for two users."""

    user1: User
    user2: User
    user1_ips: Dict[str, List[AccessLog]]  # IP -> list of access logs
    user2_ips: Dict[str, List[AccessLog]]
    shared_ips: Set[str]
    user1_locations: Set[str]  # Set of "City, Region, Country"
    user2_locations: Set[str]
    shared_locations: Set[str]
    geolocation_data: Dict[str, GeoLocation]  # IP -> geolocation
    total_logs_analyzed: int
    date_range_days: int = 0
