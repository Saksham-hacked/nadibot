"""
Analytics repository – thin query layer for dashboard metrics.
Delegates computation to the analytics service.
"""

from __future__ import annotations
from supabase import Client
from app.repositories.complaint_repository import ComplaintRepository
from app.repositories.incident_repository import IncidentRepository


class AnalyticsRepository:
    """
    Aggregates repositories needed by the analytics service.
    Add specialised analytics queries here as the product grows.
    """

    def __init__(self, client: Client) -> None:
        self.complaints = ComplaintRepository(client)
        self.incidents = IncidentRepository(client)
