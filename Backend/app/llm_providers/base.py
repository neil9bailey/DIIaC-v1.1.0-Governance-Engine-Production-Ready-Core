from abc import ABC, abstractmethod
from typing import Dict, Any


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.

    Design invariants:
    - Providers are optional and external
    - No provider is required for DIIaC operation
    - Providers must be deterministic *given the same inputs*
    - Providers must return structured output + metadata
    """

    name: str

    @abstractmethod
    def generate(self, prompt: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate content from an LLM.

        Must return a dictionary with:
        {
            "content": <structured or unstructured output>,
            "metadata": {
                "provider": <provider name>,
                "model": <model identifier>,
                "parameters": <generation parameters>
            }
        }
        """
        raise NotImplementedError
