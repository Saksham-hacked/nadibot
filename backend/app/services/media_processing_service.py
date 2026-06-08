"""
Media processing service.
Orchestrates upload → AI analysis for images and audio.
"""

from __future__ import annotations
from typing import Optional
from fastapi import UploadFile

from app.services.storage_service import StorageService
from app.services.gemini_service import GeminiService
from app.schemas.media import MediaUploadResult, ImageAnalysisResult, AudioTranscriptResult
from app.core.constants import (
    ALLOWED_IMAGE_MIME_TYPES,
    ALLOWED_AUDIO_MIME_TYPES,
    MAX_IMAGE_SIZE_BYTES,
    MAX_AUDIO_SIZE_BYTES,
    AUDIO_TRANSCRIPTION_PENDING_PLACEHOLDER,
)
from app.core.exceptions import UnsupportedMediaTypeError, FileTooLargeError
from app.core.config import get_settings
from app.core.logging import get_logger

log = get_logger(__name__)


class MediaProcessingService:
    def __init__(self, storage: StorageService, gemini: GeminiService) -> None:
        self._storage = storage
        self._gemini = gemini

    async def process_image(
        self, file: UploadFile
    ) -> tuple[MediaUploadResult, ImageAnalysisResult]:
        """
        Validate → upload → analyse image with Gemini Vision.
        Returns (upload_result, analysis_result).
        """
        content_type = file.content_type or ""
        if content_type not in ALLOWED_IMAGE_MIME_TYPES:
            raise UnsupportedMediaTypeError(
                f"Image type '{content_type}' is not supported.",
                {"allowed": list(ALLOWED_IMAGE_MIME_TYPES)},
            )

        file_bytes = await file.read()

        if len(file_bytes) > MAX_IMAGE_SIZE_BYTES:
            raise FileTooLargeError(
                f"Image exceeds {MAX_IMAGE_SIZE_BYTES // (1024 * 1024)} MB limit.",
                {"size_bytes": len(file_bytes)},
            )

        # Upload
        upload_result = self._storage.upload_image(
            file_bytes=file_bytes,
            filename=file.filename or "image",
            mime_type=content_type,
        )

        # Analyse
        description = self._gemini.analyse_image(file_bytes, content_type)
        analysis = ImageAnalysisResult(
            description=description,
            water_related=bool(description),
            detected_issues=[],
        )

        log.info("Image processed: url=%s", upload_result.url)
        return upload_result, analysis

    async def process_audio(
        self, file: UploadFile
    ) -> tuple[MediaUploadResult, AudioTranscriptResult]:
        """
        Validate → upload → transcribe audio.
        Falls back to placeholder if file is too large for inline Gemini processing.
        """
        content_type = file.content_type or ""
        if content_type not in ALLOWED_AUDIO_MIME_TYPES:
            raise UnsupportedMediaTypeError(
                f"Audio type '{content_type}' is not supported.",
                {"allowed": list(ALLOWED_AUDIO_MIME_TYPES)},
            )

        file_bytes = await file.read()

        if len(file_bytes) > MAX_AUDIO_SIZE_BYTES:
            raise FileTooLargeError(
                f"Audio exceeds {MAX_AUDIO_SIZE_BYTES // (1024 * 1024)} MB limit.",
                {"size_bytes": len(file_bytes)},
            )

        # Upload first (always)
        upload_result = self._storage.upload_audio(
            file_bytes=file_bytes,
            filename=file.filename or "audio",
            mime_type=content_type,
        )

        # Transcribe – use placeholder if too large for inline
        settings = get_settings()
        if len(file_bytes) > settings.AUDIO_INLINE_MAX_BYTES:
            log.info(
                "Audio file too large for inline transcription (%d bytes), using placeholder",
                len(file_bytes),
            )
            transcript_result = AudioTranscriptResult(
                transcript=AUDIO_TRANSCRIPTION_PENDING_PLACEHOLDER,
                is_placeholder=True,
            )
        else:
            transcript_text = self._gemini.transcribe_audio(file_bytes, content_type)
            transcript_result = AudioTranscriptResult(
                transcript=transcript_text or "",
                is_placeholder=False,
            )

        log.info("Audio processed: url=%s, placeholder=%s", upload_result.url, transcript_result.is_placeholder)
        return upload_result, transcript_result
