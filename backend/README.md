# NadiBot — Backend

AI-powered water governance platform. Citizens report water-related issues (text, voice, images); the backend classifies, clusters, and routes them to the right authority.

---

## Sanity Check Summary

| Area | Status | Notes |
|---|---|---|
| Folder structure | ✅ Complete | Matches spec exactly |
| FastAPI app wiring | ✅ | `main.py` → `app/main.py` → routers correct |
| Config / settings | ✅ | Pydantic `BaseSettings`, `.env` support, `lru_cache` singleton |
| Exception hierarchy | ✅ | Full custom hierarchy, middleware maps to correct HTTP codes |
| Admin key guard | ✅ | `hmac.compare_digest`, `require_admin` DI dependency |
| Complaint pipeline | ✅ | 10-step flow in `ComplaintService`, service/repo separation clean |
| Gemini integration | ✅ | Structured JSON output, Pydantic validation, retry + fallback |
| Authority routing | ✅ | 100% deterministic, `CATEGORY_TO_AUTHORITY` constant, Gemini never touches routing |
| Incident clustering | ✅ | Haversine in Python, bounding-box pre-filter on Supabase, find-or-create |
| Storage abstraction | ✅ | `StorageProvider` ABC, Supabase + Cloudinary providers, factory pattern |
| Reverse geocoding | ✅ | Nominatim via `httpx`, in-memory TTL cache in `LocationRepository` |
| Analytics layer | ✅ | All 13 required metrics, service + repo separation |
| Anonymous reporter | ✅ | Server-side UUID fallback, `reporters` table, no auth |
| Tests | ✅ | pytest, mocked repos, covers validation/routing/incidents/analytics/Gemini parsing |
| Known issue | ⚠️ | `transcript_service.py` exports `GeocodingService` — misleading filename (see below) |

> **One naming issue found:** `app/services/transcript_service.py` actually contains `GeocodingService`, not a transcript service. The transcript logic lives in `gemini_service.py`. This doesn't break anything but will confuse contributors. The fix is noted in the README and should be renamed in a future refactor.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI + Uvicorn |
| Language | Python 3.12+ |
| Validation | Pydantic v2 |
| Database | Supabase (Postgres) |
| Storage | Supabase Storage (Cloudinary fallback) |
| AI | Google Gemini Flash (`gemini-1.5-flash`) |
| Geocoding | OpenStreetMap Nominatim |
| HTTP client | httpx (async) |
| Testing | pytest + pytest-asyncio |
| Deployment | Render |

---

## Project Structure

```
backend/
├── main.py                        # Render/uvicorn entry point
├── requirements.txt
├── .env.example                   # Copy → .env and fill in values
└── app/
    ├── main.py                    # FastAPI app, middleware, routers
    ├── api/
    │   ├── dependencies.py        # DI wiring — all services/repos assembled here
    │   ├── middleware.py          # Error handling + request logging
    │   └── routes/
    │       ├── complaints.py      # POST/GET /api/v1/complaints
    │       ├── incidents.py       # GET/PATCH /api/v1/incidents
    │       ├── analytics.py       # GET /api/v1/analytics/*
    │       ├── authorities.py     # Admin-protected dashboard endpoints
    │       └── health.py          # /api/v1/health
    ├── core/
    │   ├── config.py              # Settings via pydantic-settings
    │   ├── constants.py           # Enums, authority routing table, Gemini prompt
    │   ├── exceptions.py          # Custom exception hierarchy
    │   ├── logging.py             # Structured logging (JSON in prod, readable in dev)
    │   └── security.py            # Admin key verification (hmac.compare_digest)
    ├── db/
    │   └── supabase.py            # Supabase client singleton
    ├── models/                    # Domain models (Pydantic, mirror DB rows)
    │   ├── complaint.py
    │   ├── incident.py
    │   └── reporter.py
    ├── schemas/                   # Request/response schemas
    │   ├── complaint.py
    │   ├── incident.py
    │   ├── analytics.py
    │   ├── media.py
    │   └── common.py
    ├── repositories/              # All DB interactions, no business logic
    │   ├── complaint_repository.py
    │   ├── incident_repository.py
    │   ├── reporter_repository.py
    │   ├── analytics_repository.py
    │   └── location_repository.py  # In-memory geocoding cache
    ├── services/                  # All business logic
    │   ├── complaint_service.py   # Main 10-step submission pipeline
    │   ├── incident_service.py    # find-or-create incident clustering
    │   ├── gemini_service.py      # Gemini API: classify + image + audio
    │   ├── media_processing_service.py  # Validate → upload → AI analyse
    │   ├── storage_service.py     # Provider-agnostic file upload
    │   ├── authority_service.py   # Deterministic category → authority mapping
    │   ├── analytics_service.py   # Dashboard metric computation
    │   ├── reporter_service.py    # Anonymous session management
    │   └── transcript_service.py  # ⚠️ Actually GeocodingService — see note above
    ├── utils/
    │   ├── helpers.py             # haversine_distance, truncate_string
    │   ├── validators.py          # Coordinate + reporter ID validation
    │   └── datetime.py
    └── tests/
        ├── test_complaints.py
        ├── test_incidents.py
        ├── test_authority_mapping.py
        └── test_analytics.py
```

---

## Setup & Running Locally

### 1. Prerequisites

- Python 3.12+
- A [Supabase](https://supabase.com) project (free tier works)
- A [Google AI Studio](https://aistudio.google.com) API key for Gemini

### 2. Clone and create virtual environment

```bash
cd nadibot/backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in the required values:

```env
# Required
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-service-role-key
SUPABASE_STORAGE_BUCKET=nadibot-media

GEMINI_API_KEY=your-gemini-api-key

ADMIN_KEY=change-this-to-a-strong-random-string

# Storage: "supabase" or "cloudinary"
STORAGE_PROVIDER=supabase

# Optional: only needed if STORAGE_PROVIDER=cloudinary
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
```

### 5. Set up Supabase tables

Run the following SQL in your Supabase SQL editor to create the required tables:

```sql
-- Reporters (anonymous device sessions)
CREATE TABLE reporters (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  reporter_id   TEXT UNIQUE NOT NULL,
  complaint_count INT DEFAULT 0,
  first_seen_at TIMESTAMPTZ DEFAULT now(),
  last_seen_at  TIMESTAMPTZ DEFAULT now()
);

-- Incidents (grouped complaints)
CREATE TABLE incidents (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title           TEXT NOT NULL,
  category        TEXT NOT NULL,
  severity        TEXT NOT NULL,
  authority       TEXT NOT NULL,
  latitude        FLOAT NOT NULL,
  longitude       FLOAT NOT NULL,
  district        TEXT,
  state           TEXT,
  status          TEXT DEFAULT 'OPEN',
  complaint_count INT DEFAULT 0,
  resolution_notes TEXT,
  created_at      TIMESTAMPTZ DEFAULT now(),
  updated_at      TIMESTAMPTZ DEFAULT now()
);

-- Complaints
CREATE TABLE complaints (
  id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  reporter_id      TEXT NOT NULL,
  text             TEXT,
  transcript       TEXT,
  image_url        TEXT,
  audio_url        TEXT,
  image_summary    TEXT,
  latitude         FLOAT NOT NULL,
  longitude        FLOAT NOT NULL,
  location_accuracy FLOAT NOT NULL,
  location_source  TEXT,
  locality         TEXT,
  district         TEXT,
  state            TEXT,
  full_address     TEXT,
  category         TEXT DEFAULT 'Other',
  subcategory      TEXT DEFAULT 'Other',
  severity         TEXT DEFAULT 'Medium',
  authority        TEXT DEFAULT 'General Grievance',
  summary          TEXT,
  confidence       FLOAT,
  status           TEXT DEFAULT 'OPEN',
  incident_id      UUID REFERENCES incidents(id),
  created_at       TIMESTAMPTZ DEFAULT now(),
  updated_at       TIMESTAMPTZ DEFAULT now()
);
```

Also create a **public storage bucket** named `nadibot-media` in your Supabase project under Storage.

### 6. Start the development server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API root:** http://localhost:8000
- **Swagger docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health check:** http://localhost:8000/api/v1/health

---

## Running Tests

```bash
pytest app/tests/ -v
```

Tests use mocked repositories and do not require a live Supabase or Gemini connection.

---

## API Overview

### Public Endpoints (no auth required)

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/v1/complaints` | Submit a citizen complaint (multipart/form-data) |
| `GET` | `/api/v1/complaints` | List complaints (filterable) |
| `GET` | `/api/v1/complaints/{id}` | Get single complaint |
| `GET` | `/api/v1/complaints/reporter/{reporter_id}` | All complaints by a reporter |
| `GET` | `/api/v1/incidents` | List incidents |
| `GET` | `/api/v1/analytics/overview` | Dashboard overview stats |
| `GET` | `/api/v1/analytics/categories` | Complaints per category |
| `GET` | `/api/v1/analytics/districts` | Complaints per district |
| `GET` | `/api/v1/analytics/trends?range=7d\|30d\|90d` | Time-series trends |
| `GET` | `/api/v1/analytics/geospatial` | All coordinates for map |
| `GET` | `/api/v1/health` | Liveness check |
| `GET` | `/api/v1/health/db` | Database connectivity check |

### Admin-Protected Endpoints

Require header: `X-Admin-Key: <your ADMIN_KEY value>`

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/v1/authorities/incidents` | List incidents for authority dashboard |
| `GET` | `/api/v1/authorities/complaints` | List complaints for authority dashboard |
| `PATCH` | `/api/v1/incidents/{id}/status` | Update incident status |
| `PATCH` | `/api/v1/incidents/{id}/notes` | Update incident resolution notes |

### Submitting a Complaint

```bash
curl -X POST http://localhost:8000/api/v1/complaints \
  -F "latitude=28.6139" \
  -F "longitude=77.2090" \
  -F "accuracy=15.0" \
  -F "text=There is a broken pipe leaking near the main road." \
  -F "reporter_id=device_abc123"
```

With an image:
```bash
curl -X POST http://localhost:8000/api/v1/complaints \
  -F "latitude=28.6139" \
  -F "longitude=77.2090" \
  -F "accuracy=15.0" \
  -F "text=Waterlogging on my street" \
  -F "image=@/path/to/photo.jpg"
```

---

## Complaint Processing Pipeline

When a complaint is submitted, the backend runs these steps in order:

```
1. Validate inputs (at least one of text/image/audio; valid GPS)
2. Resolve reporter identity (use provided ID or generate server-side UUID)
3. Upload media files to storage (Supabase or Cloudinary)
4. Extract image description via Gemini Vision (if image present)
5. Transcribe audio via Gemini (if audio present and within size limit)
6. Build aggregated context string (text + transcript + image description)
7. Classify with Gemini → structured JSON (category, subcategory, severity, summary, confidence)
8. Validate Gemini output with Pydantic — retry up to 2× on failure, fallback to "Other"
9. Route to authority deterministically (rule table, Gemini never decides this)
10. Reverse geocode GPS coordinates via Nominatim (cached, non-fatal on failure)
11. Find matching open incident within 500m with same category + authority, or create new one
12. Persist complaint and return structured response
```

---

## Key Design Decisions

**No citizen authentication.** Completely anonymous. Frontend generates a `reporter_id` and stores it in `localStorage`. Backend accepts it or generates one server-side.

**Gemini never routes.** Authority routing is a deterministic lookup table in `core/constants.py`. Gemini only classifies; a broken or hallucinating Gemini response cannot misdirect a complaint.

**Gemini output is always validated.** The classification response is parsed through a Pydantic model with strict enum values. Invalid responses trigger a repair prompt and up to 2 retries before falling back to `Other / Medium`.

**Incident clustering uses Haversine.** PostGIS is not assumed. A bounding box pre-filters candidates from Supabase, then Python calculates exact distances. Default radius is 500 metres (configurable via `DEFAULT_INCIDENT_RADIUS_METERS`).

**Storage is provider-agnostic.** `StorageProvider` is an ABC. Swap from Supabase to Cloudinary by changing `STORAGE_PROVIDER=cloudinary` in `.env`.

**Geocoding is cached in-memory.** Coordinates are rounded to 4 decimal places (~11 m precision) and cached for 1 hour to avoid hammering Nominatim.

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|---|---|---|---|
| `SUPABASE_URL` | ✅ | — | Your Supabase project URL |
| `SUPABASE_KEY` | ✅ | — | Service role key (bypasses RLS) |
| `SUPABASE_STORAGE_BUCKET` | — | `nadibot-media` | Storage bucket name |
| `GEMINI_API_KEY` | ✅ | — | Google AI Studio API key |
| `GEMINI_MODEL` | — | `gemini-1.5-flash` | Gemini model name |
| `GEMINI_MAX_RETRIES` | — | `2` | Classification retry attempts |
| `ADMIN_KEY` | ✅ | — | Secret key for authority dashboard |
| `STORAGE_PROVIDER` | — | `supabase` | `supabase` or `cloudinary` |
| `CLOUDINARY_CLOUD_NAME` | ⚠️ | — | Required if `STORAGE_PROVIDER=cloudinary` |
| `CLOUDINARY_API_KEY` | ⚠️ | — | Required if `STORAGE_PROVIDER=cloudinary` |
| `CLOUDINARY_API_SECRET` | ⚠️ | — | Required if `STORAGE_PROVIDER=cloudinary` |
| `REVERSE_GEOCODER_PROVIDER` | — | `nominatim` | Geocoding provider |
| `NOMINATIM_USER_AGENT` | — | `nadibot/1.0` | User-Agent for Nominatim requests |
| `DEFAULT_INCIDENT_RADIUS_METERS` | — | `500` | Incident clustering radius |
| `AUDIO_INLINE_MAX_BYTES` | — | `900000` | Max audio size for inline Gemini transcription |
| `APP_ENV` | — | `development` | `development` or `production` |
| `LOG_LEVEL` | — | `INFO` | Python logging level |

---

## Deployment on Render

1. Push the `backend/` folder to a GitHub repository.
2. Create a new **Web Service** on [Render](https://render.com).
3. Set the **Root Directory** to `backend` (or the folder containing `main.py`).
4. Set the **Build Command:** `pip install -r requirements.txt`
5. Set the **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add all required environment variables in the Render dashboard.

---

## Known Issues & Future Work

| Issue | Notes |
|---|---|
| `transcript_service.py` is misnamed | Contains `GeocodingService`, not a transcript service. Rename to `geocoding_service.py` |
| In-memory geocoding cache | Resets on process restart / Render redeploy. Use Redis for multi-instance deployments |
| `increment_complaint_count` is not atomic | Race condition possible under load; replace with a Postgres `UPDATE ... SET count = count + 1` |
| No DB migrations tooling | `db/migrations/` folder exists but is empty. Add Alembic or use Supabase migrations |
| CORS is open (`allow_origins=["*"]`) | Tighten to frontend domain before production |
| Audio transcription is synchronous | Large files block the request. Move to a background task queue (e.g. Celery, ARQ) |
