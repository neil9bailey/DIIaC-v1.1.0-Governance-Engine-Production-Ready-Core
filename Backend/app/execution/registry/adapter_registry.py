from typing import List

from app.execution.contracts import ExecutionAdapter, ExecutionRequest


class AdapterResolutionError(Exception):
    pass


class AdapterRegistry:
    """
    Deterministic adapter registry.
    Exactly one adapter must match a request.
    """

    def __init__(self) -> None:
        self._adapters: List[ExecutionAdapter] = []

    def register(self, adapter: ExecutionAdapter) -> None:
        self._adapters.append(adapter)

    def resolve(self, request: ExecutionRequest) -> ExecutionAdapter:
        matches = [
            a for a in self._adapters
            if request.schema in a.capabilities.get("schemas", [])
            and request.role in a.capabilities.get("roles", [])
        ]

        if not matches:
            raise AdapterResolutionError(
                f"No adapter for role='{request.role}', schema='{request.schema}'"
            )

        if len(matches) > 1:
            raise AdapterResolutionError(
                f"Multiple adapters match: {[a.name for a in matches]}"
            )

        return matches[0]
