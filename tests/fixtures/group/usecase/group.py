from datetime import datetime, timedelta

import pytest_asyncio

from src.core.dto.group.group import GroupCreateDTO
from src.core.dto.group.invite import GroupInviteDTO, GroupInviteUpdateDTO
from src.core.entity.group import Group
from src.core.enum.group.privacy import GroupPrivacyEnum
from src.core.interfaces.repository.group.group import GroupFilter
from tests.fixtures.const import DEFAULT_TEST_USECASE_GROUP_ID
from tests.utils import get_random_str


@pytest_asyncio.fixture
async def mock_group_get_default(monkeypatch) -> Group:
    async def f(*args, **kwargs) -> Group:
        return Group(
            id=DEFAULT_TEST_USECASE_GROUP_ID,
            name="n",
            description="n",
            active=True,
            privacy=GroupPrivacyEnum.PUBLIC,
        )

    monkeypatch.setattr("src.data.repository.group.RepositoryGroup.get", f)
    return await f()


@pytest_asyncio.fixture
async def mock_group_get_not_active(monkeypatch) -> Group:
    async def f(*args, **kwargs) -> Group:
        return Group(
            id=DEFAULT_TEST_USECASE_GROUP_ID,
            name="n",
            description="n",
            active=False,
            privacy=GroupPrivacyEnum.PUBLIC,
        )

    monkeypatch.setattr("src.data.repository.group.RepositoryGroup.get", f)
    return await f()


@pytest_asyncio.fixture
async def mock_group_get_active_private(monkeypatch) -> Group:
    async def f(*args, **kwargs) -> Group:
        return Group(
            id=DEFAULT_TEST_USECASE_GROUP_ID,
            name="n",
            description="n",
            active=True,
            privacy=GroupPrivacyEnum.PRIVATE,
        )

    monkeypatch.setattr("src.data.repository.group.RepositoryGroup.get", f)
    return await f()


@pytest_asyncio.fixture
async def mock_group_create(monkeypatch) -> Group:
    async def f(*args, **kwargs) -> Group:
        return Group(
            id=DEFAULT_TEST_USECASE_GROUP_ID,
            name="n",
            description="n",
            active=True,
            privacy=GroupPrivacyEnum.PUBLIC,
        )

    monkeypatch.setattr("src.data.repository.group.RepositoryGroup.create", f)
    return await f()


@pytest_asyncio.fixture
async def mock_group_update(monkeypatch) -> Group:
    async def f(*args, **kwargs) -> Group:
        return Group(
            id=DEFAULT_TEST_USECASE_GROUP_ID,
            name="n",
            description="n",
            active=True,
            privacy=GroupPrivacyEnum.PUBLIC,
        )

    monkeypatch.setattr("src.data.repository.group.RepositoryGroup.update", f)
    return await f()


@pytest_asyncio.fixture
async def mock_group_lst(monkeypatch):
    async def f(*args, filter_obj: GroupFilter, **kwargs) -> list[Group]:
        assert isinstance(filter_obj, GroupFilter)
        return []

    monkeypatch.setattr("src.data.repository.group.RepositoryGroup.lst", f)


@pytest_asyncio.fixture
async def mock_group_lst_check_filter(monkeypatch):
    async def f(*args, filter_obj: GroupFilter, **kwargs) -> list[Group]:
        assert isinstance(filter_obj, GroupFilter)
        assert isinstance(filter_obj.active, bool)
        assert isinstance(filter_obj.user_id, str)
        assert filter_obj.active is True
        return []

    monkeypatch.setattr("src.data.repository.group.RepositoryGroup.lst", f)


@pytest_asyncio.fixture
async def mock_group_deactivate(monkeypatch) -> int:
    async def f(*args, **kwargs) -> int:
        return DEFAULT_TEST_USECASE_GROUP_ID

    monkeypatch.setattr("src.data.repository.group.RepositoryGroup.deactivate", f)
    return await f()


@pytest_asyncio.fixture
async def mock_group_get_by_code(monkeypatch) -> Group:
    async def f(*args, **kwargs) -> Group:
        return Group(
            id=DEFAULT_TEST_USECASE_GROUP_ID,
            name="n",
            description="n",
            active=True,
            privacy=GroupPrivacyEnum.PUBLIC,
        )

    monkeypatch.setattr("src.data.repository.group.RepositoryGroup.get_by_code", f)
    return await f()


@pytest_asyncio.fixture
async def mock_group_get_by_code_not_active(monkeypatch) -> Group:
    async def f(*args, **kwargs) -> Group:
        return Group(
            id=DEFAULT_TEST_USECASE_GROUP_ID,
            name="n",
            description="n",
            active=False,
            privacy=GroupPrivacyEnum.PUBLIC,
        )

    monkeypatch.setattr("src.data.repository.group.RepositoryGroup.get_by_code", f)
    return await f()


@pytest_asyncio.fixture
async def mock_group_code_get_default(monkeypatch) -> GroupInviteDTO:
    async def f(*args, **kwargs) -> GroupInviteDTO:
        return GroupInviteDTO(
            group_id=DEFAULT_TEST_USECASE_GROUP_ID,
            code=get_random_str(),
            expire_time=datetime.now() + timedelta(seconds=30),
        )

    monkeypatch.setattr("src.data.repository.group.RepositoryGroup.code_get", f)
    return await f()


@pytest_asyncio.fixture
async def mock_group_code_get_code_none(monkeypatch) -> GroupInviteDTO:
    async def f(*args, **kwargs) -> GroupInviteDTO:
        return GroupInviteDTO(group_id=DEFAULT_TEST_USECASE_GROUP_ID, code=None, expire_time=None)

    monkeypatch.setattr("src.data.repository.group.RepositoryGroup.code_get", f)
    return await f()


@pytest_asyncio.fixture
async def mock_group_code_set_default(monkeypatch):
    async def f(self, id, obj: GroupInviteUpdateDTO) -> GroupInviteDTO:
        return GroupInviteDTO(
            group_id=id,
            code=obj.code,
            expire_time=obj.expire_time,
        )

    monkeypatch.setattr("src.data.repository.group.RepositoryGroup.code_set", f)
