"""
Bot configuration – reads from environment / .env file.
"""
from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

# Load the backend .env that sits one level above the bot/ folder
_env_path = Path(__file__).parent.parent / ".env"
load_dotenv(_env_path)


class BotConfig:
    TELEGRAM_BOT_TOKEN: str = os.environ["TELEGRAM_BOT_TOKEN"]
    API_BASE_URL: str = os.environ.get("API_BASE_URL", "http://localhost:8000")
    # Hardcoded GPS accuracy sent to backend (Telegram location is real lat/lng)
    GPS_ACCURACY: float = 20.0
    # How many past complaints to show in /mystatus
    HISTORY_LIMIT: int = 5


config = BotConfig()
