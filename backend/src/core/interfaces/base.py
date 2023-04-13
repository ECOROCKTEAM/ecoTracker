from abc import ABC, abstractmethod

from src.core.dto.misc import SubscriptionTypeConstraintCreateDTO
from src.core.entity.subscription import Constraint
from src.core.dto.contact import ContactTypeCreateDTO, ContactTypeDTO
from src.core.entity.user import User
from src.core.enum.subscription import SubscriptionTypeEnum
from src.core.dto.user import BaseUserContactDTO, BaseUserContactIdDTO


class IRepositoryCore(ABC):

    @abstractmethod
    async def user_create(self, *, new_user: BaseUserContactDTO) -> BaseUserContactIdDTO:
        """_summary_

        Args:
            new_user (CreateUserDTO): DTO для создания\регистрации пользователя

        Returns:
            User: Сущность пользователя + по дефолту присвоенный ему обычный тип подписки

        Raises:

        """
        pass

    @abstractmethod
    async def user_subscription_assignment(self, *,
                                           username: str = None,
                                           user: User = None,
                                           subscription_type: SubscriptionTypeEnum) -> User:
        """ If user just registrating we can't get his User entity, just his username.
        Otherwise we can get User entity

        Args:
            user (BaseUserContactIdDTO): User wich take subscription
            subscription_type (SubscriptionTypeEnum): Subscription type

        Returns:
            User: Сущность юзера
        """
        pass

    @abstractmethod
    async def contact_type_create(self, *, new_type: ContactTypeCreateDTO) -> ContactTypeDTO:
        """ Creating contact type. This can only be done by application administrator 

        Args:
            new_type (ContactTypeCreateDTO): DTO contact type for creating

        Returns:
            ContactTypeBaseDTO: New contact type
        """
        pass

    @abstractmethod
    async def subscription_type_constraint_create(self, *, new_obj: SubscriptionTypeConstraintCreateDTO) -> Constraint:
        """Create constraint for Subscription

        Args:
            new_obj (SubscriptionTypeConstraintCreate): DTO for create  new constrains

        Returns:
            Constraint: Constraint entity
        """

    @abstractmethod
    async def subscription_type_constraint_delete(self, *, constraint_name: str) -> int:
        """Delete constraint for Subscription

        Args:
            constraint_name (str): Name of delete constraint

        Returns:
            int: id of deleted constraint
        """
        pass