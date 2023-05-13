from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


def build_engine(url: str, echo: bool = False) -> AsyncEngine:
    return create_async_engine(
        url=url,
        echo=echo,
    )


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False,
    )


class Base(DeclarativeBase):
    __allow_unmapped__ = True
