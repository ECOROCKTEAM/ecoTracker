from dataclasses import dataclass

from src.core.entity.user import User
from src.core.interfaces.subscription.subscription import ISubscriptionRepository
from src.core.dto.subscription.period import SubscriptionPeriodDTO
from src.core.exception.user import UserPermissionError


@dataclass
class Result:
    items: list[SubscriptionPeriodDTO]


class SubscriptionPeriodListUseCase:
    def __init__(self, repo: ISubscriptionRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User) -> Result:
        if not user.role.enum.ADMIN:
            raise UserPermissionError
        
        obj_list = await self.repo.period_list()
        return Result(items=obj_list)