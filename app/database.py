from pathlib import Path

from sqlalchemy import func
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)

database_url = "sqlite+aiosqlite:///db.sqlite3"
BASE_DIR = Path(__file__).parent.parent
database_path = BASE_DIR / "db.sqlite3"
engine_url = f"sqlite+aiosqlite:///{database_path}"
engine = create_async_engine(url=engine_url)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


class Base(AsyncAttrs, DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
