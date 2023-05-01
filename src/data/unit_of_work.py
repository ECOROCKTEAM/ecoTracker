from sqlalchemy.ext.asyncio import AsyncSession

from src.core.interfaces.repository.community.community import IRepositoryCommunity
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.data.repository.community import RepositoryCommunity


class SqlAlchemyUnitOfWork(IUnitOfWork):
    @property
    def community(self) -> IRepositoryCommunity:
        if self._community:
            return self._community
        raise ValueError("UoW not in context")

    def __init__(self, session_factory) -> None:
        self.session_factory = session_factory
        self._session: AsyncSession | None = None
        self._community: IRepositoryCommunity | None = None

    async def __aenter__(self) -> IUnitOfWork:
        self._session = self.session_factory()
        self._community = RepositoryCommunity(self._session)
        return self

    async def __aexit__(self, *args):
        await self._session.rollback()
        await self._session.close()
        self._session = None

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
