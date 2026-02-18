from pathlib import Path
import pytest

from app.services.assembler import assemble_prompt

GOLDEN = Path(__file__).parent / "golden"


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
    prompt = assemble_prompt(role, task, schema).strip()
    golden_file = GOLDEN / filename

    update = request.config.getoption("--update-golden")

    if update:
        golden_file.write_text(prompt, encoding="utf-8")
        pytest.skip("Golden updated")

    expected = golden_file.read_text(encoding="utf-8").strip()
    assert prompt == expected
