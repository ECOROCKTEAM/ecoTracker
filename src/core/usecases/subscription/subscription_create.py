from dataclasses import dataclass

from src.core.entity.user import User
from src.core.interfaces.repository.subscription.subscription import (
    ISubscriptionRepository,
)
from src.core.entity.subscription import Subscription, SubscriptionCreateDTO


@dataclass
class Result:
    item: Subscription


class SubscriptionCreateUseCase:
    def __init__(self, repo: ISubscriptionRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, obj: SubscriptionCreateDTO) -> Result:
        subscription = await self.repo.create(obj=obj)
        return Result(item=subscription)
