from typing import Optional, AsyncIterator
from contextlib import asynccontextmanager
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)

def build_engine(url: str, echo: bool = False) -> AsyncEngine:
    return create_async_engine(
        url=url,
        echo=echo,
    )

def build_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False,
    )




class Base(DeclarativeBase):
    __allow_unmapped__ = True
