from app.adapters.mock_adapter import MockAdapter
from app.adapters.openai_adapter import OpenAIAdapter
from app.adapters.bootstrap_adapter import BootstrapAdapter

ADAPTER_REGISTRY = [
    MockAdapter(),        # ← baseline, credential-free
    BootstrapAdapter(),  # optional bootstrap
    OpenAIAdapter(),     # production only
]

