"""
Complaint routes – thin. All logic in ComplaintService.
"""

from __future__ import annotations
from typing import Optional
from fastapi import APIRouter, Depends, File, Form, UploadFile, Query

from app.api.dependencies import get_complaint_service
from app.services.complaint_service import ComplaintService
from app.schemas.complaint import (
    ComplaintCreateRequest,
    ComplaintResponse,
    ComplaintListResponse,
)

router = APIRouter(prefix="/complaints", tags=["Complaints"])


@router.post("", response_model=ComplaintResponse, status_code=201)
async def submit_complaint(
    # Form fields
    latitude: float = Form(...),
    longitude: float = Form(...),
    accuracy: float = Form(...),
    text: Optional[str] = Form(None),
    reporter_id: Optional[str] = Form(None),
    location_source: Optional[str] = Form(None),
    # Files
    image: Optional[UploadFile] = File(None),
    audio: Optional[UploadFile] = File(None),
    # Dependency
    service: ComplaintService = Depends(get_complaint_service),
) -> ComplaintResponse:
    """
    Submit a citizen water complaint.
    Accepts multipart/form-data with optional image and audio files.
    At least one of: text, image, or audio must be present.
    GPS coordinates are required.
    """
    request = ComplaintCreateRequest(
        reporter_id=reporter_id,
        text=text,
        latitude=latitude,
        longitude=longitude,
        accuracy=accuracy,
        location_source=location_source,
    )
    return await service.submit_complaint(
        request=request,
        image_file=image if (image and image.filename) else None,
        audio_file=audio if (audio and audio.filename) else None,
    )


@router.get("/{complaint_id}", response_model=ComplaintResponse)
def get_complaint(
    complaint_id: str,
    service: ComplaintService = Depends(get_complaint_service),
) -> ComplaintResponse:
    """Fetch a single complaint by ID."""
    return service.get_complaint(complaint_id)


@router.get("", response_model=ComplaintListResponse)
def list_complaints(
    status: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    authority: Optional[str] = Query(None),
    district: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: ComplaintService = Depends(get_complaint_service),
) -> ComplaintListResponse:
    """List complaints with optional filters. Paginated."""
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


@router.get("/reporter/{reporter_id}", response_model=list[ComplaintResponse])
def get_reporter_complaints(
    reporter_id: str,
    service: ComplaintService = Depends(get_complaint_service),
) -> list[ComplaintResponse]:
    """Fetch all complaints submitted by a specific anonymous reporter."""
    return service.get_reporter_complaints(reporter_id)
