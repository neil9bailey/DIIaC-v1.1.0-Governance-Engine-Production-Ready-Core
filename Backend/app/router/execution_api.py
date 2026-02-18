from fastapi import APIRouter, Depends, HTTPException

from app.api.rbac import require_roles
from app.execution.router import execute


router = APIRouter()


@router.post("/api/execute")
def execute_api(
    *,
    role: str,
    schema: str,
    intent: str,
    input_data,
    assembled_prompt: str,
    constraints=None,
    _=Depends(require_roles(["EXECUTOR"])),
):
    """
    API execution endpoint.

    - Auth/RBAC enforced here
    - Deterministic execution delegated unchanged
    """

    try:
        return execute(
            role=role,
            schema=schema,
            intent=intent,
            input_data=input_data,
            assembled_prompt=assembled_prompt,
            constraints=constraints,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
