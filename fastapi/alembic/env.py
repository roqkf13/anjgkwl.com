from __future__ import annotations

import asyncio
import os
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

_backend = Path(__file__).resolve().parent.parent
_apps = _backend / "apps"
for path in (_backend, _apps):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

load_dotenv(_backend / ".env")
load_dotenv(_apps / ".env")

from core.matrix.grid_oracle_database_manager import import_titanic_metadata  # noqa: E402

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = import_titanic_metadata()

database_url = (os.getenv("DATABASE_URL") or "").strip()
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    url = config.get_main_option("sqlalchemy.url") or ""
    connect_args: dict = {}
    if "+asyncpg" in url:
        if "sslmode=require" in url:
            connect_args["ssl"] = True
        url = url.replace("?sslmode=require&channel_binding=require", "")
        url = url.replace("&sslmode=require", "").replace("?sslmode=require", "")
        url = url.replace("&channel_binding=require", "").replace("?channel_binding=require", "")
        config.set_main_option("sqlalchemy.url", url)

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        connect_args=connect_args,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
