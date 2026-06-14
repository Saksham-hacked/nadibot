"""
NadiBot Telegram bot - webhook mode.

Builds the python-telegram-bot Application and exposes lifecycle hooks
(`start_bot` / `stop_bot`) plus `process_update` for use from the FastAPI
webhook route. No polling is used here - Telegram pushes updates to us.

Run alongside the FastAPI app (single Render web service, free tier).
"""
from __future__ import annotations

import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from bot.config import config
from bot.api_client import close_client
from bot.handlers.start import (
    cmd_start,
    cmd_mystatus,
    cb_language,
    cb_main_menu,
)
from bot.handlers.complaint import handle_message, handle_callback

logger = logging.getLogger(__name__)

# Module-level singleton, created in start_bot()
telegram_app: Application | None = None


def build_app() -> Application:
    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("mystatus", cmd_mystatus))

    # Inline keyboard callbacks
    app.add_handler(CallbackQueryHandler(cb_language, pattern=r"^lang:"))
    app.add_handler(CallbackQueryHandler(cb_main_menu, pattern=r"^menu:"))
    app.add_handler(CallbackQueryHandler(handle_callback, pattern=r"^complaint:"))

    # Messages
    app.add_handler(MessageHandler(filters.LOCATION, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_message))
    app.add_handler(MessageHandler(filters.VOICE, handle_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    return app


async def start_bot(webhook_url: str | None = None, webhook_secret: str | None = None) -> None:
    """
    Initialize the PTB Application and register the Telegram webhook.
    Call this from FastAPI's startup/lifespan event.
    """
    global telegram_app

    telegram_app = build_app()
    await telegram_app.initialize()
    await telegram_app.start()

    if webhook_url:
        await telegram_app.bot.set_webhook(
            url=webhook_url,
            secret_token=webhook_secret or None,
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True,
        )
        logger.info("Telegram webhook set to %s", webhook_url)
    else:
        logger.warning(
            "start_bot called without webhook_url - webhook NOT registered. "
            "Set TELEGRAM_WEBHOOK_URL env var."
        )


async def stop_bot() -> None:
    """Cleanly shut down the PTB Application. Call from FastAPI shutdown."""
    global telegram_app
    if telegram_app is not None:
        await telegram_app.stop()
        await telegram_app.shutdown()
        telegram_app = None
    await close_client()
    logger.info("Telegram bot shut down cleanly.")


async def process_update(update_data: dict) -> None:
    """
    Feed a raw update dict (from the Telegram webhook POST body) into PTB.
    """
    if telegram_app is None:
        logger.error("process_update called before start_bot - dropping update")
        return

    update = Update.de_json(update_data, telegram_app.bot)
    await telegram_app.process_update(update)
