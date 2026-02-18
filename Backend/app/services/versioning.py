import hashlib
import json
from datetime import datetime
from pathlib import Path

DATA_DIR = (
    Path(__file__).resolve().parent.parent / "data" / "prompts"
)
DATA_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = DATA_DIR / "prompts.jsonl"


def store_prompt(record: dict) -> dict:
    """
    Persist a versioned prompt record (append-only).
    """
    payload = json.dumps(record, sort_keys=True).encode()
    record["id"] = "sha256:" + hashlib.sha256(payload).hexdigest()
    record["timestamp"] = datetime.utcnow().isoformat() + "Z"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

    return record
