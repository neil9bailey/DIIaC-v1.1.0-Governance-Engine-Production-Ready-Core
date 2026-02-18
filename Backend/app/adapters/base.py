from abc import ABC, abstractmethod
from typing import Dict, Any


class ExecutionAdapter(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def capabilities(self) -> Dict[str, Any]:
        ...

    @abstractmethod
    def execute(self, request: Dict[str, Any]) -> Dict[str, Any]:
        ...
