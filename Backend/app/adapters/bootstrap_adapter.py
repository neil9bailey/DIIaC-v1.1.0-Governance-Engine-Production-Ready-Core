"""
BootstrapAdapter
----------------
Deterministic execution adapter used to bootstrap the VendorLogic control plane.
Implements ExecutionAdapter explicitly and declares its capabilities.
"""

from typing import Dict, Any
from app.adapters.base import ExecutionAdapter


class BootstrapAdapter(ExecutionAdapter):

    @property
    def name(self) -> str:
        return "bootstrap"

    @property
    def capabilities(self) -> Dict[str, Any]:
        """
        Declares which execution schemas and roles this adapter supports.
        """
        return {
            "execution_schemas": ["bootstrap"],
            "roles": ["bootstrap"]
        }

    def execute(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deterministic execution path:
        - No external calls
        - Echoes the request payload for validation
        """
        return {
            "adapter": self.name,
            "execution_schema": request.get("execution_schema"),
            "role": request.get("role"),
            "intent": request.get("intent"),
            "input": request.get("input"),
            "options": request.get("options"),
            "note": "Bootstrap adapter execution (deterministic, no external model)"
        }
