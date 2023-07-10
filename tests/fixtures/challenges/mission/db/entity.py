from collections.abc import AsyncGenerator

import pytest_asyncio

from src.core.entity.mission import Mission
from src.data.models.challenges.mission import MissionModel, MissionTranslateModel
from src.data.repository.challenges.mission import mission_to_entity
from tests.fixtures.challenges.category.db.entity import fxe_category_default
from tests.fixtures.challenges.mission.db.model import (
    fxm_mission_default,
    fxm_mission_en,
)


@pytest_asyncio.fixture(scope="function")
async def fxe_mission_default(
    fxm_mission_default: tuple[MissionModel, MissionTranslateModel],
) -> AsyncGenerator[Mission, None]:
    mission, translate = fxm_mission_default
    yield mission_to_entity(mission, translate)


@pytest_asyncio.fixture(scope="function")
async def fxe_mission_en(
    fxm_mission_en: tuple[MissionModel, MissionTranslateModel],
) -> AsyncGenerator[Mission, None]:
    mission, translate = fxm_mission_en
    yield mission_to_entity(mission, translate)
