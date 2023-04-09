from typing import Optional
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncSession
)



class Database:

    def __init__(self, database_url: str, echo: bool = False) -> None:
        self.__url = database_url
        self.__echo = echo
        
        self._session_factory: Optional[async_sessionmaker[AsyncSession]] = None

    @property
    def url(self) -> str:
        return self.__url
    
    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        if self._session_factory is None:
            raise Exception("Database holder not setup!")
        return self._session_factory
    
    @property
    async def session(self) -> AsyncSession: # type: ignore
        async with self.session_factory() as session:
            try:
                yield session
            except:
                await session.rollback()
            finally:
                await session.close()
    
    def _setup(self):
        engine = create_async_engine(
            url=self.__url,
            echo=self.__echo,
        )
        self._session_factory = async_sessionmaker(
            bind=engine,
            expire_on_commit=False,
        )



class Base(DeclarativeBase):
    pass