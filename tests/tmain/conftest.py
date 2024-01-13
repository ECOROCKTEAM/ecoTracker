import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.repository.group import IRepositoryGroup, RepositoryGroup

# Repository


@pytest.fixture(scope="function")
def repo_group(
    session: AsyncSession,
) -> IRepositoryGroup:
    return RepositoryGroup(session)
