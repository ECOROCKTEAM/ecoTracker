from dataclasses import dataclass

from src.core.entity.user import User
from src.core.interfaces.repository.subscription.subscription import ISubscriptionRepository
from src.core.entity.subscription import Subscription, SubscriptionCreateDTO
from src.core.exception.user import UserPermissionError


@dataclass
class Result:
    item: Subscription


class SubscriptionCreateUseCase:
    def __init__(self, repo: ISubscriptionRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, obj: SubscriptionCreateDTO) -> Result:
        if not user.role.enum.ADMIN:
            raise UserPermissionError(username=user.username)

        subscription = await self.repo.create(obj=obj)
        return Result(item=subscription)
