"""
Reporter service – manage anonymous device identities.
"""

from __future__ import annotations
import uuid
from app.repositories.reporter_repository import ReporterRepository
from app.core.logging import get_logger

log = get_logger(__name__)


class ReporterService:
    def __init__(self, repo: ReporterRepository) -> None:
        self._repo = repo

    def resolve_reporter_id(self, provided_id: str | None) -> str:
        """Return the provided ID or generate a new server-side UUID."""
        if provided_id and provided_id.strip():
            return provided_id.strip()
        new_id = f"srv_{uuid.uuid4().hex}"
        log.info("Generated server-side reporter_id: %s", new_id)
        return new_id

    def register(self, reporter_id: str) -> None:
        """Ensure the reporter exists in the DB and bump last_seen_at."""
        self._repo.get_or_create(reporter_id)

    def increment(self, reporter_id: str) -> None:
        self._repo.increment_complaint_count(reporter_id)
