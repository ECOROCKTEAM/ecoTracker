from collections.abc import AsyncGenerator
from datetime import datetime, timedelta

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.enum.group.privacy import GroupPrivacyEnum
from src.data.models.group.group import GroupModel
from tests.utils import get_random_str


@pytest_asyncio.fixture(scope="function")
async def fxm_group_default(session: AsyncSession) -> AsyncGenerator[GroupModel, None]:
    model = GroupModel(
        name=get_random_str(),
        description=get_random_str(),
        active=True,
        privacy=GroupPrivacyEnum.PUBLIC,
        code=None,
        code_expire_time=None,
    )
    session.add(model)
    await session.commit()

    yield model

    await session.delete(model)
    await session.commit()


@pytest_asyncio.fixture(scope="function")
async def fxm_group_default_2(session: AsyncSession) -> AsyncGenerator[GroupModel, None]:
    model = GroupModel(
        name=get_random_str(),
        description=get_random_str(),
        active=True,
        privacy=GroupPrivacyEnum.PUBLIC,
        code=None,
        code_expire_time=None,
    )
    session.add(model)
    await session.commit()

    yield model

    await session.delete(model)
    await session.commit()


@pytest_asyncio.fixture(scope="function")
async def fxm_group_with_code(session: AsyncSession) -> AsyncGenerator[GroupModel, None]:
    model = GroupModel(
        name=get_random_str(),
        description=get_random_str(),
        active=True,
        privacy=GroupPrivacyEnum.PUBLIC,
        code=get_random_str(),
        code_expire_time=datetime.utcnow() + timedelta(minutes=5),
    )
    session.add(model)
    await session.commit()

    yield model

    await session.delete(model)
    await session.commit()


@pytest_asyncio.fixture(scope="function")
async def fxm_group_with_code_expired(session: AsyncSession) -> AsyncGenerator[GroupModel, None]:
    model = GroupModel(
        name=get_random_str(),
        description=get_random_str(),
        active=True,
        privacy=GroupPrivacyEnum.PUBLIC,
        code=get_random_str(),
        code_expire_time=datetime.utcnow() - timedelta(minutes=5),
    )
    session.add(model)
    await session.commit()

    yield model

    await session.delete(model)
    await session.commit()
