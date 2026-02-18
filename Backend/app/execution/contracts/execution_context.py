from dataclasses import dataclass
from typing import Optional, Literal

@dataclass(frozen=True)
class ExecutionContext:
    contract_version: Literal["1.0"]
    mode: Literal["standard"]
    strict: Literal[True]
    trace_id: Optional[str] = None
