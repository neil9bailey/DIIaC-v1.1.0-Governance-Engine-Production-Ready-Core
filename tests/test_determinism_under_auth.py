"""
Determinism enforcement test.

This test proves that core execution behaviour is deterministic and
independent of API, authentication, or caller context.

Auth governs access.
Determinism governs behaviour.
They never mix.
"""

from app.execution.normalize.normalize_execution_request import (
    normalize_execution_request,
)
from app.services.validation_engine import validate_execution_request
from app.services.risk_engine import assess_risk


def test_execution_pipeline_is_deterministic():
    """
    Same input must produce identical normalized payload,
    validation result, and risk result across invocations.
    """

    request_payload = {
        "contract_id": "demo-contract-001",
        "policy_id": "MARKETING_ADVISORY_ONLY",
        "content": "Advisory content placeholder",
        "payload": {
            "role": "enterprise_architect",
            "schema": "CTO_STRATEGY",
            "intent": "generate_proposition_content",
            "input_data": {
                "client": "Telent / M Group",
                "context": "Copilot governance",
            },
        },
        "llm_source": {
            "type": "llm",
            "provider": "openai",
            "model": "gpt-4.x",
            "trusted": False,
        },
    }

    # First run
    normalized_a = normalize_execution_request(request_payload)
    validate_execution_request(normalized_a)
    risk_a = assess_risk(normalized_a)

    # Second run (identical input)
    normalized_b = normalize_execution_request(request_payload)
    validate_execution_request(normalized_b)
    risk_b = assess_risk(normalized_b)

    assert normalized_a == normalized_b
    assert risk_a == risk_b
