"""
Shared/common schema components reused across the codebase.
"""

from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class OKResponse(BaseModel):
    ok: bool = True
    message: str = "Success"


class ErrorResponse(BaseModel):
    ok: bool = False
    error: str
    details: dict = Field(default_factory=dict)


class PaginationMeta(BaseModel):
    total: int
    page: int
    page_size: int


def new_uuid() -> str:
    return str(uuid.uuid4())


def utcnow() -> datetime:
    from datetime import timezone
    return datetime.now(timezone.utc)
