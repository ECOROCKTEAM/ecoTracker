from dataclasses import dataclass

from src.core.entity.user import User 
from src.core.interfaces.base import IRepositoryCore
from src.core.dto.subscription import SubscriptionPeriodCreateDTO, SubscriptionPeriodDTO
from src.core.exception.base import PermissionError


@dataclass 
class Result:
    item: SubscriptionPeriodDTO
 

class SubscriptionPeriodCreateUseCase:

    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, create_obj: SubscriptionPeriodCreateDTO) -> Result:
        
        if not user.application_role.ADMIN:
            raise PermissionError(username=user.username)
        
        period = await self.repo.subscription_period_create(obj=create_obj)
        return Result(item=period)

        
