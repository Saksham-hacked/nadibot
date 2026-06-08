"""
/start handler and language selection.
"""
from __future__ import annotations

import uuid
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from bot.state import get_session
from bot.strings import t

logger = logging.getLogger(__name__)


def _lang_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇬🇧 English", callback_data="lang:en"),
            InlineKeyboardButton("🇮🇳 हिंदी", callback_data="lang:hi"),
            InlineKeyboardButton("🇮🇳 मराठी", callback_data="lang:mr"),
        ]
    ])


def _main_menu_keyboard(lang) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t("btn_report", lang), callback_data="menu:report")],
        [InlineKeyboardButton(t("btn_my_reports", lang), callback_data="menu:my_reports")],
        [InlineKeyboardButton(t("btn_language", lang), callback_data="menu:language")],
    ])


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    session = get_session(chat_id)

    if not session.reporter_id:
        uid = update.effective_user.id if update.effective_user else uuid.uuid4().hex
        session.reporter_id = f"tg_{uid}"
        logger.info("New reporter: %s (chat_id=%s)", session.reporter_id, chat_id)

    await update.message.reply_text(
        t("welcome", "en"),
        parse_mode="Markdown",
        reply_markup=_lang_keyboard(),
    )


async def cb_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    chat_id = update.effective_chat.id
    session = get_session(chat_id)

    lang = query.data.split(":")[1]   # "en", "hi", or "mr"
    session.lang = lang               # type: ignore[assignment]

    await query.edit_message_text(
        t("lang_set", lang),
        parse_mode="Markdown",
    )

    await query.message.reply_text(
        t("main_menu", lang),
        parse_mode="Markdown",
        reply_markup=_main_menu_keyboard(lang),
    )


async def cb_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    from bot.handlers.complaint import start_complaint_flow

    query = update.callback_query
    await query.answer()

    chat_id = update.effective_chat.id
    session = get_session(chat_id)
    lang = session.lang
    action = query.data.split(":")[1]

    if action == "report":
        await start_complaint_flow(query.message, session)
    elif action == "my_reports":
        await _show_my_reports(query.message, session)
    elif action == "language":
        await query.message.reply_text(
            t("language_prompt", lang),
            reply_markup=_lang_keyboard(),
        )


async def cmd_mystatus(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    session = get_session(chat_id)
    await _show_my_reports(update.message, session)


async def _show_my_reports(message, session) -> None:
    from bot.api_client import get_reporter_complaints
    from bot.config import config
    from datetime import datetime

    lang = session.lang

    if not session.reporter_id:
        await message.reply_text(t("my_reports_empty", lang))
        return

    complaints = await get_reporter_complaints(session.reporter_id)

    if not complaints:
        await message.reply_text(t("my_reports_empty", lang), parse_mode="Markdown")
        return

    recent = complaints[-config.HISTORY_LIMIT:][::-1]
    header = t("my_reports_header", lang, count=len(recent))
    lines = [header]

    for c in recent:
        try:
            dt = datetime.fromisoformat(c["created_at"].replace("Z", "+00:00"))
            date_str = dt.strftime("%d %b %Y")
        except Exception:
            date_str = c.get("created_at", "")[:10]

        lines.append(
            t(
                "report_item", lang,
                id_short=c["id"][:8],
                category=c.get("category", "-"),
                subcategory=c.get("subcategory", "-"),
                severity=c.get("severity", "-"),
                status=c.get("status", "-"),
                date=date_str,
            )
        )
        lines.append("")

    await message.reply_text("\n".join(lines), parse_mode="Markdown")
