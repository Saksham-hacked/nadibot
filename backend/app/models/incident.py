"""
Incident domain model.
"""

from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.common import new_uuid, utcnow


class Incident(BaseModel):
    id: str = Field(default_factory=new_uuid)
    title: str
    category: str
    severity: str
    authority: str
    latitude: float
    longitude: float
    district: Optional[str] = None
    state: Optional[str] = None
    status: str = "OPEN"
    complaint_count: int = 0
    resolution_notes: Optional[str] = None
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)

    model_config = {"from_attributes": True}
