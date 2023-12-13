import pytest_asyncio

from src.core.dto.m2m.user.group import UserGroupDTO
from src.core.entity.user import User
from src.core.enum.group.role import GroupRoleEnum
from tests.fixtures.const import (
    DEFAULT_TEST_USECASE_GROUP_ID,
    DEFAULT_TEST_USECASE_USER_ID,
)


@pytest_asyncio.fixture
async def mock_group_user_get_default(monkeypatch) -> UserGroupDTO:
    async def f(*args, **kwargs) -> UserGroupDTO:
        return UserGroupDTO(
            user_id=DEFAULT_TEST_USECASE_USER_ID,
            group_id=DEFAULT_TEST_USECASE_GROUP_ID,
            role=GroupRoleEnum.ADMIN,
        )

    monkeypatch.setattr("src.data.repository.group.RepositoryGroup.user_get", f)
    return await f()


@pytest_asyncio.fixture
async def mock_group_user_get_admin(monkeypatch) -> UserGroupDTO:
    async def f(*args, **kwargs) -> UserGroupDTO:
        return UserGroupDTO(
            user_id=DEFAULT_TEST_USECASE_USER_ID,
            group_id=DEFAULT_TEST_USECASE_GROUP_ID,
            role=GroupRoleEnum.ADMIN,
        )

    monkeypatch.setattr("src.data.repository.group.RepositoryGroup.user_get", f)
    return await f()


@pytest_asyncio.fixture
async def mock_group_user_get_blocked(monkeypatch) -> UserGroupDTO:
    async def f(*args, **kwargs) -> UserGroupDTO:
        return UserGroupDTO(
            user_id=DEFAULT_TEST_USECASE_USER_ID,
            group_id=DEFAULT_TEST_USECASE_GROUP_ID,
            role=GroupRoleEnum.BLOCKED,
        )

    monkeypatch.setattr("src.data.repository.group.RepositoryGroup.user_get", f)
    return await f()


@pytest_asyncio.fixture
async def mock_group_user_add_superuser(monkeypatch, fxe_user_default: User) -> UserGroupDTO:
    async def f(*args, **kwargs) -> UserGroupDTO:
        return UserGroupDTO(
            user_id=DEFAULT_TEST_USECASE_USER_ID,
            group_id=DEFAULT_TEST_USECASE_GROUP_ID,
            role=GroupRoleEnum.SUPERUSER,
        )

    monkeypatch.setattr("src.data.repository.group.RepositoryGroup.user_add", f)
    return await f()


@pytest_asyncio.fixture
async def mock_group_user_add_user(monkeypatch, fxe_user_default: User) -> UserGroupDTO:
    async def f(*args, **kwargs) -> UserGroupDTO:
        return UserGroupDTO(
            user_id=DEFAULT_TEST_USECASE_USER_ID,
            group_id=DEFAULT_TEST_USECASE_GROUP_ID,
            role=GroupRoleEnum.USER,
        )

    monkeypatch.setattr("src.data.repository.group.RepositoryGroup.user_add", f)
    return await f()


@pytest_asyncio.fixture
async def mock_group_user_update_role(monkeypatch) -> UserGroupDTO:
    async def f(*args, **kwargs) -> UserGroupDTO:
        return UserGroupDTO(
            user_id=DEFAULT_TEST_USECASE_USER_ID,
            group_id=DEFAULT_TEST_USECASE_GROUP_ID,
            role=GroupRoleEnum.USER,
        )

    monkeypatch.setattr("src.data.repository.group.RepositoryGroup.user_role_update", f)
    return await f()


@pytest_asyncio.fixture
async def mock_group_user_get_superuser(monkeypatch) -> UserGroupDTO:
    async def f(*args, **kwargs) -> UserGroupDTO:
        return UserGroupDTO(
            user_id=DEFAULT_TEST_USECASE_USER_ID,
            group_id=DEFAULT_TEST_USECASE_GROUP_ID,
            role=GroupRoleEnum.SUPERUSER,
        )

    monkeypatch.setattr("src.data.repository.group.RepositoryGroup.user_get", f)
    return await f()


@pytest_asyncio.fixture
async def mock_group_user_get_user(monkeypatch) -> UserGroupDTO:
    async def f(*args, **kwargs) -> UserGroupDTO:
        return UserGroupDTO(
            user_id=DEFAULT_TEST_USECASE_USER_ID,
            group_id=DEFAULT_TEST_USECASE_GROUP_ID,
            role=GroupRoleEnum.USER,
        )

    monkeypatch.setattr("src.data.repository.group.RepositoryGroup.user_get", f)
    return await f()


@pytest_asyncio.fixture
async def mock_group_user_remove(monkeypatch) -> bool:
    async def f(*args, **kwargs) -> bool:
        return True

    monkeypatch.setattr("src.data.repository.group.RepositoryGroup.user_remove", f)
    return await f()


@pytest_asyncio.fixture
async def mock_group_user_list_ret_superusers_10(monkeypatch) -> list[UserGroupDTO]:
    async def f(*args, **kwargs) -> list[UserGroupDTO]:
        return [
            UserGroupDTO(
                user_id=str(x),
                group_id=DEFAULT_TEST_USECASE_GROUP_ID,
                role=GroupRoleEnum.SUPERUSER,
            )
            for x in range(10)
        ]

    monkeypatch.setattr("src.data.repository.group.RepositoryGroup.user_list", f)
    return await f()


@pytest_asyncio.fixture
async def mock_group_user_list_ret_superusers_1(monkeypatch) -> list[UserGroupDTO]:
    async def f(*args, **kwargs) -> list[UserGroupDTO]:
        return [
            UserGroupDTO(
                user_id=DEFAULT_TEST_USECASE_USER_ID,
                group_id=DEFAULT_TEST_USECASE_GROUP_ID,
                role=GroupRoleEnum.SUPERUSER,
            )
        ]

    monkeypatch.setattr("src.data.repository.group.RepositoryGroup.user_list", f)
    return await f()


@pytest_asyncio.fixture
async def mock_group_user_list_ret_superuser_admin(monkeypatch) -> list[UserGroupDTO]:
    async def f(*args, **kwargs) -> list[UserGroupDTO]:
        return [
            UserGroupDTO(
                user_id=DEFAULT_TEST_USECASE_USER_ID,
                group_id=DEFAULT_TEST_USECASE_GROUP_ID,
                role=GroupRoleEnum.SUPERUSER,
            ),
            UserGroupDTO(
                user_id=DEFAULT_TEST_USECASE_USER_ID,
                group_id=DEFAULT_TEST_USECASE_GROUP_ID,
                role=GroupRoleEnum.ADMIN,
            ),
        ]

    monkeypatch.setattr("src.data.repository.group.RepositoryGroup.user_list", f)
    return await f()


@pytest_asyncio.fixture
async def mock_group_user_list_ret_admin_superuser(monkeypatch) -> list[UserGroupDTO]:
    async def f(*args, **kwargs) -> list[UserGroupDTO]:
        return [
            UserGroupDTO(
                user_id="1",
                group_id=DEFAULT_TEST_USECASE_GROUP_ID,
                role=GroupRoleEnum.ADMIN,
            ),
            UserGroupDTO(
                user_id="2",
                group_id=DEFAULT_TEST_USECASE_GROUP_ID,
                role=GroupRoleEnum.SUPERUSER,
            ),
        ]

    monkeypatch.setattr("src.data.repository.group.RepositoryGroup.user_list", f)
    return await f()


@pytest_asyncio.fixture
async def mock_group_user_list_ret_user_user(monkeypatch) -> list[UserGroupDTO]:
    async def f(*args, **kwargs) -> list[UserGroupDTO]:
        return [
            UserGroupDTO(
                user_id=DEFAULT_TEST_USECASE_USER_ID,
                group_id=DEFAULT_TEST_USECASE_GROUP_ID,
                role=GroupRoleEnum.USER,
            ),
            UserGroupDTO(
                user_id=DEFAULT_TEST_USECASE_USER_ID,
                group_id=DEFAULT_TEST_USECASE_GROUP_ID,
                role=GroupRoleEnum.USER,
            ),
        ]

    monkeypatch.setattr("src.data.repository.group.RepositoryGroup.user_list", f)
    return await f()


@pytest_asyncio.fixture
async def mock_group_user_list_ret_not_found_current_user(monkeypatch) -> list[UserGroupDTO]:
    async def f(*args, **kwargs) -> list[UserGroupDTO]:
        return [
            UserGroupDTO(
                user_id=DEFAULT_TEST_USECASE_USER_ID,
                group_id=DEFAULT_TEST_USECASE_GROUP_ID,
                role=GroupRoleEnum.ADMIN,
            )
        ]

    monkeypatch.setattr("src.data.repository.group.RepositoryGroup.user_list", f)
    return await f()
