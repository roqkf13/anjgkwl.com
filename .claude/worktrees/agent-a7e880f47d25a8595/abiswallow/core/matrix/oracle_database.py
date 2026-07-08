"""Neon PostgreSQL 연결 — FastAPI Depends(get_db)로 세션 주입."""

from __future__ import annotations

from collections.abc import AsyncGenerator
import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

load_dotenv()

_engine: AsyncEngine | None = None
_async_session: async_sessionmaker[AsyncSession] | None = None


def configure_engine(database_url: str | None = None) -> None:
    """DATABASE_URL(Neon postgresql+asyncpg://...) — 앱 시작 시 1회 호출."""
    global _engine, _async_session
    url = (database_url or os.getenv("DATABASE_URL", "")).strip()
    if not url:
        return
    if _engine is not None:
        return

    connect_args: dict[str, object] = {}
    if "+asyncpg" in url:
        # asyncpg는 sslmode/channel_binding 쿼리 문자열을 직접 받지 못하므로
        # URL에서 제거하고 ssl은 connect_args로 전달한다.
        if "sslmode=require" in url:
            connect_args["ssl"] = True
        url = url.replace("?sslmode=require&channel_binding=require", "")
        url = url.replace("&sslmode=require", "").replace("?sslmode=require", "")
        url = url.replace("&channel_binding=require", "").replace(
            "?channel_binding=require", ""
        )

    _engine = create_async_engine(
        url,
        pool_pre_ping=True,
        echo=False,
        connect_args=connect_args,
    )
    _async_session = async_sessionmaker(
        _engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )


def get_engine() -> AsyncEngine | None:
    return _engine


async def dispose_engine() -> None:
    global _engine, _async_session
    if _engine is not None:
        await _engine.dispose()
    _engine = None
    _async_session = None


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI Route에서 Depends(get_db)로 사용."""
    if _async_session is None:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=503,
            detail="DATABASE_URL이 설정되지 않았습니다. .env에 postgresql+asyncpg://... 형식으로 추가하세요.",
        )
    async with _async_session() as session:
        yield session


def import_titanic_metadata():
    """Alembic·create_all용 — Person/Booking ORM을 metadata에 등록."""
    from titanic.adapter.outbound.orm import Base  # noqa: F401
    from titanic.adapter.outbound.orm.booking_orm import Booking  # noqa: F401
    from titanic.adapter.outbound.orm.person_orm import Person  # noqa: F401

    return Base.metadata


async def create_titanic_tables() -> None:
    """Neon에 titanic_person / titanic_booking 테이블 생성."""
    if _engine is None:
        return
    metadata = import_titanic_metadata()
    async with _engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
