import pytest

from src.core.entity.mission import MissionUser
from src.core.entity.user import User
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.mission.mission_user_get import MissionUserGetUsecase
from tests.fixtures.challenges.mission.usecase.user_mission import mock_user_mission_get
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/challenges/mission/usecases/user_mission/test_user_get.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_user_mission_get: MissionUser,
):
    uc = MissionUserGetUsecase(uow=uow)
    res = await uc(user=fxe_user_default, id=1)
    mission = res.item
    assert isinstance(mission, MissionUser)
    assert mock_user_mission_get.id == mission.id
