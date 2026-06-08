"""
Analytics service – computes all dashboard metrics from repositories.
No business logic in routes. All computation lives here.
"""

from __future__ import annotations
from datetime import datetime, timezone, timedelta
from collections import defaultdict

from app.repositories.analytics_repository import AnalyticsRepository
from app.schemas.analytics import (
    OverviewResponse,
    CategoryStat,
    DistrictStat,
    TrendPoint,
    TrendsResponse,
    GeospatialResponse,
    GeospatialComplaint,
    GeospatialIncident,
)
from app.core.logging import get_logger

log = get_logger(__name__)


class AnalyticsService:
    def __init__(self, repo: AnalyticsRepository) -> None:
        self._repo = repo

    def get_overview(self) -> OverviewResponse:
        log.info("Computing analytics overview")
        c = self._repo.complaints
        i = self._repo.incidents

        total_complaints = c.count_total()
        open_complaints = c.count_by_status("OPEN")
        resolved_complaints = c.count_by_status("RESOLVED")
        critical_complaints = c.count_by_severity("Critical")

        total_incidents = i.count_total()
        open_incidents = i.count_by_status("OPEN")
        resolved_incidents = i.count_by_status("RESOLVED")

        resolution_rate = (
            resolved_complaints / total_complaints if total_complaints > 0 else 0.0
        )

        avg_resolution_time = self._compute_avg_resolution_hours()

        return OverviewResponse(
            total_complaints=total_complaints,
            open_complaints=open_complaints,
            resolved_complaints=resolved_complaints,
            critical_complaints=critical_complaints,
            total_incidents=total_incidents,
            open_incidents=open_incidents,
            resolved_incidents=resolved_incidents,
            resolution_rate=round(resolution_rate, 4),
            average_resolution_time=round(avg_resolution_time, 2),
        )

    def _compute_avg_resolution_hours(self) -> float:
        rows = self._repo.complaints.get_resolved_with_times()
        if not rows:
            return 0.0
        total_hours = 0.0
        count = 0
        for row in rows:
            try:
                created = datetime.fromisoformat(str(row["created_at"]).replace("Z", "+00:00"))
                updated = datetime.fromisoformat(str(row["updated_at"]).replace("Z", "+00:00"))
                delta_hours = (updated - created).total_seconds() / 3600
                total_hours += max(delta_hours, 0)
                count += 1
            except Exception:
                continue
        return total_hours / count if count > 0 else 0.0

    def get_category_distribution(self) -> list[CategoryStat]:
        log.info("Computing category distribution")
        raw = self._repo.complaints.get_category_distribution()
        return [CategoryStat(category=r["category"], count=r["count"]) for r in raw]

    def get_district_distribution(self) -> list[DistrictStat]:
        log.info("Computing district distribution")
        raw = self._repo.complaints.get_district_distribution()
        return [DistrictStat(district=r["district"], count=r["count"]) for r in raw]

    def get_trends(self, range_str: str) -> TrendsResponse:
        log.info("Computing trends for range=%s", range_str)
        days_map = {"7d": 7, "30d": 30, "90d": 90}
        days = days_map.get(range_str, 7)

        since = datetime.now(timezone.utc) - timedelta(days=days)
        since_iso = since.isoformat()

        complaint_rows = self._repo.complaints.get_complaints_since(since_iso)
        incident_rows = self._repo.incidents.get_incidents_since(since_iso)

        # Build day-keyed counts
        complaint_by_day: dict[str, int] = defaultdict(int)
        for row in complaint_rows:
            day = str(row["created_at"])[:10]
            complaint_by_day[day] += 1

        incident_by_day: dict[str, int] = defaultdict(int)
        for row in incident_rows:
            day = str(row["created_at"])[:10]
            incident_by_day[day] += 1

        # Build ordered date list
        data: list[TrendPoint] = []
        for i in range(days):
            d = (since + timedelta(days=i)).strftime("%Y-%m-%d")
            data.append(
                TrendPoint(
                    date=d,
                    complaints=complaint_by_day.get(d, 0),
                    incidents=incident_by_day.get(d, 0),
                )
            )

        return TrendsResponse(range=range_str, data=data)

    def get_geospatial(self) -> GeospatialResponse:
        log.info("Fetching geospatial data")
        complaint_rows = self._repo.complaints.get_all_coordinates()
        incident_rows = self._repo.incidents.get_all_coordinates()

        complaints = [
            GeospatialComplaint(
                id=r["id"],
                latitude=r["latitude"],
                longitude=r["longitude"],
                category=r["category"],
                severity=r["severity"],
                status=r["status"],
            )
            for r in complaint_rows
        ]

        incidents = [
            GeospatialIncident(
                id=r["id"],
                latitude=r["latitude"],
                longitude=r["longitude"],
                category=r["category"],
                severity=r["severity"],
                status=r["status"],
                complaint_count=r["complaint_count"],
            )
            for r in incident_rows
        ]

        return GeospatialResponse(complaints=complaints, incidents=incidents)
