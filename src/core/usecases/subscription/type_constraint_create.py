from dataclasses import dataclass

from src.core.dto.m2m.subscription_type.constraint import (
    SubscriptionTypeConstrainCreateDTO,
    SubscriptionTypeConstrainDTO,
)
from src.core.interfaces.repository.subscription.subscription import ISubscriptionRepository
from src.core.exception.user import UserPermissionError
from src.core.entity.user import User


@dataclass
class Result:
    item: SubscriptionTypeConstrainDTO


class SubscriptionTypeConstraintCreateUseCase:
    def __init__(self, repo: ISubscriptionRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, obj: SubscriptionTypeConstrainCreateDTO) -> Result:
        if not user.role.enum.ADMIN:
            raise UserPermissionError(username=user.username)

        constraint = await self.repo.type_constraint_create(obj=obj)
        return Result(item=constraint)
