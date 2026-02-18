import uuid
from datetime import datetime
from typing import Optional, Dict, Any

# Simple in-memory ledger for MVP / demo purposes
_LEDGER: Dict[str, Dict[str, Any]] = {}


def record_ledger_entry(
    *,
    intent: str,
    risk_level: str,
    policy_id: str,
    llm_provider: Optional[str] = None,
    model: Optional[str] = None,
    trusted: bool = False,
    submitted_by: Optional[str] = None,
) -> str:
    """
    Record an immutable ledger entry for audit purposes.

    IMPORTANT:
    - submitted_by is non-decisional
    - never influences execution or policy
    - audit-only metadata
    """

    ledger_id = str(uuid.uuid4())

    _LEDGER[ledger_id] = {
        "ledger_id": ledger_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "intent": intent,
        "risk_level": risk_level,
        "policy_id": policy_id,
        "llm_provider": llm_provider,
        "model": model,
        "trusted": trusted,
        "submitted_by": submitted_by,
    }

    return ledger_id


def read_ledger() -> Dict[str, Dict[str, Any]]:
    return _LEDGER.copy()


def verify_ledger() -> Dict[str, Any]:
    """
    Placeholder for ledger verification / hashing.
    """
    return {
        "entries": len(_LEDGER),
        "status": "ok"
    }
