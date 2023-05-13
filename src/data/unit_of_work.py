from sqlalchemy.ext.asyncio import AsyncSession
from src.core.interfaces.repository.challenges.mission import IRepositoryMission
from src.core.interfaces.repository.challenges.occupancy import IRepositoryOccupancyCategory
from src.core.interfaces.repository.challenges.task import IRepositoryTask

from src.core.interfaces.repository.community.community import IRepositoryCommunity
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.data.repository.challenges.mission import RepositoryMission
from src.data.repository.challenges.occupancy_category import RepositoryOccupancyCategory
from src.data.repository.community import RepositoryCommunity


class SqlAlchemyUnitOfWork(IUnitOfWork):
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
        return super().task

    @property
    def occupancy_category(self) -> IRepositoryOccupancyCategory:
        if self._occupancy_category:
            return self._occupancy_category
        raise ValueError("UoW not in context")

    def __init__(self, session_factory) -> None:
        self.__session_factory = session_factory
        self.__session: AsyncSession | None = None
        self._community: IRepositoryCommunity | None = None

    @property
    def _session(self) -> AsyncSession:
        if self.__session is None:
            raise ValueError("UoW not in context")
        return self.__session

    async def __aenter__(self) -> IUnitOfWork:
        self.__session = self.__session_factory()
        self._community = RepositoryCommunity(self._session)
        self._mission = RepositoryMission(self._session)
        self._occupancy_category = RepositoryOccupancyCategory(self._session)
        return self

    async def __aexit__(self, *args):
        await self._session.rollback()
        await self._session.close()
        self.__session = None

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
