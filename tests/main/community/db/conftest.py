import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.repository.community import IRepositoryCommunity, RepositoryCommunity


@pytest.fixture(scope="function")
def repo(session: AsyncSession) -> IRepositoryCommunity:
    return RepositoryCommunity(session)
