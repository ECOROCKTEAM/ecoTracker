from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.enum.language import LanguageEnum
from src.data.models.challenges.mission import MissionModel, MissionTranslateModel
from src.data.models.challenges.occupancy import (
    OccupancyCategoryModel,
    OccupancyCategoryTranslateModel,
)
from tests.fixtures.challenges.category.db.model import fxm_category_default
from tests.fixtures.const import DEFAULT_TEST_CHALLENGE_SCORE, DEFAULT_TEST_LANGUAGE
from tests.utils import get_random_str


@pytest_asyncio.fixture(scope="function")
async def fxm_mission_default(
    session: AsyncSession,
    fxm_category_default: tuple[OccupancyCategoryModel, OccupancyCategoryTranslateModel],
) -> AsyncGenerator[tuple[MissionModel, MissionTranslateModel], None]:
    category, _ = fxm_category_default
    model = MissionModel(
        active=True, author=get_random_str(), category_id=category.id, score=DEFAULT_TEST_CHALLENGE_SCORE
    )
    session.add(model)
    await session.flush()
    translate = MissionTranslateModel(
        mission_id=model.id,
        name=get_random_str(),
        description=get_random_str(),
        instruction=get_random_str(),
        language=DEFAULT_TEST_LANGUAGE,
    )
    session.add(translate)
    await session.commit()

    yield model, translate

    await session.delete(translate)
    await session.flush()
    await session.delete(model)
    await session.commit()


@pytest_asyncio.fixture(scope="function")
async def fxm_mission_en(
    session: AsyncSession,
    fxm_category_default: tuple[OccupancyCategoryModel, OccupancyCategoryTranslateModel],
) -> AsyncGenerator[tuple[MissionModel, MissionTranslateModel], None]:
    category, _ = fxm_category_default
    model = MissionModel(
        active=True, author=get_random_str(), category_id=category.id, score=DEFAULT_TEST_CHALLENGE_SCORE
    )
    session.add(model)
    await session.flush()
    translate = MissionTranslateModel(
        mission_id=model.id,
        name=get_random_str(),
        description=get_random_str(),
        instruction=get_random_str(),
        language=LanguageEnum.EN,
    )
    session.add(translate)
    await session.commit()

    yield model, translate

    await session.delete(translate)
    await session.flush()
    await session.delete(model)
    await session.commit()
