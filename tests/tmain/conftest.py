import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.repository.group import IRepositoryGroup, RepositoryGroup


@pytest.fixture(scope="function")
def repo(
    session: AsyncSession,
) -> IRepositoryGroup:
    return RepositoryGroup(session)
