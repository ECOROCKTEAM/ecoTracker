from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.models.challenges.mission import (
    GroupMissionModel,
    MissionModel,
    MissionTranslateModel,
)
from src.data.models.user.user import UserGroupModel
from tests.fixtures.challenges.mission.db.model import fxm_mission_default
from tests.fixtures.const import DEFAULT_TEST_OCCUPANCY_STATUS
from tests.fixtures.group.db.user.model import fxm_user_group_default
from tests.fixtures.user.db.model import fxm_user_default
from tests.utils import get_random_str


@pytest_asyncio.fixture(scope="function")
async def fxm_group_mission_default(
    session: AsyncSession,
    fxm_user_group_default: UserGroupModel,
    fxm_mission_default: tuple[MissionModel, MissionTranslateModel],
) -> AsyncGenerator[GroupMissionModel, None]:
    mission, _ = fxm_mission_default
    model = GroupMissionModel(
        group_id=fxm_user_group_default.group_id,
        mission_id=mission.id,
        author=get_random_str(),
        status=DEFAULT_TEST_OCCUPANCY_STATUS,
    )
    session.add(model)
    await session.commit()

    yield model

    await session.delete(model)
    await session.commit()
