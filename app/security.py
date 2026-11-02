"""API-key authentication as a FastAPI dependency.

Usage in a router:  dependencies=[Depends(require_api_key)]
"""

import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from app.config import Settings, get_settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def require_api_key(
    api_key: Annotated[str | None, Depends(api_key_header)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> None:
    if api_key is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing API key")
    # compare_digest takes the same time whether the first or last character is wrong,
    # so attackers can't guess the key one character at a time (timing attack).
    if not any(secrets.compare_digest(api_key, valid) for valid in settings.api_key_list):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing API key")
