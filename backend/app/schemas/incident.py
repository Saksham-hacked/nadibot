"""
Incident request and response schemas.
"""

from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.core.constants import IncidentStatus


class IncidentStatusUpdateRequest(BaseModel):
    status: IncidentStatus
    resolution_notes: Optional[str] = Field(None, max_length=2000)


class IncidentNotesUpdateRequest(BaseModel):
    resolution_notes: str = Field(..., min_length=1, max_length=2000)


class IncidentQueryParams(BaseModel):
    status: Optional[IncidentStatus] = None
    authority: Optional[str] = None
    district: Optional[str] = None
    category: Optional[str] = None
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


class IncidentResponse(BaseModel):
    id: str
    title: str
    category: str
    severity: str
    authority: str
    latitude: float
    longitude: float
    district: Optional[str]
    state: Optional[str]
    status: str
    complaint_count: int
    resolution_notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class IncidentListResponse(BaseModel):
    incidents: list[IncidentResponse]
    total: int
    page: int
    page_size: int
