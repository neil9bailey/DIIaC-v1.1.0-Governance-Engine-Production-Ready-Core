from pathlib import Path
import json
from typing import Any

# Directory that holds execution / vendor schemas
SCHEMA_DIR = Path(__file__).parent.parent / "schemas"


class SchemaNotFound(Exception):
    pass


def list_schemas() -> list[str]:
    """
    Return a list of available schema names (without file extension).
    Used by the API and execution router for discovery.
    """
    if not SCHEMA_DIR.exists():
        return []

    return sorted(
        f.stem
        for f in SCHEMA_DIR.glob("*.json")
        if f.is_file()
    )


def load_schema(name: str) -> dict[str, Any]:
    """
    Load a schema by name.
    Raises SchemaNotFound if the schema does not exist.
    """
    schema_path = SCHEMA_DIR / f"{name}.json"

    if not schema_path.exists():
        raise SchemaNotFound(f"Schema '{name}' not found")

    with schema_path.open("r", encoding="utf-8") as f:
        return json.load(f)
