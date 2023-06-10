from sqlalchemy.ext.asyncio import AsyncSession

from src.core.interfaces.repository.challenges.mission import IRepositoryMission
from src.core.interfaces.repository.challenges.occupancy import (
    IRepositoryOccupancyCategory,
)
from src.core.interfaces.repository.challenges.task import IRepositoryTask
from src.core.interfaces.repository.community.community import IRepositoryCommunity
from src.core.interfaces.repository.score.community import IRepositoryCommunityScore
from src.core.interfaces.repository.score.user import IRepositoryUserScore
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.data.repository.challenges.mission import RepositoryMission
from src.data.repository.challenges.occupancy_category import (
    RepositoryOccupancyCategory,
)
from src.data.repository.challenges.task import RepositoryTask
from src.data.repository.community import RepositoryCommunity
from src.data.repository.score.community_score import CommunityScoreRepository
from src.data.repository.score.user_score import UserScoreRepository


class SqlAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session_factory) -> None:
        self.__session_factory = session_factory
        self.__session: AsyncSession | None = None
        self._community: IRepositoryCommunity | None = None
        self._task: IRepositoryTask | None = None
        self._mission: IRepositoryMission | None = None
        self._score_user: IRepositoryUserScore | None = None
        self._score_community: IRepositoryCommunityScore | None = None

    @property
    def score_user(self) -> IRepositoryUserScore:
        if self._score_user:
            return self._score_user
        raise ValueError("UoW not in context")

    @property
    def score_community(self) -> IRepositoryCommunityScore:
        if self._score_community:
            return self._score_community
        raise ValueError("UoW not in context")

    @property
    def community(self) -> IRepositoryCommunity:
        if self._community:
            return self._community
        raise ValueError("UoW not in context")

    @property
    def mission(self) -> IRepositoryMission:
        if self._mission:
            return self._mission
        raise ValueError("UoW not in context")

    @property
    def task(self) -> IRepositoryTask:
        if self._task:
            return self._task
        raise ValueError("UoW not in context")

    @property
    def occupancy_category(self) -> IRepositoryOccupancyCategory:
        if self._occupancy_category:
            return self._occupancy_category
        raise ValueError("UoW not in context")

    @property
    def _session(self) -> AsyncSession:
        if self.__session is None:
            raise ValueError("UoW not in context")
        return self.__session

    async def __aenter__(self) -> IUnitOfWork:
        self.__session = self.__session_factory()
        self._community = RepositoryCommunity(self._session)
        self._task = RepositoryTask(self._session)
        self._mission = RepositoryMission(self._session)
        self._occupancy_category = RepositoryOccupancyCategory(self._session)
        self._score_user = UserScoreRepository(self._session)
        self._score_community = CommunityScoreRepository(self._session)
        return self

    async def __aexit__(self, *args):
        await self._session.rollback()
        await self._session.close()
        self.__session = None

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
