import asyncio
from typing import AsyncGenerator

from sqlalchemy.exc import DisconnectionError
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import Config
from src.routers.auth.exceptions import InvalidCredentials

async_engine = create_async_engine(
    url=Config.DATABASE_URL_ASYNC,
    echo=True
)

Session = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False, autoflush=False, autocommit=False
)


async def init_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    while True:
        async with Session() as session:
            try:
                yield session
                return
            except DisconnectionError:
                await session.rollback()
                await asyncio.sleep(5)
                continue



