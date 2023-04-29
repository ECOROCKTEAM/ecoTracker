from dataclasses import dataclass

from src.core.entity.user import User
from src.core.interfaces.subscription.subscription import ISubscriptionRepository
from src.core.dto.subscription.period_unit import SubscriptionPeriodUnitCreateDTO, SubscriptionPeriodUnitDTO
from src.core.exception.user import UserPermissionError


@dataclass
class Result:
    item: SubscriptionPeriodUnitDTO


class SubscriptionPeriodUnitCreateUseCase:
    def __init__(self, repo: ISubscriptionRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, obj: SubscriptionPeriodUnitCreateDTO) -> Result:
        if not user.role.enum.ADMIN:
            raise UserPermissionError(username=user.username)

        period = await self.repo.period_unit_create(obj=obj)
        return Result(item=period)
