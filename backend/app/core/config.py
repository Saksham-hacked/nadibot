"""
Application configuration via environment variables.
All settings are loaded once at startup via Pydantic BaseSettings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    # ── Supabase ──────────────────────────────────────────────────────────────
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_STORAGE_BUCKET: str = "nadibot-media"

    # ── Gemini ────────────────────────────────────────────────────────────────
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash"
    GEMINI_MAX_RETRIES: int = 2

    # ── Admin ─────────────────────────────────────────────────────────────────
    ADMIN_KEY: str

    # ── Storage ───────────────────────────────────────────────────────────────
    STORAGE_PROVIDER: str = "supabase"
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""

    # ── Geocoding ─────────────────────────────────────────────────────────────
    REVERSE_GEOCODER_PROVIDER: str = "nominatim"
    NOMINATIM_USER_AGENT: str = "nadibot/1.0"

    # ── Incident clustering ───────────────────────────────────────────────────
    DEFAULT_INCIDENT_RADIUS_METERS: float = 500.0

    # ── App ───────────────────────────────────────────────────────────────────
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"

    # ── Audio ─────────────────────────────────────────────────────────────────
    AUDIO_INLINE_MAX_BYTES: int = 900_000

    # ── Telegram Bot (used by bot/config.py, ignored by FastAPI itself) ───────
    TELEGRAM_BOT_TOKEN: str = ""
    API_BASE_URL: str = "http://localhost:8000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",          # ← ignore any unknown env vars instead of crashing
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached singleton of Settings."""
    return Settings()  # type: ignore[call-arg]
