from pathlib import Path
from app.services.assembler import assemble_prompt

GOLDEN = Path(__file__).parent / "golden"

def test_enterprise_architect_ea_solution_prompt_is_stable():
    expected = (GOLDEN / "enterprise_architect_ea_solution.txt").read_text().strip()

    actual = assemble_prompt(
        role="Enterprise Architect",
        task="Design a target state architecture",
        schema_name="EA_SOLUTION",
    ).strip()

    assert actual == expected
