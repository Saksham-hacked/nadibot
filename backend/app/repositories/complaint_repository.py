"""
Complaint repository – all direct Supabase DB interactions for complaints.
Business logic must NOT live here.
"""

from __future__ import annotations
from typing import Optional
from supabase import Client
from app.models.complaint import Complaint
from app.core.exceptions import DatabaseError, ComplaintNotFoundError
from app.core.logging import get_logger

log = get_logger(__name__)


class ComplaintRepository:
    TABLE = "complaints"

    def __init__(self, client: Client) -> None:
        self._db = client

    # ── Write ──────────────────────────────────────────────────────────────────

    def create(self, complaint: Complaint) -> Complaint:
        data = complaint.model_dump(mode="json")
        try:
            res = self._db.table(self.TABLE).insert(data).execute()
        except Exception as exc:
            log.error("DB insert complaint failed: %s", exc)
            raise DatabaseError("Failed to create complaint", {"error": str(exc)})

        if not res.data:
            raise DatabaseError("Complaint insert returned no data")

        log.info("Complaint created: %s", complaint.id)
        return Complaint(**res.data[0])

    def update_incident(self, complaint_id: str, incident_id: str) -> None:
        try:
            self._db.table(self.TABLE).update(
                {"incident_id": incident_id}
            ).eq("id", complaint_id).execute()
        except Exception as exc:
            raise DatabaseError("Failed to update complaint incident_id", {"error": str(exc)})

    # ── Read ───────────────────────────────────────────────────────────────────

    def get_by_id(self, complaint_id: str) -> Complaint:
        try:
            res = self._db.table(self.TABLE).select("*").eq("id", complaint_id).execute()
        except Exception as exc:
            raise DatabaseError("Failed to fetch complaint", {"error": str(exc)})

        if not res.data:
            raise ComplaintNotFoundError(f"Complaint {complaint_id} not found")

        return Complaint(**res.data[0])

    def list_complaints(
        self,
        status: Optional[str] = None,
        category: Optional[str] = None,
        authority: Optional[str] = None,
        district: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Complaint], int]:
        try:
            query = self._db.table(self.TABLE).select("*", count="exact")

            if status:
                query = query.eq("status", status)
            if category:
                query = query.eq("category", category)
            if authority:
                query = query.eq("authority", authority)
            if district:
                query = query.eq("district", district)

            offset = (page - 1) * page_size
            query = query.order("created_at", desc=True).range(offset, offset + page_size - 1)
            res = query.execute()
        except Exception as exc:
            raise DatabaseError("Failed to list complaints", {"error": str(exc)})

        items = [Complaint(**row) for row in res.data]
        total = res.count or 0
        return items, total

    def list_by_reporter(self, reporter_id: str) -> list[Complaint]:
        try:
            res = (
                self._db.table(self.TABLE)
                .select("*")
                .eq("reporter_id", reporter_id)
                .order("created_at", desc=True)
                .execute()
            )
        except Exception as exc:
            raise DatabaseError("Failed to fetch reporter complaints", {"error": str(exc)})

        return [Complaint(**row) for row in res.data]

    def count_by_status(self, status: str) -> int:
        try:
            res = (
                self._db.table(self.TABLE)
                .select("id", count="exact")
                .eq("status", status)
                .execute()
            )
            return res.count or 0
        except Exception as exc:
            raise DatabaseError("Failed to count complaints", {"error": str(exc)})

    def count_by_severity(self, severity: str) -> int:
        try:
            res = (
                self._db.table(self.TABLE)
                .select("id", count="exact")
                .eq("severity", severity)
                .execute()
            )
            return res.count or 0
        except Exception as exc:
            raise DatabaseError("Failed to count complaints by severity", {"error": str(exc)})

    def count_total(self) -> int:
        try:
            res = self._db.table(self.TABLE).select("id", count="exact").execute()
            return res.count or 0
        except Exception as exc:
            raise DatabaseError("Failed to count total complaints", {"error": str(exc)})

    def get_category_distribution(self) -> list[dict]:
        """Returns list of {category, count} dicts."""
        try:
            res = self._db.table(self.TABLE).select("category").execute()
            from collections import Counter
            counts = Counter(row["category"] for row in res.data)
            return [{"category": k, "count": v} for k, v in counts.items()]
        except Exception as exc:
            raise DatabaseError("Failed to get category distribution", {"error": str(exc)})

    def get_district_distribution(self) -> list[dict]:
        """Returns list of {district, count} dicts."""
        try:
            res = self._db.table(self.TABLE).select("district").execute()
            from collections import Counter
            counts = Counter(
                row["district"] for row in res.data if row.get("district")
            )
            return [{"district": k, "count": v} for k, v in counts.items()]
        except Exception as exc:
            raise DatabaseError("Failed to get district distribution", {"error": str(exc)})

    def get_complaints_since(self, since_iso: str) -> list[dict]:
        """Return lightweight rows (id, created_at) since a date for trend calculation."""
        try:
            res = (
                self._db.table(self.TABLE)
                .select("id, created_at")
                .gte("created_at", since_iso)
                .execute()
            )
            return res.data
        except Exception as exc:
            raise DatabaseError("Failed to get complaint trend data", {"error": str(exc)})

    def get_all_coordinates(self) -> list[dict]:
        """Lightweight fetch for geospatial endpoint."""
        try:
            res = (
                self._db.table(self.TABLE)
                .select("id, latitude, longitude, category, severity, status")
                .execute()
            )
            return res.data
        except Exception as exc:
            raise DatabaseError("Failed to fetch complaint coordinates", {"error": str(exc)})

    def get_resolved_with_times(self) -> list[dict]:
        """Fetch created_at and updated_at for RESOLVED complaints for avg resolution time."""
        try:
            res = (
                self._db.table(self.TABLE)
                .select("created_at, updated_at")
                .eq("status", "RESOLVED")
                .execute()
            )
            return res.data
        except Exception as exc:
            raise DatabaseError("Failed to fetch resolution times", {"error": str(exc)})
