import json
import re
from pathlib import Path
from typing import Any

from app.exceptions import (
    RoleNotFoundError,
    InvalidSchemaNameError,
    LibraryFileError,
)
from app.services.content_normaliser import normalise_content
from app.services.schema_resolver import load_schema

BASE_DIR = Path(__file__).resolve().parents[1]
LIBRARY_DIR = BASE_DIR / "library"

ROLES_DIR = LIBRARY_DIR / "roles"
MODULES_DIR = LIBRARY_DIR / "modules"

REQUIRED_MODULES = [
    "first_principles",
    "deep_research",
    "devils_advocate",
    "constraints_first",
]

SCHEMA_NAME_PATTERN = re.compile(r"^[A-Z0-9_]+$")


def _role_to_filename(role: str) -> str:
    return role.lower().replace(" ", "_") + ".json"


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise LibraryFileError(f"Missing file: {path.name}")

    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        raise LibraryFileError(f"File is empty: {path.name}")

    try:
        return json.loads(raw)
    except Exception as exc:
        raise LibraryFileError(f"Invalid JSON in {path.name}") from exc


def _validate_schema_name(schema_name: str) -> None:
    if not SCHEMA_NAME_PATTERN.match(schema_name.replace(" ", "")):
        raise InvalidSchemaNameError(f"Invalid schema name: {schema_name}")


def assemble_prompt(role: str, task: str, schema_name: str) -> str:
    _validate_schema_name(schema_name)

    role_file = ROLES_DIR / _role_to_filename(role)
    if not role_file.exists():
        raise RoleNotFoundError(f"Unsupported role: {role}")

    role_data = _load_json(role_file)
    schema_data = load_schema(schema_name)

    sections: list[str] = [
        "ACT AS:",
        f"Role: {role}",
        f"Mission: {role_data.get('mission', '')}",
        f"Decision Style: {role_data.get('decision_style', '')}",
        f"Communication Style: {role_data.get('communication_style', '')}",
        "",
        "TASK:",
        task,
        "",
    ]

    for module in REQUIRED_MODULES:
        module_file = MODULES_DIR / f"{module}.json"
        module_data = _load_json(module_file)
        content = normalise_content(module_data.get("content"))

        if not content:
            raise LibraryFileError(f"Module '{module}' has no usable content")

        sections.append(content)
        sections.append("")

    sections.append("OUTPUT FORMAT:")
    sections.append(json.dumps(schema_data, indent=2))

    return "\n".join(sections).strip()
