"""
Reverse geocoding service using OpenStreetMap Nominatim.
Caches results in the LocationRepository (in-memory TTL cache).
"""

from __future__ import annotations
from typing import Optional
import httpx

from app.repositories.location_repository import LocationRepository
from app.core.config import get_settings
from app.core.exceptions import GeocodingError
from app.core.logging import get_logger

log = get_logger(__name__)

NOMINATIM_BASE_URL = "https://nominatim.openstreetmap.org/reverse"


class GeocodingService:
    def __init__(self, cache: LocationRepository) -> None:
        self._cache = cache
        self._user_agent = get_settings().NOMINATIM_USER_AGENT

    async def reverse_geocode(self, latitude: float, longitude: float) -> dict:
        """
        Convert GPS coordinates into a location dict:
        {locality, district, state, full_address}

        Returns an empty dict on failure (non-fatal).
        """
        # Check cache first
        cached = self._cache.get(latitude, longitude)
        if cached is not None:
            log.info("Geocoding cache hit for (%.4f, %.4f)", latitude, longitude)
            return cached

        log.info("Reverse geocoding (%.6f, %.6f)", latitude, longitude)
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    NOMINATIM_BASE_URL,
                    params={
                        "lat": latitude,
                        "lon": longitude,
                        "format": "json",
                        "addressdetails": 1,
                    },
                    headers={"User-Agent": self._user_agent},
                )
                response.raise_for_status()
                data = response.json()
        except httpx.HTTPError as exc:
            log.warning("Nominatim request failed: %s", exc)
            return {}
        except Exception as exc:
            log.warning("Geocoding unexpected error: %s", exc)
            return {}

        address = data.get("address", {})

        # Nominatim returns different keys depending on location granularity
        locality = (
            address.get("village")
            or address.get("suburb")
            or address.get("town")
            or address.get("hamlet")
            or address.get("neighbourhood")
        )
        district = (
            address.get("county")
            or address.get("district")
            or address.get("city_district")
        )
        state = address.get("state")
        full_address = data.get("display_name")

        result = {
            "locality": locality,
            "district": district,
            "state": state,
            "full_address": full_address,
        }

        self._cache.set(latitude, longitude, result)
        log.info(
            "Geocoded (%.4f, %.4f) → district=%s, state=%s",
            latitude, longitude, district, state,
        )
        return result
