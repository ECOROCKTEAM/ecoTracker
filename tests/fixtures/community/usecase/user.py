import pytest_asyncio

from src.core.dto.m2m.user.community import UserCommunityDTO
from src.core.entity.user import User
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
async def mock_community_user_get_admin(monkeypatch) -> UserCommunityDTO:
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


@pytest_asyncio.fixture
async def mock_community_user_add_superuser(monkeypatch, fxe_user_default: User) -> UserCommunityDTO:
    async def f(*args, **kwargs) -> UserCommunityDTO:
        return UserCommunityDTO(
            user_id=DEFAULT_TEST_USECASE_USER_ID,
            community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
            role=CommunityRoleEnum.SUPERUSER,
        )

    monkeypatch.setattr("src.data.repository.community.RepositoryCommunity.user_add", f)
    return await f()


@pytest_asyncio.fixture
async def mock_community_user_add_user(monkeypatch, fxe_user_default: User) -> UserCommunityDTO:
    async def f(*args, **kwargs) -> UserCommunityDTO:
        return UserCommunityDTO(
            user_id=DEFAULT_TEST_USECASE_USER_ID,
            community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
            role=CommunityRoleEnum.USER,
        )

    monkeypatch.setattr("src.data.repository.community.RepositoryCommunity.user_add", f)
    return await f()


@pytest_asyncio.fixture
async def mock_community_user_update_role(monkeypatch) -> UserCommunityDTO:
    async def f(*args, **kwargs) -> UserCommunityDTO:
        return UserCommunityDTO(
            user_id=DEFAULT_TEST_USECASE_USER_ID,
            community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
            role=CommunityRoleEnum.USER,
        )

    monkeypatch.setattr("src.data.repository.community.RepositoryCommunity.user_role_update", f)
    return await f()


@pytest_asyncio.fixture
async def mock_community_user_get_superuser(monkeypatch) -> UserCommunityDTO:
    async def f(*args, **kwargs) -> UserCommunityDTO:
        return UserCommunityDTO(
            user_id=DEFAULT_TEST_USECASE_USER_ID,
            community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
            role=CommunityRoleEnum.SUPERUSER,
        )

    monkeypatch.setattr("src.data.repository.community.RepositoryCommunity.user_get", f)
    return await f()


@pytest_asyncio.fixture
async def mock_community_user_get_user(monkeypatch) -> UserCommunityDTO:
    async def f(*args, **kwargs) -> UserCommunityDTO:
        return UserCommunityDTO(
            user_id=DEFAULT_TEST_USECASE_USER_ID,
            community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
            role=CommunityRoleEnum.USER,
        )

    monkeypatch.setattr("src.data.repository.community.RepositoryCommunity.user_get", f)
    return await f()


@pytest_asyncio.fixture
async def mock_community_user_remove(monkeypatch) -> bool:
    async def f(*args, **kwargs) -> bool:
        return True

    monkeypatch.setattr("src.data.repository.community.RepositoryCommunity.user_remove", f)
    return await f()


@pytest_asyncio.fixture
async def mock_community_user_list_ret_superusers_10(monkeypatch) -> list[UserCommunityDTO]:
    async def f(*args, **kwargs) -> list[UserCommunityDTO]:
        return [
            UserCommunityDTO(
                user_id=x,
                community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
                role=CommunityRoleEnum.SUPERUSER,
            )
            for x in range(10)
        ]

    monkeypatch.setattr("src.data.repository.community.RepositoryCommunity.user_list", f)
    return await f()


@pytest_asyncio.fixture
async def mock_community_user_list_ret_superusers_1(monkeypatch) -> list[UserCommunityDTO]:
    async def f(*args, **kwargs) -> list[UserCommunityDTO]:
        return [
            UserCommunityDTO(
                user_id=DEFAULT_TEST_USECASE_USER_ID,
                community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
                role=CommunityRoleEnum.SUPERUSER,
            )
        ]

    monkeypatch.setattr("src.data.repository.community.RepositoryCommunity.user_list", f)
    return await f()


@pytest_asyncio.fixture
async def mock_community_user_list_ret_superuser_admin(monkeypatch) -> list[UserCommunityDTO]:
    async def f(*args, **kwargs) -> list[UserCommunityDTO]:
        return [
            UserCommunityDTO(
                user_id=DEFAULT_TEST_USECASE_USER_ID,
                community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
                role=CommunityRoleEnum.SUPERUSER,
            ),
            UserCommunityDTO(
                user_id=DEFAULT_TEST_USECASE_USER_ID,
                community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
                role=CommunityRoleEnum.ADMIN,
            ),
        ]

    monkeypatch.setattr("src.data.repository.community.RepositoryCommunity.user_list", f)
    return await f()


@pytest_asyncio.fixture
async def mock_community_user_list_ret_admin_superuser(monkeypatch) -> list[UserCommunityDTO]:
    async def f(*args, **kwargs) -> list[UserCommunityDTO]:
        return [
            UserCommunityDTO(
                user_id=1,
                community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
                role=CommunityRoleEnum.ADMIN,
            ),
            UserCommunityDTO(
                user_id=2,
                community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
                role=CommunityRoleEnum.SUPERUSER,
            ),
        ]

    monkeypatch.setattr("src.data.repository.community.RepositoryCommunity.user_list", f)
    return await f()


@pytest_asyncio.fixture
async def mock_community_user_list_ret_user_user(monkeypatch) -> list[UserCommunityDTO]:
    async def f(*args, **kwargs) -> list[UserCommunityDTO]:
        return [
            UserCommunityDTO(
                user_id=DEFAULT_TEST_USECASE_USER_ID,
                community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
                role=CommunityRoleEnum.USER,
            ),
            UserCommunityDTO(
                user_id=DEFAULT_TEST_USECASE_USER_ID,
                community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
                role=CommunityRoleEnum.USER,
            ),
        ]

    monkeypatch.setattr("src.data.repository.community.RepositoryCommunity.user_list", f)
    return await f()


@pytest_asyncio.fixture
async def mock_community_user_list_ret_not_found_current_user(monkeypatch) -> list[UserCommunityDTO]:
    async def f(*args, **kwargs) -> list[UserCommunityDTO]:
        return [
            UserCommunityDTO(
                user_id=DEFAULT_TEST_USECASE_USER_ID,
                community_id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
                role=CommunityRoleEnum.ADMIN,
            )
        ]

    monkeypatch.setattr("src.data.repository.community.RepositoryCommunity.user_list", f)
    return await f()
