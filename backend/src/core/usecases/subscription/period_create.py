from dataclasses import dataclass

from src.core.entity.user import User
from src.core.interfaces.base import IRepositoryCore
from src.core.dto.subscription import SubscriptionPeriodDTO, SubscriptionPeriodCreateDTO
from src.core.exception.base import PermissionError


@dataclass
class SuccessResult:
    item: SubscriptionPeriodDTO


class SubscriptionPeriodCreateUseCase:

    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, new_obj: SubscriptionPeriodCreateDTO, user: User) -> SuccessResult:

        if not user.application_role.ADMIN:
            raise PermissionError
        
        period = await self.repo.subscription_period_create(new_obj=new_obj)

        return SuccessResult(item=period)