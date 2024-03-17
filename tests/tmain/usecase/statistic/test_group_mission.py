from random import randint

import pytest

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
from src.data.models.user.user import UserModel
from src.data.repository.user import model_to_dto as user_model_to_dto
from tests.dataloader import dataloader


async def _arrange_group_mission(
    dl: dataloader,
    group_privacy: GroupPrivacyEnum,
    user: UserModel | None = None,
    user_role: GroupRoleEnum | None = None,
) -> tuple[int, dict]:
    group = await dl.group_loader.create(privacy=group_privacy)
    category = await dl.create_category(name="")
    mission = await dl.mission_loader.create(category=category)

    if user is not None:
        if user_role is None:
            user_role = GroupRoleEnum.SUPERUSER
        await dl.user_group_loader.create(user=user, group=group, role=user_role)

    status_in = []

    for e in list(OccupancyStatusEnum):
        status_in.extend([e] * randint(1, 4))

    for status in status_in:
        await dl.group_mission_loader.create(group=group, mission=mission, author="", status=status)

    status_count_dict = {status: status_in.count(status) for status in list(OccupancyStatusEnum)}
    return group.id, status_count_dict


# pytest tests/tmain/usecase/statistic/test_group_mission.py::test_group_mission_counter_private_group_user_not_in_group_error -v -s
@pytest.mark.asyncio
async def test_group_mission_counter_private_group_user_not_in_group_error(
    uow: IUnitOfWork,
    dl: dataloader,
):
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    group_id, _ = await _arrange_group_mission(dl=dl, group_privacy=GroupPrivacyEnum.PRIVATE)
    filter_obj = OccupancyStatisticFilter(status__in=[OccupancyStatusEnum.FINISH])

    uc = GroupMissionCounterStatisticUsecase(uow=uow)
    with pytest.raises(PermissionError) as e:
        await uc(user=user, group_id=group_id, filter_obj=filter_obj)
    assert "not in PRIVATE" in str(e.value)


# pytest tests/tmain/usecase/statistic/test_group_mission.py::test_group_mission_counter_private_group_without_missions_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filter_list",
    [
        [OccupancyStatusEnum.ACTIVE],
        [OccupancyStatusEnum.FINISH, OccupancyStatusEnum.OVERDUE],
        [*list(OccupancyStatusEnum)],
        [],
    ],
)
async def test_group_mission_counter_private_group_without_missions_ok(
    uow: IUnitOfWork, dl: dataloader, filter_list: list[OccupancyStatusEnum]
):
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)
    group = await dl.group_loader.create(privacy=GroupPrivacyEnum.PRIVATE)
    await dl.user_group_loader.create(user=user_model, group=group, role=GroupRoleEnum.USER)

    uc = GroupMissionCounterStatisticUsecase(uow=uow)
    res = await uc(user=user, group_id=group.id, filter_obj=OccupancyStatisticFilter(status__in=filter_list))

    assert res.item.counter == 0
    assert res.item.group_id == group.id


# pytest tests/tmain/usecase/statistic/test_group_mission.py::test_group_mission_counter_public_group_without_missions_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filter_list",
    [
        [OccupancyStatusEnum.ACTIVE],
        [OccupancyStatusEnum.FINISH, OccupancyStatusEnum.OVERDUE],
        [*list(OccupancyStatusEnum)],
        [],
    ],
)
async def test_group_mission_counter_public_group_without_missions_ok(
    uow: IUnitOfWork, dl: dataloader, filter_list: list[OccupancyStatusEnum]
):
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)
    group = await dl.group_loader.create(privacy=GroupPrivacyEnum.PUBLIC)
    await dl.user_group_loader.create(user=user_model, group=group, role=GroupRoleEnum.USER)

    uc = GroupMissionCounterStatisticUsecase(uow=uow)
    res = await uc(user=user, group_id=group.id, filter_obj=OccupancyStatisticFilter(status__in=filter_list))

    assert res.item.counter == 0
    assert res.item.group_id == group.id


# pytest tests/tmain/usecase/statistic/test_group_mission.py::test_group_mission_counter_private_group_user_in_group_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filter_list",
    [
        [OccupancyStatusEnum.ACTIVE],
        [OccupancyStatusEnum.FINISH, OccupancyStatusEnum.OVERDUE],
        [*list(OccupancyStatusEnum)],
        [],
    ],
)
async def test_group_mission_counter_private_group_user_in_group_ok(
    uow: IUnitOfWork, dl: dataloader, filter_list: list[OccupancyStatusEnum]
):
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    group_id, status_count_dict = await _arrange_group_mission(
        dl=dl, group_privacy=GroupPrivacyEnum.PRIVATE, user=user_model, user_role=GroupRoleEnum.USER
    )
    assrt_mission_count = sum([status_count_dict[status] for status in filter_list])

    uc = GroupMissionCounterStatisticUsecase(uow=uow)
    result = await uc(user=user, group_id=group_id, filter_obj=OccupancyStatisticFilter(status__in=filter_list))

    assert result.item.counter == assrt_mission_count
    assert result.item.group_id == group_id


# pytest tests/tmain/usecase/statistic/test_group_mission.py::test_group_mission_counter_public_user_not_in_group_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filter_list",
    [
        [OccupancyStatusEnum.ACTIVE],
        [OccupancyStatusEnum.FINISH, OccupancyStatusEnum.OVERDUE],
        [*list(OccupancyStatusEnum)],
        [],
    ],
)
async def test_group_mission_counter_public_user_not_in_group_ok(
    uow: IUnitOfWork, dl: dataloader, filter_list: list[OccupancyStatusEnum]
):
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    group_id, status_count_dict = await _arrange_group_mission(dl=dl, group_privacy=GroupPrivacyEnum.PUBLIC)
    assrt_mission_count = sum([status_count_dict[status] for status in filter_list])

    uc = GroupMissionCounterStatisticUsecase(uow=uow)
    res = await uc(user=user, group_id=group_id, filter_obj=OccupancyStatisticFilter(status__in=filter_list))

    assert res.item.counter == assrt_mission_count
    assert res.item.group_id == group_id


# pytest tests/tmain/usecase/statistic/test_group_mission.py::test_group_mission_counter_public_user_in_group_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filter_list",
    [
        [OccupancyStatusEnum.ACTIVE],
        [OccupancyStatusEnum.FINISH, OccupancyStatusEnum.OVERDUE],
        [*list(OccupancyStatusEnum)],
        [],
    ],
)
async def test_group_mission_counter_public_user_in_group_ok(
    uow: IUnitOfWork, dl: dataloader, filter_list: list[OccupancyStatusEnum]
):
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    group_id, status_count_dict = await _arrange_group_mission(
        dl=dl, group_privacy=GroupPrivacyEnum.PUBLIC, user=user_model, user_role=GroupRoleEnum.USER
    )
    assrt_mission_count = sum([status_count_dict[status] for status in filter_list])

    uc = GroupMissionCounterStatisticUsecase(uow=uow)
    res = await uc(user=user, group_id=group_id, filter_obj=OccupancyStatisticFilter(status__in=filter_list))

    assert res.item.counter == assrt_mission_count
    assert res.item.group_id == group_id


# pytest tests/tmain/usecase/statistic/test_group_mission.py::test_group_mission_counter_public_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filter_list",
    [
        [OccupancyStatusEnum.ACTIVE],
        [OccupancyStatusEnum.FINISH, OccupancyStatusEnum.OVERDUE],
        [*list(OccupancyStatusEnum)],
        [],
    ],
)
async def test_group_mission_counter_public_ok(
    uow: IUnitOfWork, dl: dataloader, filter_list: list[OccupancyStatusEnum]
):
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    group_id, status_count_dict = await _arrange_group_mission(dl=dl, group_privacy=GroupPrivacyEnum.PUBLIC)
    assrt_mission_count = sum([status_count_dict[status] for status in filter_list])

    uc = GroupMissionCounterStatisticUsecase(uow=uow)
    res = await uc(user=user, group_id=group_id, filter_obj=OccupancyStatisticFilter(status__in=filter_list))

    assert res.item.counter == assrt_mission_count
    assert res.item.group_id == group_id


# pytest tests/tmain/usecase/statistic/test_group_mission.py::test_group_mission_counter_private_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filter_list",
    [
        [OccupancyStatusEnum.ACTIVE],
        [OccupancyStatusEnum.FINISH, OccupancyStatusEnum.OVERDUE],
        [*list(OccupancyStatusEnum)],
        [],
    ],
)
async def test_group_mission_counter_private_ok(
    uow: IUnitOfWork, dl: dataloader, filter_list: list[OccupancyStatusEnum]
):
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    group_id, status_count_dict = await _arrange_group_mission(
        dl=dl, group_privacy=GroupPrivacyEnum.PRIVATE, user=user_model, user_role=GroupRoleEnum.USER
    )
    assrt_mission_count = sum([status_count_dict[status] for status in filter_list])

    uc = GroupMissionCounterStatisticUsecase(uow=uow)
    res = await uc(user=user, group_id=group_id, filter_obj=OccupancyStatisticFilter(status__in=filter_list))

    assert res.item.counter == assrt_mission_count
    assert res.item.group_id == group_id
