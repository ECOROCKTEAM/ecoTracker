from dataclasses import dataclass

from src.core.entity.user import User
from src.core.interfaces.repository.subscription.subscription import (
    ISubscriptionRepository,
)
from src.core.dto.subscription.period import SubscriptionPeriodDTO
from src.core.exception.user import UserPermissionError


@dataclass
class Result:
    item: SubscriptionPeriodDTO


class SubscriptionPeriodGetUseCase:
    def __init__(self, repo: ISubscriptionRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, id: int) -> Result:
        if not user.role.enum.ADMIN:
            raise UserPermissionError

        obj = await self.repo.period_get(id=id)
        return Result(item=obj)
