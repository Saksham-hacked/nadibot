"""
Structured logging setup using Python's standard logging.
Produces JSON-friendly structured output in production,
readable coloured output in development.
"""

import logging
import sys
from app.core.config import get_settings


def configure_logging() -> None:
    settings = get_settings()
    level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    handler = logging.StreamHandler(sys.stdout)

    if settings.APP_ENV == "production":
        import json

        class JsonFormatter(logging.Formatter):
            def format(self, record: logging.LogRecord) -> str:
                payload = {
                    "level": record.levelname,
                    "logger": record.name,
                    "message": record.getMessage(),
                    "time": self.formatTime(record, self.datefmt),
                }
                if record.exc_info:
                    payload["exc_info"] = self.formatException(record.exc_info)
                return json.dumps(payload)

        handler.setFormatter(JsonFormatter())
    else:
        fmt = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        handler.setFormatter(logging.Formatter(fmt))

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()
    root.addHandler(handler)

    # Silence noisy third-party loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("supabase").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
