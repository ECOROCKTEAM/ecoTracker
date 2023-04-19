from dataclasses import dataclass

from src.core.entity.user import User
from src.core.interfaces.base import IRepositoryCore
from src.core.dto.subscription import (
    SubscriptionPeriodUnitDTO,
    SubscriptionPeriodUnitCreateDTO,
)
from src.core.exception.user import UserPermissionError


@dataclass
class Result:
    item: SubscriptionPeriodUnitDTO


class SubscriptionPeriodUnitCreateUseCase:
    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(
        self, *, user: User, create_obj: SubscriptionPeriodUnitCreateDTO
    ) -> Result:
        if not user.application_role.ADMIN:
            raise UserPermissionError(username=user.username)

        period = await self.repo.subscription_period_unit_create(obj=create_obj)

        return Result(item=period)
