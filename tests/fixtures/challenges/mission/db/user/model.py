from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.models.challenges.mission import (
    MissionModel,
    MissionTranslateModel,
    UserMissionModel,
)
from src.data.models.user.user import UserModel
from tests.fixtures.challenges.mission.db.model import fxm_mission_default
from tests.fixtures.const import DEFAULT_TEST_OCCUPANCY_STATUS
from tests.fixtures.user.db.model import fxm_user_default


@pytest_asyncio.fixture(scope="function")
async def fxm_user_mission_default(
    session: AsyncSession,
    fxm_user_default: UserModel,
    fxm_mission_default: tuple[MissionModel, MissionTranslateModel],
) -> AsyncGenerator[UserMissionModel, None]:
    mission, _ = fxm_mission_default
    model = UserMissionModel(user_id=fxm_user_default.id, mission_id=mission.id, status=DEFAULT_TEST_OCCUPANCY_STATUS)
    session.add(model)
    await session.commit()

    yield model

    await session.delete(model)
    await session.commit()
