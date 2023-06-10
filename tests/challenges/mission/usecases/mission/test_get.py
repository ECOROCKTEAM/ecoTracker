import pytest

from src.core.entity.mission import Mission
from src.core.entity.user import User
from src.core.exception.base import EntityNotActive
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.mission.mission_get import MissionGetUsecase
from tests.fixtures.challenges.mission.usecase.mission import (
    mock_mission_get_default,
    mock_mission_not_active,
)
from tests.fixtures.user.usecase.entity import fxe_user_default


# python -m pytest tests/challenges/mission/usecases/mission/test_get.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_mission_get_default: Mission,
):
    uc = MissionGetUsecase(uow=uow)
    res = await uc(user=fxe_user_default, id=1)
    mission = res.item
    assert isinstance(mission, Mission)
    assert mock_mission_get_default.id == mission.id
    assert mock_mission_get_default.active == mission.active
    assert mock_mission_get_default.score == mission.score
    assert mock_mission_get_default.description == mission.description
    assert mock_mission_get_default.instruction == mission.instruction
    assert mock_mission_get_default.category_id == mission.category_id
    assert mock_mission_get_default.language == mission.language


# python -m pytest tests/challenges/mission/usecases/mission/test_get.py::test_not_active -v -s
@pytest.mark.asyncio
async def test_not_active(uow: IUnitOfWork, fxe_user_default: User, mock_mission_not_active: Mission):
    assert mock_mission_not_active.active is False
    uc = MissionGetUsecase(uow=uow)
    with pytest.raises(EntityNotActive):
        _ = await uc(user=fxe_user_default, id=1)
