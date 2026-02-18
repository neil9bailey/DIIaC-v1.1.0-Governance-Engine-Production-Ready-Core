from typing import Optional, Dict, Any, Literal
from pydantic import BaseModel


class LLMSource(BaseModel):
    """
    Phase 3.2 — Declarative provenance metadata.

    This model is informational only.
    It MUST NOT influence execution, validation semantics, or risk scoring.
    """

    type: Literal["llm", "human", "unknown"]
    provider: Optional[str] = None
    model: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    trusted: bool


class ExecutionRequest(BaseModel):
    """
    Canonical execution request contract.

    Phase 3.2 extends this contract to optionally carry LLM source metadata.
    """

    contract_id: str
    policy_id: str
    content: Dict[str, Any]

    # Phase 3.2 — optional, declarative provenance
    llm_source: Optional[LLMSource] = None
