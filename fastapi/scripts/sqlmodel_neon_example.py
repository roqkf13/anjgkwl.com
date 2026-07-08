"""
SQLModel Hero 예제 스타일 — Neon PostgreSQL 비동기 버전.

실행:
  cd backend
  python scripts/sqlmodel_neon_example.py
"""
import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

_BACKEND_DIR = Path(__file__).resolve().parent.parent
_APPS_DIR = _BACKEND_DIR / "apps"
sys.path.insert(0, str(_APPS_DIR))

load_dotenv(_BACKEND_DIR / ".env")

from core.config import get_settings  # noqa: E402
from secom.app.models.user_entity import User  # noqa: E402


async def main() -> None:
    settings = get_settings()
    if not settings.database_url:
        raise RuntimeError("backend/.env 에 DATABASE_URL 을 설정하세요.")

    engine = create_async_engine(settings.database_url, echo=True, pool_pre_ping=True)

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(engine) as session:
        demo_email = "sqlmodel-demo@example.com"
        found = await session.exec(select(User).where(User.email == demo_email))
        if found.first() is None:
            user_1 = User(
                user_id=demo_email,
                email=demo_email,
                name="Spider-Boy",
                password_hash="demo-hash",
                role="user",
                age=30,
            )
            user_2 = User(
                user_id="rusty@example.com",
                email="rusty@example.com",
                name="Rusty-Man",
                password_hash="demo-hash",
                role="user",
                age=48,
            )
            session.add(user_1)
            session.add(user_2)
            await session.commit()
            await session.refresh(user_1)
            print(f"생성된 유저: {user_1.name} (ID: {user_1.id})")

        result = await session.exec(select(User).where(User.age >= 20))
        for u in result.all():
            print(f"조회된 유저: {u.name} ({u.age}세) email={u.email}")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
