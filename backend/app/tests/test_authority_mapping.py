"""
Tests for authority routing and Gemini JSON parsing/fallback.
"""

import pytest
from app.services.authority_service import AuthorityService
from app.services.gemini_service import GeminiService, GeminiClassificationOutput, DEFAULT_CLASSIFICATION
from app.core.constants import Authority


class TestAuthorityMapping:
    def setup_method(self):
        self.service = AuthorityService()

    def test_water_supply_routes_to_phed(self):
        assert self.service.resolve("Water Supply") == Authority.PHED.value

    def test_water_quality_routes_to_phed(self):
        assert self.service.resolve("Water Quality") == Authority.PHED.value

    def test_infrastructure_routes_to_phed(self):
        assert self.service.resolve("Infrastructure") == Authority.PHED.value

    def test_flooding_routes_to_disaster_management(self):
        assert self.service.resolve("Flooding") == Authority.DISASTER_MANAGEMENT.value

    def test_drainage_routes_to_municipality(self):
        assert self.service.resolve("Drainage") == Authority.MUNICIPALITY.value

    def test_groundwater_routes_to_water_resources(self):
        assert self.service.resolve("Groundwater") == Authority.WATER_RESOURCES.value

    def test_sanitation_routes_to_municipality(self):
        assert self.service.resolve("Sanitation") == Authority.MUNICIPALITY.value

    def test_other_routes_to_general_grievance(self):
        assert self.service.resolve("Other") == Authority.GENERAL_GRIEVANCE.value

    def test_unknown_category_routes_to_general_grievance(self):
        assert self.service.resolve("Aliens") == Authority.GENERAL_GRIEVANCE.value


class TestGeminiParsing:
    def setup_method(self):
        # We only test the parsing logic, not actual API calls
        import os
        os.environ.setdefault("GEMINI_API_KEY", "test_key")
        os.environ.setdefault("SUPABASE_URL", "https://test.supabase.co")
        os.environ.setdefault("SUPABASE_KEY", "test_key")
        os.environ.setdefault("ADMIN_KEY", "test_admin")

    def test_parse_valid_json(self):
        raw = '{"category": "Water Supply", "subcategory": "No Water Supply", "severity": "High", "summary": "No water for 2 days.", "confidence": 0.9}'
        from app.services.gemini_service import GeminiService
        # Directly test the private parse method
        svc = object.__new__(GeminiService)
        result = svc._parse_classification(raw)
        assert result is not None
        assert result.category == "Water Supply"
        assert result.severity == "High"
        assert result.confidence == pytest.approx(0.9)

    def test_parse_json_with_markdown_fences(self):
        raw = '```json\n{"category": "Flooding", "subcategory": "Waterlogging", "severity": "Critical", "summary": "Road flooded.", "confidence": 0.95}\n```'
        svc = object.__new__(GeminiService)
        result = svc._parse_classification(raw)
        assert result is not None
        assert result.category == "Flooding"

    def test_parse_invalid_json_returns_none(self):
        raw = "This is not JSON at all."
        svc = object.__new__(GeminiService)
        result = svc._parse_classification(raw)
        assert result is None

    def test_parse_wrong_enum_value_returns_none(self):
        raw = '{"category": "NotARealCategory", "subcategory": "Other", "severity": "High", "summary": "X", "confidence": 0.5}'
        svc = object.__new__(GeminiService)
        result = svc._parse_classification(raw)
        assert result is None

    def test_default_classification_is_safe(self):
        assert DEFAULT_CLASSIFICATION.category == "Other"
        assert DEFAULT_CLASSIFICATION.confidence == 0.0
        assert DEFAULT_CLASSIFICATION.severity == "Medium"
