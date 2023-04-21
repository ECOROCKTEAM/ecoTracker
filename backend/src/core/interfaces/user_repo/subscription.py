from abc import ABC, abstractmethod

from src.core.dto.mock import MockObj

class ISubscriptionRepository(ABC):


    @abstractmethod
    async def subscription_create(self, *, obj: SubscriptionCreateDTO) -> SubscriptionDTO:
        """Create subscription

        Args:
            obj (SubscriptionCreateDTO): DTO for creating subscription

        Returns:
            SubscriptionDTO: DTO of subscription object
        """

    @abstractmethod
    async def subscription_delete(self, *, subscription_id: int) -> int:
        """Delete subscription

        Args:
            subscription_id (int): subscruption identify

        Returns:
            int: id of deleted subscription
        """

    @abstractmethod
    async def subscription_get(self, *, subscription_id: int) -> SubscriptionDTO:
        """Get one subscription

        Args:
            subscription_id (int): subscruption identify

        Returns:
            SubscriptionDTO: DTO of subscription object
        """

    @abstractmethod # не думаю, что у нас много подписок будет, чтобы их фильтровать, сортировать и тп. Хотя исключать бесплатную можно, наверное...
    async def subscription_list(self, *, order_obj: MockObj = None) -> list[SubscriptionDTO]:
        """List of subscriptions

        Args:
            order_obj (MockObj, optional): order object. Defaults to None.

        Returns:
            list[SubscriptionDTO]: _description_
        """


    @abstractmethod
    async def subscription_type_constraint_create(self, *, obj: SubscriptionTypeConstraintCreateDTO) -> Constraint:
        """Create constraint for Subscription

        Args:
            obj (SubscriptionTypeConstraintCreate): DTO for create  new constrains

        Returns:
            Constraint: Constraint entity
        """

    @abstractmethod
    async def subscription_type_constraint_delete(self, *, constraint_id: int) -> int:
        """Delete constraint for Subscription

        Args:
            constraint_name (str): Name of delete constraint

        Returns:
            int: id of deleted constraint
        """
        pass

    @abstractmethod
    async def subscription_period_unit_create(self, *, obj: SubscriptionPeriodUnitCreateDTO) -> SubscriptionPeriodUnitDTO:
        """creating subscription period

        Args:
            obj (SubscriptionPeriodCreateDTO): DTO for creating subscription period

        Returns:
            SubscriptionPeriodDTO: New subscription period
        """

    @abstractmethod
    async def subscription_period_create(self, *, obj: SubscriptionPeriodCreateDTO) -> SubscriptionPeriodDTO:
        """Creating new period for subscriptios

        Args:
            obj (SubscriptionPeriodCreateDTO): DTO object for create period for subscriptions

        Returns:
            SubscriptionPeriodDTO: New period
        """
        pass


    @abstractmethod
    async def subscription_type_translate_create(self, *, obj: SubscriptionTypeCreateDTO) -> SubscriptionTypeDTO:
        """We'll create subscription_type if for it will be all translate.

        Args:
            obj (SubscriptionTypeCreateDTO): DTO for creating a new subscription type

        Returns:
            SubscriptionTypeDTO: subscription type
        """
        pass
