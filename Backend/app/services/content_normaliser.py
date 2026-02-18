from typing import Any


def normalise_content(content: Any) -> str:
    if isinstance(content, list):
        return "\n".join(
            str(item).strip()
            for item in content
            if isinstance(item, (str, int, float)) and str(item).strip()
        )

    if isinstance(content, str):
        return content.strip()

    return ""
