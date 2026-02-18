from typing import Dict
from app.llm_providers.base import LLMProvider
from app.llm_providers.mock_provider import MockLLMProvider


class LLMProviderRegistry:
    """
    Registry for LLM providers.

    Guarantees:
    - A default provider always exists
    - Providers are resolved by name
    - Core execution logic never imports provider implementations directly
    """

    def __init__(self):
        self._providers: Dict[str, LLMProvider] = {}
        self.register(MockLLMProvider())

    def register(self, provider: LLMProvider) -> None:
        self._providers[provider.name] = provider

    def get(self, name: str) -> LLMProvider:
        if name not in self._providers:
            raise ValueError(f"LLM provider '{name}' is not registered")
        return self._providers[name]


# Global singleton
llm_provider_registry = LLMProviderRegistry()
