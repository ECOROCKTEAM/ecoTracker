import pytest_asyncio

from src.core.entity.mission import Mission
from src.core.interfaces.repository.challenges.mission import MissionFilter
from tests.fixtures.const import DEFAULT_TEST_CHALLENGE_SCORE, DEFAULT_TEST_LANGUAGE


@pytest_asyncio.fixture
async def mock_mission_get_default(monkeypatch) -> Mission:
    async def f(*args, **kwargs) -> Mission:
        return Mission(
            id=1337,
            active=True,
            name="a",
            score=DEFAULT_TEST_CHALLENGE_SCORE,
            description="a",
            instruction="a",
            category_id=1,
            language=DEFAULT_TEST_LANGUAGE,
        )

    monkeypatch.setattr("src.data.repository.challenges.mission.RepositoryMission.get", f)
    return await f()


@pytest_asyncio.fixture
async def mock_mission_not_active(monkeypatch) -> Mission:
    async def f(*args, **kwargs) -> Mission:
        return Mission(
            id=1337,
            active=False,
            name="a",
            score=DEFAULT_TEST_CHALLENGE_SCORE,
            description="a",
            instruction="a",
            category_id=1,
            language=DEFAULT_TEST_LANGUAGE,
        )

    monkeypatch.setattr("src.data.repository.challenges.mission.RepositoryMission.get", f)
    return await f()


@pytest_asyncio.fixture
async def mock_mission_lst_check_filter(monkeypatch):
    async def f(*args, filter_obj: MissionFilter, **kwargs):
        assert isinstance(filter_obj, MissionFilter)
        assert filter_obj.active is True
        return []

    monkeypatch.setattr("src.data.repository.challenges.mission.RepositoryMission.lst", f)
