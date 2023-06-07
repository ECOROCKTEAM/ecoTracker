from datetime import datetime

import pytest
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.challenges.mission import MissionUserUpdateDTO
from src.core.entity.mission import MissionUser
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.exception.base import EntityNotChange
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.mission.mission_user_update import (
    MissionUserUpdateUsecase,
)
from src.data.models.challenges.mission import UserMissionModel
from src.data.models.user.user import UserScoreModel


# python -m pytest tests/challenges/mission/usecases/user_mission/test_user_update.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    session: AsyncSession,
    uow: IUnitOfWork,
    test_user_premium_ru_entity: User,
    test_user_mission_entity: MissionUser,
):
    uc = MissionUserUpdateUsecase(uow=uow)
    res = await uc(
        user=test_user_premium_ru_entity,
        id=test_user_mission_entity.id,
        update_obj=MissionUserUpdateDTO(status=OccupancyStatusEnum.FINISH),
    )
    mission = res.item
    assert isinstance(mission, MissionUser)
    assert test_user_mission_entity.id == mission.id
    assert test_user_mission_entity.user_id == mission.user_id
    assert test_user_mission_entity.mission_id == mission.mission_id
    assert test_user_mission_entity.date_start == mission.date_start
    assert test_user_mission_entity.date_close != mission.date_close
    assert test_user_mission_entity.status != mission.status
    assert isinstance(mission.date_close, datetime)
    assert mission.status == OccupancyStatusEnum.FINISH

    # check score
    async with uow as _uow:
        base_mission = await uow.mission.get(
            id=test_user_mission_entity.mission_id, lang=test_user_premium_ru_entity.language
        )
        user_score = await _uow.score_user.user_get(
            user_id=test_user_premium_ru_entity.id,
        )
        assert user_score.value == base_mission.score
        assert base_mission.id == test_user_mission_entity.mission_id

    await session.execute(delete(UserScoreModel).where(UserScoreModel.user_id == test_user_premium_ru_entity.id))
    await session.commit()


# python -m pytest tests/challenges/mission/usecases/user_mission/test_user_update.py::test_not_change -v -s
@pytest.mark.asyncio
async def test_not_change(
    uow: IUnitOfWork,
    test_user_premium_ru_entity: User,
    test_user_mission_entity: MissionUser,
):
    uc = MissionUserUpdateUsecase(uow=uow)
    res = await uc(
        user=test_user_premium_ru_entity,
        id=test_user_mission_entity.id,
        update_obj=MissionUserUpdateDTO(status=OccupancyStatusEnum.REJECT),
    )
    mission = res.item
    assert isinstance(mission, MissionUser)
    assert mission.status == OccupancyStatusEnum.REJECT

    with pytest.raises(EntityNotChange):
        await uc(
            user=test_user_premium_ru_entity,
            id=test_user_mission_entity.id,
            update_obj=MissionUserUpdateDTO(status=OccupancyStatusEnum.ACTIVE),
        )
