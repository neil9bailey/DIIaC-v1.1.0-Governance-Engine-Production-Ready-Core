from pathlib import Path
import pytest

from app.services.assembler import assemble_prompt

GOLDEN_DIR = Path(__file__).parent / "golden"
GOLDEN_DIR.mkdir(exist_ok=True)


@pytest.mark.parametrize(
    "role,task,schema,filename",
    [
        (
            "Enterprise Architect",
            "Design a target state architecture",
            "EA_SOLUTION",
            "EA_SOLUTION.prompt.txt",
        ),
        (
            "CTO",
            "Define a three year technology strategy",
            "CTO_STRATEGY",
            "CTO_STRATEGY.prompt.txt",
        ),
    ],
)
def test_prompt_matches_golden(role, task, schema, filename, request):
    prompt = assemble_prompt(
        role=role,
        task=task,
        schema_name=schema,
    ).strip()

    golden_file = GOLDEN_DIR / filename

    if request.config.getoption("--update-golden"):
        golden_file.write_text(prompt, encoding="utf-8")
        pytest.skip("Golden updated")

    assert golden_file.exists(), "Golden file missing. Run with --update-golden"
    assert prompt == golden_file.read_text(encoding="utf-8").strip()
