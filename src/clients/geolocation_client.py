"""IP geolocation client."""
import requests
from typing import Dict, Set, Optional
from ..models.ip_analysis import GeoLocation


class GeolocationClient:
    """Handles IP geolocation lookups with caching."""

    def __init__(self, timeout: int = 5):
        """Initialize geolocation client."""
        self.timeout = timeout
        self.cache: Dict[str, GeoLocation] = {}

    def lookup(self, ip: str) -> Optional[GeoLocation]:
        """
        Lookup geolocation for a single IP address.

        Args:
            ip: IP address to lookup

        Returns:
            GeoLocation object or None if lookup fails
        """
        # Check cache first
        if ip in self.cache:
            return self.cache[ip]

        try:
            response = requests.get(
                f"https://ipinfo.io/{ip}/json",
                timeout=self.timeout
            )

            if response.status_code == 200:
                data = response.json()
                geo = GeoLocation.from_ipinfo_response(ip, data)
                self.cache[ip] = geo
                return geo

        except Exception as e:
            print(f"  Warning: Could not lookup IP {ip}: {e}")

        return None

    def lookup_batch(self, ips: Set[str]) -> Dict[str, GeoLocation]:
        """
        Lookup geolocation for multiple IP addresses.

        Args:
            ips: Set of IP addresses to lookup

        Returns:
            Dictionary mapping IP to GeoLocation
        """
        results = {}
        total = len(ips)
        count = 0

        print(f"  Looking up geolocation for {total} unique IPs...")

        for ip in ips:
            count += 1
            if count % 10 == 0 or count == total:
                print(f"  Progress: {count}/{total} IPs processed")

            geo = self.lookup(ip)
            if geo:
                results[ip] = geo

        print(f"  Completed: {len(results)}/{total} successful lookups")
        return results
