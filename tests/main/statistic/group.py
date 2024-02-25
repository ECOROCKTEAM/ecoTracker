import pytest

from src.core.dto.m2m.user.group import UserGroupDTO
from src.core.entity.group import Group
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.exception.base import PermissionError
from src.core.interfaces.repository.statistic.occupancy import OccupancyStatisticFilter
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.statistic.group_mission_counter import (
    GroupMissionFinishedCounterUseCase,
)
from tests.fixtures.group.usecase.group import mock_group_get_active_private
from tests.fixtures.group.usecase.user import mock_group_user_get_default
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/statistic/group.py::test_group_mission_counter_private_group_user_in_group_ok -v -s
@pytest.mark.asyncio
async def test_group_mission_counter_private_group_user_in_group_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_get_active_private: Group,
    mock_group_user_get_default: UserGroupDTO,
):
    filter_obj = OccupancyStatisticFilter(status__in=[OccupancyStatusEnum.ACTIVE])

    uc = GroupMissionFinishedCounterUseCase(uow=uow)
    await uc(user=fxe_user_default, group_id=mock_group_get_active_private.id, filter_obj=filter_obj)


# pytest tests/main/statistic/group.py::test_group_mission_counter_private_group_user_not_in_group_error -v -s
@pytest.mark.asyncio
async def test_group_mission_counter_private_group_user_not_in_group_error(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_get_active_private: Group,
):
    filter_obj = OccupancyStatisticFilter(status__in=[OccupancyStatusEnum.FINISH])

    uc = GroupMissionFinishedCounterUseCase(uow=uow)
    with pytest.raises(PermissionError) as e:
        await uc(user=fxe_user_default, group_id=mock_group_get_active_private.id, filter_obj=filter_obj)
    assert "not in PRIVATE" in str(e.value)
