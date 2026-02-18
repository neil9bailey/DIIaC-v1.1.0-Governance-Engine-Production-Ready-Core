import os
from typing import Dict, Any, Optional

from fastapi import Header, HTTPException
import jwt


AUTH_ENABLED = os.getenv("AUTH_ENABLED", "false").lower() == "true"
JWT_ISSUER = os.getenv("JWT_ISSUER")
JWT_AUDIENCE = os.getenv("JWT_AUDIENCE")
JWT_PUBLIC_KEY = os.getenv("JWT_PUBLIC_KEY")


def get_current_principal(
    authorization: Optional[str] = Header(default=None),
) -> Dict[str, Any]:
    """
    API-layer authentication dependency.

    - Enforced only if AUTH_ENABLED=true
    - JWT verification only (no user lookup)
    - Extracts claims as opaque metadata
    """

    if not AUTH_ENABLED:
        return {}

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")

    token = authorization.split(" ", 1)[1]

    try:
        payload = jwt.decode(
            token,
            JWT_PUBLIC_KEY,
            algorithms=["RS256"],
            audience=JWT_AUDIENCE,
            issuer=JWT_ISSUER,
        )
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc

    return payload
