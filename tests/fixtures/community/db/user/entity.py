from collections.abc import AsyncGenerator

import pytest_asyncio

from src.core.dto.m2m.user.community import UserCommunityDTO
from src.data.models.user.user import UserCommunityModel
from src.data.repository.community import user_community_model_to_dto
from tests.fixtures.community.db.user.model import (
    fxm_user_community_default,
    fxm_user_community_superuser,
)


@pytest_asyncio.fixture(scope="function")
async def fxe_user_community_default(
    fxm_user_community_default: UserCommunityModel,
) -> AsyncGenerator[UserCommunityDTO, None]:
    yield user_community_model_to_dto(fxm_user_community_default)


@pytest_asyncio.fixture(scope="function")
async def fxe_user_community_admin(
    fxm_user_community_default: UserCommunityModel,
) -> AsyncGenerator[UserCommunityDTO, None]:
    yield user_community_model_to_dto(fxm_user_community_default)


@pytest_asyncio.fixture(scope="function")
async def fxe_user_community_default_2(
    fxm_user_community_superuser: UserCommunityModel,
) -> AsyncGenerator[UserCommunityDTO, None]:
    yield user_community_model_to_dto(fxm_user_community_superuser)
