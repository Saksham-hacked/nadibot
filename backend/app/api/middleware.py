"""
Global middleware: structured error handling, request logging.
"""

from __future__ import annotations
import time
import uuid
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.exceptions import (
    NadiBotError,
    ValidationError,
    LocationMissingError,
    MediaRequiredError,
    UnsupportedMediaTypeError,
    FileTooLargeError,
    NotFoundError,
    AdminAuthError,
    StorageError,
    GeminiError,
    GeocodingError,
    DatabaseError,
)
from app.core.logging import get_logger

log = get_logger(__name__)


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Catch all NadiBotError subclasses and return consistent JSON error responses.
    Unhandled exceptions become HTTP 500.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            return await call_next(request)

        except (ValidationError, LocationMissingError, MediaRequiredError,
                UnsupportedMediaTypeError, FileTooLargeError) as exc:
            return JSONResponse(
                status_code=422,
                content={"ok": False, "error": exc.message, "details": exc.details},
            )
        except (NotFoundError,) as exc:
            return JSONResponse(
                status_code=404,
                content={"ok": False, "error": exc.message, "details": exc.details},
            )
        except AdminAuthError as exc:
            return JSONResponse(
                status_code=401,
                content={"ok": False, "error": exc.message, "details": exc.details},
            )
        except (StorageError, GeminiError, GeocodingError, DatabaseError) as exc:
            log.error("Service error: %s | %s", exc.message, exc.details)
            return JSONResponse(
                status_code=502,
                content={"ok": False, "error": exc.message, "details": exc.details},
            )
        except NadiBotError as exc:
            log.error("Unclassified domain error: %s", exc.message)
            return JSONResponse(
                status_code=500,
                content={"ok": False, "error": exc.message, "details": exc.details},
            )
        except Exception as exc:
            log.exception("Unhandled exception: %s", exc)
            return JSONResponse(
                status_code=500,
                content={"ok": False, "error": "An unexpected error occurred.", "details": {}},
            )


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log every request with method, path, status code, and duration."""

    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = uuid.uuid4().hex[:8]
        start = time.perf_counter()
        log.info("[%s] → %s %s", request_id, request.method, request.url.path)

        response = await call_next(request)

        duration_ms = (time.perf_counter() - start) * 1000
        log.info(
            "[%s] ← %s %s %d (%.1fms)",
            request_id, request.method, request.url.path,
            response.status_code, duration_ms,
        )
        return response
