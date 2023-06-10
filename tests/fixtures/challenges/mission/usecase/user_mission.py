from datetime import datetime

import pytest_asyncio

from src.core.entity.mission import MissionUser
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.interfaces.repository.challenges.mission import MissionUserFilter
from tests.fixtures.const import (
    DEFAULT_TEST_OCCUPANCY_STATUS,
    DEFAULT_TEST_USECASE_USER_ID,
)


@pytest_asyncio.fixture
async def mock_user_mission_get(monkeypatch) -> MissionUser:
    async def f(*args, **kwargs) -> MissionUser:
        return MissionUser(
            id=1337,
            user_id=DEFAULT_TEST_USECASE_USER_ID,
            mission_id=321,
            date_start=datetime.now(),
            date_close=None,
            status=DEFAULT_TEST_OCCUPANCY_STATUS,
        )

    monkeypatch.setattr("src.data.repository.challenges.mission.RepositoryMission.user_mission_get", f)
    return await f()


@pytest_asyncio.fixture
async def mock_user_mission_finish_status(monkeypatch) -> MissionUser:
    async def f(*args, **kwargs) -> MissionUser:
        return MissionUser(
            id=1337,
            user_id=DEFAULT_TEST_USECASE_USER_ID,
            mission_id=321,
            date_start=datetime.now(),
            date_close=None,
            status=OccupancyStatusEnum.FINISH,
        )

    monkeypatch.setattr("src.data.repository.challenges.mission.RepositoryMission.user_mission_get", f)
    return await f()


@pytest_asyncio.fixture
async def mock_user_mission_lst(monkeypatch):
    async def f(*args, filter_obj: MissionUserFilter, **kwargs):
        assert isinstance(filter_obj, MissionUserFilter)
        return []

    monkeypatch.setattr("src.data.repository.challenges.mission.RepositoryMission.user_mission_lst", f)


@pytest_asyncio.fixture
async def mock_user_mission_create(monkeypatch) -> MissionUser:
    async def f(*args, **kwargs) -> MissionUser:
        return MissionUser(
            id=1337,
            user_id=DEFAULT_TEST_USECASE_USER_ID,
            mission_id=321,
            date_start=datetime.now(),
            date_close=None,
            status=DEFAULT_TEST_OCCUPANCY_STATUS,
        )

    monkeypatch.setattr("src.data.repository.challenges.mission.RepositoryMission.user_mission_create", f)
    return await f()


@pytest_asyncio.fixture
async def mock_user_mission_update(monkeypatch) -> MissionUser:
    async def f(*args, **kwargs) -> MissionUser:
        return MissionUser(
            id=1337,
            user_id=DEFAULT_TEST_USECASE_USER_ID,
            mission_id=321,
            date_start=datetime.now(),
            date_close=datetime.now(),
            status=OccupancyStatusEnum.FINISH,
        )

    monkeypatch.setattr("src.data.repository.challenges.mission.RepositoryMission.user_mission_update", f)
    return await f()
