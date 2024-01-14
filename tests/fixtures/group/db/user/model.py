from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.enum.group.role import GroupRoleEnum
from src.data.models.group.group import GroupModel
from src.data.models.user.user import UserGroupModel, UserModel
from tests.fixtures.const import DEFAULT_TEST_USER_GROUP_ROLE
from tests.fixtures.group.db.model import fxm_group_default
from tests.fixtures.user.db.model import fxm_user_default, fxm_user_default_2
from tests.utils import get_random_str


@pytest_asyncio.fixture(scope="function")
async def fxm_user_group_default(
    session: AsyncSession,
    fxm_group_default: GroupModel,
    fxm_user_default: UserModel,
) -> AsyncGenerator[UserGroupModel, None]:
    model = UserGroupModel(
        user_id=fxm_user_default.id, group_id=fxm_group_default.id, role=DEFAULT_TEST_USER_GROUP_ROLE
    )
    session.add(model)
    await session.commit()

    yield model

    await session.delete(model)
    await session.commit()


@pytest_asyncio.fixture(scope="function")
async def fxm_user_group_admin(
    session: AsyncSession,
    fxm_group_default: GroupModel,
    fxm_user_default: UserModel,
) -> AsyncGenerator[UserGroupModel, None]:
    model = UserGroupModel(user_id=fxm_user_default.id, group_id=fxm_group_default.id, role=GroupRoleEnum.ADMIN)
    session.add(model)
    await session.commit()

    yield model

    await session.delete(model)
    await session.commit()


@pytest_asyncio.fixture(scope="function")
async def fxm_user_group_superuser(
    session: AsyncSession,
    fxm_group_default: GroupModel,
    fxm_user_default_2: UserModel,
) -> AsyncGenerator[UserGroupModel, None]:
    model = UserGroupModel(user_id=fxm_user_default_2.id, group_id=fxm_group_default.id, role=GroupRoleEnum.SUPERUSER)
    session.add(model)
    await session.commit()

    yield model

    await session.delete(model)
    await session.commit()
