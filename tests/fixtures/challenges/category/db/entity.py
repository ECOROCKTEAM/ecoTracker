from collections.abc import AsyncGenerator

import pytest_asyncio

from src.core.entity.occupancy import OccupancyCategory
from src.data.models.challenges.occupancy import (
    OccupancyCategoryModel,
    OccupancyCategoryTranslateModel,
)
from src.data.repository.challenges.occupancy_category import occupancy_model_to_entity
from tests.fixtures.challenges.category.db.model import fxm_category_default


@pytest_asyncio.fixture(scope="function")
async def fxe_category_default(
    fxm_category_default: tuple[OccupancyCategoryModel, OccupancyCategoryTranslateModel]
) -> AsyncGenerator[OccupancyCategory, None]:
    _, translate = fxm_category_default
    yield occupancy_model_to_entity(translate)
