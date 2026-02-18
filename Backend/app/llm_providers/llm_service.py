from typing import Dict, Any
from app.llm_providers.registry import llm_provider_registry


def generate_from_llm(
    prompt: str,
    provider_name: str,
    parameters: Dict[str, Any],
    trusted: bool,
) -> Dict[str, Any]:
    """
    Generate content from an LLM provider.

    Important:
    - This function does NOT perform execution
    - Trust is declared by the caller
    - Returned metadata must be persisted if used in execution
    """

    provider = llm_provider_registry.get(provider_name)

    result = provider.generate(prompt=prompt, parameters=parameters)

    return {
        "content": result["content"],
        "source": {
            "type": "llm",
            "provider": result["metadata"]["provider"],
            "model": result["metadata"]["model"],
            "parameters": result["metadata"]["parameters"],
            "trusted": trusted,
        },
    }
