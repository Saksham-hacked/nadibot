"""
Admin key security helper.
A simple constant-time comparison against the env-var ADMIN_KEY.
No JWT, no sessions – this is MVP-grade protection.
"""

import hmac
from app.core.config import get_settings
from app.core.exceptions import AdminAuthError


def verify_admin_key(provided_key: str) -> None:
    """
    Raise AdminAuthError if the provided key does not match the configured key.
    Uses hmac.compare_digest to prevent timing attacks.
    """
    expected = get_settings().ADMIN_KEY
    if not hmac.compare_digest(provided_key.strip(), expected.strip()):
        raise AdminAuthError("Invalid or missing admin key.")
