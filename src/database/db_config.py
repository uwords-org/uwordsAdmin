from fastapi import Depends
from datetime import datetime
from typing import AsyncGenerator
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Boolean, TIMESTAMP
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase

from src.utils.instance import DATABASE_URL


Base = declarative_base()
engine = create_async_engine(
    DATABASE_URL, future=True
)

async_session_maker: AsyncSession = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Admin(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "admin"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(length=128), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    created_at = mapped_column(TIMESTAMP, default=datetime.now)

    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_admin_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, Admin)