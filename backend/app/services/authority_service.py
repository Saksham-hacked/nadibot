"""
Authority service – deterministic rule-based authority routing.
Gemini never decides routing. This file is the single source of truth.
"""

from __future__ import annotations
from app.core.constants import CATEGORY_TO_AUTHORITY, ComplaintCategory, Authority
from app.core.logging import get_logger

log = get_logger(__name__)


class AuthorityService:
    def resolve(self, category: str) -> str:
        """
        Map a complaint category string to the responsible authority.
        Falls back to GENERAL_GRIEVANCE for unknown categories.
        """
        try:
            cat_enum = ComplaintCategory(category)
        except ValueError:
            log.warning("Unknown category '%s' – routing to General Grievance", category)
            return Authority.GENERAL_GRIEVANCE.value

        authority = CATEGORY_TO_AUTHORITY.get(cat_enum, Authority.GENERAL_GRIEVANCE)
        log.info("Authority routed: category=%s → authority=%s", category, authority.value)
        return authority.value
