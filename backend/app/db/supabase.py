"""
Supabase client singleton.
Uses the service-role key so the backend can bypass RLS for server-side ops.
"""

from supabase import create_client, Client
from app.core.config import get_settings
from functools import lru_cache


@lru_cache(maxsize=1)
def get_supabase_client() -> Client:
    settings = get_settings()
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
