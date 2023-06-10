from collections.abc import AsyncGenerator

import pytest_asyncio

from src.core.entity.mission import MissionCommunity
from src.data.models.challenges.mission import CommunityMissionModel
from src.data.repository.challenges.mission import mission_community_to_entity
from tests.fixtures.challenges.category.db.entity import fxe_category_default
from tests.fixtures.challenges.mission.db.model import (
    fxm_mission_default,
    fxm_mission_en,
)


@pytest_asyncio.fixture(scope="function")
async def fxe_community_mission_default(
    fxm_community_mission_default: CommunityMissionModel,
) -> AsyncGenerator[MissionCommunity, None]:
    yield mission_community_to_entity(fxm_community_mission_default)
