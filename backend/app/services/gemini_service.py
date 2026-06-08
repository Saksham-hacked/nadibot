"""
Gemini service – wraps Google Gemini Flash API calls.
Handles:
- complaint classification (text → structured JSON)
- image understanding
- audio transcription

All outputs are validated with Pydantic before returning.
"""

from __future__ import annotations
import json
import base64
import re
from typing import Optional
import google.generativeai as genai
from pydantic import BaseModel, ValidationError

from app.core.config import get_settings
from app.core.constants import (
    ComplaintCategory,
    ComplaintSubcategory,
    SeverityLevel,
    GEMINI_CLASSIFICATION_SYSTEM_PROMPT,
)
from app.core.exceptions import GeminiError, GeminiParseError
from app.core.logging import get_logger

log = get_logger(__name__)


# ── Pydantic schema for Gemini classification output ──────────────────────────

class GeminiClassificationOutput(BaseModel):
    category: ComplaintCategory
    subcategory: ComplaintSubcategory
    severity: SeverityLevel
    summary: str
    confidence: float

    class Config:
        use_enum_values = True


# ── Default fallback classification ───────────────────────────────────────────

DEFAULT_CLASSIFICATION = GeminiClassificationOutput(
    category=ComplaintCategory.OTHER,
    subcategory=ComplaintSubcategory.OTHER,
    severity=SeverityLevel.MEDIUM,
    summary="Classification could not be determined. Marked for manual review.",
    confidence=0.0,
)


# ── Service ────────────────────────────────────────────────────────────────────

class GeminiService:
    def __init__(self) -> None:
        settings = get_settings()
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self._model_name = settings.GEMINI_MODEL
        self._max_retries = settings.GEMINI_MAX_RETRIES

    def _get_model(self):
        return genai.GenerativeModel(self._model_name)

    def _extract_json(self, text: str) -> str:
        """Strip markdown code fences and whitespace from Gemini output."""
        text = text.strip()
        # Remove ```json ... ``` or ``` ... ```
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
        return text.strip()

    def _parse_classification(self, raw: str) -> Optional[GeminiClassificationOutput]:
        try:
            cleaned = self._extract_json(raw)
            data = json.loads(cleaned)
            return GeminiClassificationOutput(**data)
        except (json.JSONDecodeError, ValidationError, KeyError) as exc:
            log.warning("Gemini classification parse failed: %s | raw=%s", exc, raw[:300])
            return None

    # ── Public API ─────────────────────────────────────────────────────────────

    def classify_complaint(self, context: str) -> GeminiClassificationOutput:
        """
        Send aggregated complaint context to Gemini and return structured classification.
        Retries up to GEMINI_MAX_RETRIES times on parse failure, then falls back to default.
        """
        model = self._get_model()
        prompt = (
            f"{GEMINI_CLASSIFICATION_SYSTEM_PROMPT}\n\n"
            f"Complaint context:\n{context}\n\n"
            "Return ONLY the JSON object:"
        )

        for attempt in range(1, self._max_retries + 2):
            try:
                log.info("Gemini classify attempt %d", attempt)
                response = model.generate_content(prompt)
                raw = response.text
                result = self._parse_classification(raw)
                if result is not None:
                    log.info("Gemini classify OK (attempt %d), category=%s", attempt, result.category)
                    return result

                # Repair prompt on subsequent attempts
                prompt = (
                    "The previous JSON was invalid. Return ONLY valid JSON matching this schema:\n"
                    '{"category": "", "subcategory": "", "severity": "", "summary": "", "confidence": 0.0}\n\n'
                    f"Complaint context:\n{context}"
                )
            except Exception as exc:
                log.error("Gemini API error on attempt %d: %s", attempt, exc)
                if attempt > self._max_retries:
                    break

        log.warning("All Gemini classify attempts failed. Using default classification.")
        return DEFAULT_CLASSIFICATION

    def analyse_image(self, image_bytes: bytes, mime_type: str) -> str:
        """
        Send image to Gemini Vision and return a descriptive summary string.
        Returns empty string on failure (non-fatal – complaint still proceeds).
        """
        model = self._get_model()
        image_part = {"mime_type": mime_type, "data": base64.b64encode(image_bytes).decode()}
        prompt = (
            "You are analysing an image submitted as part of a water-governance complaint in India. "
            "Describe what you see in 2-4 sentences, focusing on any water-related issues visible. "
            "Be factual. Do not guess if nothing water-related is visible."
        )
        try:
            log.info("Gemini image analysis started (%d bytes)", len(image_bytes))
            response = model.generate_content([prompt, image_part])
            description = response.text.strip()
            log.info("Gemini image analysis OK")
            return description
        except Exception as exc:
            log.error("Gemini image analysis failed: %s", exc)
            return ""

    def transcribe_audio(self, audio_bytes: bytes, mime_type: str) -> str:
        """
        Send audio bytes to Gemini for transcription.
        Returns transcript string or empty string on failure.
        Only call this when file size is within the inline limit.
        """
        model = self._get_model()
        audio_part = {"mime_type": mime_type, "data": base64.b64encode(audio_bytes).decode()}
        prompt = (
            "Transcribe the following audio recording. "
            "The speaker may be reporting a water-related issue in India. "
            "Output only the transcription text, preserving the original language. "
            "If you cannot transcribe, output an empty string."
        )
        try:
            log.info("Gemini audio transcription started (%d bytes)", len(audio_bytes))
            response = model.generate_content([prompt, audio_part])
            transcript = response.text.strip()
            log.info("Gemini audio transcription OK (%d chars)", len(transcript))
            return transcript
        except Exception as exc:
            log.error("Gemini audio transcription failed: %s", exc)
            return ""
