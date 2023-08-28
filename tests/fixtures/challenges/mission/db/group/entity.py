from collections.abc import AsyncGenerator

import pytest_asyncio

from src.core.entity.mission import MissionGroup
from src.data.models.challenges.mission import GroupMissionModel
from src.data.repository.challenges.mission import mission_group_to_entity
from tests.fixtures.challenges.category.db.entity import fxe_category_default
from tests.fixtures.challenges.mission.db.model import (
    fxm_mission_default,
    fxm_mission_en,
)


@pytest_asyncio.fixture(scope="function")
async def fxe_group_mission_default(
    fxm_group_mission_default: GroupMissionModel,
) -> AsyncGenerator[MissionGroup, None]:
    yield mission_group_to_entity(fxm_group_mission_default)
