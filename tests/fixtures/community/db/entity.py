from collections.abc import AsyncGenerator

import pytest_asyncio

from src.core.entity.community import Community
from src.data.models.community.community import CommunityModel
from src.data.repository.community import model_to_dto
from tests.fixtures.community.db.model import fxm_community_default


@pytest_asyncio.fixture(scope="function")
async def fxe_community_default(fxm_community_default: CommunityModel) -> AsyncGenerator[Community, None]:
    yield model_to_dto(fxm_community_default)
