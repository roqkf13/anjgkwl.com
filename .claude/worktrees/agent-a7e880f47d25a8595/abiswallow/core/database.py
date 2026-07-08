"""Neon DB — core.matrix.oracle_database 단일 구현."""

from __future__ import annotations

from core.config import get_settings
from core.matrix.oracle_database import (
    configure_engine,
    create_titanic_tables,
    dispose_engine,
    get_db,
    get_engine,
    import_titanic_metadata,
)

__all__ = [
    "configure_engine",
    "create_all_tables",
    "create_titanic_tables",
    "dispose_engine",
    "get_db",
    "get_engine",
    "get_sqlmodel_session",
    "import_titanic_metadata",
    "init_engine",
]

get_sqlmodel_session = get_db


def init_engine(database_url: str | None = None) -> None:
    url = (database_url or get_settings().database_url).strip()
    configure_engine(url or None)


async def create_all_tables() -> None:
    await create_titanic_tables()
