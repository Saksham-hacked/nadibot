"""
Storage service – provider-agnostic file upload abstraction.
Primary: Supabase Storage
Fallback: Cloudinary
Switch via STORAGE_PROVIDER env var.
"""

from __future__ import annotations
import io
import uuid
import mimetypes
from abc import ABC, abstractmethod
from typing import Optional
from app.schemas.media import MediaUploadResult
from app.core.exceptions import StorageError
from app.core.logging import get_logger

log = get_logger(__name__)


# ── Abstract interface ─────────────────────────────────────────────────────────

class StorageProvider(ABC):
    @abstractmethod
    def upload(
        self,
        file_bytes: bytes,
        filename: str,
        mime_type: str,
        folder: str = "uploads",
    ) -> MediaUploadResult:
        ...


# ── Supabase provider ──────────────────────────────────────────────────────────

class SupabaseStorageProvider(StorageProvider):
    def __init__(self, client, bucket: str) -> None:
        self._client = client
        self._bucket = bucket

    def upload(
        self,
        file_bytes: bytes,
        filename: str,
        mime_type: str,
        folder: str = "uploads",
    ) -> MediaUploadResult:
        unique_name = f"{folder}/{uuid.uuid4().hex}_{filename}"
        try:
            self._client.storage.from_(self._bucket).upload(
                path=unique_name,
                file=file_bytes,
                file_options={"content-type": mime_type},
            )
            public_url = self._client.storage.from_(self._bucket).get_public_url(unique_name)
        except Exception as exc:
            log.error("Supabase storage upload failed: %s", exc)
            raise StorageError("Failed to upload file to Supabase", {"error": str(exc)})

        log.info("Supabase upload OK: %s", unique_name)
        return MediaUploadResult(
            url=public_url,
            provider="supabase",
            storage_path=unique_name,
            mime_type=mime_type,
            size_bytes=len(file_bytes),
        )


# ── Cloudinary provider ────────────────────────────────────────────────────────

class CloudinaryStorageProvider(StorageProvider):
    def __init__(self, cloud_name: str, api_key: str, api_secret: str) -> None:
        try:
            import cloudinary
            import cloudinary.uploader

            cloudinary.config(
                cloud_name=cloud_name,
                api_key=api_key,
                api_secret=api_secret,
                secure=True,
            )
            self._uploader = cloudinary.uploader
        except ImportError:
            raise StorageError("cloudinary package not installed. Run: pip install cloudinary")

    def upload(
        self,
        file_bytes: bytes,
        filename: str,
        mime_type: str,
        folder: str = "uploads",
    ) -> MediaUploadResult:
        resource_type = "video" if mime_type.startswith("audio") else "image"
        try:
            result = self._uploader.upload(
                io.BytesIO(file_bytes),
                folder=f"nadibot/{folder}",
                resource_type=resource_type,
                public_id=f"{uuid.uuid4().hex}_{filename}",
            )
        except Exception as exc:
            log.error("Cloudinary upload failed: %s", exc)
            raise StorageError("Failed to upload file to Cloudinary", {"error": str(exc)})

        log.info("Cloudinary upload OK: %s", result["public_id"])
        return MediaUploadResult(
            url=result["secure_url"],
            provider="cloudinary",
            storage_path=result["public_id"],
            mime_type=mime_type,
            size_bytes=len(file_bytes),
        )


# ── Storage service (facade) ───────────────────────────────────────────────────

class StorageService:
    def __init__(self, provider: StorageProvider) -> None:
        self._provider = provider

    def upload_image(self, file_bytes: bytes, filename: str, mime_type: str) -> MediaUploadResult:
        log.info("Uploading image: %s (%d bytes)", filename, len(file_bytes))
        return self._provider.upload(file_bytes, filename, mime_type, folder="images")

    def upload_audio(self, file_bytes: bytes, filename: str, mime_type: str) -> MediaUploadResult:
        log.info("Uploading audio: %s (%d bytes)", filename, len(file_bytes))
        return self._provider.upload(file_bytes, filename, mime_type, folder="audio")


# ── Factory ────────────────────────────────────────────────────────────────────

def build_storage_service() -> StorageService:
    from app.core.config import get_settings
    from app.db.supabase import get_supabase_client

    settings = get_settings()

    if settings.STORAGE_PROVIDER == "cloudinary":
        log.info("Storage provider: Cloudinary")
        provider = CloudinaryStorageProvider(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
        )
    else:
        log.info("Storage provider: Supabase Storage")
        provider = SupabaseStorageProvider(
            client=get_supabase_client(),
            bucket=settings.SUPABASE_STORAGE_BUCKET,
        )

    return StorageService(provider)
