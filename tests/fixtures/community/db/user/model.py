from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.enum.community.role import CommunityRoleEnum
from src.data.models.community.community import CommunityModel
from src.data.models.user.user import UserCommunityModel, UserModel
from src.http.api.community.models.community_role import CommunityRole
from tests.fixtures.community.db.model import fxm_community_default
from tests.fixtures.const import DEFAULT_TEST_USER_COMMUNITY_ROLE
from tests.fixtures.user.db.model import fxm_user_default, fxm_user_default_2
from tests.utils import get_random_str


@pytest_asyncio.fixture(scope="function")
async def fxm_user_community_default(
    session: AsyncSession,
    fxm_community_default: CommunityModel,
    fxm_user_default: UserModel,
) -> AsyncGenerator[UserCommunityModel, None]:
    model = UserCommunityModel(
        user_id=fxm_user_default.id, community_id=fxm_community_default.id, role=DEFAULT_TEST_USER_COMMUNITY_ROLE
    )
    session.add(model)
    await session.commit()

    yield model

    await session.delete(model)
    await session.commit()


@pytest_asyncio.fixture(scope="function")
async def fxm_user_community_admin(
    session: AsyncSession,
    fxm_community_default: CommunityModel,
    fxm_user_default: UserModel,
) -> AsyncGenerator[UserCommunityModel, None]:
    model = UserCommunityModel(
        user_id=fxm_user_default.id, community_id=fxm_community_default.id, role=CommunityRoleEnum.ADMIN
    )
    session.add(model)
    await session.commit()

    yield model

    await session.delete(model)
    await session.commit()


@pytest_asyncio.fixture(scope="function")
async def fxm_user_community_superuser(
    session: AsyncSession,
    fxm_community_default: CommunityModel,
    fxm_user_default_2: UserModel,
) -> AsyncGenerator[UserCommunityModel, None]:
    model = UserCommunityModel(
        user_id=fxm_user_default_2.id, community_id=fxm_community_default.id, role=CommunityRoleEnum.SUPERUSER
    )
    session.add(model)
    await session.commit()

    yield model

    await session.delete(model)
    await session.commit()
