"""
Tests for analytics service calculations.
"""

import pytest
from unittest.mock import MagicMock
from app.services.analytics_service import AnalyticsService
from app.repositories.analytics_repository import AnalyticsRepository


def _make_analytics_service(
    total_complaints=10,
    open_complaints=6,
    resolved_complaints=4,
    critical_complaints=2,
    total_incidents=3,
    open_incidents=2,
    resolved_incidents=1,
    category_dist=None,
    district_dist=None,
    resolved_times=None,
) -> AnalyticsService:
    mock_repo = MagicMock(spec=AnalyticsRepository)

    mock_repo.complaints.count_total.return_value = total_complaints
    mock_repo.complaints.count_by_status.side_effect = lambda s: (
        open_complaints if s == "OPEN" else resolved_complaints if s == "RESOLVED" else 0
    )
    mock_repo.complaints.count_by_severity.return_value = critical_complaints
    mock_repo.complaints.get_category_distribution.return_value = category_dist or [
        {"category": "Water Supply", "count": 5},
        {"category": "Flooding", "count": 3},
        {"category": "Other", "count": 2},
    ]
    mock_repo.complaints.get_district_distribution.return_value = district_dist or [
        {"district": "South Delhi", "count": 7},
        {"district": "North Delhi", "count": 3},
    ]
    mock_repo.complaints.get_resolved_with_times.return_value = resolved_times or []
    mock_repo.complaints.get_complaints_since.return_value = []
    mock_repo.complaints.get_all_coordinates.return_value = []

    mock_repo.incidents.count_total.return_value = total_incidents
    mock_repo.incidents.count_by_status.side_effect = lambda s: (
        open_incidents if s == "OPEN" else resolved_incidents if s == "RESOLVED" else 0
    )
    mock_repo.incidents.get_incidents_since.return_value = []
    mock_repo.incidents.get_all_coordinates.return_value = []

    return AnalyticsService(repo=mock_repo)


class TestAnalyticsOverview:
    def test_basic_overview(self):
        svc = _make_analytics_service()
        overview = svc.get_overview()
        assert overview.total_complaints == 10
        assert overview.open_complaints == 6
        assert overview.resolved_complaints == 4
        assert overview.critical_complaints == 2
        assert overview.total_incidents == 3

    def test_resolution_rate_calculation(self):
        svc = _make_analytics_service(total_complaints=10, resolved_complaints=4)
        overview = svc.get_overview()
        assert overview.resolution_rate == pytest.approx(0.4, abs=1e-4)

    def test_resolution_rate_zero_when_no_complaints(self):
        svc = _make_analytics_service(total_complaints=0, resolved_complaints=0)
        overview = svc.get_overview()
        assert overview.resolution_rate == 0.0

    def test_avg_resolution_time_with_data(self):
        from datetime import datetime, timezone, timedelta
        now = datetime.now(timezone.utc)
        six_hours_ago = now - timedelta(hours=6)
        resolved_times = [
            {"created_at": six_hours_ago.isoformat(), "updated_at": now.isoformat()},
            {"created_at": six_hours_ago.isoformat(), "updated_at": now.isoformat()},
        ]
        svc = _make_analytics_service(resolved_times=resolved_times)
        overview = svc.get_overview()
        assert overview.average_resolution_time == pytest.approx(6.0, abs=0.1)

    def test_avg_resolution_time_zero_when_no_resolved(self):
        svc = _make_analytics_service(resolved_times=[])
        overview = svc.get_overview()
        assert overview.average_resolution_time == 0.0


class TestCategoryDistribution:
    def test_returns_correct_categories(self):
        svc = _make_analytics_service()
        cats = svc.get_category_distribution()
        names = [c.category for c in cats]
        assert "Water Supply" in names
        assert "Flooding" in names

    def test_counts_are_correct(self):
        svc = _make_analytics_service()
        cats = {c.category: c.count for c in svc.get_category_distribution()}
        assert cats["Water Supply"] == 5
        assert cats["Other"] == 2


class TestTrends:
    def test_trends_returns_correct_range_length(self):
        svc = _make_analytics_service()
        result = svc.get_trends("7d")
        assert result.range == "7d"
        assert len(result.data) == 7

    def test_trends_30d(self):
        svc = _make_analytics_service()
        result = svc.get_trends("30d")
        assert len(result.data) == 30

    def test_trends_data_points_have_correct_fields(self):
        svc = _make_analytics_service()
        result = svc.get_trends("7d")
        for point in result.data:
            assert hasattr(point, "date")
            assert hasattr(point, "complaints")
            assert hasattr(point, "incidents")
