from dataclasses import dataclass

from src.core.dto.subscription.type import SubscriptionTypeConstraintDTO
from src.core.entity.user import User
from src.core.interfaces.subscription.subscription import ISubscriptionRepository
from src.core.exception.user import UserPermissionError


@dataclass
class Result:
    items: list[SubscriptionTypeConstraintDTO] 


class SubscriptionTypeConstraintListUseCase:
    def __init__(self, repo: ISubscriptionRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User) -> Result:
        if not user.role.enum.ADMIN:
            raise UserPermissionError(username=user.username)
        
        # Нужны ли тут какие-то сортировки и фильтры... Хз
        objects = await self.repo.type_constraint_list()

        return Result(items=objects)
