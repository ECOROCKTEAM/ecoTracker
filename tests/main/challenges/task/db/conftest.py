import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.repository.challenges.task import IRepositoryTask, RepositoryTask


@pytest.fixture(scope="function")
def repo(session: AsyncSession) -> IRepositoryTask:
    return RepositoryTask(session)
