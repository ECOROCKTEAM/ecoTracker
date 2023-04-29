from dataclasses import dataclass

from src.core.dto.mock import MockObj
from src.core.dto.subscription.type import SubscriptionTypeConstraintDTO
from src.core.entity.user import User
from src.core.interfaces.repository.subscription.subscription import ISubscriptionRepository
from src.core.exception.user import UserPermissionError


@dataclass
class Result:
    items: list[SubscriptionTypeConstraintDTO]


class SubscriptionTypeConstraintListUseCase:
    def __init__(self, repo: ISubscriptionRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, subscription_type: MockObj = None) -> Result:
        if not user.role.enum.ADMIN:
            raise UserPermissionError(username=user.username)

        objects = await self.repo.type_constraint_list(subscription_type=subscription_type)

        return Result(items=objects)
