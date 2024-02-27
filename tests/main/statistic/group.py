import pytest

from src.core.dto.m2m.user.group import UserGroupDTO
from src.core.entity.group import Group
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.group.privacy import GroupPrivacyEnum
from src.core.enum.group.role import GroupRoleEnum
from src.core.exception.base import PermissionError
from src.core.interfaces.repository.statistic.occupancy import OccupancyStatisticFilter
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.statistic.group_mission_counter import (
    GroupMissionCounterStatisticUsecase,
)
from src.data.repository.user import model_to_dto as user_model_to_dto
from tests.dataloader import dataloader


# pytest tests/main/statistic/group.py::test_group_mission_counter_private_group_user_in_group_ok -v -s
@pytest.mark.asyncio
async def test_group_mission_counter_private_group_user_in_group_ok(
    uow: IUnitOfWork,
    dl: dataloader,
):
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    group = await dl.group_loader.create()
    await dl.user_group_loader.create(user_id=user.id, group_id=group.id, role=GroupRoleEnum.ADMIN)

    filter_obj = OccupancyStatisticFilter(status__in=[OccupancyStatusEnum.FINISH])

    uc = GroupMissionCounterStatisticUsecase(uow=uow)
    await uc(user=user, group_id=group.id, filter_obj=filter_obj)


# pytest tests/main/statistic/group.py::test_group_mission_counter_private_group_user_not_in_group_error -v -s
@pytest.mark.asyncio
async def test_group_mission_counter_private_group_user_not_in_group_error(
    uow: IUnitOfWork,
    dl: dataloader,
):
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    group = await dl.group_loader.create(privacy=GroupPrivacyEnum.PRIVATE)

    filter_obj = OccupancyStatisticFilter(status__in=[OccupancyStatusEnum.FINISH])

    uc = GroupMissionCounterStatisticUsecase(uow=uow)
    with pytest.raises(PermissionError) as e:
        await uc(user=user, group_id=group.id, filter_obj=filter_obj)
    assert "not in PRIVATE" in str(e.value)
