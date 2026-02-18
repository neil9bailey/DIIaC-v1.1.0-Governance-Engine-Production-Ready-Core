from pathlib import Path
import json

OVERLAY_DIR = (
    Path(__file__).resolve().parent.parent / "library" / "overlays"
)


def load_overlays(
    vendors: list[str] | None = None,
    security: list[str] | None = None,
) -> list[str]:
    """
    Load vendor and security overlays as formatted sections.
    """
    sections: list[str] = []

    vendors = vendors or []
    security = security or []

    for vendor in vendors:
        path = OVERLAY_DIR / "vendors" / f"{vendor}.json"
        if path.exists():
            sections.append(_format_overlay(path))

    for sec in security:
        path = OVERLAY_DIR / "security" / f"{sec}.json"
        if path.exists():
            sections.append(_format_overlay(path))

    return sections


def _format_overlay(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    lines = "\n".join(f"- {item}" for item in data.get("content", []))
    return f"{data.get('section', 'OVERLAY')}:\n{lines}"
