import pytest

from src.core.dto.mock import MockObj
from src.core.entity.user import User
from src.core.interfaces.repository.challenges.mission import MissionGroupFilter
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.mission.mission_group_list import (
    MissionGroupListUsecase,
)
from tests.fixtures.group.usecase.group import mock_group_lst
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/challenges/mission/usecases/group_mission/test_group_list.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_lst,
):
    uc = MissionGroupListUsecase(uow=uow)
    await uc(
        user=fxe_user_default,
        filter_obj=MissionGroupFilter(),
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
