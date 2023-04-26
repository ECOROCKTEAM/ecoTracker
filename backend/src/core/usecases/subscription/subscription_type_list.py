from dataclasses import dataclass
from src.core.interfaces.subscription.subscription import ISubscriptionRepository
from src.core.dto.subscription.type import SubscriptionTypeDTO
from src.core.entity.user import User
from src.core.exception.user import UserPermissionError


@dataclass
class Result:
    items: list[SubscriptionTypeDTO]


class SubscriptionTypeListUseCase:
    def __init__(self, repo: ISubscriptionRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User) -> Result:
        if not user.role.enum.ADMIN:
            raise UserPermissionError(username=user.username)
        
        obj_list = await self.repo.type_list()
        return Result(items=obj_list)