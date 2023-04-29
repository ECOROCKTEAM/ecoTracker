from dataclasses import dataclass

from src.core.entity.user import User
from src.core.interfaces.repository.subscription.subscription import ISubscriptionRepository
from src.core.dto.subscription.period import SubscriptionPeriodCreateDTO, SubscriptionPeriodDTO
from src.core.exception.user import UserPermissionError


@dataclass
class Result:
    item: SubscriptionPeriodDTO


class SubscriptionPeriodCreateUseCase:
    def __init__(self, repo: ISubscriptionRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, obj: SubscriptionPeriodCreateDTO) -> Result:
        if not user.role.enum.ADMIN:
            raise UserPermissionError(username=user.username)

        period = await self.repo.period_create(obj=obj)
        return Result(item=period)
