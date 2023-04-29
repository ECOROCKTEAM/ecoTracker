from abc import ABC, abstractmethod

from src.core.dto.m2m.user.subscription import UserSubscription, UserSubscriptionUpdateDTO, UserSubscriptionCreateDTO


class IUserSubscriptionRepository(ABC):
    
    @abstractmethod
    async def create(self, *, obj: UserSubscriptionCreateDTO) -> UserSubscription:
        """Create user subscription object

        Args:
            obj (UserSubscriptionCreateDTO): DTO of user subscription object

        Returns:
            UserSubscription: User subscription entity object
        """

    @abstractmethod
    async def get(self, *, user_id: str, sub_id: int) -> UserSubscription:
        """Get user subscription object

        Args:
            user_id (str): user identify
            sub_id (int): subscription identify

        Returns:
            UserSubscription: User Subscription object
        """

    @abstractmethod
    async def update(self, *, obj: UserSubscriptionUpdateDTO) -> UserSubscription:
        """Update user subscription

        Args:
            obj (UserSubscriptionUpdateDTO): DTO for update user subsctiprion

        Returns:
            UserSubscription: DTO of user subscription object
        """

    @abstractmethod
    async def list(self) -> list[UserSubscription]:
        """List of user subscriptions

        Returns:
            list[UserSubscription]: List of user subscriptions objects
        """

    @abstractmethod
    async def delete(self, user_id: str, sub_id: int) -> int:
        """Delete user subscription object

        Args:
            user_id (str): user identify
            sub_id (int): subscription identify

        Returns:
            int: int of deleted user subscription object
        """