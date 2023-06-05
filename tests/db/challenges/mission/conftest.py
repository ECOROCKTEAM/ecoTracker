from typing import AsyncGenerator, Tuple

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.entity.mission import Mission, MissionUser
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.language import LanguageEnum
from src.data.models.challenges.mission import (
    MissionModel,
    MissionTranslateModel,
    UserMissionModel,
)
from src.data.models.challenges.occupancy import (
    OccupancyCategoryModel,
    OccupancyCategoryTranslateModel,
)
from src.data.models.user.user import UserModel
from src.data.repository.challenges.mission import RepositoryMission
from tests.conftest import session


@pytest_asyncio.fixture(scope="function")
async def repo(session: AsyncSession):
    repo = RepositoryMission(session)
    return repo


# Mission

## models


@pytest_asyncio.fixture(scope="function")
async def mission_model_ru(
    session: AsyncSession, category_model_ru: Tuple[OccupancyCategoryModel, OccupancyCategoryTranslateModel]
) -> AsyncGenerator[Tuple[MissionModel, MissionTranslateModel], None]:
    category, _ = category_model_ru
    lang = LanguageEnum.RU
    model = MissionModel(active=True, author="test", score=155, category_id=category.id)
    session.add(model)
    await session.flush()
    translate_model = MissionTranslateModel(
        name=f"f_mission_{lang.value}",
        description="",
        instruction="",
        mission_id=model.id,
        language=lang,
    )
    session.add(translate_model)
    await session.commit()

    yield (model, translate_model)

    await session.delete(translate_model)
    await session.flush()
    await session.delete(model)
    await session.commit()


@pytest_asyncio.fixture(scope="function")
async def mission_model_en(
    session: AsyncSession, category_model_en: Tuple[OccupancyCategoryModel, OccupancyCategoryTranslateModel]
) -> AsyncGenerator[Tuple[MissionModel, MissionTranslateModel], None]:
    category, _ = category_model_en
    lang = LanguageEnum.EN
    model = MissionModel(active=True, author="test", score=155, category_id=category.id)
    session.add(model)
    await session.flush()
    translate_model = MissionTranslateModel(
        name=f"f_mission_{lang.value}",
        description="",
        instruction="",
        mission_id=model.id,
        language=lang,
    )
    session.add(translate_model)
    await session.commit()

    yield (model, translate_model)

    await session.delete(translate_model)
    await session.flush()
    await session.delete(model)
    await session.commit()


## entity
@pytest_asyncio.fixture(scope="function")
async def test_mission_entity_ru(
    mission_model_ru: Tuple[MissionModel, MissionTranslateModel]
) -> AsyncGenerator[Mission, None]:
    mission, translate = mission_model_ru
    yield Mission(
        id=mission.id,
        name=translate.name,
        active=mission.active,
        score=mission.score,
        description=translate.description,
        instruction=translate.instruction,
        category_id=mission.category_id,
        language=translate.language,
    )


@pytest_asyncio.fixture(scope="function")
async def test_mission_entity_en(
    mission_model_en: Tuple[MissionModel, MissionTranslateModel]
) -> AsyncGenerator[Mission, None]:
    mission, translate = mission_model_en
    yield Mission(
        id=mission.id,
        name=translate.name,
        active=mission.active,
        score=mission.score,
        description=translate.description,
        instruction=translate.instruction,
        category_id=mission.category_id,
        language=translate.language,
    )


# UserMission


## models
@pytest_asyncio.fixture(scope="function")
async def test_user_mission_model(
    session: AsyncSession, mission_model_ru: Tuple[MissionModel, MissionTranslateModel], test_user_model: UserModel
) -> AsyncGenerator[Tuple[UserModel, MissionModel, UserMissionModel], None]:
    mission_model, _ = mission_model_ru
    model = UserMissionModel(user_id=test_user_model.id, mission_id=mission_model.id, status=OccupancyStatusEnum.ACTIVE)
    session.add(model)
    await session.commit()

    yield (test_user_model, mission_model, model)

    await session.delete(model)
    await session.commit()


## entity


@pytest_asyncio.fixture(scope="function")
async def test_user_mission_entity(
    test_user_mission_model: Tuple[UserModel, MissionModel, UserMissionModel]
) -> AsyncGenerator[MissionUser, None]:
    user, mission, user_mission = test_user_mission_model
    yield MissionUser(
        id=mission.id,
        user_id=user.id,
        mission_id=mission.id,
        date_start=user_mission.date_start,
        date_close=user_mission.date_close,
        status=user_mission.status,
    )
