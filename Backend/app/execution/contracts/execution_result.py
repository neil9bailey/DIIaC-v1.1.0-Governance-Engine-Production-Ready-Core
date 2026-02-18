from dataclasses import dataclass
from typing import Any, Optional, Dict

@dataclass(frozen=True)
class ExecutionResult:
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
