import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
ROLES_DIR = BASE_DIR / "library" / "roles"


def list_roles() -> list[str]:
    roles = []
    for f in ROLES_DIR.glob("*.json"):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            roles.append(data.get("role", f.stem))
        except Exception:
            continue
    return sorted(roles)
