import abc
from src.core.interfaces.repository.challenges.mission import IRepositoryMission
from src.core.interfaces.repository.challenges.task import IRepositoryTask
from src.core.interfaces.repository.community.community import IRepositoryCommunity


class IUnitOfWork(abc.ABC):
    @property
    @abc.abstractmethod
    def community(self) -> IRepositoryCommunity:
        ...

    @property
    @abc.abstractmethod
    def mission(self) -> IRepositoryMission:
        ...

    @property
    @abc.abstractmethod
    def task(self) -> IRepositoryTask:
        ...

    @abc.abstractmethod
    async def __aenter__(self) -> "IUnitOfWork":
        ...

    @abc.abstractmethod
    async def __aexit__(self, *args):
        ...

    @abc.abstractmethod
    async def commit(self):
        ...

    @abc.abstractmethod
    async def rollback(self):
        ...
