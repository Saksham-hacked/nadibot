"""
Authority dashboard routes.
All endpoints require X-Admin-Key header.
"""

from __future__ import annotations
from typing import Optional
from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_incident_service, get_complaint_service, require_admin
from app.services.incident_service import IncidentService
from app.services.complaint_service import ComplaintService
from app.schemas.incident import IncidentResponse, IncidentListResponse
from app.schemas.complaint import ComplaintListResponse, ComplaintResponse

router = APIRouter(
    prefix="/authorities",
    tags=["Authority Dashboard"],
    dependencies=[Depends(require_admin)],  # All routes in this router require admin key
)


@router.get("/incidents", response_model=IncidentListResponse)
def get_authority_incidents(
    authority: Optional[str] = Query(None, description="Filter by authority name"),
    status: Optional[str] = Query(None),
    district: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: IncidentService = Depends(get_incident_service),
) -> IncidentListResponse:
    """
    List incidents filtered by authority, status, district, or category.
    Used by the authority dashboard to manage their assigned incidents.
    """
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


@router.get("/complaints", response_model=ComplaintListResponse)
def get_authority_complaints(
    authority: Optional[str] = Query(None),
    status: Optional[str] = Query(None, description="e.g. OPEN, IN_PROGRESS"),
    district: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: ComplaintService = Depends(get_complaint_service),
) -> ComplaintListResponse:
    """
    List complaints for authority review.
    Filter by authority, status, district, or category.
    """
    complaints, total = service.list_complaints(
        status=status,
        category=category,
        authority=authority,
        district=district,
        page=page,
        page_size=page_size,
    )
    return ComplaintListResponse(
        complaints=complaints,
        total=total,
        page=page,
        page_size=page_size,
    )
