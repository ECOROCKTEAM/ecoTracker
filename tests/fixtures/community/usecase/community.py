import pytest_asyncio

from src.core.dto.community.community import CommunityCreateDTO
from src.core.entity.community import Community
from src.core.enum.community.privacy import CommunityPrivacyEnum
from src.core.interfaces.repository.community.community import CommunityFilter
from tests.fixtures.const import DEFAULT_TEST_USECASE_COMMUNITY_ID


@pytest_asyncio.fixture
async def mock_community_get_default(monkeypatch) -> Community:
    async def f(*args, **kwargs) -> Community:
        return Community(
            id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
            name="n",
            description="n",
            active=True,
            privacy=CommunityPrivacyEnum.PUBLIC,
        )

    monkeypatch.setattr("src.data.repository.community.RepositoryCommunity.get", f)
    return await f()


@pytest_asyncio.fixture
async def mock_community_get_not_active(monkeypatch) -> Community:
    async def f(*args, **kwargs) -> Community:
        return Community(
            id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
            name="n",
            description="n",
            active=False,
            privacy=CommunityPrivacyEnum.PUBLIC,
        )

    monkeypatch.setattr("src.data.repository.community.RepositoryCommunity.get", f)
    return await f()


@pytest_asyncio.fixture
async def mock_community_get_active_private(monkeypatch) -> Community:
    async def f(*args, **kwargs) -> Community:
        return Community(
            id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
            name="n",
            description="n",
            active=True,
            privacy=CommunityPrivacyEnum.PRIVATE,
        )

    monkeypatch.setattr("src.data.repository.community.RepositoryCommunity.get", f)
    return await f()


@pytest_asyncio.fixture
async def mock_community_create(monkeypatch) -> Community:
    async def f(*args, **kwargs) -> Community:
        return Community(
            id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
            name="n",
            description="n",
            active=True,
            privacy=CommunityPrivacyEnum.PUBLIC,
        )

    monkeypatch.setattr("src.data.repository.community.RepositoryCommunity.create", f)
    return await f()


@pytest_asyncio.fixture
async def mock_community_update(monkeypatch) -> Community:
    async def f(*args, **kwargs) -> Community:
        return Community(
            id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
            name="n",
            description="n",
            active=True,
            privacy=CommunityPrivacyEnum.PUBLIC,
        )

    monkeypatch.setattr("src.data.repository.community.RepositoryCommunity.update", f)
    return await f()


@pytest_asyncio.fixture
async def mock_community_lst(monkeypatch):
    async def f(*args, filter_obj: CommunityFilter, **kwargs) -> list[Community]:
        assert isinstance(filter_obj, CommunityFilter)
        return []

    monkeypatch.setattr("src.data.repository.community.RepositoryCommunity.lst", f)


@pytest_asyncio.fixture
async def mock_community_lst_check_filter(monkeypatch):
    async def f(*args, filter_obj: CommunityFilter, **kwargs) -> list[Community]:
        assert isinstance(filter_obj, CommunityFilter)
        assert isinstance(filter_obj.active, bool)
        assert isinstance(filter_obj.user_id, int)
        assert filter_obj.active is True
        return []

    monkeypatch.setattr("src.data.repository.community.RepositoryCommunity.lst", f)


@pytest_asyncio.fixture
async def mock_community_deactivate(monkeypatch) -> int:
    async def f(*args, **kwargs) -> int:
        return DEFAULT_TEST_USECASE_COMMUNITY_ID

    monkeypatch.setattr("src.data.repository.community.RepositoryCommunity.deactivate", f)
    return await f()


@pytest_asyncio.fixture
async def mock_community_get_by_code(monkeypatch) -> Community:
    async def f(*args, **kwargs) -> Community:
        return Community(
            id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
            name="n",
            description="n",
            active=True,
            privacy=CommunityPrivacyEnum.PUBLIC,
        )

    monkeypatch.setattr("src.data.repository.community.RepositoryCommunity.get_by_code", f)
    return await f()


@pytest_asyncio.fixture
async def mock_community_get_by_code_not_active(monkeypatch) -> Community:
    async def f(*args, **kwargs) -> Community:
        return Community(
            id=DEFAULT_TEST_USECASE_COMMUNITY_ID,
            name="n",
            description="n",
            active=False,
            privacy=CommunityPrivacyEnum.PUBLIC,
        )

    monkeypatch.setattr("src.data.repository.community.RepositoryCommunity.get_by_code", f)
    return await f()
