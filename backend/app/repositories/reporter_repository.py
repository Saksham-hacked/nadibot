"""
Reporter repository – track anonymous device sessions.
"""

from __future__ import annotations
from typing import Optional
from supabase import Client
from app.models.reporter import Reporter
from app.core.exceptions import DatabaseError
from app.core.logging import get_logger

log = get_logger(__name__)


class ReporterRepository:
    TABLE = "reporters"

    def __init__(self, client: Client) -> None:
        self._db = client

    def get_or_create(self, reporter_id: str) -> Reporter:
        """
        Return the existing reporter record or create a new one.
        Also bumps last_seen_at on every call.
        """
        try:
            res = (
                self._db.table(self.TABLE)
                .select("*")
                .eq("reporter_id", reporter_id)
                .execute()
            )
        except Exception as exc:
            raise DatabaseError("Failed to query reporter", {"error": str(exc)})

        from app.schemas.common import utcnow
        now_iso = utcnow().isoformat()

        if res.data:
            row = res.data[0]
            try:
                self._db.table(self.TABLE).update(
                    {"last_seen_at": now_iso}
                ).eq("reporter_id", reporter_id).execute()
            except Exception:
                pass  # non-critical
            return Reporter(**row)

        # Create new
        from app.schemas.common import new_uuid
        new_row = {
            "id": new_uuid(),
            "reporter_id": reporter_id,
            "complaint_count": 0,
            "first_seen_at": now_iso,
            "last_seen_at": now_iso,
        }
        try:
            insert_res = self._db.table(self.TABLE).insert(new_row).execute()
        except Exception as exc:
            raise DatabaseError("Failed to create reporter", {"error": str(exc)})

        log.info("New reporter registered: %s", reporter_id)
        return Reporter(**insert_res.data[0])

    def increment_complaint_count(self, reporter_id: str) -> None:
        try:
            reporter = self.get_or_create(reporter_id)
            self._db.table(self.TABLE).update(
                {"complaint_count": reporter.complaint_count + 1}
            ).eq("reporter_id", reporter_id).execute()
        except Exception as exc:
            log.warning("Failed to increment reporter count: %s", exc)
