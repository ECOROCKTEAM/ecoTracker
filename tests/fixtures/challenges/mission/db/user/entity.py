from collections.abc import AsyncGenerator

import pytest_asyncio

from src.core.entity.mission import MissionUser
from src.data.models.challenges.mission import UserMissionModel
from src.data.repository.challenges.mission import mission_user_to_entity
from tests.fixtures.challenges.category.db.entity import fxe_category_default
from tests.fixtures.challenges.mission.db.model import (
    fxm_mission_default,
    fxm_mission_en,
)


@pytest_asyncio.fixture(scope="function")
async def fxe_user_mission_default(
    fxm_user_mission_default: UserMissionModel,
) -> AsyncGenerator[MissionUser, None]:
    yield mission_user_to_entity(fxm_user_mission_default)
