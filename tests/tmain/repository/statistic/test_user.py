from random import randint

import pytest

from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.language import LanguageEnum
from src.core.interfaces.repository.statistic.occupancy import OccupancyStatisticFilter
from src.core.interfaces.repository.statistic.user import IRepositoryUserStatistic
from tests.dataloader import dataloader


async def _arrange_user_task(dl: dataloader) -> tuple[str, dict]:
    user = await dl.user_loader.create()
    category = await dl.create_category(
        name="test task category", language_list=[LanguageEnum.EN, LanguageEnum.FR, LanguageEnum.RU]
    )
    task = await dl.task_loader.create(category=category)

    status_in = []
    for e in list(OccupancyStatusEnum):
        status_in.extend([e] * randint(1, 4))

    for status in status_in:
        await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=status)

    status_count_dict = {status: status_in.count(status) for status in list(OccupancyStatusEnum)}
    return user.id, status_count_dict


# pytest tests/tmain/repository/statistic/test_user.py::test_user_task_counter_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filter_list",
    [
        [
            OccupancyStatusEnum.ACTIVE,
        ],
        [OccupancyStatusEnum.ACTIVE, OccupancyStatusEnum.FINISH],
        [*list(OccupancyStatusEnum)],
        [],
    ],
)
async def test_user_task_counter_ok(
    dl: dataloader, repo_user_statistic: IRepositoryUserStatistic, filter_list: list[OccupancyStatusEnum]
):
    user_id, status_count_dict = await _arrange_user_task(dl=dl)
    asrt_count = sum([status_count_dict[status] for status in filter_list])

    user_task_counter = await repo_user_statistic.task_counter(
        user_id=user_id, filter_obj=OccupancyStatisticFilter(status__in=filter_list)
    )

    assert asrt_count == user_task_counter.counter
    assert user_id == user_task_counter.user_id


async def _arrange_user_mission(dl: dataloader) -> tuple[str, dict]:
    user = await dl.user_loader.create()
    category = await dl.create_category(
        name="test task category", language_list=[LanguageEnum.EN, LanguageEnum.FR, LanguageEnum.RU]
    )
    mission = await dl.mission_loader.create(category_id=category.id)

    status_in = []
    for e in list(OccupancyStatusEnum):
        status_in.extend([e] * randint(1, 4))

    for status in status_in:
        await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=status)

    status_count_dict = {status: status_in.count(status) for status in list(OccupancyStatusEnum)}
    return user.id, status_count_dict


# pytest tests/tmain/repository/statistic/test_user.py::test_user_mission_finished_counter_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filter_list",
    [
        [
            OccupancyStatusEnum.ACTIVE,
        ],
        [OccupancyStatusEnum.ACTIVE, OccupancyStatusEnum.FINISH],
        [*list(OccupancyStatusEnum)],
        [],
    ],
)
async def test_user_mission_finished_counter_ok(
    dl: dataloader, repo_user_statistic: IRepositoryUserStatistic, filter_list: list[OccupancyStatusEnum]
):
    user_id, status_count_dict = await _arrange_user_mission(dl=dl)
    status_count = sum([status_count_dict[status] for status in filter_list])

    user_mission_counter = await repo_user_statistic.mission_counter(
        user_id=user_id, filter_obj=OccupancyStatisticFilter(status__in=filter_list)
    )

    assert user_mission_counter.user_id == user_id
    assert user_mission_counter.counter == status_count
