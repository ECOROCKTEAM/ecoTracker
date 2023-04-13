from dataclasses import dataclass

from src.core.entity.user import User
from src.core.interfaces.base import IRepositoryCore
from src.core.dto.subscription import SubscriptionPeriodUnitDTO, SubscriptionPeriodUnitCreateDTO
from src.core.exception.base import PermissionError


@dataclass
class SuccessResult:
    item: SubscriptionPeriodUnitDTO


class SubscriptionPeriodUnitCreateUseCase:

    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, new_obj: SubscriptionPeriodUnitCreateDTO, user: User) -> SuccessResult:

        if not user.application_role.ADMIN:
            raise PermissionError(username=user.username)
        
        period = await self.repo.subscription_period_unit_create(new_obj=new_obj)

        return SuccessResult(item=period)