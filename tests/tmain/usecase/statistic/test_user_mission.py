from random import randint

import pytest

from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.interfaces.repository.statistic.occupancy import OccupancyStatisticFilter
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.statistic.user_mission_counter import (
    UserMissionCounterStatisticUsecase,
)
from src.data.repository.user import model_to_dto as user_model_to_dto
from tests.dataloader import dataloader


async def _arrange_user_mission(dl: dataloader) -> tuple[User, dict]:
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    category = await dl.category_loader.create()
    mission = await dl.mission_loader.create(category=category)

    status_in = []
    for e in list(OccupancyStatusEnum):
        status_in.extend([e] * randint(1, 4))

    for status in status_in:
        await dl.user_mission_loader.create(user=user_model, mission=mission, status=status)

    status_count_dict = {status: status_in.count(status) for status in list(OccupancyStatusEnum)}
    return user, status_count_dict


# pytest tests/tmain/usecase/statistic/test_user_mission.py::test_user_mission_get_count_ok -v -s
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
async def test_user_mission_get_count_ok(uow: IUnitOfWork, dl: dataloader, filter_list: list[OccupancyStatusEnum]):
    user, status_count_dict = await _arrange_user_mission(dl=dl)

    assrt_mission_count = sum([status_count_dict[status] for status in filter_list])

    uc = UserMissionCounterStatisticUsecase(uow=uow)
    res = await uc(user=user, filter_obj=OccupancyStatisticFilter(status__in=filter_list))

    assert res.item.counter == assrt_mission_count
    assert res.item.user_id == user.id


# pytest tests/tmain/usecase/statistic/test_user_mission.py::test_user_mission_empty_list_ok -v -s
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
async def test_user_mission_empty_list_ok(uow: IUnitOfWork, dl: dataloader, filter_list: list[OccupancyStatusEnum]):
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    uc = UserMissionCounterStatisticUsecase(uow=uow)
    res = await uc(user=user, filter_obj=OccupancyStatisticFilter(status__in=filter_list))

    assert res.item.counter == 0
    assert res.item.user_id == user.id
