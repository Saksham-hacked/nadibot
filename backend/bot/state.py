"""
In-memory session state per chat_id.
Each chat gets its own ComplaintSession that lives until submission or /cancel.
Thread-safe for single-process polling mode.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
from bot.strings import Lang


@dataclass
class ComplaintSession:
    """Holds everything collected during a complaint flow."""
    text: Optional[str] = None
    photo_file_id: Optional[str] = None
    voice_file_id: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    step: str = "text"   # text | photo | voice | location | review


@dataclass
class UserSession:
    lang: Lang = "en"
    reporter_id: Optional[str] = None
    complaint: Optional[ComplaintSession] = None

    def start_complaint(self) -> ComplaintSession:
        self.complaint = ComplaintSession()
        return self.complaint

    def clear_complaint(self) -> None:
        self.complaint = None


_sessions: dict[int, UserSession] = {}


def get_session(chat_id: int) -> UserSession:
    if chat_id not in _sessions:
        _sessions[chat_id] = UserSession()
    return _sessions[chat_id]


def clear_complaint(chat_id: int) -> None:
    if chat_id in _sessions:
        _sessions[chat_id].clear_complaint()
