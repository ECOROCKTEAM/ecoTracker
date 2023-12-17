import pytest

from src.core.dto.challenges.mission import MissionUserUpdateDTO
from src.core.entity.mission import Mission, MissionUser
from src.core.entity.score import ScoreUser
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.exception.base import EntityNotChange
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.mission.mission_user_update import (
    MissionUserUpdateUsecase,
)
from tests.fixtures.challenges.mission.usecase.mission import mock_mission_get_default
from tests.fixtures.challenges.mission.usecase.user_mission import (
    mock_user_mission_finish_status,
    mock_user_mission_get,
    mock_user_mission_update,
)
from tests.fixtures.const import DEFAULT_TEST_USECASE_MISSION_ID
from tests.fixtures.score.usecase.user_score import mock_user_score_add
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/challenges/mission/usecases/user_mission/test_user_update.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_user_mission_get: MissionUser,
    mock_mission_get_default: Mission,
    mock_user_mission_update: MissionUser,
    mock_user_score_add: ScoreUser,
):
    uc = MissionUserUpdateUsecase(uow=uow)
    res = await uc(
        user=fxe_user_default,
        id=DEFAULT_TEST_USECASE_MISSION_ID,
        update_obj=MissionUserUpdateDTO(status=OccupancyStatusEnum.FINISH),
    )
    mission = res.item
    assert isinstance(mission, MissionUser)


# pytest tests/main/challenges/mission/usecases/user_mission/test_user_update.py::test_not_change -v -s
@pytest.mark.asyncio
async def test_not_change(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_user_mission_finish_status: MissionUser,
):
    uc = MissionUserUpdateUsecase(uow=uow)
    with pytest.raises(EntityNotChange):
        await uc(
            user=fxe_user_default,
            id=1,
            update_obj=MissionUserUpdateDTO(status=OccupancyStatusEnum.ACTIVE),
        )
