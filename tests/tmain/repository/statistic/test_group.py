import random

import pytest

from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.interfaces.repository.statistic.group import IRepositoryGroupStatistic
from src.core.interfaces.repository.statistic.occupancy import OccupancyStatisticFilter
from tests.dataloader import dataloader


async def _arrange_group_mission_count(dl: dataloader) -> tuple[int, dict]:
    user = await dl.user_loader.create()
    group = await dl.group_loader.create()
    category = await dl.create_category()
    mission = await dl.mission_loader.create(category=category)
    status_list = []
    # We iterate over each value of OccupancyStatusEnum
    for e in list(OccupancyStatusEnum):
        # Add random count of current enum value
        # For example:
        #    e = OccupancyStatusEnum.ACTIVE, random_number = 2
        #    we add [OccupancyStatusEnum.ACTIVE, OccupancyStatusEnum.ACTIVE]
        status_list.extend([e] * random.randint(1, 5))

    # Create missions with generated list of status
    for status in status_list:
        await dl.group_mission_loader.create(group=group, mission=mission, author=user.id, status=status)

    # Calculate count of each unique value OccupancyStatusEnum
    # For example:
    #    status_list = [OccupancyStatusEnum.ACTIVE, OccupancyStatusEnum.ACTIVE, OccupancyStatusEnum.FINISH]
    #    we get map: {OccupancyStatusEnum.ACTIVE: 2, OccupancyStatusEnum.FINISH: 1}
    status_count_dict = {e: status_list.count(e) for e in list(OccupancyStatusEnum)}
    return group.id, status_count_dict


# pytest tests/tmain/repository/statistic/test_group.py::test_group_mission_counter_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status__in",
    [
        [
            OccupancyStatusEnum.ACTIVE,
        ],
        [OccupancyStatusEnum.ACTIVE, OccupancyStatusEnum.FINISH],
        [*list(OccupancyStatusEnum)],
        [],
    ],
)
async def test_group_mission_counter_ok(
    dl: dataloader, repo_group_statistic: IRepositoryGroupStatistic, status__in: list[OccupancyStatusEnum]
):
    # Arrange
    group_id, status_count_dict = await _arrange_group_mission_count(dl=dl)
    asrt_count = sum([status_count_dict[status] for status in status__in])

    # Act
    group_mission_counter = await repo_group_statistic.mission_counter(
        group_id=group_id, filter_obj=OccupancyStatisticFilter(status__in=status__in)
    )

    # Assert
    assert group_id == group_mission_counter.group_id
    assert asrt_count == group_mission_counter.counter
