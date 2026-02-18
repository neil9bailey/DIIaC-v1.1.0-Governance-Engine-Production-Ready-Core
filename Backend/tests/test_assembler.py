import pytest

from app.services.assembler import assemble_prompt
from app.exceptions import (
    RoleNotFoundError,
    InvalidSchemaNameError,
    LibraryFileError,
)


def test_missing_role_raises_error():
    with pytest.raises(RoleNotFoundError):
        assemble_prompt("NonExistentRole", "Test task", "EA_SOLUTION")


def test_invalid_schema_name():
    with pytest.raises(InvalidSchemaNameError):
        assemble_prompt("Enterprise Architect", "Test task", "bad-schema")


def test_valid_prompt_generation():
    result = assemble_prompt(
        "Enterprise Architect",
        "Design a target state architecture",
        "EA_SOLUTION",
    )
    assert "ACT AS:" in result
    assert "OUTPUT FORMAT:" in result


def test_corrupt_role_json_raises_error(tmp_path, monkeypatch):
    from app.services import assembler

    roles = tmp_path / "roles"
    modules = tmp_path / "modules"
    roles.mkdir()
    modules.mkdir()

    (roles / "enterprise_architect.json").write_text("")

    monkeypatch.setattr(assembler, "ROLES_DIR", roles)
    monkeypatch.setattr(assembler, "MODULES_DIR", modules)

    with pytest.raises(LibraryFileError):
        assemble_prompt(
            "Enterprise Architect",
            "Task",
            "EA_SOLUTION",
        )
