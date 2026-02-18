import hashlib
import json
from typing import Any, Dict


def _canonical_json(data: Dict[str, Any]) -> str:
    """
    Produce a canonical JSON string for deterministic hashing.
    """
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def sha256_hash(data: Dict[str, Any]) -> str:
    """
    Compute SHA-256 hash of canonical JSON.
    """
    canonical = _canonical_json(data)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def compute_library_hashes(
    role_def: Dict[str, Any],
    schema_def: Dict[str, Any],
    module_defs: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Compute deterministic hashes for role, schema, and modules.
    """
    return {
        "role": sha256_hash(role_def),
        "schema": sha256_hash(schema_def),
        "modules": {
            module_id: sha256_hash(module_def)
            for module_id, module_def in module_defs.items()
        },
    }

