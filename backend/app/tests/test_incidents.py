"""
Tests for incident linking logic (haversine + find_or_create).
"""

import pytest
from unittest.mock import MagicMock, patch
from app.utils.helpers import haversine_distance
from app.models.complaint import Complaint
from app.models.incident import Incident
from app.services.incident_service import IncidentService


class TestHaversineDistance:
    def test_same_point_is_zero(self):
        assert haversine_distance(28.6, 77.2, 28.6, 77.2) == pytest.approx(0.0, abs=1e-3)

    def test_known_distance(self):
        # Delhi to Agra is roughly 200 km
        dist = haversine_distance(28.6139, 77.2090, 27.1767, 78.0081)
        assert 190_000 < dist < 210_000

    def test_within_500m(self):
        # ~400 metres apart
        dist = haversine_distance(28.6000, 77.2000, 28.6036, 77.2000)
        assert dist < 500

    def test_beyond_500m(self):
        # ~1.1 km apart
        dist = haversine_distance(28.6000, 77.2000, 28.6100, 77.2000)
        assert dist > 500


class TestIncidentService:
    def _make_complaint(self, **kwargs) -> Complaint:
        defaults = dict(
            reporter_id="test_reporter",
            latitude=28.6139,
            longitude=77.2090,
            location_accuracy=10.0,
            category="Water Supply",
            subcategory="No Water Supply",
            severity="High",
            authority="PHED",
            status="OPEN",
        )
        defaults.update(kwargs)
        return Complaint(**defaults)

    def test_links_to_existing_nearby_incident(self):
        mock_repo = MagicMock()
        existing = Incident(
            id="existing-id",
            title="Water Supply – Delhi",
            category="Water Supply",
            severity="High",
            authority="PHED",
            latitude=28.6140,
            longitude=77.2091,
            status="OPEN",
            complaint_count=2,
        )
        mock_repo.find_nearby_open.return_value = existing
        mock_repo.increment_complaint_count.return_value = None

        service = IncidentService(repo=mock_repo)
        complaint = self._make_complaint()
        incident = service.find_or_create_incident(complaint)

        assert incident.id == "existing-id"
        mock_repo.increment_complaint_count.assert_called_once_with("existing-id")
        mock_repo.create.assert_not_called()

    def test_creates_new_incident_when_none_nearby(self):
        mock_repo = MagicMock()
        mock_repo.find_nearby_open.return_value = None

        new_incident = Incident(
            id="new-id",
            title="Water Supply – Unknown Location",
            category="Water Supply",
            severity="High",
            authority="PHED",
            latitude=28.6139,
            longitude=77.2090,
            status="OPEN",
            complaint_count=1,
        )
        mock_repo.create.return_value = new_incident

        service = IncidentService(repo=mock_repo)
        complaint = self._make_complaint()
        incident = service.find_or_create_incident(complaint)

        assert incident.id == "new-id"
        mock_repo.create.assert_called_once()
        mock_repo.increment_complaint_count.assert_not_called()

    def test_incident_title_includes_district(self):
        mock_repo = MagicMock()
        mock_repo.find_nearby_open.return_value = None
        mock_repo.create.side_effect = lambda i: i

        service = IncidentService(repo=mock_repo)
        complaint = self._make_complaint(district="South Delhi", state="Delhi")
        incident = service.find_or_create_incident(complaint)

        assert "South Delhi" in incident.title
