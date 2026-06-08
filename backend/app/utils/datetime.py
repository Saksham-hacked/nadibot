"""
Datetime utilities.
"""

from __future__ import annotations
from datetime import datetime, timezone


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def to_iso(dt: datetime) -> str:
    return dt.isoformat()


def from_iso(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))
