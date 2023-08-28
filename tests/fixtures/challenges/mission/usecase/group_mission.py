from datetime import datetime

import pytest_asyncio

from src.core.entity.mission import MissionGroup
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.interfaces.repository.challenges.mission import MissionGroupFilter
from tests.fixtures.const import (
    DEFAULT_TEST_OCCUPANCY_STATUS,
    DEFAULT_TEST_USECASE_GROUP_ID,
)


@pytest_asyncio.fixture
async def mock_group_mission_get(monkeypatch) -> MissionGroup:
    async def f(*args, **kwargs) -> MissionGroup:
        return MissionGroup(
            id=1337,
            group_id=DEFAULT_TEST_USECASE_GROUP_ID,
            author="a",
            mission_id=321,
            date_start=datetime.now(),
            date_close=None,
            status=DEFAULT_TEST_OCCUPANCY_STATUS,
        )

    monkeypatch.setattr("src.data.repository.challenges.mission.RepositoryMission.group_mission_get", f)
    return await f()


@pytest_asyncio.fixture
async def mock_group_mission_status_finish(monkeypatch) -> MissionGroup:
    async def f(*args, **kwargs) -> MissionGroup:
        return MissionGroup(
            id=1337,
            group_id=DEFAULT_TEST_USECASE_GROUP_ID,
            author="a",
            mission_id=321,
            date_start=datetime.now(),
            date_close=None,
            status=OccupancyStatusEnum.FINISH,
        )

    monkeypatch.setattr("src.data.repository.challenges.mission.RepositoryMission.group_mission_get", f)
    return await f()


@pytest_asyncio.fixture
async def mock_group_mission_create(monkeypatch) -> MissionGroup:
    async def f(*args, **kwargs) -> MissionGroup:
        return MissionGroup(
            id=1337,
            group_id=DEFAULT_TEST_USECASE_GROUP_ID,
            author="a",
            mission_id=321,
            date_start=datetime.now(),
            date_close=None,
            status=DEFAULT_TEST_OCCUPANCY_STATUS,
        )

    monkeypatch.setattr("src.data.repository.challenges.mission.RepositoryMission.group_mission_create", f)
    return await f()


@pytest_asyncio.fixture
async def mock_group_mission_update(monkeypatch) -> MissionGroup:
    async def f(*args, **kwargs) -> MissionGroup:
        return MissionGroup(
            id=1337,
            group_id=DEFAULT_TEST_USECASE_GROUP_ID,
            author="a",
            mission_id=321,
            date_start=datetime.now(),
            date_close=datetime.now(),
            status=OccupancyStatusEnum.FINISH,
        )

    monkeypatch.setattr("src.data.repository.challenges.mission.RepositoryMission.group_mission_update", f)
    return await f()
