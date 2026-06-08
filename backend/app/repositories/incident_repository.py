"""
Incident repository – all DB operations for incidents.
"""

from __future__ import annotations
from typing import Optional
from supabase import Client
from app.models.incident import Incident
from app.core.exceptions import DatabaseError, IncidentNotFoundError
from app.core.logging import get_logger

log = get_logger(__name__)


class IncidentRepository:
    TABLE = "incidents"

    def __init__(self, client: Client) -> None:
        self._db = client

    # ── Write ──────────────────────────────────────────────────────────────────

    def create(self, incident: Incident) -> Incident:
        data = incident.model_dump(mode="json")
        try:
            res = self._db.table(self.TABLE).insert(data).execute()
        except Exception as exc:
            raise DatabaseError("Failed to create incident", {"error": str(exc)})

        if not res.data:
            raise DatabaseError("Incident insert returned no data")

        log.info("Incident created: %s", incident.id)
        return Incident(**res.data[0])

    def increment_complaint_count(self, incident_id: str) -> None:
        try:
            current = self.get_by_id(incident_id)
            self._db.table(self.TABLE).update(
                {"complaint_count": current.complaint_count + 1}
            ).eq("id", incident_id).execute()
        except IncidentNotFoundError:
            raise
        except Exception as exc:
            raise DatabaseError("Failed to increment incident complaint_count", {"error": str(exc)})

    def update_status(
        self, incident_id: str, status: str, resolution_notes: Optional[str] = None
    ) -> Incident:
        payload: dict = {"status": status}
        if resolution_notes is not None:
            payload["resolution_notes"] = resolution_notes
        try:
            res = (
                self._db.table(self.TABLE)
                .update(payload)
                .eq("id", incident_id)
                .execute()
            )
        except Exception as exc:
            raise DatabaseError("Failed to update incident status", {"error": str(exc)})

        if not res.data:
            raise IncidentNotFoundError(f"Incident {incident_id} not found")

        return Incident(**res.data[0])

    def update_notes(self, incident_id: str, notes: str) -> Incident:
        try:
            res = (
                self._db.table(self.TABLE)
                .update({"resolution_notes": notes})
                .eq("id", incident_id)
                .execute()
            )
        except Exception as exc:
            raise DatabaseError("Failed to update incident notes", {"error": str(exc)})

        if not res.data:
            raise IncidentNotFoundError(f"Incident {incident_id} not found")

        return Incident(**res.data[0])

    # ── Read ───────────────────────────────────────────────────────────────────

    def get_by_id(self, incident_id: str) -> Incident:
        try:
            res = self._db.table(self.TABLE).select("*").eq("id", incident_id).execute()
        except Exception as exc:
            raise DatabaseError("Failed to fetch incident", {"error": str(exc)})

        if not res.data:
            raise IncidentNotFoundError(f"Incident {incident_id} not found")

        return Incident(**res.data[0])

    def find_nearby_open(
        self,
        latitude: float,
        longitude: float,
        category: str,
        authority: str,
        radius_meters: float,
    ) -> Optional[Incident]:
        """
        Find the nearest OPEN incident with matching category + authority within radius.
        Uses the Haversine formula via Python since PostGIS may not be enabled.
        Fetches a bounding-box set and filters in Python.
        """
        try:
            # Rough bounding box: 1 degree lat ≈ 111 km
            deg_margin = (radius_meters / 111_000) * 1.5
            res = (
                self._db.table(self.TABLE)
                .select("*")
                .eq("status", "OPEN")
                .eq("category", category)
                .eq("authority", authority)
                .gte("latitude", latitude - deg_margin)
                .lte("latitude", latitude + deg_margin)
                .gte("longitude", longitude - deg_margin)
                .lte("longitude", longitude + deg_margin)
                .execute()
            )
        except Exception as exc:
            raise DatabaseError("Failed to search nearby incidents", {"error": str(exc)})

        from app.utils.helpers import haversine_distance

        best: Optional[Incident] = None
        best_dist = float("inf")

        for row in res.data:
            incident = Incident(**row)
            dist = haversine_distance(
                latitude, longitude, incident.latitude, incident.longitude
            )
            if dist <= radius_meters and dist < best_dist:
                best = incident
                best_dist = dist

        return best

    def list_incidents(
        self,
        status: Optional[str] = None,
        authority: Optional[str] = None,
        district: Optional[str] = None,
        category: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Incident], int]:
        try:
            query = self._db.table(self.TABLE).select("*", count="exact")

            if status:
                query = query.eq("status", status)
            if authority:
                query = query.eq("authority", authority)
            if district:
                query = query.eq("district", district)
            if category:
                query = query.eq("category", category)

            offset = (page - 1) * page_size
            query = query.order("created_at", desc=True).range(offset, offset + page_size - 1)
            res = query.execute()
        except Exception as exc:
            raise DatabaseError("Failed to list incidents", {"error": str(exc)})

        items = [Incident(**row) for row in res.data]
        return items, res.count or 0

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
            raise DatabaseError("Failed to count incidents", {"error": str(exc)})

    def count_total(self) -> int:
        try:
            res = self._db.table(self.TABLE).select("id", count="exact").execute()
            return res.count or 0
        except Exception as exc:
            raise DatabaseError("Failed to count total incidents", {"error": str(exc)})

    def get_incidents_since(self, since_iso: str) -> list[dict]:
        try:
            res = (
                self._db.table(self.TABLE)
                .select("id, created_at")
                .gte("created_at", since_iso)
                .execute()
            )
            return res.data
        except Exception as exc:
            raise DatabaseError("Failed to get incident trend data", {"error": str(exc)})

    def get_all_coordinates(self) -> list[dict]:
        try:
            res = (
                self._db.table(self.TABLE)
                .select("id, latitude, longitude, category, severity, status, complaint_count")
                .execute()
            )
            return res.data
        except Exception as exc:
            raise DatabaseError("Failed to fetch incident coordinates", {"error": str(exc)})
