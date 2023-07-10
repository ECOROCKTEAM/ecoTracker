import pytest_asyncio

from src.core.entity.task import Task
from src.core.interfaces.repository.challenges.task import TaskFilter
from tests.fixtures.const import DEFAULT_TEST_CHALLENGE_SCORE, DEFAULT_TEST_LANGUAGE


@pytest_asyncio.fixture
async def mock_task_get_default(monkeypatch) -> Task:
    async def f(*args, **kwargs) -> Task:
        return Task(
            id=1337,
            active=True,
            name="a",
            score=DEFAULT_TEST_CHALLENGE_SCORE,
            description="a",
            category_id=1,
            language=DEFAULT_TEST_LANGUAGE,
        )

    monkeypatch.setattr("src.data.repository.challenges.task.RepositoryTask.get", f)
    return await f()


@pytest_asyncio.fixture
async def mock_task_not_active(monkeypatch) -> Task:
    async def f(*args, **kwargs) -> Task:
        return Task(
            id=1337,
            active=False,
            name="a",
            score=DEFAULT_TEST_CHALLENGE_SCORE,
            description="a",
            category_id=1,
            language=DEFAULT_TEST_LANGUAGE,
        )

    monkeypatch.setattr("src.data.repository.challenges.task.RepositoryTask.get", f)
    return await f()


@pytest_asyncio.fixture
async def mock_task_lst_check_filter(monkeypatch):
    async def f(*args, filter_obj: TaskFilter, **kwargs):
        assert isinstance(filter_obj, TaskFilter)
        assert filter_obj.active is True
        return []

    monkeypatch.setattr("src.data.repository.challenges.task.RepositoryTask.lst", f)
