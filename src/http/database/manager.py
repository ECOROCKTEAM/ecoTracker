from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class IDbManager(ABC):
    @property
    @abstractmethod
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        ...

    @abstractmethod
    async def initialize(self, db_url):
        ...

    @abstractmethod
    async def dispose(self):
        ...


class DbManager(IDbManager):
    def __init__(self):
        self._session_factory = None
        self.__engine = None

    @property
    def _engine(self) -> AsyncEngine:
        if self.__engine is None:
            raise NotImplementedError("DbManager is not ready by engine")
        return self.__engine

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        if self._session_factory is None:
            raise NotImplementedError("DbManager is not ready by factory")
        return self._session_factory

    async def initialize(self, db_url):
        self.__engine = create_async_engine(url=db_url)
        # async with self._engine.begin() as conn:
        #     await conn.run_sync(UserModel.metadata.create_all)
        self._session_factory = async_sessionmaker(bind=self._engine, expire_on_commit=False)

    async def dispose(self):
        await self._engine.dispose()


db_manager = DbManager()
