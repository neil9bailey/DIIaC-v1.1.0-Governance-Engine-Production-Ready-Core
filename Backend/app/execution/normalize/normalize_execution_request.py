from typing import Dict, Any


def normalize_execution_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Phase 3.2 normalization rules:

    - Preserve llm_source verbatim if present
    - Do not infer defaults
    - Do not coerce trust
    - Do not mutate metadata
    """

    normalized = dict(payload)

    # Explicitly preserve llm_source if present
    if "llm_source" in payload:
        normalized["llm_source"] = payload["llm_source"]

    return normalized
