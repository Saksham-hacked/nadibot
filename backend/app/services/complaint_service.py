"""
Complaint service – main orchestrator for complaint submission pipeline.

Flow:
1. Resolve reporter identity
2. Process media (upload + AI analysis)
3. Build complaint context string
4. Classify with Gemini
5. Route to authority (deterministic)
6. Reverse geocode
7. Find or create incident
8. Persist complaint
9. Return structured response
"""

from __future__ import annotations
from typing import Optional
from fastapi import UploadFile

from app.models.complaint import Complaint
from app.repositories.complaint_repository import ComplaintRepository
from app.services.gemini_service import GeminiService
from app.services.media_processing_service import MediaProcessingService
from app.services.authority_service import AuthorityService
from app.services.incident_service import IncidentService
from app.services.reporter_service import ReporterService
from app.services.transcript_service import GeocodingService
from app.schemas.complaint import ComplaintCreateRequest, ComplaintResponse, LocationResponse
from app.schemas.incident import IncidentResponse
from app.core.exceptions import MediaRequiredError
from app.core.logging import get_logger

log = get_logger(__name__)


class ComplaintService:
    def __init__(
        self,
        complaint_repo: ComplaintRepository,
        gemini: GeminiService,
        media: MediaProcessingService,
        authority: AuthorityService,
        incident: IncidentService,
        reporter: ReporterService,
        geocoding: GeocodingService,
    ) -> None:
        self._repo = complaint_repo
        self._gemini = gemini
        self._media = media
        self._authority = authority
        self._incident = incident
        self._reporter = reporter
        self._geocoding = geocoding

    async def submit_complaint(
        self,
        request: ComplaintCreateRequest,
        image_file: Optional[UploadFile] = None,
        audio_file: Optional[UploadFile] = None,
    ) -> ComplaintResponse:
        # ── 1. Validate: at least one content source ──────────────────────────
        has_text = bool(request.text)
        has_image = image_file is not None
        has_audio = audio_file is not None

        if not (has_text or has_image or has_audio):
            raise MediaRequiredError(
                "At least one of text, image, or audio must be provided."
            )

        log.info(
            "Complaint submission started | text=%s image=%s audio=%s lat=%.4f lon=%.4f",
            has_text, has_image, has_audio, request.latitude, request.longitude,
        )

        # ── 2. Resolve reporter ───────────────────────────────────────────────
        reporter_id = self._reporter.resolve_reporter_id(request.reporter_id)
        self._reporter.register(reporter_id)

        # ── 3. Process media ──────────────────────────────────────────────────
        image_url: Optional[str] = None
        image_summary: Optional[str] = None
        audio_url: Optional[str] = None
        transcript: Optional[str] = None

        if has_image:
            upload_result, analysis = await self._media.process_image(image_file)
            image_url = upload_result.url
            image_summary = analysis.description or None

        if has_audio:
            upload_result, transcript_result = await self._media.process_audio(audio_file)
            audio_url = upload_result.url
            transcript = transcript_result.transcript or None

        # ── 4. Build context for Gemini ───────────────────────────────────────
        context_parts: list[str] = []
        if request.text:
            context_parts.append(f"Citizen text: {request.text}")
        if transcript:
            context_parts.append(f"Audio transcript: {transcript}")
        if image_summary:
            context_parts.append(f"Image description: {image_summary}")

        context = "\n\n".join(context_parts)

        # ── 5. Classify with Gemini ───────────────────────────────────────────
        classification = self._gemini.classify_complaint(context)

        # ── 6. Deterministic authority routing ────────────────────────────────
        authority_name = self._authority.resolve(classification.category)

        # ── 7. Reverse geocode ────────────────────────────────────────────────
        geo = await self._geocoding.reverse_geocode(request.latitude, request.longitude)

        # ── 8. Build complaint model ──────────────────────────────────────────
        complaint = Complaint(
            reporter_id=reporter_id,
            text=request.text,
            transcript=transcript,
            image_url=image_url,
            audio_url=audio_url,
            image_summary=image_summary,
            latitude=request.latitude,
            longitude=request.longitude,
            location_accuracy=request.accuracy,
            location_source=request.location_source,
            locality=geo.get("locality"),
            district=geo.get("district"),
            state=geo.get("state"),
            full_address=geo.get("full_address"),
            category=classification.category,
            subcategory=classification.subcategory,
            severity=classification.severity,
            authority=authority_name,
            summary=classification.summary,
            confidence=classification.confidence,
            status="OPEN",
        )

        # ── 9. Find or create incident ────────────────────────────────────────
        incident = self._incident.find_or_create_incident(complaint)
        complaint.incident_id = incident.id

        # ── 10. Persist complaint ─────────────────────────────────────────────
        saved = self._repo.create(complaint)
        self._reporter.increment(reporter_id)

        log.info(
            "Complaint saved: id=%s category=%s severity=%s incident=%s",
            saved.id, saved.category, saved.severity, saved.incident_id,
        )

        return self._to_response(saved)

    def get_complaint(self, complaint_id: str) -> ComplaintResponse:
        complaint = self._repo.get_by_id(complaint_id)
        return self._to_response(complaint)

    def list_complaints(self, **filters) -> tuple[list[ComplaintResponse], int]:
        complaints, total = self._repo.list_complaints(**filters)
        return [self._to_response(c) for c in complaints], total

    def get_reporter_complaints(self, reporter_id: str) -> list[ComplaintResponse]:
        complaints = self._repo.list_by_reporter(reporter_id)
        return [self._to_response(c) for c in complaints]

    # ── Serialisation helper ──────────────────────────────────────────────────

    def _to_response(self, complaint: Complaint) -> ComplaintResponse:
        return ComplaintResponse(
            id=complaint.id,
            reporter_id=complaint.reporter_id,
            text=complaint.text,
            transcript=complaint.transcript,
            image_url=complaint.image_url,
            audio_url=complaint.audio_url,
            image_summary=complaint.image_summary,
            location=LocationResponse(
                latitude=complaint.latitude,
                longitude=complaint.longitude,
                location_accuracy=complaint.location_accuracy,
                location_source=complaint.location_source,
                locality=complaint.locality,
                district=complaint.district,
                state=complaint.state,
                full_address=complaint.full_address,
            ),
            category=complaint.category,
            subcategory=complaint.subcategory,
            severity=complaint.severity,
            authority=complaint.authority,
            summary=complaint.summary,
            confidence=complaint.confidence,
            status=complaint.status,
            incident_id=complaint.incident_id,
            created_at=complaint.created_at,
            updated_at=complaint.updated_at,
        )
