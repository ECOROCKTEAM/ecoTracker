from dataclasses import dataclass

from src.core.exception.user import UserPermissionError
from src.core.entity.user import User
from src.core.interfaces.subscription.subscription import ISubscriptionRepository


@dataclass
class Result:
    item: int


class SubscriptionConstraintDeleteUseCase:
    def __init__(self, repo: ISubscriptionRepository) -> None:
        self.repo = repo

    async def __call__(self, user: User, id: int) -> Result:
        if not user.role.enum.ADMIN:
            raise UserPermissionError(username=user.username)

        constraint_id = await self.repo.type_constraint_delete(id=id)
        return Result(item=constraint_id)
