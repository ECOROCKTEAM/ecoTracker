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


async def _test_user_mission_list_first(dl: dataloader) -> tuple[User, int, OccupancyStatisticFilter]:
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    category = await dl.category_loader.create()
    mission = await dl.mission_loader.create(category_id=category.id)

    await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.FINISH)
    await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.FINISH)
    await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.FINISH)

    await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.ACTIVE)
    await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.OVERDUE)
    await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.REJECT)

    filter_obj = OccupancyStatisticFilter(status__in=[OccupancyStatusEnum.FINISH])
    counter = 3
    return user, counter, filter_obj


async def _test_user_mission_list_second(dl: dataloader) -> tuple[User, int, OccupancyStatisticFilter]:
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    category = await dl.category_loader.create()
    mission = await dl.mission_loader.create(category_id=category.id)

    await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.FINISH)
    await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.FINISH)
    await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.FINISH)

    await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.ACTIVE)
    await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.OVERDUE)
    await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.REJECT)

    filter_obj = OccupancyStatisticFilter(status__in=[OccupancyStatusEnum.REJECT, OccupancyStatusEnum.ACTIVE])
    counter = 2
    return user, counter, filter_obj


async def _test_user_mission_list_third(dl: dataloader) -> tuple[User, int, OccupancyStatisticFilter]:
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    category = await dl.category_loader.create()
    mission = await dl.mission_loader.create(category_id=category.id)

    await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.ACTIVE)
    await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.ACTIVE)
    await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.ACTIVE)

    await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.ACTIVE)
    await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.OVERDUE)
    await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.REJECT)

    filter_obj = OccupancyStatisticFilter(status__in=[OccupancyStatusEnum.FINISH])
    counter = 0
    return user, counter, filter_obj


# pytest tests/tmain/usecase/statistic/user_mission.py::test_user_mission_get_mission_count -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "create_data", [_test_user_mission_list_first, _test_user_mission_list_second, _test_user_mission_list_third]
)
async def test_user_mission_get_count(uow: IUnitOfWork, dl: dataloader, create_data):
    user, assrt_counter, filter_obj = await create_data(dl=dl)

    uc = UserMissionCounterStatisticUsecase(uow=uow)
    res = await uc(user=user, filter_obj=filter_obj)

    assert res.item.counter == assrt_counter
    assert res.item.user_id == user.id


# pytest tests/tmain/usecase/statistic/user_mission.py::test_user_mission_ok -v -s
@pytest.mark.asyncio
async def test_user_mission_ok(uow: IUnitOfWork, dl: dataloader):
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    category = await dl.category_loader.create()
    mission = await dl.mission_loader.create(category_id=category.id)
    user_mission = await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id)

    filter_obj = OccupancyStatisticFilter(status__in=[OccupancyStatusEnum.ACTIVE])

    uc = UserMissionCounterStatisticUsecase(uow=uow)
    res = await uc(user=user, filter_obj=filter_obj)

    assert res.item.counter == 1
    assert res.item.user_id == user.id


# pytest tests/tmain/usecase/statistic/user_mission.py::test_user_mission_empty_list_ok -v -s
@pytest.mark.asyncio
async def test_user_mission_empty_list_ok(uow: IUnitOfWork, dl: dataloader):
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)

    filter_obj = OccupancyStatisticFilter(status__in=[OccupancyStatusEnum.FINISH])

    uc = UserMissionCounterStatisticUsecase(uow=uow)
    res = await uc(user=user, filter_obj=filter_obj)

    assert res.item.counter == 0
    assert res.item.user_id == user.id
