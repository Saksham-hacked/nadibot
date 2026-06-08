"""
Location repository – simple in-memory cache for reverse geocoding results.
No DB table; cache lives in-process memory.
"""

from __future__ import annotations
import time
from typing import Optional
from app.core.constants import GEOCODING_CACHE_TTL_SECONDS, GEOCODING_COORD_PRECISION


class LocationRepository:
    """
    In-memory TTL cache for geocoding results.
    Key: rounded (lat, lon) tuple. Value: (result_dict, expiry_timestamp).
    """

    def __init__(self) -> None:
        self._cache: dict[tuple[float, float], tuple[dict, float]] = {}

    def _make_key(self, lat: float, lon: float) -> tuple[float, float]:
        p = GEOCODING_COORD_PRECISION
        return (round(lat, p), round(lon, p))

    def get(self, lat: float, lon: float) -> Optional[dict]:
        key = self._make_key(lat, lon)
        entry = self._cache.get(key)
        if entry is None:
            return None
        result, expiry = entry
        if time.monotonic() > expiry:
            del self._cache[key]
            return None
        return result

    def set(self, lat: float, lon: float, result: dict) -> None:
        key = self._make_key(lat, lon)
        self._cache[key] = (result, time.monotonic() + GEOCODING_CACHE_TTL_SECONDS)

    def clear(self) -> None:
        self._cache.clear()
