from fastapi import APIRouter, Header, HTTPException
from typing import Optional

from app.execution.contracts.execution_request import ExecutionRequest
from app.execution.normalize.normalize_execution_request import normalize_execution_request
from app.services.validation_engine import validate_execution_request
from app.services.risk_engine import assess_risk
from app.execution.ledger.ledger_store import LedgerStore

router = APIRouter()

ledger = LedgerStore(path="ledger.jsonl")


@router.post("/api/execute/validate")
def execute_validate(
    request: ExecutionRequest,
    x_execution_intent: Optional[str] = Header(default=None),
):
    if x_execution_intent != "true":
        raise HTTPException(status_code=400, detail="Explicit execution intent required")

    payload = normalize_execution_request(request.dict())

    validate_execution_request(payload)

    validation_result = {
        "status": "pass",
        "policy_id": request.policy_id,
    }

    risk_result = assess_risk(payload)

    ledger_entry = ledger.append(
        contract_id=request.contract_id,
        policy_id=request.policy_id,
        validation_result=validation_result,
        risk_result=risk_result,
        output_snapshot=request.content,
        source_metadata=payload.get("llm_source"),
    )

    return {
        "validation": validation_result,
        "risk": risk_result,
        "ledger_entry": ledger_entry,
    }
