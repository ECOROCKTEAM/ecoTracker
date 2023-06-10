import pytest

from src.core.dto.mock import MockObj
from src.core.entity.user import User
from src.core.interfaces.repository.challenges.mission import MissionUserFilter
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.mission.mission_user_list import (
    MissionUserListUsecase,
)
from tests.fixtures.challenges.mission.usecase.user_mission import mock_user_mission_lst
from tests.fixtures.user.usecase.entity import fxe_user_default


# python -m pytest tests/challenges/mission/usecases/user_mission/test_user_list.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_user_mission_lst,
):
    uc = MissionUserListUsecase(uow=uow)
    res = await uc(
        user=fxe_user_default,
        filter_obj=MissionUserFilter(),
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    mission_list = res.item
    assert len(mission_list) == 0
