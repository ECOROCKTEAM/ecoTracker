import pytest

from src.core.entity.mission import MissionUser
from src.core.entity.user import User
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.mission.mission_user_get import MissionUserGetUsecase


# python -m pytest tests/challenges/mission/usecases/user_mission/test_user_get.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    test_user_premium_ru_entity: User,
    test_user_mission_entity: MissionUser,
):
    uc = MissionUserGetUsecase(uow=uow)
    res = await uc(user=test_user_premium_ru_entity, id=test_user_mission_entity.id)
    mission = res.item
    assert isinstance(mission, MissionUser)
    assert test_user_mission_entity.id == mission.id
    assert test_user_mission_entity.user_id == mission.user_id
    assert test_user_mission_entity.mission_id == mission.mission_id
    assert test_user_mission_entity.date_start == mission.date_start
    assert test_user_mission_entity.date_close == mission.date_close
    assert test_user_mission_entity.status == mission.status
