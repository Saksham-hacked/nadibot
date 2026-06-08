"""
NadiBot Telegram bot – main entry point.
Run with: python -m bot.main  (from the backend/ directory)
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

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def build_app() -> Application:
    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    # ── Commands ─────────────────────────────────────────────────────────
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("mystatus", cmd_mystatus))

    # ── Inline keyboard callbacks ─────────────────────────────────────────
    app.add_handler(CallbackQueryHandler(cb_language, pattern=r"^lang:"))
    app.add_handler(CallbackQueryHandler(cb_main_menu, pattern=r"^menu:"))
    app.add_handler(CallbackQueryHandler(handle_callback, pattern=r"^complaint:"))

    # ── Messages ──────────────────────────────────────────────────────────
    # Location shares
    app.add_handler(
        MessageHandler(filters.LOCATION, handle_message)
    )
    # Photo
    app.add_handler(
        MessageHandler(filters.PHOTO, handle_message)
    )
    # Voice note
    app.add_handler(
        MessageHandler(filters.VOICE, handle_message)
    )
    # Plain text (not commands)
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    return app


async def on_shutdown(app: Application) -> None:
    await close_client()
    logger.info("Bot shut down cleanly.")


def main() -> None:
    logger.info("Starting NadiBot (polling mode)…")
    app = build_app()
    app.post_shutdown = on_shutdown  # type: ignore[assignment]
    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()
