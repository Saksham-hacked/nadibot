"""
Tests for complaint validation logic.
"""

import pytest
from pydantic import ValidationError as PydanticValidationError
from app.schemas.complaint import ComplaintCreateRequest
from app.core.exceptions import MediaRequiredError, LocationMissingError
from app.utils.validators import validate_coordinates


class TestComplaintCreateRequest:
    def test_valid_minimal_request(self):
        req = ComplaintCreateRequest(
            latitude=28.6139,
            longitude=77.2090,
            accuracy=10.0,
            text="There is no water supply in my area.",
        )
        assert req.latitude == 28.6139
        assert req.text == "There is no water supply in my area."

    def test_text_is_stripped(self):
        req = ComplaintCreateRequest(
            latitude=28.6139,
            longitude=77.2090,
            accuracy=10.0,
            text="  leaking pipe   ",
        )
        assert req.text == "leaking pipe"

    def test_whitespace_only_text_becomes_none(self):
        req = ComplaintCreateRequest(
            latitude=28.6139,
            longitude=77.2090,
            accuracy=10.0,
            text="   ",
        )
        assert req.text is None

    def test_invalid_latitude_raises(self):
        with pytest.raises(PydanticValidationError):
            ComplaintCreateRequest(
                latitude=95.0,  # invalid
                longitude=77.2090,
                accuracy=10.0,
                text="test",
            )

    def test_invalid_longitude_raises(self):
        with pytest.raises(PydanticValidationError):
            ComplaintCreateRequest(
                latitude=28.6,
                longitude=200.0,  # invalid
                accuracy=10.0,
                text="test",
            )

    def test_zero_accuracy_raises(self):
        with pytest.raises(PydanticValidationError):
            ComplaintCreateRequest(
                latitude=28.6,
                longitude=77.2,
                accuracy=0.0,  # must be > 0
                text="test",
            )

    def test_reporter_id_optional(self):
        req = ComplaintCreateRequest(
            latitude=28.0,
            longitude=77.0,
            accuracy=5.0,
            text="waterlogging",
        )
        assert req.reporter_id is None


class TestCoordinateValidator:
    def test_valid_coordinates(self):
        validate_coordinates(28.6, 77.2, 10.0)  # should not raise

    def test_invalid_lat(self):
        with pytest.raises(LocationMissingError):
            validate_coordinates(91.0, 77.0, 10.0)

    def test_invalid_lon(self):
        with pytest.raises(LocationMissingError):
            validate_coordinates(28.0, 181.0, 10.0)

    def test_zero_accuracy(self):
        with pytest.raises(LocationMissingError):
            validate_coordinates(28.0, 77.0, 0.0)

    def test_negative_accuracy(self):
        with pytest.raises(LocationMissingError):
            validate_coordinates(28.0, 77.0, -5.0)
