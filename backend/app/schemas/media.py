"""
Schemas related to media/file handling.
"""

from __future__ import annotations
from typing import Optional
from pydantic import BaseModel


class MediaUploadResult(BaseModel):
    """Returned by StorageService after a successful upload."""
    url: str
    provider: str           # "supabase" | "cloudinary"
    storage_path: str       # path/key inside the bucket
    mime_type: str
    size_bytes: int


class ImageAnalysisResult(BaseModel):
    """Structured output from Gemini image analysis."""
    description: str        # human-readable description
    water_related: bool     # is the image clearly water-related?
    detected_issues: list[str] = []


class AudioTranscriptResult(BaseModel):
    """Structured output from Gemini audio transcription."""
    transcript: str
    language: Optional[str] = None
    is_placeholder: bool = False   # True when file was too large for inline
