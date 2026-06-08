"""
Incident service – create incidents or link complaints to existing ones.
All geospatial matching logic lives here.
"""

from __future__ import annotations
from typing import Optional
from app.models.incident import Incident
from app.models.complaint import Complaint
from app.repositories.incident_repository import IncidentRepository
from app.schemas.incident import IncidentStatusUpdateRequest, IncidentNotesUpdateRequest
from app.core.config import get_settings
from app.core.logging import get_logger

log = get_logger(__name__)


class IncidentService:
    def __init__(self, repo: IncidentRepository) -> None:
        self._repo = repo

    def find_or_create_incident(self, complaint: Complaint) -> Incident:
        """
        Search for a matching open incident within the configured radius.
        If found → link. If not → create a new incident.
        """
        settings = get_settings()
        radius = settings.DEFAULT_INCIDENT_RADIUS_METERS

        existing = self._repo.find_nearby_open(
            latitude=complaint.latitude,
            longitude=complaint.longitude,
            category=complaint.category,
            authority=complaint.authority,
            radius_meters=radius,
        )

        if existing:
            log.info(
                "Linking complaint %s to existing incident %s",
                complaint.id, existing.id,
            )
            self._repo.increment_complaint_count(existing.id)
            return existing

        # Create new incident
        title = self._build_title(complaint)
        incident = Incident(
            title=title,
            category=complaint.category,
            severity=complaint.severity,
            authority=complaint.authority,
            latitude=complaint.latitude,
            longitude=complaint.longitude,
            district=complaint.district,
            state=complaint.state,
            status="OPEN",
            complaint_count=1,
        )
        created = self._repo.create(incident)
        log.info("New incident created: %s for category=%s", created.id, created.category)
        return created

    def _build_title(self, complaint: Complaint) -> str:
        location = complaint.district or complaint.state or "Unknown Location"
        return f"{complaint.category} – {location}"

    def update_status(
        self, incident_id: str, request: IncidentStatusUpdateRequest
    ) -> Incident:
        log.info("Updating incident %s status → %s", incident_id, request.status)
        return self._repo.update_status(
            incident_id=incident_id,
            status=request.status.value,
            resolution_notes=request.resolution_notes,
        )

    def update_notes(
        self, incident_id: str, request: IncidentNotesUpdateRequest
    ) -> Incident:
        log.info("Updating incident %s notes", incident_id)
        return self._repo.update_notes(incident_id, request.resolution_notes)

    def list_incidents(self, **filters) -> tuple[list[Incident], int]:
        return self._repo.list_incidents(**filters)
