"""
Reporter domain model – represents an anonymous device session.
"""

from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.common import utcnow


class Reporter(BaseModel):
    id: str                    # UUID from DB
    reporter_id: str           # device-generated or server-assigned string
    complaint_count: int = 0
    first_seen_at: datetime = Field(default_factory=utcnow)
    last_seen_at: datetime = Field(default_factory=utcnow)

    model_config = {"from_attributes": True}
