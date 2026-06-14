"""
Telegram webhook route.

Receives update payloads pushed by Telegram and forwards them to the
python-telegram-bot Application running in-process (see bot/webhook.py).
"""

import logging

from fastapi import APIRouter, Request, Header, HTTPException, status

from app.core.config import get_settings
from bot.webhook import process_update

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/telegram", tags=["Telegram"])


@router.post("/webhook")
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
) -> dict:
    settings = get_settings()

    # Validate the secret token Telegram echoes back on every webhook call
    if settings.TELEGRAM_WEBHOOK_SECRET:
        if x_telegram_bot_api_secret_token != settings.TELEGRAM_WEBHOOK_SECRET:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid webhook secret",
            )

    update_data = await request.json()

    try:
        await process_update(update_data)
    except Exception:
        logger.exception("Error processing Telegram update")
        # Still return 200 so Telegram doesn't retry indefinitely on our bugs
        return {"ok": False}

    return {"ok": True}
