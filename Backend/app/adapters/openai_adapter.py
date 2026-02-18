import os
import time
from typing import Dict, Any

import requests

from app.adapters.base import ExecutionAdapter


class OpenAIAdapter(ExecutionAdapter):
    """
    OpenAI Responses API adapter (text-only).
    Correctly extracts output_text from raw HTTP Responses API.
    """

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    @property
    def name(self) -> str:
        return "openai-llm"

    @property
    def capabilities(self) -> Dict[str, Any]:
        return {
            "schemas": ["network-design"],
            "roles": ["network-architect", "security-lead", "cto"],
            "modalities": ["text"],
        }

    def execute(self, request: Dict[str, Any]) -> Dict[str, Any]:
        if not self.api_key:
            return {
                "error": "ADAPTER_NOT_CONFIGURED",
                "detail": "OPENAI_API_KEY is not set",
            }

        start = time.time()

        prompt = (
            f"You are acting as a {request['role']}.\n"
            f"Execution schema: {request['schema']}.\n"
            "Be precise, structured, and security-conscious.\n\n"
            f"Intent:\n{request['intent']}\n\n"
            f"Structured Input:\n{request['input']}"
        )

        payload = {
            "model": self.model,
            "input": prompt,
        }

        response = requests.post(
            f"{self.api_base}/responses",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=60,
        )

        if response.status_code != 200:
            return {
                "error": "EXECUTION_FAILED",
                "detail": response.text,
            }

        data = response.json()

        # ✅ Correct extraction for raw Responses API
        try:
            content = data["output"][0]["content"][0]["text"]
        except Exception:
            return {
                "error": "EMPTY_MODEL_RESPONSE",
                "detail": data,
            }

        return {
            "result": content,
            "metadata": {
                "latency_ms": int((time.time() - start) * 1000),
                "model": self.model,
                "response_id": data.get("id"),
            },
        }
