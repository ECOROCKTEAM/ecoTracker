from dataclasses import dataclass

from src.core.exception.user import UserPermissionError
from src.core.entity.user import User
from src.core.dto.subscription.type import SubscriptionTypeCreateDTO, SubscriptionTypeDTO
from src.core.interfaces.subscription.subscription import ISubscriptionRepository


@dataclass
class Result:
    item: SubscriptionTypeDTO


class SubscriptionTypeCreateUseCase:
    def __init__(self, repo: ISubscriptionRepository) -> None:
        self.repo = repo

    async def __call__(self, user: User, obj: SubscriptionTypeCreateDTO) -> Result:
        if not user.role.enum.ADMIN:
            raise UserPermissionError(username=user.username)

        subscription_type = await self.repo.type_create(obj=obj)
        return Result(item=subscription_type)
