import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.interfaces.auth.firebase import IFirebaseApplication
from src.core.interfaces.repository.auth import IAuthProviderRepository
from src.core.interfaces.repository.challenges.mission import IRepositoryMission
from src.core.interfaces.repository.score.group import IRepositoryGroupScore
from src.core.interfaces.repository.score.user import IRepositoryUserScore
from src.core.interfaces.repository.statistic.group import IRepositoryGroupStatistic
from src.core.interfaces.repository.statistic.user import IRepositoryUserStatistic
from src.core.interfaces.repository.user.contact import IUserContactRepository
from src.data.repository.auth import AuthProviderRepository
from src.data.repository.challenges.category import (
    IRepositoryOccupancyCategory,
    RepositoryOccupancyCategory,
)
from src.data.repository.challenges.mission import RepositoryMission
from src.data.repository.challenges.task import IRepositoryTask, RepositoryTask
from src.data.repository.group import IRepositoryGroup, RepositoryGroup
from src.data.repository.score.group_score import RepositoryGroupScore
from src.data.repository.score.user_score import RepositoryUserScore
from src.data.repository.statistic.group import GroupStatisticRepository
from src.data.repository.statistic.user import UserStatisticRepository
from src.data.repository.user import IUserRepository, UserRepository
from src.data.repository.user_contacts import UserContactRepository

# Repository


@pytest.fixture(scope="function")
def repo_mission(session: AsyncSession) -> IRepositoryMission:
    return RepositoryMission(db_context=session)


@pytest.fixture(scope="function")
def user_contact_repo(session: AsyncSession) -> IUserContactRepository:
    return UserContactRepository(db_context=session)


@pytest.fixture(scope="function")
def repo_auth(firebase_app: IFirebaseApplication) -> IAuthProviderRepository:
    return AuthProviderRepository(firebase_app=firebase_app)


@pytest.fixture(scope="function")
def repo_user_statistic(session: AsyncSession) -> IRepositoryUserStatistic:
    return UserStatisticRepository(db_context=session)


@pytest.fixture(scope="function")
def repo_group_statistic(session: AsyncSession) -> IRepositoryGroupStatistic:
    return GroupStatisticRepository(db_context=session)


@pytest.fixture(scope="function")
def repo_group(
    session: AsyncSession,
) -> IRepositoryGroup:
    return RepositoryGroup(session)


@pytest.fixture(scope="function")
def repo_user(
    session: AsyncSession,
) -> IUserRepository:
    return UserRepository(session)


@pytest.fixture(scope="function")
def repo_task(session: AsyncSession) -> IRepositoryTask:
    return RepositoryTask(session)


@pytest.fixture(scope="function")
def repo_user_score(session: AsyncSession) -> IRepositoryUserScore:
    return RepositoryUserScore(session)


@pytest.fixture(scope="function")
def repo_group_score(session: AsyncSession) -> IRepositoryGroupScore:
    return RepositoryGroupScore(session)


@pytest.fixture(scope="function")
def repo_category(session: AsyncSession) -> IRepositoryOccupancyCategory:
    return RepositoryOccupancyCategory(session)
