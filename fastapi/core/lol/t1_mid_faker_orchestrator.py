"""EXAONE 3.5:7.8b 오케스트레이터 — Ollama 백엔드로 exaone3.5:7.8b 모델을 구동한다."""

import os
from functools import lru_cache

from ollama import Client

EXAONE_MODEL = "exaone3.5:7.8b"


@lru_cache
def _get_base_url() -> str:
    return (os.getenv("OLLAMA_BASE_URL") or "http://localhost:11434").strip()


@lru_cache
def get_exaone_client() -> Client:
    return Client(host=_get_base_url())


def generate_reply_exaone(*, message: str, system: str | None = None) -> str:
    client = get_exaone_client()
    messages: list[dict] = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": message})

    response = client.chat(model=EXAONE_MODEL, messages=messages)
    text = (response.message.content or "").strip()
    if not text:
        raise ValueError("EXAONE이 비어 있는 응답을 반환했습니다.")
    return text


__all__ = [
    "EXAONE_MODEL",
    "get_exaone_client",
    "generate_reply_exaone",
]
