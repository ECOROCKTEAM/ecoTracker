import asyncio
from dataclasses import dataclass

from src.core.exception.subscription import ConstraintDeleteError
from src.core.dto.subscription.type import SubscriptionTypeConstraintDTO
from src.core.dto.subscription.constraint import SubscriptionConstraintDTO
from src.core.exception.user import UserPermissionError
from src.core.entity.user import User
from src.core.interfaces.repository.subscription.subscription import ISubscriptionRepository


@dataclass
class Result:
    item: int


class SubscriptionConstraintDeleteUseCase:
    def __init__(self, repo: ISubscriptionRepository) -> None:
        self.repo = repo

    async def __call__(self, user: User, constraint_id: int) -> Result:
        if not user.role.enum.ADMIN:
            raise UserPermissionError(username=user.username)

        # По идее было бы неплохо проверить привязано ли ограничение к какой-нибудь подписке прежде, чем удалить её.
        # Не знаю на каком этапе это делается, но мне кажется, что проверку эту надо делать тут

        tasks: tuple[asyncio.Task[SubscriptionConstraintDTO], asyncio.Task[list[SubscriptionTypeConstraintDTO]]] = (
            asyncio.create_task(self.repo.constraint_get(id=constraint_id)),
            asyncio.create_task(self.repo.type_constraint_list()),
        )
        constraint, subscription_type_constraint_list = await asyncio.gather(*tasks)

        for item in subscription_type_constraint_list:
            if item.constraint_id == constraint.id:
                raise ConstraintDeleteError(constraint=constraint.name)

        id = await self.repo.type_constraint_delete(id=constraint_id)
        return Result(item=id)
