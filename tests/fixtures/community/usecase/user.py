import pytest_asyncio

from src.core.dto.m2m.user.community import UserCommunityDTO
from src.core.enum.community.role import CommunityRoleEnum
from tests.fixtures.const import (
    DEFAULT_TEST_USECASE_COMMUNITY_ID,
    DEFAULT_TEST_USECASE_USER_ID,
)


@pytest_asyncio.fixture
async def mock_community_user_get_default(monkeypatch) -> UserCommunityDTO:
    async def f(*args, **kwargs) -> UserCommunityDTO:
        return UserCommunityDTO(
            user_id=DEFAULT_TEST_USECASE_USER_ID,
            community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
            role=CommunityRoleEnum.ADMIN,
        )

    monkeypatch.setattr("src.data.repository.community.RepositoryCommunity.user_get", f)
    return await f()


@pytest_asyncio.fixture
async def mock_community_user_get_blocked(monkeypatch) -> UserCommunityDTO:
    async def f(*args, **kwargs) -> UserCommunityDTO:
        return UserCommunityDTO(
            user_id=DEFAULT_TEST_USECASE_USER_ID,
            community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
            role=CommunityRoleEnum.BLOCKED,
        )

    monkeypatch.setattr("src.data.repository.community.RepositoryCommunity.user_get", f)
    return await f()
