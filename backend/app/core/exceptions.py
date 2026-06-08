"""
Custom exception hierarchy for NadiBot.
All domain errors are subclasses of NadiBotError.
HTTP mapping is done in middleware, not here.
"""


class NadiBotError(Exception):
    """Base exception for all application errors."""

    def __init__(self, message: str, details: dict | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


# ── Validation ────────────────────────────────────────────────────────────────

class ValidationError(NadiBotError):
    """Input failed domain-level validation."""


class LocationMissingError(ValidationError):
    """GPS coordinates or accuracy were not provided."""


class MediaRequiredError(ValidationError):
    """No media (text/image/audio) was provided."""


class UnsupportedMediaTypeError(ValidationError):
    """Uploaded file has an unsupported MIME type."""


class FileTooLargeError(ValidationError):
    """Uploaded file exceeds the allowed size limit."""


# ── Not found ─────────────────────────────────────────────────────────────────

class NotFoundError(NadiBotError):
    """Requested resource does not exist."""


class ComplaintNotFoundError(NotFoundError):
    """Complaint record not found."""


class IncidentNotFoundError(NotFoundError):
    """Incident record not found."""


# ── Auth / admin ──────────────────────────────────────────────────────────────

class AdminAuthError(NadiBotError):
    """Invalid or missing admin key."""


# ── External services ─────────────────────────────────────────────────────────

class StorageError(NadiBotError):
    """File could not be uploaded or retrieved."""


class GeminiError(NadiBotError):
    """Gemini API call failed or returned unparseable output."""


class GeminiParseError(GeminiError):
    """Gemini returned a response that could not be parsed into the expected schema."""


class GeocodingError(NadiBotError):
    """Reverse geocoding failed."""


# ── Database ──────────────────────────────────────────────────────────────────

class DatabaseError(NadiBotError):
    """Supabase / database operation failed."""
