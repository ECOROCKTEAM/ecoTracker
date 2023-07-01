from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.models.challenges.occupancy import (
    OccupancyCategoryModel,
    OccupancyCategoryTranslateModel,
)
from tests.fixtures.const import DEFAULT_TEST_LANGUAGE
from tests.utils import get_random_str


@pytest_asyncio.fixture(scope="function")
async def fxm_category_default(
    session: AsyncSession,
) -> AsyncGenerator[tuple[OccupancyCategoryModel, OccupancyCategoryTranslateModel], None]:
    model = OccupancyCategoryModel()
    session.add(model)
    await session.flush()
    translate = OccupancyCategoryTranslateModel(
        name=get_random_str(), language=DEFAULT_TEST_LANGUAGE, category_id=model.id
    )
    session.add(translate)
    await session.commit()

    yield model, translate

    await session.delete(translate)
    await session.flush()
    await session.delete(model)
    await session.commit()
