import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
LIBRARY_DIR = BASE_DIR / "library"


def validate_library_or_exit() -> None:
    errors: list[str] = []

    for file in LIBRARY_DIR.rglob("*.json"):
        try:
            raw = file.read_text(encoding="utf-8").strip()
            if not raw:
                raise ValueError("File is empty")
            json.loads(raw)
        except Exception as exc:
            errors.append(f"{file.relative_to(LIBRARY_DIR)} → {exc}")

    if errors:
        print("\n❌ INVALID LIBRARY CONTENT\n")
        for e in errors:
            print(" -", e)
        sys.exit(1)
