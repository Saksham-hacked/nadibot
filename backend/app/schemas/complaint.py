"""
Complaint request and response schemas.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator, model_validator
from app.core.constants import (
    ComplaintCategory,
    ComplaintSubcategory,
    SeverityLevel,
    ComplaintStatus,
    Authority,
)


# ── Request ────────────────────────────────────────────────────────────────────

class ComplaintCreateRequest(BaseModel):
    """
    Parsed from multipart/form-data in the route.
    Media files are handled separately as UploadFile.
    """
    reporter_id: Optional[str] = Field(None, description="Device-generated reporter ID")
    text: Optional[str] = Field(None, min_length=1, max_length=5000)
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    accuracy: float = Field(..., gt=0, description="GPS accuracy in metres")
    location_source: Optional[str] = Field(None, max_length=100)

    @field_validator("text")
    @classmethod
    def strip_text(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip()
            return v if v else None
        return v


class ComplaintQueryParams(BaseModel):
    """Filters for listing complaints (admin/authority use)."""
    status: Optional[ComplaintStatus] = None
    category: Optional[ComplaintCategory] = None
    authority: Optional[str] = None
    district: Optional[str] = None
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


# ── Response ───────────────────────────────────────────────────────────────────

class LocationResponse(BaseModel):
    latitude: float
    longitude: float
    location_accuracy: float
    location_source: Optional[str]
    locality: Optional[str]
    district: Optional[str]
    state: Optional[str]
    full_address: Optional[str]


class ComplaintResponse(BaseModel):
    id: str
    reporter_id: str
    text: Optional[str]
    transcript: Optional[str]
    image_url: Optional[str]
    audio_url: Optional[str]
    image_summary: Optional[str]
    location: LocationResponse
    category: str
    subcategory: str
    severity: str
    authority: str
    summary: Optional[str]
    confidence: Optional[float]
    status: str
    incident_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ComplaintListResponse(BaseModel):
    complaints: list[ComplaintResponse]
    total: int
    page: int
    page_size: int
