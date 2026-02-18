import json
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional


class LedgerStore:
    """
    Append-only, hash-chained ledger.

    Phase 3.2:
    - source_metadata is persisted verbatim
    - included in the hash chain
    """

    def __init__(self, path: str):
        self.path = path

    def _hash_entry(self, entry: Dict[str, Any]) -> str:
        encoded = json.dumps(entry, sort_keys=True).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def append(
        self,
        contract_id: str,
        policy_id: str,
        validation_result: Dict[str, Any],
        risk_result: Dict[str, Any],
        output_snapshot: Dict[str, Any],
        source_metadata: Optional[Dict[str, Any]],
        previous_hash: Optional[str] = None,
    ) -> Dict[str, Any]:

        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "contract_id": contract_id,
            "policy_id": policy_id,
            "validation": validation_result,
            "risk": risk_result,
            "output": output_snapshot,
            "source_metadata": source_metadata,
            "previous_hash": previous_hash,
        }

        entry_hash = self._hash_entry(entry)
        entry["entry_hash"] = entry_hash

        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

        return entry
