from abc import ABC, abstractmethod

from src.core.enum.subscription import SubscriptionTypeEnum
from src.core.dto.subscription import (
    SubscriptionCreateDTO,
    SubscriptionDTO,
    SubscriptionPeriodCreateDTO,
    SubscriptionPeriodDTO,
    SubscriptionPeriodUnitCreateDTO,
    SubscriptionPeriodUnitDTO,
    SubscriptionTypeCreateDTO,
    SubscriptionTypeDTO
)

from src.core.entity.user import UserSubscription, User
from src.core.entity.subscription import Constraint
from src.core.entity.contact import UserContact

from src.core.dto.misc import SubscriptionTypeConstraintCreateDTO
from src.core.dto.contact import ContactDeleteDTO, ContactTypeCreateDTO, ContactTypeDTO, ContactCreateDTO
from src.core.dto.user import UserContactDTO


class IRepositoryCore(ABC):

    @abstractmethod
    async def user_create(self, *, user: UserContactDTO, subscription: SubscriptionTypeEnum) -> User:
        """_summary_

        Args:
            user (CreateUserDTO): DTO for creating user
            subscription (SubscriptionTypeEnum): Enum, Usual type of subscription which assigned user in the moment creation

        Returns:
            User: Сущность пользователя + по дефолту присвоенный ему обычный тип подписки

        Raises:

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

    @abstractmethod
    async def user_subscription_add(self, *,
                                    user_id: str,
                                    subscription_id: int) -> UserSubscription:
        """ Adds a subscription to user.

        Args:
            user_id (str): User identify
            subscription_id (int): Subscription identify

        Returns:
            UserSubscription: Relation between user and subscription.
        """
        pass

    @abstractmethod
    async def contact_type_create(self, *, obj: ContactTypeCreateDTO) -> ContactTypeDTO:
        """ Creating contact type. This can only be done by application administrator 

        Args:
            create_obj (ContactTypeCreateDTO): DTO contact type for creating

        Returns:
            ContactTypeDTO: New contact type
        """
        pass

    @abstractmethod
    async def contact_create(self, *, user_id: str, obj: ContactCreateDTO) -> UserContact:
        """contact creating by user for himself

        Args:
            user_id (str): user identify
            create_obj (ContactCreateDTO): DTO for new user contact

        Returns:
            UserContact: Relation between user and his new contact
        """
        pass

    @abstractmethod
    async def contact_delete(self, *, user_id: str, obj: ContactDeleteDTO) -> int:
        """delete contact from user contact list

        Args:
            user_id (str): user identify
            obj (ContactDeleteDTO): DTO for deleting user contact

        Returns:
            int: id of deleted contact
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
    async def subscription_create(self, *, obj: SubscriptionCreateDTO) -> SubscriptionDTO:
        """create new subscription

        Args:
            obj (SubscriptionCreateDTO): DTO for creating subscription

        Returns:
            SubscriptionDTO: New subscription
        """
        pass
