"""
Domain-level input validators (beyond Pydantic field-level validation).
"""

from __future__ import annotations
from app.core.exceptions import LocationMissingError, ValidationError


def validate_coordinates(latitude: float, longitude: float, accuracy: float) -> None:
    """
    Raise LocationMissingError if coordinates are outside valid ranges.
    Pydantic already enforces ge/le bounds; this is an extra safeguard.
    """
    if not (-90.0 <= latitude <= 90.0):
        raise LocationMissingError(
            "Latitude must be between -90 and 90.",
            {"latitude": latitude},
        )
    if not (-180.0 <= longitude <= 180.0):
        raise LocationMissingError(
            "Longitude must be between -180 and 180.",
            {"longitude": longitude},
        )
    if accuracy <= 0:
        raise LocationMissingError(
            "Location accuracy must be a positive number.",
            {"accuracy": accuracy},
        )


def validate_reporter_id_format(reporter_id: str) -> bool:
    """
    Basic sanity check – reporter IDs must be non-empty strings
    under 128 characters containing only safe characters.
    """
    import re
    if not reporter_id or len(reporter_id) > 128:
        return False
    return bool(re.match(r"^[a-zA-Z0-9_\-\.]+$", reporter_id))
