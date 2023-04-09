from typing import Optional, AsyncIterator
from contextlib import asynccontextmanager
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)

from src.application.settings import get_settings

settings = get_settings()


class Database:
    def __init__(self, database_url: str, echo: bool = False) -> None:
        self.__url = database_url
        self.__echo = echo

        self._session_factory: Optional[async_sessionmaker[AsyncSession]] = None
        self.__engine: Optional[AsyncEngine] = None

    @property
    def url(self) -> str:
        return self.__url

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        if self._session_factory is None:
            raise Exception("Database holder not setup!")
        return self._session_factory

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        async with self.session_factory() as session:
            try:
                yield session
            except:
                await session.rollback()
            finally:
                await session.close()

    @property
    def engine(self) -> AsyncEngine:
        if self.__engine is None:
            raise Exception("Database holder not setup!")
        return self.__engine

    def setup(self):
        self.__engine = create_async_engine(
            url=self.__url,
            echo=self.__echo,
        )
        self._session_factory = async_sessionmaker(
            bind=self.__engine,
            expire_on_commit=False,
        )


class Base(DeclarativeBase):
    __allow_unmapped__ = True
