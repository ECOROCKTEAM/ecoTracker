from collections.abc import AsyncGenerator

import pytest_asyncio

from src.core.dto.m2m.user.group import UserGroupDTO
from src.data.models.user.user import UserGroupModel
from src.data.repository.group import user_group_model_to_dto
from tests.fixtures.group.db.user.model import (
    fxm_user_group_default,
    fxm_user_group_superuser,
)


@pytest_asyncio.fixture(scope="function")
async def fxe_user_group_default(
    fxm_user_group_default: UserGroupModel,
) -> AsyncGenerator[UserGroupDTO, None]:
    yield user_group_model_to_dto(fxm_user_group_default)


@pytest_asyncio.fixture(scope="function")
async def fxe_user_group_admin(
    fxm_user_group_default: UserGroupModel,
) -> AsyncGenerator[UserGroupDTO, None]:
    yield user_group_model_to_dto(fxm_user_group_default)


@pytest_asyncio.fixture(scope="function")
async def fxe_user_group_default_2(
    fxm_user_group_superuser: UserGroupModel,
) -> AsyncGenerator[UserGroupDTO, None]:
    yield user_group_model_to_dto(fxm_user_group_superuser)
