from typing import AsyncGenerator, Tuple

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.enum.language import LanguageEnum
from src.data.models.challenges.occupancy import (
    OccupancyCategoryModel,
    OccupancyCategoryTranslateModel,
)


@pytest_asyncio.fixture(scope="function")
async def category_model(session: AsyncSession) -> AsyncGenerator[OccupancyCategoryModel, None]:
    model = OccupancyCategoryModel()
    session.add(model)
    await session.commit()

    yield model

    await session.delete(model)
    await session.commit()


@pytest_asyncio.fixture(scope="function")
async def category_model_ru(
    session: AsyncSession, category_model: OccupancyCategoryModel
) -> AsyncGenerator[Tuple[OccupancyCategoryModel, OccupancyCategoryTranslateModel], None]:
    lang = LanguageEnum.RU
    translate_model = OccupancyCategoryTranslateModel(
        name=f"f_occupancy_{lang.value}",
        category_id=category_model.id,
        language=lang,
    )
    session.add(translate_model)
    await session.flush()
    await session.refresh(category_model)
    await session.commit()

    yield (category_model, translate_model)

    await session.delete(translate_model)
    await session.commit()


@pytest_asyncio.fixture(scope="function")
async def category_model_en(
    session: AsyncSession, category_model: OccupancyCategoryModel
) -> AsyncGenerator[Tuple[OccupancyCategoryModel, OccupancyCategoryTranslateModel], None]:
    lang = LanguageEnum.EN
    translate_model = OccupancyCategoryTranslateModel(
        name=f"f_occupancy_{lang.value}",
        category_id=category_model.id,
        language=lang,
    )
    session.add(translate_model)
    await session.flush()
    await session.refresh(category_model)
    await session.commit()

    yield (category_model, translate_model)

    await session.delete(translate_model)
    await session.commit()
