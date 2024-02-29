import pytest

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


async def _test_lst_of_group_mission_public_first(
    dl: dataloader,
) -> tuple[int, int, OccupancyStatisticFilter]:
    group = await dl.group_loader.create(privacy=GroupPrivacyEnum.PUBLIC)
    category = await dl.create_category(name="")
    mission = await dl.mission_loader.create(category_id=category.id)

    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.FINISH
    )

    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.REJECT
    )
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.REJECT
    )
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.REJECT
    )
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.REJECT
    )
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.REJECT
    )

    filter_obj = OccupancyStatisticFilter(
        status__in=[OccupancyStatusEnum.FINISH, OccupancyStatusEnum.ACTIVE, OccupancyStatusEnum.OVERDUE]
    )
    counter = 1
    return group.id, counter, filter_obj


async def _test_lst_of_group_mission_public_second(
    dl: dataloader,
) -> tuple[int, int, OccupancyStatisticFilter]:
    group = await dl.group_loader.create(privacy=GroupPrivacyEnum.PUBLIC)
    category = await dl.create_category(name="")
    mission = await dl.mission_loader.create(category_id=category.id)

    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.FINISH
    )

    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.REJECT
    )
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.REJECT
    )
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.REJECT
    )
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.REJECT
    )
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.REJECT
    )

    filter_obj = OccupancyStatisticFilter(status__in=[OccupancyStatusEnum.ACTIVE, OccupancyStatusEnum.OVERDUE])
    counter = 0
    return group.id, counter, filter_obj


async def _test_lst_of_group_mission_public_third(
    dl: dataloader,
) -> tuple[int, int, OccupancyStatisticFilter]:
    group = await dl.group_loader.create(privacy=GroupPrivacyEnum.PUBLIC)
    category = await dl.create_category(name="")
    mission = await dl.mission_loader.create(category_id=category.id)

    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.FINISH
    )

    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.REJECT
    )
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.REJECT
    )
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.REJECT
    )
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.REJECT
    )
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.REJECT
    )

    filter_obj = OccupancyStatisticFilter(status__in=[OccupancyStatusEnum.REJECT, OccupancyStatusEnum.OVERDUE])
    counter = 5
    return group.id, counter, filter_obj


async def _test_lst_of_group_mission_private_first(
    dl: dataloader,
) -> tuple[int, int, OccupancyStatisticFilter]:
    group = await dl.group_loader.create(privacy=GroupPrivacyEnum.PRIVATE)
    category = await dl.create_category(name="")
    mission = await dl.mission_loader.create(category_id=category.id)

    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.FINISH
    )
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.FINISH
    )

    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.ACTIVE
    )
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.ACTIVE
    )

    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.REJECT
    )
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.OVERDUE
    )

    filter_obj = OccupancyStatisticFilter(status__in=[OccupancyStatusEnum.FINISH])
    counter = 2
    return group.id, counter, filter_obj


async def _test_lst_of_group_mission_private_second(
    dl: dataloader,
) -> tuple[int, int, OccupancyStatisticFilter]:
    group = await dl.group_loader.create(privacy=GroupPrivacyEnum.PRIVATE)
    category = await dl.create_category(name="")
    mission = await dl.mission_loader.create(category_id=category.id)

    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.FINISH
    )
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.FINISH
    )

    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.ACTIVE
    )
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.ACTIVE
    )

    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.REJECT
    )
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.OVERDUE
    )

    filter_obj = OccupancyStatisticFilter(status__in=[OccupancyStatusEnum.ACTIVE])
    counter = 2
    return group.id, counter, filter_obj


async def _test_lst_of_group_mission_private_third(
    dl: dataloader,
) -> tuple[int, int, OccupancyStatisticFilter]:
    group = await dl.group_loader.create(privacy=GroupPrivacyEnum.PRIVATE)
    category = await dl.create_category(name="")
    mission = await dl.mission_loader.create(category_id=category.id)

    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.FINISH
    )
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.FINISH
    )

    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.ACTIVE
    )
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.ACTIVE
    )

    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.REJECT
    )
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author="", status=OccupancyStatusEnum.OVERDUE
    )

    filter_obj = OccupancyStatisticFilter(
        status__in=[OccupancyStatusEnum.FINISH, OccupancyStatusEnum.ACTIVE, OccupancyStatusEnum.OVERDUE]
    )
    counter = 5
    return group.id, counter, filter_obj


# pytest tests/tmain/usecase/statistic/group.py::test_group_mission_counter_private_group_user_not_in_group_error -v -s
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


# pytest tests/tmain/usecase/statistic/group.py::test_group_mission_counter_private_group_without_missions_ok -v -s
@pytest.mark.asyncio
async def test_group_mission_counter_private_group_without_missions_ok(
    uow: IUnitOfWork,
    dl: dataloader,
):
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    group = await dl.group_loader.create(privacy=GroupPrivacyEnum.PRIVATE)
    await dl.user_group_loader.create(user_id=user.id, group_id=group.id, role=GroupRoleEnum.USER)

    filter_obj = OccupancyStatisticFilter(status__in=[OccupancyStatusEnum.FINISH])

    uc = GroupMissionCounterStatisticUsecase(uow=uow)
    res = await uc(user=user, group_id=group.id, filter_obj=filter_obj)

    assert res.item.counter == 0
    assert res.item.group_id == group.id


# pytest tests/tmain/usecase/statistic/group.py::test_group_mission_counter_public_group_without_missions_ok -v -s
@pytest.mark.asyncio
async def test_group_mission_counter_public_group_without_missions_ok(
    uow: IUnitOfWork,
    dl: dataloader,
):
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    group = await dl.group_loader.create(privacy=GroupPrivacyEnum.PUBLIC)
    await dl.user_group_loader.create(user_id=user.id, group_id=group.id, role=GroupRoleEnum.USER)

    filter_obj = OccupancyStatisticFilter(status__in=[OccupancyStatusEnum.FINISH])

    uc = GroupMissionCounterStatisticUsecase(uow=uow)
    res = await uc(user=user, group_id=group.id, filter_obj=filter_obj)

    assert res.item.counter == 0
    assert res.item.group_id == group.id


# pytest tests/tmain/usecase/statistic/group.py::test_group_mission_counter_private_group_user_in_group_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "create_data",
    [
        _test_lst_of_group_mission_private_first,
        _test_lst_of_group_mission_private_second,
        _test_lst_of_group_mission_private_third,
    ],
)
async def test_group_mission_counter_private_group_user_in_group_ok(
    uow: IUnitOfWork,
    dl: dataloader,
    create_data,
):
    group_id, assert_counter, filter_obj = await create_data(dl=dl)

    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    await dl.user_group_loader.create(user_id=user.id, group_id=group_id, role=GroupRoleEnum.USER)

    uc = GroupMissionCounterStatisticUsecase(uow=uow)
    result = await uc(user=user, group_id=group_id, filter_obj=filter_obj)

    assert result.item.counter == assert_counter
    assert result.item.group_id == group_id


# pytest tests/tmain/usecase/statistic/group.py::test_group_mission_counter_public_user_not_in_group_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "create_data",
    [
        _test_lst_of_group_mission_public_third,
        _test_lst_of_group_mission_public_first,
        _test_lst_of_group_mission_public_second,
    ],
)
async def test_group_mission_counter_public_user_not_in_group_ok(uow: IUnitOfWork, dl: dataloader, create_data):
    group_id, assrt_counter, filter_obj = await create_data(dl=dl)

    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    uc = GroupMissionCounterStatisticUsecase(uow=uow)
    res = await uc(user=user, group_id=group_id, filter_obj=filter_obj)

    assert res.item.counter == assrt_counter
    assert res.item.group_id == group_id


# pytest tests/tmain/usecase/statistic/group.py::test_group_mission_counter_public_user_in_group_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "create_data",
    [
        _test_lst_of_group_mission_public_third,
        _test_lst_of_group_mission_public_first,
        _test_lst_of_group_mission_public_second,
    ],
)
async def test_group_mission_counter_public_user_in_group_ok(uow: IUnitOfWork, dl: dataloader, create_data):
    group_id, assrt_counter, filter_obj = await create_data(dl=dl)

    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    await dl.user_group_loader.create(user_id=user.id, group_id=group_id, role=GroupRoleEnum.USER)

    uc = GroupMissionCounterStatisticUsecase(uow=uow)
    res = await uc(user=user, group_id=group_id, filter_obj=filter_obj)

    assert res.item.counter == assrt_counter
    assert res.item.group_id == group_id


# pytest tests/tmain/usecase/statistic/group.py::test_test_group_mission_counter_public_ok -v -s
@pytest.mark.asyncio
async def test_group_mission_counter_public_ok(
    uow: IUnitOfWork,
    dl: dataloader,
):
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    group = await dl.group_loader.create(privacy=GroupPrivacyEnum.PUBLIC)

    filter_obj = OccupancyStatisticFilter(status__in=[OccupancyStatusEnum.FINISH])

    await dl.user_group_loader.create(user_id=user.id, group_id=group.id, role=GroupRoleEnum.USER)

    uc = GroupMissionCounterStatisticUsecase(uow=uow)
    res = await uc(user=user, group_id=group.id, filter_obj=filter_obj)

    assert res.item.counter == 0
    assert res.item.group_id == group.id


# pytest tests/tmain/usecase/statistic/group.py::test_test_group_mission_counter_private_ok -v -s
@pytest.mark.asyncio
async def test_group_mission_counter_private_ok(
    uow: IUnitOfWork,
    dl: dataloader,
):
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    group = await dl.group_loader.create(privacy=GroupPrivacyEnum.PUBLIC)

    filter_obj = OccupancyStatisticFilter(status__in=[OccupancyStatusEnum.FINISH])

    await dl.user_group_loader.create(user_id=user.id, group_id=group.id, role=GroupRoleEnum.USER)

    uc = GroupMissionCounterStatisticUsecase(uow=uow)
    res = await uc(user=user, group_id=group.id, filter_obj=filter_obj)

    assert res.item.counter == 0
    assert res.item.group_id == group.id
