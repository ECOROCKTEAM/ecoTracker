from dataclasses import dataclass

from src.core.entity.user import User
from src.core.interfaces.repository.subscription.subscription import (
    ISubscriptionRepository,
)
from src.core.entity.subscription import Subscription
from src.core.exception.user import UserIsNotActivateError


@dataclass
class Result:
    item: Subscription


class SubscriptionGetUseCase:
    def __init__(self, repo: ISubscriptionRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, id: int) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)

        sub = await self.repo.get(id=id)
        return Result(item=sub)
