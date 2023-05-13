from abc import ABC, abstractmethod

from src.core.interfaces.repository.challenges.mission import IRepositoryMission
from src.core.interfaces.repository.challenges.occupancy import IRepositoryOccupancyCategory
from src.core.interfaces.repository.challenges.task import IRepositoryTask
from src.core.interfaces.repository.community.community import IRepositoryCommunity


class IUnitOfWork(ABC):
    @property
    @abstractmethod
    def community(self) -> IRepositoryCommunity:
        ...

    @property
    @abstractmethod
    def mission(self) -> IRepositoryMission:
        ...

    @property
    @abstractmethod
    def task(self) -> IRepositoryTask:
        ...

    @property
    @abstractmethod
    def occupancy_category(self) -> IRepositoryOccupancyCategory:
        ...

    @abstractmethod
    async def __aenter__(self) -> "IUnitOfWork":
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...
