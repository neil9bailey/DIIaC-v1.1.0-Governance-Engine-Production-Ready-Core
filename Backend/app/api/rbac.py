from typing import List, Callable, Dict, Any

from fastapi import Depends, HTTPException

from app.api.auth import get_current_principal, AUTH_ENABLED


def require_roles(required_roles: List[str]) -> Callable:
    """
    API-layer RBAC dependency.

    - Binary allow/deny
    - Roles read from JWT claims
    - Enforced only if AUTH_ENABLED=true
    """

    def dependency(
        principal: Dict[str, Any] = Depends(get_current_principal),
    ) -> None:
        if not AUTH_ENABLED:
            return

        roles = principal.get("roles", [])

        if not any(role in roles for role in required_roles):
            raise HTTPException(status_code=403, detail="Insufficient role")

    return dependency
