from typing import List
from abc import ABC, abstractmethod

from src.core.dto.contact import ContactTypeCreateDTO, ContactTypeBaseDTO, ContactTypeDTO
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
                                           user: User,
                                           subscription_type: SubscriptionTypeEnum) -> User:
        """

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
