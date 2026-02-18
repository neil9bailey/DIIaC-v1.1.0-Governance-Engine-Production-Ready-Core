from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

from app.api.auth import get_current_principal
from app.api.rbac import require_roles
from app.execution.router import execute
from app.llm_providers.llm_service import generate_from_llm
from app.services.ledger import record_ledger_entry


router = APIRouter()


@router.post(
    "/api/generate/proposition",
    dependencies=[Depends(require_roles(["EXECUTIVE", "ARCHITECT"]))],
)
def generate_proposition(
    payload: Dict[str, Any],
    principal: Dict[str, Any] = Depends(get_current_principal),
):
    """
    Generate governed, advisory-only proposition content.

    - Auth & RBAC enforced here
    - submitted_by captured for audit only
    - execution remains deterministic
    """

    try:
        execution_result = execute(
            role=payload["role"],
            schema=payload["schema"],
            intent="generate_proposition_content",
            input_data=payload["input_data"],
            assembled_prompt=payload.get("assembled_prompt", ""),
            constraints=payload.get("constraints"),
        )

        llm_response = generate_from_llm(
            prompt=execution_result["governed_prompt"]
        )

        submitted_by = principal.get("sub") if principal else None

        ledger_id = record_ledger_entry(
            intent="generate_proposition_content",
            risk_level=execution_result["risk_level"],
            policy_id=execution_result["policy_applied"],
            llm_provider=llm_response["source"]["provider"],
            model=llm_response["source"]["model"],
            trusted=False,
            submitted_by=submitted_by,
        )

        return {
            "content": llm_response["content"]["text"],
            "disclaimer": "AI-generated advisory content. Not a factual or contractual statement.",
            "risk_level": execution_result["risk_level"],
            "policy": execution_result["policy_applied"],
            "audit_ref": ledger_id,
        }

    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
