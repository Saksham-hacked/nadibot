"""
Incident routes – PATCH endpoints are admin-protected.
"""

from __future__ import annotations
from typing import Optional
from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_incident_service, require_admin
from app.services.incident_service import IncidentService
from app.schemas.incident import (
    IncidentResponse,
    IncidentListResponse,
    IncidentStatusUpdateRequest,
    IncidentNotesUpdateRequest,
)

router = APIRouter(prefix="/incidents", tags=["Incidents"])


@router.get("", response_model=IncidentListResponse)
def list_incidents(
    status: Optional[str] = Query(None),
    authority: Optional[str] = Query(None),
    district: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: IncidentService = Depends(get_incident_service),
) -> IncidentListResponse:
    """List incidents with optional filters. Paginated."""
    incidents, total = service.list_incidents(
        status=status,
        authority=authority,
        district=district,
        category=category,
        page=page,
        page_size=page_size,
    )
    return IncidentListResponse(
        incidents=[IncidentResponse.model_validate(i.model_dump()) for i in incidents],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.patch("/{incident_id}/status", response_model=IncidentResponse)
def update_incident_status(
    incident_id: str,
    body: IncidentStatusUpdateRequest,
    service: IncidentService = Depends(get_incident_service),
    _: None = Depends(require_admin),
) -> IncidentResponse:
    """Update the status of an incident. Requires admin key."""
    incident = service.update_status(incident_id, body)
    return IncidentResponse.model_validate(incident.model_dump())


@router.patch("/{incident_id}/notes", response_model=IncidentResponse)
def update_incident_notes(
    incident_id: str,
    body: IncidentNotesUpdateRequest,
    service: IncidentService = Depends(get_incident_service),
    _: None = Depends(require_admin),
) -> IncidentResponse:
    """Add or update resolution notes on an incident. Requires admin key."""
    incident = service.update_notes(incident_id, body)
    return IncidentResponse.model_validate(incident.model_dump())
