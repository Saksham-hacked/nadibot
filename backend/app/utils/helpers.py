"""
General-purpose helpers.
"""

from __future__ import annotations
import math


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Return the great-circle distance in metres between two GPS coordinates.
    Uses the Haversine formula.
    """
    R = 6_371_000  # Earth radius in metres

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def truncate_string(text: str, max_len: int = 500) -> str:
    """Truncate a string to max_len characters, appending '…' if truncated."""
    if len(text) <= max_len:
        return text
    return text[:max_len - 1] + "…"


def safe_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default
