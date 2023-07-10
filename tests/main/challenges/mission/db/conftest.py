import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.repository.challenges.mission import RepositoryMission


@pytest.fixture(scope="function")
def repo(session: AsyncSession) -> RepositoryMission:
    return RepositoryMission(session)
