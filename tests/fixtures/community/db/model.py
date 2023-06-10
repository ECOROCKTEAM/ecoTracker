from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.enum.community.privacy import CommunityPrivacyEnum
from src.data.models.community.community import CommunityModel
from tests.utils import get_random_str


@pytest_asyncio.fixture(scope="function")
async def fxm_community_default(session: AsyncSession) -> AsyncGenerator[CommunityModel, None]:
    model = CommunityModel(
        name=get_random_str(), description=get_random_str(), active=True, privacy=CommunityPrivacyEnum.PUBLIC
    )
    session.add(model)
    await session.commit()

    yield model

    await session.delete(model)
    await session.commit()
