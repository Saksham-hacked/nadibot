"""
Analytics response schemas.
"""

from __future__ import annotations
from typing import Optional
from pydantic import BaseModel


class OverviewResponse(BaseModel):
    total_complaints: int
    open_complaints: int
    resolved_complaints: int
    critical_complaints: int
    total_incidents: int
    open_incidents: int
    resolved_incidents: int
    resolution_rate: float          # 0.0 – 1.0
    average_resolution_time: float  # hours


class CategoryStat(BaseModel):
    category: str
    count: int


class DistrictStat(BaseModel):
    district: str
    count: int


class TrendPoint(BaseModel):
    date: str    # ISO date string "YYYY-MM-DD"
    complaints: int
    incidents: int


class TrendsResponse(BaseModel):
    range: str
    data: list[TrendPoint]


class GeospatialComplaint(BaseModel):
    id: str
    latitude: float
    longitude: float
    category: str
    severity: str
    status: str


class GeospatialIncident(BaseModel):
    id: str
    latitude: float
    longitude: float
    category: str
    severity: str
    status: str
    complaint_count: int


class GeospatialResponse(BaseModel):
    complaints: list[GeospatialComplaint]
    incidents: list[GeospatialIncident]
