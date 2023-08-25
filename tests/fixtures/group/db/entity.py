from collections.abc import AsyncGenerator

import pytest_asyncio

from src.core.dto.group.invite import GroupInviteDTO
from src.core.entity.group import Group
from src.data.models.group.group import GroupModel
from src.data.repository.group import model_to_dto, model_to_invite_dto
from tests.fixtures.group.db.model import (
    fxm_group_default,
    fxm_group_default_2,
    fxm_group_with_code,
    fxm_group_with_code_expired,
)


@pytest_asyncio.fixture(scope="function")
async def fxe_group_default(fxm_group_default: GroupModel) -> AsyncGenerator[Group, None]:
    yield model_to_dto(fxm_group_default)


@pytest_asyncio.fixture(scope="function")
async def fxe_group_default_2(fxm_group_default_2: GroupModel) -> AsyncGenerator[Group, None]:
    yield model_to_dto(fxm_group_default_2)


@pytest_asyncio.fixture(scope="function")
async def fxe_group_invite_code(
    fxm_group_with_code: GroupModel,
) -> AsyncGenerator[GroupInviteDTO, None]:
    yield model_to_invite_dto(fxm_group_with_code)


@pytest_asyncio.fixture(scope="function")
async def fxe_group_invite_code_expired(
    fxm_group_with_code_expired: GroupModel,
) -> AsyncGenerator[GroupInviteDTO, None]:
    yield model_to_invite_dto(fxm_group_with_code_expired)
