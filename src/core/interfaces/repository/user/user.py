from abc import ABC, abstractmethod

from src.core.entity.subscription import Subscription
from src.core.entity.user import User, UserCreateDTO, UserUpdateDTO


class IUserRepository(ABC):
    @abstractmethod
    async def create(self, *, user_obj: UserCreateDTO, sub_obj: Subscription) -> User:
        """Create user

        Args:
            obj (UserCreateDTO): DTO for creating user object

        Returns:
            User: User entity

        Raises:
            RepoError: Repository error
            UserDidNotCreated: User didn't created

        """

    @abstractmethod
    async def update(self, *, obj: UserUpdateDTO) -> User:
        """User update

        Args:
            obj (UserUpdateDTO): DTO for update user

        Returns:
            User: User entity
        """

    @abstractmethod
    async def update_subscription(self, *, user_id: int, sub_id: int) -> User:
        """Update user subscription

        Args:
            user_id (int): user identify
            sub_id (int): subscription identify

        Returns:
            User: User entity object
        """
