from dataclasses import dataclass

from src.core.entity.user import User
from src.core.interfaces.base import IRepositoryCore
from src.core.dto.subscription import SubscriptionDTO, SubscriptionCreateDTO
from src.core.exception.user import UserPermissionError


@dataclass
class Result:
    item: SubscriptionDTO


class SubscriptionCreateUseCase:

    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, create_obj: SubscriptionCreateDTO) -> Result:

        if not user.application_role.ADMIN:
            raise UserPermissionError(username=user.username)
        
        subscription = await self.repo.subscription_create(obj=create_obj)

        return Result(item=subscription)