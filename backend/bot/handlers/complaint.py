"""
Complaint flow handlers.

Flow:
  start_complaint_flow()
    → step_text   (optional, skip button)
    → step_photo  (optional, skip button)
    → step_voice  (optional, skip button)
    → step_location (required, native Telegram location share)
    → review + submit inline button

State machine is stored in session.complaint.step so every incoming
message/callback is dispatched to the right handler.
"""
from __future__ import annotations

import io
import logging
from datetime import datetime
from typing import Optional

import httpx
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import ContextTypes

from bot.state import get_session, ComplaintSession, clear_complaint
from bot.strings import t, Lang
from bot.api_client import submit_complaint as api_submit
from bot.config import config

logger = logging.getLogger(__name__)


# ── Keyboards ────────────────────────────────────────────────────────────────

def _skip_keyboard(lang: Lang) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t("btn_skip", lang), callback_data="complaint:skip")]
    ])


def _location_keyboard(lang: Lang) -> ReplyKeyboardMarkup:
    """Native Telegram location-share button (appears in reply keyboard)."""
    return ReplyKeyboardMarkup(
        [[KeyboardButton(t("btn_share_location", lang), request_location=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def _review_keyboard(lang: Lang) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t("btn_submit", lang), callback_data="complaint:submit")],
        [InlineKeyboardButton(t("btn_cancel", lang), callback_data="complaint:cancel")],
    ])


# ── Flow entry ───────────────────────────────────────────────────────────────

async def start_complaint_flow(message, session) -> None:
    """Create a fresh session and jump to the text step."""
    session.start_complaint()
    lang = session.lang
    await message.reply_text(
        t("step_text", lang),
        parse_mode="Markdown",
        reply_markup=_skip_keyboard(lang),
    )


# ── Step renderers ───────────────────────────────────────────────────────────

async def _ask_photo(message, lang: Lang) -> None:
    await message.reply_text(
        t("step_photo", lang),
        parse_mode="Markdown",
        reply_markup=_skip_keyboard(lang),
    )


async def _ask_voice(message, lang: Lang) -> None:
    await message.reply_text(
        t("step_voice", lang),
        parse_mode="Markdown",
        reply_markup=_skip_keyboard(lang),
    )


async def _ask_location(message, lang: Lang) -> None:
    await message.reply_text(
        t("step_location", lang),
        parse_mode="Markdown",
        reply_markup=_location_keyboard(lang),
    )


async def _show_review(message, complaint: ComplaintSession, lang: Lang) -> None:
    lines = [t("review_header", lang)]

    if complaint.text:
        lines.append(t("review_text", lang) + complaint.text[:200])
    if complaint.photo_file_id:
        lines.append(t("review_photo", lang))
    if complaint.voice_file_id:
        lines.append(t("review_voice", lang))
    lines.append(t("review_location", lang))

    if not any([complaint.text, complaint.photo_file_id, complaint.voice_file_id]):
        # Edge-case: only location was added – prevent empty submit
        lines.append("\n" + t("nothing_added", lang))

    await message.reply_text(
        "\n".join(lines),
        parse_mode="Markdown",
        reply_markup=_review_keyboard(lang),
    )


# ── Download helpers ─────────────────────────────────────────────────────────

async def _download_file(context: ContextTypes.DEFAULT_TYPE, file_id: str) -> bytes:
    """Download a Telegram file by file_id and return raw bytes."""
    tg_file = await context.bot.get_file(file_id)
    buf = io.BytesIO()
    await tg_file.download_to_memory(buf)
    buf.seek(0)
    return buf.read()


# ── Message dispatcher ───────────────────────────────────────────────────────

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Routes all non-command messages to the active complaint step.
    Handles: text, photo, voice, location.
    """
    chat_id = update.effective_chat.id
    session = get_session(chat_id)
    complaint = session.complaint
    lang = session.lang
    message = update.message

    if complaint is None:
        # No active complaint – prompt user to start
        await message.reply_text(t("unexpected", lang), parse_mode="Markdown")
        return

    step = complaint.step

    # ── Location (handled at any step if user sends it) ──────────────────
    if message.location:
        complaint.latitude = message.location.latitude
        complaint.longitude = message.location.longitude
        complaint.step = "review"
        # Remove the reply keyboard
        await message.reply_text(
            "✓",
            reply_markup=ReplyKeyboardRemove(),
        )
        await _show_review(message, complaint, lang)
        return

    # ── Step: text ───────────────────────────────────────────────────────
    if step == "text":
        if message.text:
            complaint.text = message.text.strip()
        complaint.step = "photo"
        await _ask_photo(message, lang)
        return

    # ── Step: photo ──────────────────────────────────────────────────────
    if step == "photo":
        if message.photo:
            # Use highest-res version (last in list)
            complaint.photo_file_id = message.photo[-1].file_id
        complaint.step = "voice"
        await _ask_voice(message, lang)
        return

    # ── Step: voice ──────────────────────────────────────────────────────
    if step == "voice":
        if message.voice:
            complaint.voice_file_id = message.voice.file_id
        complaint.step = "location"
        await _ask_location(message, lang)
        return

    # ── Step: location (waiting) ─────────────────────────────────────────
    if step == "location":
        await message.reply_text(
            t("need_location", lang),
            parse_mode="Markdown",
            reply_markup=_location_keyboard(lang),
        )
        return

    # ── Catch-all ────────────────────────────────────────────────────────
    await message.reply_text(t("unexpected", lang))


# ── Callback dispatcher ───────────────────────────────────────────────────────

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Routes complaint:* inline keyboard callbacks."""
    query = update.callback_query
    await query.answer()

    chat_id = update.effective_chat.id
    session = get_session(chat_id)
    lang = session.lang
    complaint = session.complaint
    action = query.data.split(":")[1]   # skip | submit | cancel

    if action == "cancel":
        clear_complaint(chat_id)
        await query.edit_message_text(t("cancelled", lang))
        return

    if action == "skip":
        if complaint is None:
            return
        _advance_step(complaint)
        await _send_next_step(query.message, complaint, lang)
        return

    if action == "submit":
        await _do_submit(query, session, context)
        return


def _advance_step(complaint: ComplaintSession) -> None:
    """Move to the next step when user presses Skip."""
    order = ["text", "photo", "voice", "location", "review"]
    idx = order.index(complaint.step)
    complaint.step = order[min(idx + 1, len(order) - 1)]


async def _send_next_step(message, complaint: ComplaintSession, lang: Lang) -> None:
    step = complaint.step
    if step == "photo":
        await _ask_photo(message, lang)
    elif step == "voice":
        await _ask_voice(message, lang)
    elif step == "location":
        await _ask_location(message, lang)
    elif step == "review":
        await _show_review(message, complaint, lang)


# ── Submission ────────────────────────────────────────────────────────────────

async def _do_submit(query, session, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = session.lang
    complaint = session.complaint

    # Guard: must have at least one content field
    if not any([complaint.text, complaint.photo_file_id, complaint.voice_file_id]):
        await query.message.reply_text(t("nothing_added", lang), parse_mode="Markdown")
        return

    # Guard: must have location
    if complaint.latitude is None or complaint.longitude is None:
        await query.message.reply_text(t("need_location", lang), parse_mode="Markdown")
        complaint.step = "location"
        await _ask_location(query.message, lang)
        return

    await query.edit_message_text(t("submitting", lang))

    # Download media files from Telegram
    image_bytes: Optional[tuple[bytes, str]] = None
    audio_bytes: Optional[tuple[bytes, str]] = None

    try:
        if complaint.photo_file_id:
            raw = await _download_file(context, complaint.photo_file_id)
            image_bytes = (raw, "photo.jpg")

        if complaint.voice_file_id:
            raw = await _download_file(context, complaint.voice_file_id)
            audio_bytes = (raw, "voice.ogg")
    except Exception as exc:
        logger.error("Media download failed: %s", exc)
        await query.message.reply_text(t("submit_error", lang), parse_mode="Markdown")
        return

    # POST to backend
    try:
        result = await api_submit(
            reporter_id=session.reporter_id,
            latitude=complaint.latitude,
            longitude=complaint.longitude,
            accuracy=config.GPS_ACCURACY,
            text=complaint.text,
            image_bytes=image_bytes,
            audio_bytes=audio_bytes,
        )
    except httpx.HTTPStatusError as exc:
        logger.error("Backend rejected complaint: %s %s", exc.response.status_code, exc.response.text)
        await query.message.reply_text(t("submit_error", lang), parse_mode="Markdown")
        return
    except Exception as exc:
        logger.error("Unexpected submit error: %s", exc)
        await query.message.reply_text(t("submit_error", lang), parse_mode="Markdown")
        return

    # Success
    clear_complaint(query.message.chat.id)
    await query.message.reply_text(
        t(
            "submit_success", lang,
            complaint_id=result.get("id", "N/A"),
            category=result.get("category", "-"),
            severity=result.get("severity", "-"),
            authority=result.get("authority", "-"),
            status=result.get("status", "-"),
        ),
        parse_mode="Markdown",
    )
