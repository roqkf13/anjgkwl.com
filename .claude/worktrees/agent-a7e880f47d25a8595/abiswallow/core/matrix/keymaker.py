"""GEMINI_API_KEY 및 Gemini 클라이언트 설정."""

from functools import lru_cache
from pathlib import Path

import google.generativeai as genai
from dotenv import load_dotenv

_BACKEND_ROOT = Path(__file__).resolve().parents[3]
_ENV_PATH = _BACKEND_ROOT / ".env"

load_dotenv(_ENV_PATH)

DEFAULT_GEMINI_MODEL = "gemini-3.1-flash-lite"


@lru_cache
def get_gemini_api_key() -> str:
    import os

    return (os.getenv("GEMINI_API_KEY") or "").strip()


@lru_cache
def get_gemini_model_name() -> str:
    import os

    return (os.getenv("GEMINI_MODEL") or DEFAULT_GEMINI_MODEL).strip()


def is_gemini_configured() -> bool:
    return bool(get_gemini_api_key())


def configure_gemini() -> None:
    """google-generativeai 전역 API 키 설정."""
    api_key = get_gemini_api_key()
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY 가 설정되지 않았습니다. "
            f"{_ENV_PATH} 파일을 확인하세요."
        )
    genai.configure(api_key=api_key)


def get_generative_model():
    """설정된 API 키로 GenerativeModel 인스턴스를 반환."""
    configure_gemini()
    return genai.GenerativeModel(get_gemini_model_name())


def to_gemini_history(messages: list[dict]) -> list[dict]:
    """user/assistant 메시지 목록을 Gemini chat history 형식으로 변환."""
    history: list[dict] = []
    for msg in messages:
        role = msg.get("role")
        text = (msg.get("text") or "").strip()
        if not text:
            continue
        history.append(
            {
                "role": "model" if role == "assistant" else "user",
                "parts": [{"text": text}],
            }
        )
    return history


def generate_reply(*, message: str | None = None, history: list[dict] | None = None) -> str:
    """
    단일 message 또는 history + 마지막 user 메시지로 Gemini 응답 텍스트를 생성.
    history 가 있으면 마지막 항목은 user 여야 한다.
    """
    model = get_generative_model()

    if history:
        prior = history[:-1]
        last = history[-1]
        if last.get("role") != "user":
            raise ValueError("마지막 메시지는 user 여야 합니다.")
        last_text = (last.get("text") or "").strip()
        if not last_text:
            raise ValueError("마지막 사용자 메시지가 비어 있습니다.")

        chat = model.start_chat(history=to_gemini_history(prior))
        response = chat.send_message(last_text)
    else:
        if not message or not message.strip():
            raise ValueError("message 가 필요합니다.")
        response = model.generate_content(message.strip())

    try:
        text = (response.text or "").strip()
    except ValueError as e:
        raise ValueError("응답을 가져올 수 없습니다(안전 필터 등).") from e

    if not text:
        raise ValueError("모델이 비어 있는 응답을 반환했습니다.")

    return text
