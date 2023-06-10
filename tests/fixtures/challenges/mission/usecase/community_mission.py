from datetime import datetime

import pytest_asyncio

from src.core.entity.mission import MissionCommunity
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.interfaces.repository.challenges.mission import MissionCommunityFilter
from tests.fixtures.const import (
    DEFAULT_TEST_OCCUPANCY_STATUS,
    DEFAULT_TEST_USECASE_COMMUNITY_ID,
)


@pytest_asyncio.fixture
async def mock_community_mission_get(monkeypatch) -> MissionCommunity:
    async def f(*args, **kwargs) -> MissionCommunity:
        return MissionCommunity(
            id=1337,
            community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
            author="a",
            mission_id=321,
            date_start=datetime.now(),
            date_close=None,
            status=DEFAULT_TEST_OCCUPANCY_STATUS,
        )

    monkeypatch.setattr("src.data.repository.challenges.mission.RepositoryMission.community_mission_get", f)
    return await f()


@pytest_asyncio.fixture
async def mock_community_mission_status_finish(monkeypatch) -> MissionCommunity:
    async def f(*args, **kwargs) -> MissionCommunity:
        return MissionCommunity(
            id=1337,
            community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
            author="a",
            mission_id=321,
            date_start=datetime.now(),
            date_close=None,
            status=OccupancyStatusEnum.FINISH,
        )

    monkeypatch.setattr("src.data.repository.challenges.mission.RepositoryMission.community_mission_get", f)
    return await f()


@pytest_asyncio.fixture
async def mock_community_mission_create(monkeypatch) -> MissionCommunity:
    async def f(*args, **kwargs) -> MissionCommunity:
        return MissionCommunity(
            id=1337,
            community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
            author="a",
            mission_id=321,
            date_start=datetime.now(),
            date_close=None,
            status=DEFAULT_TEST_OCCUPANCY_STATUS,
        )

    monkeypatch.setattr("src.data.repository.challenges.mission.RepositoryMission.community_mission_create", f)
    return await f()


@pytest_asyncio.fixture
async def mock_community_mission_update(monkeypatch) -> MissionCommunity:
    async def f(*args, **kwargs) -> MissionCommunity:
        return MissionCommunity(
            id=1337,
            community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
            author="a",
            mission_id=321,
            date_start=datetime.now(),
            date_close=datetime.now(),
            status=OccupancyStatusEnum.FINISH,
        )

    monkeypatch.setattr("src.data.repository.challenges.mission.RepositoryMission.community_mission_update", f)
    return await f()
