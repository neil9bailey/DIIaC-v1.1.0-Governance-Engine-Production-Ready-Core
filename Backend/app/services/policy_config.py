import json
import hashlib
import os
from typing import Dict, Any

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
POLICY_DIR = os.path.join(BASE_DIR, "library", "policies")

def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def load_policy() -> Dict[str, Any]:
    path = os.path.join(POLICY_DIR, "CTO_STRATEGY_BASELINE.json")
    with open(path, "r", encoding="utf-8") as f:
        policy = json.load(f)

    canonical = json.dumps(policy, sort_keys=True).encode("utf-8")
    policy["policy_hash"] = _sha256(canonical)
    return policy

_POLICY = load_policy()

def get_policy() -> Dict[str, Any]:
    return _POLICY

def get_policy_metadata() -> Dict[str, str]:
    return {
        "policy_id": _POLICY["policy_id"],
        "policy_version": _POLICY["policy_version"],
        "policy_hash": _POLICY["policy_hash"],
    }
