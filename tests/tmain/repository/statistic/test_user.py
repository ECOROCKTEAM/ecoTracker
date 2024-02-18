import pytest

from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.language import LanguageEnum
from src.core.interfaces.repository.statistic.user import IRepositoryUserStatistic
from tests.dataloader import dataloader


@pytest.mark.asyncio
async def test_user_task_list_finished_first(dl: dataloader) -> tuple[str, int]:
    user = await dl.user_loader.create()
    task_category = await dl.create_category(
        name="test task category", language_list=[LanguageEnum.EN, LanguageEnum.FR, LanguageEnum.RU]
    )
    task = await dl.task_loader.create(category=task_category)
    user_task_1 = await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.FINISH)
    user_task_2 = await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.FINISH)
    user_task_3 = await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.FINISH)
    user_task_4 = await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.FINISH)
    finished_tasks = 4
    return user.id, finished_tasks


@pytest.mark.asyncio
async def test_user_task_list_finished_second(dl: dataloader) -> tuple[str, int]:
    user = await dl.user_loader.create()
    task_category = await dl.create_category(
        name="test task category", language_list=[LanguageEnum.EN, LanguageEnum.FR, LanguageEnum.RU]
    )
    task = await dl.task_loader.create(category=task_category)
    user_task_1 = await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.FINISH)
    user_task_2 = await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.FINISH)
    user_task_3 = await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.FINISH)
    user_task_4 = await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.ACTIVE)
    finished_tasks = 3
    return user.id, finished_tasks


@pytest.mark.asyncio
async def test_user_task_list_finished_third(dl: dataloader) -> tuple[str, int]:
    user = await dl.user_loader.create()
    task_category = await dl.create_category(
        name="test task category", language_list=[LanguageEnum.EN, LanguageEnum.FR, LanguageEnum.RU]
    )
    task = await dl.task_loader.create(category=task_category)
    user_task_1 = await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.ACTIVE)
    user_task_2 = await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.ACTIVE)
    user_task_3 = await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.ACTIVE)
    user_task_4 = await dl.user_task_loader.create(user_id=user.id, task_id=task.id, status=OccupancyStatusEnum.ACTIVE)
    finished_tasks = 0
    return user.id, finished_tasks


# pytest tests/tmain/repository/statistic/test_group.py::test_user_task_counter_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_func",
    [test_user_task_list_finished_first, test_user_task_list_finished_second, test_user_task_list_finished_third],
)
async def test_user_task_counter_ok(dl: dataloader, repo_user_statistic: IRepositoryUserStatistic, arrange_func):
    user_id, finished_tasks = await arrange_func(dl=dl)

    user_task_counter = await repo_user_statistic.task_counter(user_id=user_id)

    assert finished_tasks == user_task_counter.counter
    assert user_id == user_task_counter.user_id


@pytest.mark.asyncio
async def test_user_mission_list_finished_first(dl: dataloader) -> tuple[str, int]:
    user = await dl.user_loader.create()
    category = await dl.create_category()
    mission = await dl.mission_loader.create(category_id=category.id)
    await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.FINISH)
    await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.FINISH)
    await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.FINISH)
    await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.FINISH)
    finished_missions = 4
    return user.id, finished_missions


@pytest.mark.asyncio
async def test_user_mission_list_finished_second(dl: dataloader) -> tuple[str, int]:
    user = await dl.user_loader.create()
    category = await dl.create_category()
    mission = await dl.mission_loader.create(category_id=category.id)
    await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.FINISH)
    await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.FINISH)
    await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.ACTIVE)
    await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.ACTIVE)
    finished_missions = 2
    return user.id, finished_missions


@pytest.mark.asyncio
async def test_user_mission_list_finished_third(dl: dataloader) -> tuple[str, int]:
    user = await dl.user_loader.create()
    category = await dl.create_category()
    mission = await dl.mission_loader.create(category_id=category.id)
    await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.ACTIVE)
    await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.ACTIVE)
    await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.ACTIVE)
    await dl.user_mission_loader.create(user_id=user.id, mission_id=mission.id, status=OccupancyStatusEnum.ACTIVE)
    finished_missions = 0
    return user.id, finished_missions


# pytest tests/tmain/repository/statistic/test_user.py::test_user_mission_finished_counter_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_func",
    [
        test_user_mission_list_finished_first,
        test_user_mission_list_finished_second,
        test_user_mission_list_finished_third,
    ],
)
async def test_user_mission_finished_counter_ok(
    dl: dataloader, repo_user_statistic: IRepositoryUserStatistic, arrange_func
):
    user_id, finished_missions = await arrange_func(dl=dl)

    user_mission_counter = await repo_user_statistic.mission_counter(user_id=user_id)

    assert user_mission_counter.user_id == user_id
    assert user_mission_counter.counter == finished_missions
