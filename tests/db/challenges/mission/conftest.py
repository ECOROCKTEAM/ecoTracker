from typing import AsyncGenerator, Tuple

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.entity.mission import Mission, MissionCommunity, MissionUser
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.language import LanguageEnum
from src.data.models.challenges.mission import (
    CommunityMissionModel,
    MissionModel,
    MissionTranslateModel,
    UserMissionModel,
)
from src.data.models.challenges.occupancy import (
    OccupancyCategoryModel,
    OccupancyCategoryTranslateModel,
)
from src.data.models.community.community import CommunityModel
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
async def test_mission_model_ru(
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
async def test_mission_model_en(
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
    test_mission_model_ru: Tuple[MissionModel, MissionTranslateModel]
) -> AsyncGenerator[Mission, None]:
    mission, translate = test_mission_model_ru
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
    test_mission_model_en: Tuple[MissionModel, MissionTranslateModel]
) -> AsyncGenerator[Mission, None]:
    mission, translate = test_mission_model_en
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
    session: AsyncSession, test_mission_model_ru: Tuple[MissionModel, MissionTranslateModel], test_user_model: UserModel
) -> AsyncGenerator[Tuple[UserModel, MissionModel, UserMissionModel], None]:
    mission_model, _ = test_mission_model_ru
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
    _, _, user_mission = test_user_mission_model
    yield MissionUser(
        id=user_mission.id,
        user_id=user_mission.user_id,
        mission_id=user_mission.mission_id,
        date_start=user_mission.date_start,
        date_close=user_mission.date_close,
        status=user_mission.status,
    )


# CommunityMission

## models


@pytest_asyncio.fixture(scope="function")
async def test_community_mission_model(
    session: AsyncSession,
    test_mission_model_ru: Tuple[MissionModel, MissionTranslateModel],
    test_community_model: CommunityModel,
) -> AsyncGenerator[Tuple[CommunityModel, MissionModel, CommunityMissionModel], None]:
    mission_model, _ = test_mission_model_ru
    model = CommunityMissionModel(
        community_id=test_community_model.id, mission_id=mission_model.id, author="t", status=OccupancyStatusEnum.ACTIVE
    )
    session.add(model)
    await session.commit()

    yield (test_community_model, mission_model, model)

    await session.delete(model)
    await session.commit()


## entity


@pytest_asyncio.fixture(scope="function")
async def test_community_mission_entity(
    test_community_mission_model: Tuple[CommunityModel, MissionModel, CommunityMissionModel]
) -> AsyncGenerator[MissionCommunity, None]:
    _, _, community_mission = test_community_mission_model
    yield MissionCommunity(
        id=community_mission.id,
        community_id=community_mission.community_id,
        mission_id=community_mission.mission_id,
        author=community_mission.author,
        date_start=community_mission.date_start,
        date_close=community_mission.date_close,
        status=community_mission.status,
    )
