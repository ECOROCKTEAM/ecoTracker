from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.challenges.mission import MissionUserCreateDTO
from src.core.dto.mock import MockObj
from src.core.entity.mission import Mission, MissionUser
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.exception.base import EntityNotActive
from src.core.interfaces.repository.challenges.mission import MissionUserFilter
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.mission.mission_user_create import (
    MissionUserCreateUsecase,
)
from src.data.models.challenges.mission import UserMissionModel


# python -m pytest tests/challenges/mission/usecases/user_mission/test_user_create.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    session: AsyncSession,
    uow: IUnitOfWork,
    test_user_premium_ru_entity: User,
    test_mission_entity_ru: Mission,
):
    uc = MissionUserCreateUsecase(uow=uow)
    res = await uc(
        user=test_user_premium_ru_entity,
        create_obj=MissionUserCreateDTO(
            mission_id=test_mission_entity_ru.id,
            status=OccupancyStatusEnum.ACTIVE,
        ),
    )
    mission = res.item
    assert isinstance(mission, MissionUser)
    assert mission.id is not None
    assert mission.user_id == test_user_premium_ru_entity.id
    assert mission.mission_id == test_mission_entity_ru.id
    assert isinstance(mission.date_start, datetime)
    assert mission.date_close is None
    assert mission.status == OccupancyStatusEnum.ACTIVE

    async with uow as _uow:
        user_mission_list = await _uow.mission.user_mission_lst(
            user_id=test_user_premium_ru_entity.id,
            filter_obj=MissionUserFilter(),
            order_obj=MockObj(),
            pagination_obj=MockObj(),
        )
        assert len(user_mission_list) == 1

    create_model = await session.get(entity=UserMissionModel, ident={"id": mission.id})
    assert isinstance(create_model, UserMissionModel)
    await session.delete(create_model)
    await session.commit()


# python -m pytest tests/challenges/mission/usecases/user_mission/test_user_create.py::test_not_active -v -s
@pytest.mark.asyncio
async def test_not_active(
    uow: IUnitOfWork,
    test_user_premium_ru_entity: User,
    test_mission_entity_not_active: Mission,
):
    assert test_mission_entity_not_active.active is False
    uc = MissionUserCreateUsecase(uow=uow)
    with pytest.raises(EntityNotActive):
        _ = await uc(
            user=test_user_premium_ru_entity,
            create_obj=MissionUserCreateDTO(
                mission_id=test_mission_entity_not_active.id,
                status=OccupancyStatusEnum.ACTIVE,
            ),
        )
