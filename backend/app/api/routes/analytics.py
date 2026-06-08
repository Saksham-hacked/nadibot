"""
Analytics routes – read-only dashboard endpoints.
"""

from __future__ import annotations
from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_analytics_service
from app.services.analytics_service import AnalyticsService
from app.schemas.analytics import (
    OverviewResponse,
    CategoryStat,
    DistrictStat,
    TrendsResponse,
    GeospatialResponse,
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/overview", response_model=OverviewResponse)
def get_overview(
    service: AnalyticsService = Depends(get_analytics_service),
) -> OverviewResponse:
    """High-level dashboard statistics."""
    return service.get_overview()


@router.get("/categories", response_model=list[CategoryStat])
def get_categories(
    service: AnalyticsService = Depends(get_analytics_service),
) -> list[CategoryStat]:
    """Complaint count per category."""
    return service.get_category_distribution()


@router.get("/districts", response_model=list[DistrictStat])
def get_districts(
    service: AnalyticsService = Depends(get_analytics_service),
) -> list[DistrictStat]:
    """Complaint count per district."""
    return service.get_district_distribution()


@router.get("/trends", response_model=TrendsResponse)
def get_trends(
    range: str = Query("7d", pattern="^(7d|30d|90d)$"),
    service: AnalyticsService = Depends(get_analytics_service),
) -> TrendsResponse:
    """Complaint and incident counts over time. range: 7d | 30d | 90d"""
    return service.get_trends(range)


@router.get("/geospatial", response_model=GeospatialResponse)
def get_geospatial(
    service: AnalyticsService = Depends(get_analytics_service),
) -> GeospatialResponse:
    """All complaint and incident coordinates for map visualisation."""
    return service.get_geospatial()
