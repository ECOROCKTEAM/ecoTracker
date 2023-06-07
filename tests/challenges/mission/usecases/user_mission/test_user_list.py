import pytest

from src.core.dto.mock import MockObj
from src.core.entity.mission import Mission, MissionUser
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.exception.base import EntityNotActive
from src.core.interfaces.repository.challenges.mission import MissionUserFilter
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.mission.mission_user_list import (
    MissionUserListUsecase,
)


# python -m pytest tests/challenges/mission/usecases/user_mission/test_user_list.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    test_user_premium_ru_entity: User,
    test_user_mission_entity: MissionUser,
):
    assert test_user_mission_entity.status == OccupancyStatusEnum.ACTIVE

    uc = MissionUserListUsecase(uow=uow)
    res = await uc(
        user=test_user_premium_ru_entity,
        filter_obj=MissionUserFilter(),
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    mission_list = res.item
    assert len(mission_list) == 1
    mission = mission_list[0]
    assert isinstance(mission, MissionUser)
    assert mission.id == test_user_mission_entity.id
    assert mission.status == test_user_mission_entity.status

    res = await uc(
        user=test_user_premium_ru_entity,
        filter_obj=MissionUserFilter(mission_id=-1),
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    mission_list = res.item
    assert len(mission_list) == 0

    res = await uc(
        user=test_user_premium_ru_entity,
        filter_obj=MissionUserFilter(status=OccupancyStatusEnum.FINISH),
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    mission_list = res.item
    assert len(mission_list) == 0
