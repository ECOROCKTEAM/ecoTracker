import pytest

from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.interfaces.repository.statistic.occupancy import OccupancyStatisticFilter
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.statistic.user_mission_counter import (
    UserMissionCounterStatisticUsecase,
)
from src.core.usecases.statistic.user_task_counter import (
    UserTaskCounterStatisticUsecase,
)
from src.data.repository.user import model_to_dto as user_model_to_dto
from tests.dataloader import dataloader


async def _test_user_task_list_first(dl: dataloader) -> tuple[User, int, OccupancyStatisticFilter]:
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    category = await dl.category_loader.create()
    task = await dl.task_loader.create(category=category)

    await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.FINISH)
    await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.FINISH)
    await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.FINISH)

    await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.ACTIVE)
    await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.OVERDUE)
    await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.REJECT)

    filter_obj = OccupancyStatisticFilter(status__in=[OccupancyStatusEnum.FINISH])
    counter = 3
    return user, counter, filter_obj


async def _test_user_task_list_second(dl: dataloader) -> tuple[User, int, OccupancyStatisticFilter]:
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    category = await dl.category_loader.create()
    task = await dl.task_loader.create(category=category)

    await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.FINISH)
    await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.FINISH)
    await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.ACTIVE)

    await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.FINISH)
    await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.OVERDUE)
    await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.REJECT)

    filter_obj = OccupancyStatisticFilter(
        status__in=[OccupancyStatusEnum.FINISH, OccupancyStatusEnum.OVERDUE, OccupancyStatusEnum.ACTIVE]
    )
    counter = 5
    return user, counter, filter_obj


async def _test_user_task_list_third(dl: dataloader) -> tuple[User, int, OccupancyStatisticFilter]:
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    category = await dl.category_loader.create()
    task = await dl.task_loader.create(category=category)

    await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.FINISH)
    await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.FINISH)
    await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.FINISH)

    await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.ACTIVE)
    await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.OVERDUE)
    await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.REJECT)

    filter_obj = OccupancyStatisticFilter(status__in=[OccupancyStatusEnum.REJECT, OccupancyStatusEnum.ACTIVE])
    counter = 2
    return user, counter, filter_obj


# pytest tests/tmain/usecase/statistic/user_task.py::test_user_task_get_task_count_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "create_data", [_test_user_task_list_first, _test_user_task_list_second, _test_user_task_list_third]
)
async def test_user_task_get_count_ok(uow: IUnitOfWork, dl: dataloader, create_data):
    user, assrt_counter, filter_obj = await create_data(dl=dl)

    uc = UserTaskCounterStatisticUsecase(uow=uow)
    res = await uc(user=user, filter_obj=filter_obj)

    assert res.item.counter == assrt_counter
    assert res.item.user_id == user.id


# pytest tests/tmain/usecase/statistic/user_task.py::test_user_task_ok -v -s
@pytest.mark.asyncio
async def test_user_task_ok(uow: IUnitOfWork, dl: dataloader):
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    filter_obj = OccupancyStatisticFilter(status__in=[OccupancyStatusEnum.FINISH])

    category = await dl.category_loader.create()
    task = await dl.task_loader.create(category=category)
    await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.FINISH)
    await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.ACTIVE)

    uc = UserTaskCounterStatisticUsecase(uow=uow)
    res = await uc(user=user, filter_obj=filter_obj)

    assert res.item.counter == 1
    assert res.item.user_id == user.id


# pytest tests/tmain/usecase/statistic/user_task.py::test_user_task_empty_list_ok -v -s
@pytest.mark.asyncio
async def test_user_task_empty_list_ok(uow: IUnitOfWork, dl: dataloader):
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    filter_obj = OccupancyStatisticFilter(status__in=[OccupancyStatusEnum.FINISH])

    uc = UserTaskCounterStatisticUsecase(uow=uow)
    res = await uc(user=user, filter_obj=filter_obj)

    assert res.item.counter == 0
    assert res.item.user_id == user.id
