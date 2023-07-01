import pytest_asyncio

from src.core.entity.occupancy import OccupancyCategory
from tests.fixtures.const import DEFAULT_TEST_LANGUAGE


@pytest_asyncio.fixture
async def mock_category_get_default(monkeypatch) -> OccupancyCategory:
    async def f(*args, **kwargs) -> OccupancyCategory:
        return OccupancyCategory(id=1337, name="T_T", language=DEFAULT_TEST_LANGUAGE)

    monkeypatch.setattr("src.data.repository.challenges.occupancy_category.RepositoryOccupancyCategory.get", f)
    return await f()


@pytest_asyncio.fixture
async def mock_category_lst_ret_one(monkeypatch) -> list[OccupancyCategory]:
    async def f(*args, **kwargs) -> list[OccupancyCategory]:
        return [OccupancyCategory(id=1337, name="T_T", language=DEFAULT_TEST_LANGUAGE)]

    monkeypatch.setattr("src.data.repository.challenges.occupancy_category.RepositoryOccupancyCategory.lst", f)
    return await f()
