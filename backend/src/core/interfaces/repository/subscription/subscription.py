from abc import ABC, abstractmethod

from src.core.dto.subscription.period import SubscriptionPeriodCreateDTO, SubscriptionPeriodDTO
from src.core.dto.subscription.type import SubscriptionTypeConstraintDTO, SubscriptionTypeCreateDTO, SubscriptionTypeDTO
from src.core.dto.subscription.period_unit import SubscriptionPeriodUnitCreateDTO, SubscriptionPeriodUnitDTO
from src.core.dto.m2m.subscription_type.constraint import SubscriptionTypeConstrainCreateDTO, SubscriptionTypeConstrainDTO
from src.core.dto.subscription.constraint import SubscriptionConstraintDTO, SubscriptionConstraintCreateDTO
from src.core.entity.subscription import Subscription, SubscriptionCreateDTO
from src.core.dto.mock import MockObj


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
    async def list(self, *, filter_obj: MockObj = None) -> list[Subscription]:
        """List of subscriptions

        Args:
            filter_obj (MockObj, optional): filter object. Defaults to None.

        Returns:
            list[SubscriptionDTO]: list of Subscription entity
        """

    @abstractmethod
    async def constraint_get(self, *, id: int) -> SubscriptionConstraintDTO:
        """Get constraint

        Args:
            id (int): int of constraint object

        Returns:
            SubscriptionConstraintDTO: DTO of constraint object
        """

    @abstractmethod
    async def constraint_create(self, *, obj: SubscriptionConstraintCreateDTO) -> SubscriptionConstraintDTO:
        """Create constraint

        Args:
            obj (SubscriptionConstraintCreateDTO): DTO for create constraint object

        Returns:
            SubscriptionConstraintDTO: DTO of constraint object
        """

    @abstractmethod
    async def type_constraint_create(self, *, obj: SubscriptionTypeConstrainCreateDTO) -> SubscriptionTypeConstrainDTO:
        """Create constraint for Subscription

        Args:
            obj (SubscriptionTypeConstrainCreateDTO): DTO for create new subscription type constraint object

        Returns:
            SubscriptionTypeConstrainDTO: DTO of subscription type constraint object
        """

    @abstractmethod
    async def type_constraint_delete(self, *, id: int) -> int:
        """Delete constraint for Subscription

        Args:
            id (int): id of delete constraint

        Returns:
            int: id of deleted constraint
        """

    @abstractmethod
    async def period_unit_create(self, *, obj: SubscriptionPeriodUnitCreateDTO) -> SubscriptionPeriodUnitDTO:
        """Subscription unit period create

        Args:
            obj (SubscriptionPeriodUnitCreateDTO): DTO for creating subscription unit period

        Returns:
            SubscriptionPeriodUnitDTO: DTO of subscription unit period
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

    @abstractmethod
    async def type_list(self) -> list[SubscriptionTypeDTO]:
        """Subscription type list

        Returns:
            list[SubscriptionTypeDTO]: List of subscription type DTO objects
        """

    @abstractmethod
    async def type_create(self, *, obj: SubscriptionTypeCreateDTO) -> SubscriptionTypeDTO:
        """ Subscription type create

        Args:
            obj (SubscriptionTypeCreateDTO): DTO for creating new subscription type object 

        Returns:
            SubscriptionTypeDTO: DTO of subscription type object
        """

    @abstractmethod
    async def type_constraint_list(self, *, subscription_type: MockObj = None) -> list[SubscriptionTypeConstraintDTO]:
        """List of type constraint objects

        Args:
            subscription_type (MockObj): Filter list by subscription type object. Default None.

        Returns:
            list[SubscriptionTypeConstraintDTO]: List of DTO type constraint objects
        """