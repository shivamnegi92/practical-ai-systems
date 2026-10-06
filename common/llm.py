"""One small provider interface for every system.

Default is offline: systems ship a deterministic baseline and only call a model
when PAS_LLM is set. Supported providers:

* ``ollama`` - local model server (PAS_MODEL, default ``llama3.2:3b``)
* ``openai`` - any OpenAI-compatible endpoint (PAS_BASE_URL, PAS_API_KEY, PAS_MODEL)

Tests use ``StubLLM`` and never touch the network.
"""
from __future__ import annotations

import json
import os
import re
import urllib.request
from typing import Callable, Protocol


class LLM(Protocol):
    def complete(self, prompt: str, system: str = "") -> str: ...


class StubLLM:
    """Deterministic fake: maps prompt -> response with a function."""

    def __init__(self, responder: Callable[[str], str]):
        self.responder = responder
        self.calls: list[str] = []

    def complete(self, prompt: str, system: str = "") -> str:
        self.calls.append(prompt)
        return self.responder(prompt)


class _HTTPLLM:
    def __init__(self, url: str, model: str, headers: dict[str, str] | None = None, timeout: int = 120):
        self.url, self.model, self.timeout = url, model, timeout
        self.headers = {"Content-Type": "application/json", **(headers or {})}

    def _post(self, payload: dict) -> dict:
        req = urllib.request.Request(self.url, json.dumps(payload).encode(), self.headers)
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            return json.load(resp)


class OllamaLLM(_HTTPLLM):
    def __init__(self, model: str, host: str = "http://localhost:11434"):
        super().__init__(f"{host}/api/generate", model)

    def complete(self, prompt: str, system: str = "") -> str:
        body = {"model": self.model, "prompt": prompt, "system": system, "stream": False, "options": {"temperature": 0}}
        return self._post(body)["response"]


class OpenAICompatibleLLM(_HTTPLLM):
    def __init__(self, model: str, base_url: str, api_key: str):
        super().__init__(f"{base_url.rstrip('/')}/chat/completions", model, {"Authorization": f"Bearer {api_key}"})

    def complete(self, prompt: str, system: str = "") -> str:
        messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
        body = {"model": self.model, "messages": messages, "temperature": 0}
        return self._post(body)["choices"][0]["message"]["content"]


def from_env(provider: str | None = None) -> LLM | None:
    """Return the configured provider, or None to use the offline baseline."""
    provider = (provider if provider is not None else os.getenv("PAS_LLM", "")).strip().lower()
    model = os.getenv("PAS_MODEL", "llama3.2:3b")
    if not provider:
        return None
    if provider == "ollama":
        return OllamaLLM(model, os.getenv("OLLAMA_HOST", "http://localhost:11434"))
    if provider == "openai":
        return OpenAICompatibleLLM(model, os.environ["PAS_BASE_URL"], os.environ["PAS_API_KEY"])
    raise ValueError(f"unknown PAS_LLM provider: {provider!r} (use 'ollama' or 'openai')")


def parse_json(text: str):
    """Pull the first JSON object out of a model reply; None if absent/invalid."""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return None
