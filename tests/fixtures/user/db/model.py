from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.models.user.user import UserModel
from tests.fixtures.const import DEFAULT_TEST_LANGUAGE
from tests.utils import get_random_str


@pytest_asyncio.fixture(scope="function")
async def fxm_user_default(session: AsyncSession) -> AsyncGenerator[UserModel, None]:
    model = UserModel(id="1", username=get_random_str(), active=True, language=DEFAULT_TEST_LANGUAGE)
    session.add(model)
    await session.commit()

    yield model

    await session.delete(model)
    await session.commit()


@pytest_asyncio.fixture(scope="function")
async def fxm_user_default_2(session: AsyncSession) -> AsyncGenerator[UserModel, None]:
    model = UserModel(id="2", username=get_random_str(), active=True, language=DEFAULT_TEST_LANGUAGE)
    session.add(model)
    await session.commit()

    yield model

    await session.delete(model)
    await session.commit()


@pytest_asyncio.fixture(scope="function")
async def fxm_user_not_active(session: AsyncSession) -> AsyncGenerator[UserModel, None]:
    model = UserModel(id="3", username=get_random_str(), active=False, language=DEFAULT_TEST_LANGUAGE)
    session.add(model)
    await session.commit()

    yield model

    await session.delete(model)
    await session.commit()


@pytest_asyncio.fixture(scope="function")
async def fxm_user_default_3(session: AsyncSession) -> AsyncGenerator[UserModel, None]:
    model = UserModel(id="aboba_id", username="test", active=True, language=DEFAULT_TEST_LANGUAGE)
    session.add(model)
    await session.commit()

    yield model

    await session.delete(model)
    await session.commit()
