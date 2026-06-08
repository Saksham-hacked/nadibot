"""
FastAPI dependency injection factories.
All services and repositories are wired here.
Route files import only from this module.
"""

from __future__ import annotations
from functools import lru_cache
from fastapi import Header, HTTPException, status

from app.db.supabase import get_supabase_client
from app.core.security import verify_admin_key
from app.core.exceptions import AdminAuthError

# ── Repositories ───────────────────────────────────────────────────────────────

from app.repositories.complaint_repository import ComplaintRepository
from app.repositories.incident_repository import IncidentRepository
from app.repositories.reporter_repository import ReporterRepository
from app.repositories.analytics_repository import AnalyticsRepository
from app.repositories.location_repository import LocationRepository

# ── Services ───────────────────────────────────────────────────────────────────

from app.services.gemini_service import GeminiService
from app.services.storage_service import build_storage_service, StorageService
from app.services.media_processing_service import MediaProcessingService
from app.services.authority_service import AuthorityService
from app.services.incident_service import IncidentService
from app.services.reporter_service import ReporterService
from app.services.transcript_service import GeocodingService
from app.services.analytics_service import AnalyticsService
from app.services.complaint_service import ComplaintService


# ── Singletons (created once per process) ─────────────────────────────────────

@lru_cache(maxsize=1)
def _gemini() -> GeminiService:
    return GeminiService()

@lru_cache(maxsize=1)
def _storage() -> StorageService:
    return build_storage_service()

@lru_cache(maxsize=1)
def _location_cache() -> LocationRepository:
    return LocationRepository()


# ── Public dependency functions (called by FastAPI DI) ────────────────────────

def get_complaint_service() -> ComplaintService:
    client = get_supabase_client()
    geocoding = GeocodingService(cache=_location_cache())
    return ComplaintService(
        complaint_repo=ComplaintRepository(client),
        gemini=_gemini(),
        media=MediaProcessingService(storage=_storage(), gemini=_gemini()),
        authority=AuthorityService(),
        incident=IncidentService(repo=IncidentRepository(client)),
        reporter=ReporterService(repo=ReporterRepository(client)),
        geocoding=geocoding,
    )


def get_incident_service() -> IncidentService:
    client = get_supabase_client()
    return IncidentService(repo=IncidentRepository(client))


def get_analytics_service() -> AnalyticsService:
    client = get_supabase_client()
    return AnalyticsService(repo=AnalyticsRepository(client))


# ── Admin key guard ────────────────────────────────────────────────────────────

def require_admin(x_admin_key: str = Header(..., alias="X-Admin-Key")) -> None:
    """
    FastAPI dependency that validates the X-Admin-Key header.
    Raises HTTP 401 on failure.
    """
    try:
        verify_admin_key(x_admin_key)
    except AdminAuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": exc.message},
        )
