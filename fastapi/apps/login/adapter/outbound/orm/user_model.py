from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Friday13thUser(Base):
    __tablename__ = "friday13th_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role: Mapped[str] = mapped_column(String(32), nullable=False, default="user")
    provider: Mapped[str] = mapped_column(String(32), nullable=False, default="local")
    oauth_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
