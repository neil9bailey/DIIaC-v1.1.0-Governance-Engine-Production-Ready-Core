from app.adapters.base import ExecutionAdapter


class MockAdapter(ExecutionAdapter):

    @property
    def name(self) -> str:
        return "mock-adapter"

    @property
    def capabilities(self):
        return {
            "schemas": ["network-design"],
            "roles": ["network-architect"]
        }

    def execute(self, request):
        return {
            "result": f"Mock execution for intent: {request['intent']}",
            "metadata": {
                "latency_ms": 5,
                "tokens": 0
            }
        }
