from sqlalchemy.ext.asyncio import AsyncSession

from src.core.interfaces.repository.challenges.mission import IRepositoryMission
from src.core.interfaces.repository.challenges.occupancy import (
    IRepositoryOccupancyCategory,
)
from src.core.interfaces.repository.challenges.task import IRepositoryTask
from src.core.interfaces.repository.group.group import IRepositoryGroup
from src.core.interfaces.repository.notifications.notifications import (
    INotificationRepository,
)
from src.core.interfaces.repository.score.group import IRepositoryGroupScore
from src.core.interfaces.repository.score.user import IRepositoryUserScore
from src.core.interfaces.repository.statistic.group import IRepositoryGroupStatistic
from src.core.interfaces.repository.statistic.user import IRepositoryUserStatistic
from src.core.interfaces.repository.subscription.subscription import (
    ISubscriptionRepository,
)
from src.core.interfaces.repository.user.contact import IUserContactRepository
from src.core.interfaces.repository.user.subscription import IUserSubscriptionRepository
from src.core.interfaces.repository.user.user import IUserRepository
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.data.repository.challenges.mission import RepositoryMission
from src.data.repository.challenges.occupancy_category import (
    RepositoryOccupancyCategory,
)
from src.data.repository.challenges.task import RepositoryTask
from src.data.repository.group import RepositoryGroup
from src.data.repository.notification import NotificationRepository
from src.data.repository.score.group_score import GroupScoreRepository
from src.data.repository.score.user_score import RepositoryUserScore
from src.data.repository.statistic.group import GroupStatisticRepository
from src.data.repository.statistic.user import UserStatisticRepository
from src.data.repository.subscription import SubscriptionRepository
from src.data.repository.user import UserRepository
from src.data.repository.user_contacts import UserContactRepository
from src.data.repository.user_subscription import UserSubscriptionRepository


class SqlAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session_factory) -> None:
        self.__session_factory = session_factory
        self.__session: AsyncSession | None = None
        self._group: IRepositoryGroup | None = None
        self._task: IRepositoryTask | None = None
        self._mission: IRepositoryMission | None = None
        self._score_user: IRepositoryUserScore | None = None
        self._score_group: IRepositoryGroupScore | None = None
        self._user_subscription: IUserSubscriptionRepository | None = None
        self._user: IUserRepository | None = None
        self._subscription: ISubscriptionRepository | None = None
        self._user_contact: IUserContactRepository | None = None
        self._user_statistic: IRepositoryUserStatistic | None = None
        self._group_statistic: IRepositoryGroupStatistic | None = None
        self._notifications: INotificationRepository | None = None

    @property
    def group_statistic(self) -> IRepositoryGroupStatistic:
        if self._group_statistic:
            return self._group_statistic
        raise ValueError("UoW not in context")

    @property
    def user_statistic(self) -> IRepositoryUserStatistic:
        if self._user_statistic:
            return self._user_statistic
        raise ValueError("UoW not in context")

    @property
    def user_contact(self) -> IUserContactRepository:
        if self._user_contact:
            return self._user_contact
        raise ValueError("UoW not in context")

    @property
    def user(self) -> IUserRepository:
        if self._user:
            return self._user
        raise ValueError("UoW not in context")

    @property
    def subscription(self) -> ISubscriptionRepository:
        if self._subscription:
            return self._subscription
        raise ValueError("UoW not in context")

    @property
    def user_subscription(self) -> IUserSubscriptionRepository:
        if self._user_subscription:
            return self._user_subscription
        raise ValueError("UoW not in context")

    @property
    def score_user(self) -> IRepositoryUserScore:
        if self._score_user:
            return self._score_user
        raise ValueError("UoW not in context")

    @property
    def score_group(self) -> IRepositoryGroupScore:
        if self._score_group:
            return self._score_group
        raise ValueError("UoW not in context")

    @property
    def group(self) -> IRepositoryGroup:
        if self._group:
            return self._group
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
    def notifications(self) -> INotificationRepository:
        if self._notifications:
            return self._notifications
        raise ValueError("UoW not in context")

    @property
    def _session(self) -> AsyncSession:
        if self.__session is None:
            raise ValueError("UoW not in context")
        return self.__session

    async def __aenter__(self) -> IUnitOfWork:
        self.__session = self.__session_factory()
        self._group = RepositoryGroup(self._session)
        self._task = RepositoryTask(self._session)
        self._mission = RepositoryMission(self._session)
        self._occupancy_category = RepositoryOccupancyCategory(self._session)
        self._score_user = RepositoryUserScore(self._session)
        self._score_group = GroupScoreRepository(self._session)
        self._user_subscription = UserSubscriptionRepository(self._session)
        self._subscription = SubscriptionRepository(self._session)
        self._user = UserRepository(self._session)
        self._user_contact = UserContactRepository(self._session)
        self._user_statistic = UserStatisticRepository(self._session)
        self._group_statistic = GroupStatisticRepository(self.__session)
        self._notifications = NotificationRepository(self._session)
        return self

    async def __aexit__(self, *args):
        await self._session.rollback()
        await self._session.close()
        self.__session = None

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
