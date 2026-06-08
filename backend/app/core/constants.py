"""
Domain constants: categories, severities, subcategories, statuses,
and the deterministic authority-routing table.
"""

from enum import Enum


# ── Complaint categories ───────────────────────────────────────────────────────

class ComplaintCategory(str, Enum):
    WATER_SUPPLY = "Water Supply"
    WATER_QUALITY = "Water Quality"
    INFRASTRUCTURE = "Infrastructure"
    FLOODING = "Flooding"
    DRAINAGE = "Drainage"
    GROUNDWATER = "Groundwater"
    SANITATION = "Sanitation"
    OTHER = "Other"


# ── Severity levels ────────────────────────────────────────────────────────────

class SeverityLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


# ── Subcategories ──────────────────────────────────────────────────────────────

class ComplaintSubcategory(str, Enum):
    NO_WATER_SUPPLY = "No Water Supply"
    LOW_PRESSURE = "Low Pressure"
    PIPE_LEAKAGE = "Pipe Leakage"
    BROKEN_HANDPUMP = "Broken Handpump"
    CONTAMINATION = "Contamination"
    WATERLOGGING = "Waterlogging"
    DRAIN_OVERFLOW = "Drain Overflow"
    DRY_BOREWELL = "Dry Borewell"
    DRY_WELL = "Dry Well"
    OTHER = "Other"


# ── Status enums ───────────────────────────────────────────────────────────────

class ComplaintStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"


class IncidentStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"


# ── Authority names ────────────────────────────────────────────────────────────

class Authority(str, Enum):
    PHED = "PHED"
    DISASTER_MANAGEMENT = "Disaster Management"
    MUNICIPALITY = "Municipality"
    WATER_RESOURCES = "Water Resources Department"
    GENERAL_GRIEVANCE = "General Grievance"


# ── Deterministic authority routing table ─────────────────────────────────────
# This is the single source of truth. Gemini never touches routing.

CATEGORY_TO_AUTHORITY: dict[ComplaintCategory, Authority] = {
    ComplaintCategory.WATER_SUPPLY:  Authority.PHED,
    ComplaintCategory.WATER_QUALITY: Authority.PHED,
    ComplaintCategory.INFRASTRUCTURE: Authority.PHED,
    ComplaintCategory.FLOODING:      Authority.DISASTER_MANAGEMENT,
    ComplaintCategory.DRAINAGE:      Authority.MUNICIPALITY,
    ComplaintCategory.GROUNDWATER:   Authority.WATER_RESOURCES,
    ComplaintCategory.SANITATION:    Authority.MUNICIPALITY,
    ComplaintCategory.OTHER:         Authority.GENERAL_GRIEVANCE,
}


# ── Geocoding ──────────────────────────────────────────────────────────────────

GEOCODING_CACHE_TTL_SECONDS: int = 3600          # 1 hour in-memory cache TTL
GEOCODING_COORD_PRECISION: int = 4               # decimal places used as cache key


# ── Media ─────────────────────────────────────────────────────────────────────

ALLOWED_IMAGE_MIME_TYPES: set[str] = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
}

ALLOWED_AUDIO_MIME_TYPES: set[str] = {
    "audio/mpeg",
    "audio/mp4",
    "audio/wav",
    "audio/ogg",
    "audio/webm",
    "audio/aac",
    "audio/flac",
    "audio/x-m4a",
}

MAX_IMAGE_SIZE_BYTES: int = 10 * 1024 * 1024    # 10 MB
MAX_AUDIO_SIZE_BYTES: int = 25 * 1024 * 1024    # 25 MB

AUDIO_TRANSCRIPTION_PENDING_PLACEHOLDER = (
    "[Transcription pending – audio file exceeds inline processing limit]"
)

# ── Gemini ─────────────────────────────────────────────────────────────────────

GEMINI_CLASSIFICATION_SYSTEM_PROMPT = """\
You are a water-grievance classification AI for an Indian civic platform.

Given a complaint description (which may include text, an image description, 
and/or an audio transcript), extract a structured JSON classification.

Return ONLY valid JSON. No markdown. No explanations. No extra keys.

Schema:
{
  "category": "<one of the allowed categories>",
  "subcategory": "<one of the allowed subcategories>",
  "severity": "<Low | Medium | High | Critical>",
  "summary": "<2-3 sentence plain-language summary for authorities>",
  "confidence": <float between 0.0 and 1.0>
}

Allowed categories: Water Supply, Water Quality, Infrastructure, Flooding, 
Drainage, Groundwater, Sanitation, Other

Allowed subcategories: No Water Supply, Low Pressure, Pipe Leakage, 
Broken Handpump, Contamination, Waterlogging, Drain Overflow, 
Dry Borewell, Dry Well, Other

Rules:
- severity Critical: threat to human health or life (contamination, flooding with casualties risk)
- severity High: no supply for >24h, infrastructure failure affecting many
- severity Medium: intermittent issues, partial outages
- severity Low: minor nuisances, slow drains, aesthetic issues
- If you are unsure, use category Other and subcategory Other
- confidence reflects how certain you are about the category
"""
