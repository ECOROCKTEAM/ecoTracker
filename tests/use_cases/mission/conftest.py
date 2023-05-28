from typing import Tuple

import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.core.entity.mission import Mission
from src.core.entity.user import User
from src.core.enum.language import LanguageEnum
from src.data.models.challenges.mission import MissionModel, MissionTranslateModel
from tests.const import MissionT


def build_entity(model: MissionModel, translate: MissionTranslateModel):
    return Mission(
        id=model.id,
        name=translate.name,
        active=model.active,
        score=model.score,
        description=translate.description,
        instruction=translate.instruction,
        category_id=model.category_id,
        language=translate.language,
    )


@pytest_asyncio.fixture(scope="function")
async def test_get_mission_ok(pool: async_sessionmaker[AsyncSession], test_user: User) -> Tuple[User, Mission]:
    lang = LanguageEnum.EN
    mission_id = MissionT.MISSION__ACTIVE.value
    async with pool() as s:
        model = await s.get(MissionModel, {"id": mission_id})
        translate = await s.scalar(
            select(MissionTranslateModel)
            .where(MissionTranslateModel.mission_id == mission_id)
            .where(MissionTranslateModel.language == lang)
        )
    if model is None or translate is None:
        raise RuntimeError("Fixture not ready")
    return test_user, build_entity(model, translate)


@pytest_asyncio.fixture(scope="function")
async def test_get_mission_not_active(pool: async_sessionmaker[AsyncSession], test_user: User) -> Tuple[User, Mission]:
    lang = LanguageEnum.EN
    mission_id = MissionT.MISSION__NOT_ACTIVE.value
    async with pool() as s:
        model = await s.get(MissionModel, {"id": mission_id})
        translate = await s.scalar(
            select(MissionTranslateModel)
            .where(MissionTranslateModel.mission_id == mission_id)
            .where(MissionTranslateModel.language == lang)
        )
    if model is None or translate is None:
        raise RuntimeError("Fixture not ready")
    return test_user, build_entity(model, translate)


@pytest_asyncio.fixture(scope="function")
async def test_get_mission_list_ok(
    pool: async_sessionmaker[AsyncSession], test_user: User
) -> Tuple[User, Mission, Mission]:
    lang = LanguageEnum.EN
    mission_id_active = MissionT.MISSION__ACTIVE.value
    mission_id_not_active = MissionT.MISSION__NOT_ACTIVE.value
    async with pool() as s:
        model_active = await s.get(MissionModel, {"id": mission_id_active})
        translate_active = await s.scalar(
            select(MissionTranslateModel)
            .where(MissionTranslateModel.mission_id == mission_id_active)
            .where(MissionTranslateModel.language == lang)
        )
        model_not_active = await s.get(MissionModel, {"id": mission_id_not_active})
        translate_not_active = await s.scalar(
            select(MissionTranslateModel)
            .where(MissionTranslateModel.mission_id == mission_id_not_active)
            .where(MissionTranslateModel.language == lang)
        )
    if model_active is None or translate_active is None or model_not_active is None or translate_not_active is None:
        raise RuntimeError("Fixture not ready")
    return test_user, build_entity(model_active, translate_active), build_entity(model_not_active, translate_not_active)
