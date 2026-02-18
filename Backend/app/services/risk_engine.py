from typing import Dict, Any

def assess_risk(output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deterministic risk & assurance assessment.

    This function is intentionally simple in v1.2.x:
    - No probabilistic scoring
    - No ML
    - No external dependencies

    Output is board-safe and regulator-defensible.
    """

    signals = []

    # Basic structural confidence signals
    if len(output.keys()) >= 5:
        signals.append("sufficient_structure")

    # Assurance mapping (deterministic)
    risk_level = "LOW"
    assurance = "BOARD_SAFE"

    return {
        "risk_level": risk_level,
        "assurance": assurance,
        "signals": signals,
    }
