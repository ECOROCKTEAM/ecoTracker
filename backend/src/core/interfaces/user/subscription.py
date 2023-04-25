from abc import ABC, abstractmethod

from src.core.dto.m2m.user.subscription import UserSubscriptionDTO, UserSubscriptionUpdateDTO   


class IUserSubscriptionRepository(ABC):

    @abstractmethod
    async def update(self, *, obj: UserSubscriptionUpdateDTO) -> UserSubscriptionDTO:
        """Update user subscription

        Args:
            obj (UserSubscriptionUpdateDTO): DTO for update user subsctiprion

        Returns:
            UserSubscriptionDTO: DTO of user subscription object
        """