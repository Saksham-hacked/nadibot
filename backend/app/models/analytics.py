"""
Analytics domain model – intermediate data structures used by the analytics service.
"""

from __future__ import annotations
from pydantic import BaseModel


class OverviewStats(BaseModel):
    total_complaints: int = 0
    open_complaints: int = 0
    resolved_complaints: int = 0
    critical_complaints: int = 0
    total_incidents: int = 0
    open_incidents: int = 0
    resolved_incidents: int = 0
    resolution_rate: float = 0.0
    average_resolution_time: float = 0.0  # hours
