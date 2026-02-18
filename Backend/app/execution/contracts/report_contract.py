from typing import Dict, Any
from dataclasses import dataclass


@dataclass(frozen=True)
class ReportContract:
    """
    Immutable execution contract for report generation.
    Used only as a type marker and payload carrier.
    """

    contract_id: str
    execution_id: str
    parameters: Dict[str, Any]
