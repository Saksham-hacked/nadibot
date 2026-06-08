"""
Health check route.
"""

from fastapi import APIRouter
from app.db.supabase import get_supabase_client

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
def health_check() -> dict:
    """Basic liveness check."""
    return {"status": "ok", "service": "nadibot-backend"}


@router.get("/db")
def db_health() -> dict:
    """Check Supabase connectivity."""
    try:
        client = get_supabase_client()
        # Lightweight query – just checks connection
        client.table("complaints").select("id").limit(1).execute()
        return {"status": "ok", "database": "connected"}
    except Exception as exc:
        return {"status": "error", "database": "unreachable", "detail": str(exc)}
