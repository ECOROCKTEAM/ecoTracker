import asyncio
from typing import AsyncGenerator, Generator
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.application.settings import get_settings
from src.application.database.base import create_async_engine, create_session_factory

settings = get_settings()


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
def pool() -> Generator[async_sessionmaker[AsyncSession], None, None]:
    engine = create_async_engine(url=settings.DATABASE_URL)
    factory = create_session_factory(engine=engine)
    yield factory


@pytest_asyncio.fixture(scope="function")
async def session(pool: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
    async with pool() as session:
        yield session
