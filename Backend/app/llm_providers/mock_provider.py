from typing import Dict, Any
from app.llm_providers.base import LLMProvider


class MockLLMProvider(LLMProvider):
    """
    Deterministic mock LLM provider.

    This is the DEFAULT provider.
    It makes no external calls and always returns
    the same output for the same prompt.
    """

    name = "mock"

    def generate(self, prompt: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "content": {
                "text": prompt
            },
            "metadata": {
                "provider": self.name,
                "model": "mock-model",
                "parameters": parameters
            }
        }
