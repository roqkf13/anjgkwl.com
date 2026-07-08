import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class Settings(BaseModel):
    """환경 변수(.env) 기반 설정. FastAPI Depends(get_settings)로 주입."""

    database_url: str = Field(
        default_factory=lambda: os.getenv("DATABASE_URL", "").strip()
    )
    gemini_api_key: str = Field(
        default_factory=lambda: os.getenv("GEMINI_API_KEY", "").strip()
    )
    nexus_api_key: str = Field(
        default_factory=lambda: os.getenv("NEXUS_API_KEY", "").strip()
    )
    steam_api_key: str = Field(
        default_factory=lambda: os.getenv("STEAM_API_KEY", "").strip()
    )
    ollama_base_url: str = Field(
        default_factory=lambda: os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").strip()
    )
    ollama_model: str = Field(
        default_factory=lambda: os.getenv("OLLAMA_MODEL", "llama3.2").strip()
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
