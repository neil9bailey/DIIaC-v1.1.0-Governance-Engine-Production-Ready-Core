from app.execution.contracts import ExecutionContext
from app.execution.normalize.normalize_execution_request import (
    normalize_execution_request,
)
from app.execution.registry.adapter_registry import AdapterRegistry
from app.execution.bootstrap.register_adapters import register_adapters


# Phase 3: single, explicit registry (v1.x)
# Phase 3: single, explicit registry (v1.x)
_registry = AdapterRegistry()
register_adapters(_registry)



def execute(
    *,
    role: str,
    schema: str,
    intent: str,
    input_data,
    assembled_prompt: str,
    constraints=None,
):
    """
    Phase 3 execution router (single-path).

    - Deterministic adapter resolution
    - Normalized adapter input
    - No fallback logic
    """
    ctx = ExecutionContext(
        contract_version="1.0",
        mode="standard",
        strict=True,
    )

    request = normalize_execution_request(
        role=role,
        schema=schema,
        intent=intent,
        input_data=input_data,
        assembled_prompt=assembled_prompt,
        constraints=constraints,
    )

    adapter = _registry.resolve(request)
    return adapter.execute(request, ctx)
