import pytest

from src.core.dto.mock import MockObj
from src.core.entity.mission import Mission
from src.core.entity.user import User
from src.core.exception.base import EntityNotActive
from src.core.interfaces.repository.challenges.mission import MissionFilter
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.mission.mission_list import MissionListUsecase


# python -m pytest tests/challenges/mission/usecases/mission/test_list.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    test_user_premium_ru_entity: User,
    test_mission_entity_ru: Mission,
    test_mission_entity_not_active: Mission,
):
    uc = MissionListUsecase(uow=uow)
    res = await uc(
        user=test_user_premium_ru_entity,
        filter_obj=MissionFilter(active=False),
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    # active filter was changed to true
    mission_list = res.item
    assert len(mission_list) == 1
    mission = mission_list[0]
    assert isinstance(mission, Mission)
    assert mission.active is True
    assert test_mission_entity_ru.id == mission.id
    assert test_mission_entity_ru.active == mission.active
