import pytest

from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.interfaces.repository.statistic.group import IRepositoryGroupStatistic
from src.core.interfaces.repository.statistic.occupancy import OccupancyStatisticFilter
from tests.dataloader import dataloader


async def _test_group_mission_finished_list_first(dl: dataloader) -> tuple[int, int]:
    user = await dl.user_loader.create()
    group = await dl.group_loader.create()
    category = await dl.create_category()
    mission = await dl.mission_loader.create(category_id=category.id)
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author=user.id, status=OccupancyStatusEnum.FINISH
    )
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author=user.id, status=OccupancyStatusEnum.FINISH
    )
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author=user.id, status=OccupancyStatusEnum.FINISH
    )
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author=user.id, status=OccupancyStatusEnum.FINISH
    )
    finished_missions = 4
    return group.id, finished_missions


async def _test_group_mission_finished_list_second(dl: dataloader) -> tuple[int, int]:
    user = await dl.user_loader.create()
    group = await dl.group_loader.create()
    category = await dl.create_category()
    mission = await dl.mission_loader.create(category_id=category.id)
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author=user.id, status=OccupancyStatusEnum.FINISH
    )
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author=user.id, status=OccupancyStatusEnum.FINISH
    )
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author=user.id, status=OccupancyStatusEnum.ACTIVE
    )
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author=user.id, status=OccupancyStatusEnum.ACTIVE
    )
    finished_missions = 2
    return group.id, finished_missions


async def _test_group_mission_finished_list_third(dl: dataloader) -> tuple[int, int]:
    user = await dl.user_loader.create()
    group = await dl.group_loader.create()
    category = await dl.create_category()
    mission = await dl.mission_loader.create(category_id=category.id)
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author=user.id, status=OccupancyStatusEnum.ACTIVE
    )
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author=user.id, status=OccupancyStatusEnum.ACTIVE
    )
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author=user.id, status=OccupancyStatusEnum.ACTIVE
    )
    await dl.group_mission_loader.create(
        group_id=group.id, mission_id=mission.id, author=user.id, status=OccupancyStatusEnum.ACTIVE
    )
    finished_missions = 0
    return group.id, finished_missions


# pytest tests/tmain/repository/statistic/test_group.py::test_group_missions_finished_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_func",
    [
        _test_group_mission_finished_list_first,
        _test_group_mission_finished_list_second,
        _test_group_mission_finished_list_third,
    ],
)
async def test_group_missions_finished_ok(
    dl: dataloader, repo_group_statistic: IRepositoryGroupStatistic, arrange_func
):
    group_id, finished_missions = await arrange_func(dl=dl)

    group_mission_counter = await repo_group_statistic.mission_counter(
        group_id=group_id, filter_obj=OccupancyStatisticFilter(status__in=[OccupancyStatusEnum.FINISH])
    )

    assert group_id == group_mission_counter.group_id
    assert finished_missions == group_mission_counter.counter
