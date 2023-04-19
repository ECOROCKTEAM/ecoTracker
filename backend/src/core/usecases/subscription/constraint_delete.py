from dataclasses import dataclass

from src.core.exception.user import UserPermissionError
from src.core.entity.user import User
from src.core.interfaces.base import IRepositoryCore


@dataclass
class Result:
    item: int


class SubscriptionConstraintDeleteUseCase:
    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, user: User, id: int) -> Result:
        if not user.application_role.ADMIN:
            raise UserPermissionError(username=user.username)

        constraint_id = await self.repo.subscription_type_constraint_delete(
            constraint_name=id
        )

        return Result(item=constraint_id)
