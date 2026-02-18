from app.execution.registry.adapter_registry import AdapterRegistry
from app.adapters.openai_adapter import OpenAIAdapter


def register_adapters(registry: AdapterRegistry) -> None:
    """
    Register all execution adapters.

    v1.x rules:
    - Explicit registration only
    - No auto-discovery
    - No conditional logic
    """
    registry.register(OpenAIAdapter())
