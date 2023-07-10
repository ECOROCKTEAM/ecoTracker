import pytest

from src.core.dto.mock import MockObj
from src.core.entity.mission import Mission
from src.core.entity.user import User
from src.core.interfaces.repository.challenges.mission import MissionFilter
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.mission.mission_list import MissionListUsecase
from tests.fixtures.challenges.mission.usecase.mission import (
    mock_mission_lst_check_filter,
)
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/challenges/mission/usecases/mission/test_list.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_mission_lst_check_filter,
):
    uc = MissionListUsecase(uow=uow)
    res = await uc(
        user=fxe_user_default,
        filter_obj=MissionFilter(active=False),
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    # active filter was changed to true
    mission_list = res.item
    assert len(mission_list) == 0
