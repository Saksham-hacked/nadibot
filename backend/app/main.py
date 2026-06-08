"""
NadiBot FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logging import configure_logging
from app.api.middleware import ErrorHandlingMiddleware, RequestLoggingMiddleware
from app.api.routes import complaints, incidents, analytics, authorities, health

# ── Configure logging first ────────────────────────────────────────────────────
configure_logging()

# ── Application ────────────────────────────────────────────────────────────────
app = FastAPI(
    title="NadiBot API",
    description=(
        "AI-powered water governance platform. "
        "Citizens report water issues; the backend classifies, clusters, and routes them."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── Middleware (order matters – outermost runs first) ──────────────────────────
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ────────────────────────────────────────────────────────────────────
API_PREFIX = "/api/v1"

app.include_router(health.router,       prefix=API_PREFIX)
app.include_router(complaints.router,   prefix=API_PREFIX)
app.include_router(incidents.router,    prefix=API_PREFIX)
app.include_router(analytics.router,    prefix=API_PREFIX)
app.include_router(authorities.router,  prefix=API_PREFIX)


# ── Root ───────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
def root():
    return {
        "service": "NadiBot Backend",
        "version": "1.0.0",
        "docs": "/docs",
    }
