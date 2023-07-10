from collections.abc import AsyncGenerator

import pytest_asyncio

from src.core.dto.community.invite import CommunityInviteDTO
from src.core.entity.community import Community
from src.data.models.community.community import CommunityModel
from src.data.repository.community import model_to_dto, model_to_invite_dto
from tests.fixtures.community.db.model import (
    fxm_community_default,
    fxm_community_default_2,
    fxm_community_with_code,
    fxm_community_with_code_expired,
)


@pytest_asyncio.fixture(scope="function")
async def fxe_community_default(fxm_community_default: CommunityModel) -> AsyncGenerator[Community, None]:
    yield model_to_dto(fxm_community_default)


@pytest_asyncio.fixture(scope="function")
async def fxe_community_default_2(fxm_community_default_2: CommunityModel) -> AsyncGenerator[Community, None]:
    yield model_to_dto(fxm_community_default_2)


@pytest_asyncio.fixture(scope="function")
async def fxe_community_invite_code(
    fxm_community_with_code: CommunityModel,
) -> AsyncGenerator[CommunityInviteDTO, None]:
    yield model_to_invite_dto(fxm_community_with_code)


@pytest_asyncio.fixture(scope="function")
async def fxe_community_invite_code_expired(
    fxm_community_with_code_expired: CommunityModel,
) -> AsyncGenerator[CommunityInviteDTO, None]:
    yield model_to_invite_dto(fxm_community_with_code_expired)
