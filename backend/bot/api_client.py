"""
HTTP client that talks to the NadiBot FastAPI backend.
All network calls are here – handlers never call httpx directly.
"""
from __future__ import annotations

import logging
from typing import Optional
import httpx

from bot.config import config

logger = logging.getLogger(__name__)

_client: Optional[httpx.AsyncClient] = None


def get_client() -> httpx.AsyncClient:
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(
            base_url=config.API_BASE_URL,
            timeout=60.0,          # Gemini + storage can be slow
        )
    return _client


async def close_client() -> None:
    global _client
    if _client and not _client.is_closed:
        await _client.aclose()


async def submit_complaint(
    *,
    reporter_id: str,
    latitude: float,
    longitude: float,
    accuracy: float,
    text: Optional[str] = None,
    image_bytes: Optional[tuple[bytes, str]] = None,   # (data, filename)
    audio_bytes: Optional[tuple[bytes, str]] = None,   # (data, filename)
) -> dict:
    """
    POST /api/v1/complaints as multipart/form-data.
    Returns the parsed JSON response dict on success.
    Raises httpx.HTTPStatusError on non-2xx.
    """
    client = get_client()

    data: dict = {
        "reporter_id": reporter_id,
        "latitude": str(latitude),
        "longitude": str(longitude),
        "accuracy": str(accuracy),
        "location_source": "telegram",
    }
    if text:
        data["text"] = text

    files: dict = {}
    if image_bytes:
        raw, fname = image_bytes
        files["image"] = (fname, raw, "image/jpeg")
    if audio_bytes:
        raw, fname = audio_bytes
        files["audio"] = (fname, raw, "audio/ogg")

    logger.info(
        "Submitting complaint | reporter=%s lat=%.4f lon=%.4f "
        "has_text=%s has_image=%s has_audio=%s",
        reporter_id, latitude, longitude,
        bool(text), bool(image_bytes), bool(audio_bytes),
    )

    response = await client.post(
        "/api/v1/complaints",
        data=data,
        files=files if files else None,
    )
    response.raise_for_status()
    return response.json()


async def get_reporter_complaints(reporter_id: str) -> list[dict]:
    """GET /api/v1/complaints/reporter/{reporter_id}"""
    client = get_client()
    try:
        response = await client.get(f"/api/v1/complaints/reporter/{reporter_id}")
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        logger.warning("Failed to fetch reporter complaints: %s", exc)
        return []
