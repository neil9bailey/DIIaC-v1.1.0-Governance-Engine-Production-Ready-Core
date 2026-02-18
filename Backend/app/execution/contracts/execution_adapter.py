from abc import ABC, abstractmethod
from typing import Dict, Any

from .execution_request import ExecutionRequest
from .execution_result import ExecutionResult
from .execution_context import ExecutionContext


class ExecutionAdapter(ABC):
    """
    Contract-locked adapter interface for v1.x.
    Adapters are pure executors.
    """

    name: str
    capabilities: Dict[str, Any]

    @abstractmethod
    def execute(
        self,
        request: ExecutionRequest,
        ctx: ExecutionContext,
    ) -> ExecutionResult:
        raise NotImplementedError
