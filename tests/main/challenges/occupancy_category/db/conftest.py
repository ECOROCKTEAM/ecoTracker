import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.repository.challenges.occupancy_category import (
    IRepositoryOccupancyCategory,
    RepositoryOccupancyCategory,
)


@pytest.fixture(scope="function")
def repo(session: AsyncSession) -> IRepositoryOccupancyCategory:
    return RepositoryOccupancyCategory(session)
