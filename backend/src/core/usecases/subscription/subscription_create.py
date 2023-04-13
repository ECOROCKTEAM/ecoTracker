from dataclasses import dataclass

from src.core.entity.user import User
from src.core.interfaces.base import IRepositoryCore
from src.core.dto.subscription import SubscriptionDTO, SubscriptionCreateDTO
from src.core.exception.base import PermissionError


@dataclass
class SuccessResult:
    item: SubscriptionDTO


class SubscriptionCreateUseCase:

    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, new_obj: SubscriptionCreateDTO) -> SuccessResult:

        if not user.application_role.ADMIN:
            raise PermissionError(username=user.username)
        
        subscription = await self.repo.subscription_create(new_obj=new_obj)

        return SuccessResult(item=subscription)