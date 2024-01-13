import asyncio
from typing import AsyncGenerator

import faker
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.application.auth.firebase import FirebaseApplication
from src.application.database.base import (
    Base,
    create_async_engine,
    create_session_factory,
)
from src.application.settings import settings
from src.core.interfaces.auth.firebase import IFirebaseApplication
from src.core.interfaces.repository.auth import IAuthProviderRepository
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.data.repository.auth import AuthProviderRepository
from src.data.unit_of_work import SqlAlchemyUnitOfWork
from tests.dataloader import dataloader

fake = faker.Faker()


def get_request_param(request, wait_type):
    if not hasattr(request, "param"):
        return
    if request.param is None and wait_type is None:
        return request.param
    if request.param is not None and isinstance(request.param, wait_type):
        return request.param
    raise NotImplementedError(f"Fail with request param: {request.param}")


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop

    # pending = asyncio.tasks.all_tasks(loop)
    # loop.run_until_complete(asyncio.gather(*pending))
    # loop.run_until_complete(asyncio.sleep(1))

    loop.close()


@pytest.fixture(scope="function")
def firebase_app(request) -> IFirebaseApplication:
    app = FirebaseApplication(name=settings.FIREBASE_APP_NAME, secret_path=settings.FIREBASE_SECRET_PATH)
    app.setup()
    params: dict | None = get_request_param(request=request, wait_type=dict)
    if params is None:
        return app
    if params.get("mock_verify_token"):
        app.verify_token = params.get("mock_verify_token")  # type: ignore
    return app


@pytest.fixture(scope="function")
def auth_provider_repository(firebase_app: IFirebaseApplication) -> IAuthProviderRepository:
    return AuthProviderRepository(firebase_app=firebase_app)


@pytest_asyncio.fixture(scope="package")
@pytest.mark.asyncio
async def pool() -> AsyncGenerator[async_sessionmaker[AsyncSession], None]:
    print(settings.DATABASE_URL, flush=True)
    engine = create_async_engine(url=settings.DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    factory = create_session_factory(engine=engine)
    yield factory


@pytest_asyncio.fixture(scope="function")
async def session(pool: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
    async with pool() as session:
        yield session
        await session.close()


@pytest_asyncio.fixture(scope="function")
async def uow(pool: async_sessionmaker[AsyncSession]) -> AsyncGenerator[IUnitOfWork, None]:
    yield SqlAlchemyUnitOfWork(pool)


@pytest_asyncio.fixture(scope="function")
async def dl(session: AsyncSession):
    async with dataloader(session=session) as dl:
        yield dl
