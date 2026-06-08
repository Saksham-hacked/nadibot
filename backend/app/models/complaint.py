"""
Complaint domain model – mirrors the DB row as a Python dataclass.
Pydantic v2 BaseModel used for easy serialisation.
"""

from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.common import new_uuid, utcnow


class Complaint(BaseModel):
    id: str = Field(default_factory=new_uuid)
    reporter_id: str
    text: Optional[str] = None
    transcript: Optional[str] = None
    image_url: Optional[str] = None
    audio_url: Optional[str] = None
    image_summary: Optional[str] = None

    # Raw GPS
    latitude: float
    longitude: float
    location_accuracy: float
    location_source: Optional[str] = None

    # Resolved location
    locality: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    full_address: Optional[str] = None

    # Classification
    category: str = "Other"
    subcategory: str = "Other"
    severity: str = "Medium"
    authority: str = "General Grievance"
    summary: Optional[str] = None
    confidence: Optional[float] = None

    # Workflow
    status: str = "OPEN"
    incident_id: Optional[str] = None

    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)

    model_config = {"from_attributes": True}
