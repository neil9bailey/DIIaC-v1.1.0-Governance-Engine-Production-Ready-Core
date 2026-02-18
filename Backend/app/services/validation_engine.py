from typing import Dict, Any


def validate_execution_request(payload: Dict[str, Any]) -> None:
    """
    Deterministic structural validation.

    Phase 3.2:
    - llm_source is OPTIONAL
    - If present, it is STRUCTURALLY validated only
    - No semantic checks
    - No inference
    """

    llm_source = payload.get("llm_source")

    if llm_source is None:
        return

    if not isinstance(llm_source, dict):
        raise ValueError("llm_source must be an object")

    if "type" not in llm_source:
        raise ValueError("llm_source missing required field: type")

    if "trusted" not in llm_source:
        raise ValueError("llm_source missing required field: trusted")

    if not isinstance(llm_source["trusted"], bool):
        raise ValueError("llm_source.trusted must be boolean")
