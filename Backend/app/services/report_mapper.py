# app/services/report_mapper.py
from typing import Dict, Any

SECTION_MAP = {
    "executive_summary": ["context", "objectives"],
    "strategic_objectives": ["objectives", "success_metrics"],
    "constraints_and_risks": ["constraints", "risks"],
    "strategy_and_roadmap": ["strategy", "roadmap"],
}


def map_ledger_to_sections(output: Dict[str, Any]) -> Dict[str, str]:
    sections: Dict[str, str] = {}

    for section, fields in SECTION_MAP.items():
        content_parts = []
        for field in fields:
            value = output.get(field)
            if value:
                content_parts.append(str(value))

        sections[section] = "\n".join(content_parts).strip()

    return sections
