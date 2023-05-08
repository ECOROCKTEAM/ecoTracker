from sqlalchemy.ext.asyncio import AsyncSession
from src.core.interfaces.repository.challenges.mission import IRepositoryMission
from src.core.interfaces.repository.challenges.task import IRepositoryTask

from src.core.interfaces.repository.community.community import IRepositoryCommunity
from src.core.interfaces.repository.score.score import IRepositoryScore
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.data.repository.community import RepositoryCommunity


class SqlAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session_factory) -> None:
        self.__session_factory = session_factory
        self.__session: AsyncSession | None = None
        self._community: IRepositoryCommunity | None = None
        self._score: IRepositoryScore | None = None

    @property
    def score(self) -> IRepositoryScore:
        if self._score:
            return self._score
        raise ValueError("UoW not in context")

    @property
    def community(self) -> IRepositoryCommunity:
        if self._community:
            return self._community
        raise ValueError("UoW not in context")

    @property
    def mission(self) -> IRepositoryMission:
        ...

    @property
    def task(self) -> IRepositoryTask:
        ...

    @property
    def _session(self) -> AsyncSession:
        if self.__session is None:
            raise ValueError("UoW not in context")
        return self.__session

    async def __aenter__(self) -> IUnitOfWork:
        self.__session = self.__session_factory()
        self._community = RepositoryCommunity(self._session)
        return self

    async def __aexit__(self, *args):
        await self._session.rollback()
        await self._session.close()
        self.__session = None

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
