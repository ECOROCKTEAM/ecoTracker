from abc import ABC, abstractmethod

from src.core.interfaces.repository.challenges.mission import IRepositoryMission
from src.core.interfaces.repository.challenges.occupancy import (
    IRepositoryOccupancyCategory,
)
from src.core.interfaces.repository.challenges.task import IRepositoryTask
from src.core.interfaces.repository.group.group import IRepositoryGroup
from src.core.interfaces.repository.score.group import IRepositoryGroupScore
from src.core.interfaces.repository.score.user import IRepositoryUserScore
from src.core.interfaces.repository.subscription.subscription import (
    ISubscriptionRepository,
)
from src.core.interfaces.repository.user.contact import IUserContactRepository
from src.core.interfaces.repository.user.subscription import IUserSubscriptionRepository
from src.core.interfaces.repository.user.user import IUserRepository


class IUnitOfWork(ABC):
    @property
    @abstractmethod
    def user_contact(self) -> IUserContactRepository:
        ...

    @property
    @abstractmethod
    def user_subscription(self) -> IUserSubscriptionRepository:
        ...

    @property
    @abstractmethod
    def subscription(self) -> ISubscriptionRepository:
        ...

    @property
    @abstractmethod
    def user(self) -> IUserRepository:
        ...

    @property
    @abstractmethod
    def group(self) -> IRepositoryGroup:
        ...

    @property
    @abstractmethod
    def score_user(self) -> IRepositoryUserScore:
        ...

    @property
    @abstractmethod
    def score_group(self) -> IRepositoryGroupScore:
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
