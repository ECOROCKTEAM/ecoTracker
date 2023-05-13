from abc import ABC, abstractmethod

from src.core.dto.mock import MockObj
from src.core.dto.subscription.period import SubscriptionPeriodCreateDTO, SubscriptionPeriodDTO
from src.core.entity.subscription import Subscription, SubscriptionCreateDTO


class ISubscriptionRepository(ABC):
    @abstractmethod
    async def create(self, *, obj: SubscriptionCreateDTO) -> Subscription:
        """Create subscription

        Args:
            obj (SubscriptionCreateDTO): DTO for creating subscription

        Returns:
            Subscription: Subscription entity
        """

    @abstractmethod
    async def delete(self, *, id: int) -> int:
        """Delete subscription

        Args:
            id (int): subscruption identify

        Returns:
            int: id of deleted subscription
        """

    @abstractmethod
    async def get(self, *, id: int) -> Subscription:
        """Get one subscription

        Args:SubscriptionTypeConstraintCreateDTO
            id (int): subscruption identify

        Returns:
            Subscription: Subscription entity
        """

    @abstractmethod
    async def list(self, *, filter_obj: MockObj | None = None) -> list[Subscription]:
        """List of subscriptions

        Args:
            filter_obj (MockObj, optional): filter object. Defaults to None.

        Returns:
            list[SubscriptionDTO]: list of Subscription entity
        """

    @abstractmethod
    async def period_create(self, *, obj: SubscriptionPeriodCreateDTO) -> SubscriptionPeriodDTO:
        """Subscription period create

        Args:
            obj (SubscriptionPeriodCreateDTO): DTO for create subscriptions period

        Returns:
            SubscriptionPeriodDTO: DTO of subscription period
        """

    @abstractmethod
    async def period_get(self, *, id: int) -> SubscriptionPeriodDTO:
        """Get subscription period

        Args:
            id (int): int edentify of subscriprion period object

        Returns:
            SubscriptionPeriodDTO: DTO of subscription period object
        """

    @abstractmethod
    async def period_list(self) -> list[SubscriptionPeriodDTO]:
        """List of subscription period

        Returns:
            list[SubscriptionPeriodDTO]: List of DTO subscription period objects
        """
