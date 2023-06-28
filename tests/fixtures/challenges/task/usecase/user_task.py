from datetime import datetime

import pytest_asyncio

from src.core.const.task import MAX_TASK_AMOUNT_NOT_PREMIUM, MAX_TASK_AMOUNT_PREMIUM
from src.core.entity.task import TaskUser, TaskUserPlan
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.interfaces.repository.challenges.task import (
    TaskUserFilter,
    TaskUserPlanFilter,
)
from tests.fixtures.const import (
    DEFAULT_TEST_OCCUPANCY_STATUS,
    DEFAULT_TEST_USECASE_TASK_ID,
    DEFAULT_TEST_USECASE_USER_ID,
)


@pytest_asyncio.fixture
async def mock_user_task_get_default(monkeypatch) -> TaskUser:
    async def f(*args, **kwargs) -> TaskUser:
        return TaskUser(
            id=1337,
            user_id=DEFAULT_TEST_USECASE_USER_ID,
            task_id=DEFAULT_TEST_USECASE_TASK_ID,
            date_start=datetime.now(),
            date_close=None,
            status=DEFAULT_TEST_OCCUPANCY_STATUS,
        )

    monkeypatch.setattr("src.data.repository.challenges.task.RepositoryTask.user_task_get", f)
    return await f()


@pytest_asyncio.fixture
async def mock_user_task_get_finish_status(monkeypatch) -> TaskUser:
    async def f(*args, **kwargs) -> TaskUser:
        return TaskUser(
            id=1337,
            user_id=DEFAULT_TEST_USECASE_USER_ID,
            task_id=DEFAULT_TEST_USECASE_TASK_ID,
            date_start=datetime.now(),
            date_close=None,
            status=OccupancyStatusEnum.FINISH,
        )

    monkeypatch.setattr("src.data.repository.challenges.task.RepositoryTask.user_task_get", f)
    return await f()


@pytest_asyncio.fixture
async def mock_user_task_add(monkeypatch) -> TaskUser:
    async def f(*args, **kwargs) -> TaskUser:
        return TaskUser(
            id=1337,
            user_id=DEFAULT_TEST_USECASE_USER_ID,
            task_id=DEFAULT_TEST_USECASE_TASK_ID,
            date_start=datetime.now(),
            date_close=None,
            status=DEFAULT_TEST_OCCUPANCY_STATUS,
        )

    monkeypatch.setattr("src.data.repository.challenges.task.RepositoryTask.user_task_add", f)
    return await f()


@pytest_asyncio.fixture
async def mock_user_task_update(monkeypatch) -> TaskUser:
    async def f(*args, **kwargs) -> TaskUser:
        return TaskUser(
            id=1337,
            user_id=DEFAULT_TEST_USECASE_USER_ID,
            task_id=DEFAULT_TEST_USECASE_TASK_ID,
            date_start=datetime.now(),
            date_close=datetime.now(),
            status=OccupancyStatusEnum.FINISH,
        )

    monkeypatch.setattr("src.data.repository.challenges.task.RepositoryTask.user_task_update", f)
    return await f()


# @pytest_asyncio.fixture
# async def mock_user_task_finish_status(monkeypatch) -> TaskUser:
#     async def f(*args, **kwargs) -> TaskUser:
#         return TaskUser(
#             id=1337,
#             user_id=DEFAULT_TEST_USECASE_USER_ID,
#             task_id=DEFAULT_TEST_USECASE_TASK_ID,
#             date_start=datetime.now(),
#             date_close=None,
#             status=OccupancyStatusEnum.FINISH,
#         )

#     monkeypatch.setattr("src.data.repository.challenges.task.RepositoryTask.user_task_get", f)
#     return await f()


@pytest_asyncio.fixture
async def mock_user_task_lst(monkeypatch):
    async def f(*args, filter_obj: TaskUserFilter, **kwargs):
        assert isinstance(filter_obj, TaskUserFilter)
        return []

    monkeypatch.setattr("src.data.repository.challenges.task.RepositoryTask.user_task_lst", f)


@pytest_asyncio.fixture
async def mock_user_task_lst_ret_one(monkeypatch):
    async def f(*args, filter_obj: TaskUserFilter, **kwargs):
        assert isinstance(filter_obj, TaskUserFilter)
        return [
            TaskUser(
                id=1337,
                user_id=DEFAULT_TEST_USECASE_USER_ID,
                task_id=DEFAULT_TEST_USECASE_TASK_ID,
                date_start=datetime.now(),
                date_close=None,
                status=DEFAULT_TEST_OCCUPANCY_STATUS,
            )
        ]

    monkeypatch.setattr("src.data.repository.challenges.task.RepositoryTask.user_task_lst", f)


@pytest_asyncio.fixture
async def mock_user_task_lst_ret_gt_max_not_premium(monkeypatch):
    async def f(*args, filter_obj: TaskUserFilter, **kwargs):
        assert isinstance(filter_obj, TaskUserFilter)
        return [
            TaskUser(
                id=1337,
                user_id=DEFAULT_TEST_USECASE_USER_ID,
                task_id=i,
                date_start=datetime.now(),
                date_close=None,
                status=DEFAULT_TEST_OCCUPANCY_STATUS,
            )
            for i in range(MAX_TASK_AMOUNT_NOT_PREMIUM + 1)
        ]

    monkeypatch.setattr("src.data.repository.challenges.task.RepositoryTask.user_task_lst", f)


@pytest_asyncio.fixture
async def mock_user_task_lst_ret_gt_max_premium(monkeypatch):
    async def f(*args, filter_obj: TaskUserFilter, **kwargs):
        assert isinstance(filter_obj, TaskUserFilter)
        return [
            TaskUser(
                id=1337,
                user_id=DEFAULT_TEST_USECASE_USER_ID,
                task_id=i,
                date_start=datetime.now(),
                date_close=None,
                status=DEFAULT_TEST_OCCUPANCY_STATUS,
            )
            for i in range(MAX_TASK_AMOUNT_PREMIUM + 1)
        ]

    monkeypatch.setattr("src.data.repository.challenges.task.RepositoryTask.user_task_lst", f)


@pytest_asyncio.fixture
async def mock_user_task_lst_ret_eq_max_not_premium(monkeypatch):
    async def f(*args, filter_obj: TaskUserFilter, **kwargs):
        assert isinstance(filter_obj, TaskUserFilter)
        return [
            TaskUser(
                id=1337,
                user_id=DEFAULT_TEST_USECASE_USER_ID,
                task_id=i,
                date_start=datetime.now(),
                date_close=None,
                status=DEFAULT_TEST_OCCUPANCY_STATUS,
            )
            for i in range(MAX_TASK_AMOUNT_NOT_PREMIUM)
        ]

    monkeypatch.setattr("src.data.repository.challenges.task.RepositoryTask.user_task_lst", f)


@pytest_asyncio.fixture
async def mock_user_task_lst_ret_eq_max_premium(monkeypatch):
    async def f(*args, filter_obj: TaskUserFilter, **kwargs):
        assert isinstance(filter_obj, TaskUserFilter)
        return [
            TaskUser(
                id=1337,
                user_id=DEFAULT_TEST_USECASE_USER_ID,
                task_id=i,
                date_start=datetime.now(),
                date_close=None,
                status=DEFAULT_TEST_OCCUPANCY_STATUS,
            )
            for i in range(MAX_TASK_AMOUNT_PREMIUM)
        ]

    monkeypatch.setattr("src.data.repository.challenges.task.RepositoryTask.user_task_lst", f)


@pytest_asyncio.fixture
async def mock_user_task_plan_lst_ret_gt_max_not_premium(monkeypatch):
    async def f(*args, filter_obj: TaskUserPlanFilter, **kwargs):
        assert isinstance(filter_obj, TaskUserPlanFilter)
        return [
            TaskUserPlan(
                user_id=DEFAULT_TEST_USECASE_USER_ID,
                task_id=DEFAULT_TEST_USECASE_TASK_ID,
            )
            for i in range(MAX_TASK_AMOUNT_NOT_PREMIUM + 1)
        ]

    monkeypatch.setattr("src.data.repository.challenges.task.RepositoryTask.plan_lst", f)


@pytest_asyncio.fixture
async def mock_user_task_plan_lst_ret_gt_max_premium(monkeypatch):
    async def f(*args, filter_obj: TaskUserPlanFilter, **kwargs):
        assert isinstance(filter_obj, TaskUserPlanFilter)
        return [
            TaskUserPlan(
                user_id=DEFAULT_TEST_USECASE_USER_ID,
                task_id=DEFAULT_TEST_USECASE_TASK_ID,
            )
            for i in range(MAX_TASK_AMOUNT_PREMIUM + 1)
        ]

    monkeypatch.setattr("src.data.repository.challenges.task.RepositoryTask.plan_lst", f)


@pytest_asyncio.fixture
async def mock_user_task_plan_lst_ret_eq_max_not_premium(monkeypatch):
    async def f(*args, filter_obj: TaskUserPlanFilter, **kwargs):
        assert isinstance(filter_obj, TaskUserPlanFilter)
        return [
            TaskUserPlan(
                user_id=DEFAULT_TEST_USECASE_USER_ID,
                task_id=DEFAULT_TEST_USECASE_TASK_ID,
            )
            for i in range(MAX_TASK_AMOUNT_NOT_PREMIUM)
        ]

    monkeypatch.setattr("src.data.repository.challenges.task.RepositoryTask.plan_lst", f)


@pytest_asyncio.fixture
async def mock_user_task_plan_lst_ret_eq_max_premium(monkeypatch):
    async def f(*args, filter_obj: TaskUserPlanFilter, **kwargs):
        assert isinstance(filter_obj, TaskUserPlanFilter)
        return [
            TaskUserPlan(
                user_id=DEFAULT_TEST_USECASE_USER_ID,
                task_id=DEFAULT_TEST_USECASE_TASK_ID,
            )
            for i in range(MAX_TASK_AMOUNT_PREMIUM)
        ]

    monkeypatch.setattr("src.data.repository.challenges.task.RepositoryTask.plan_lst", f)
