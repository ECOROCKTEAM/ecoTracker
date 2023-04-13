from dataclasses import dataclass

from src.core.exception.base import PermissionError
from src.core.entity.user import User
from src.core.interfaces.base import IRepositoryCore

@dataclass
class SuccessResult:
    item: int


class SubscriptionConstraintDeleteUseCase:

    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, user: User, constraint_name: str) -> SuccessResult:

        if not user.application_role.ADMIN:
            raise PermissionError(username=user.username)

        constraint_id = await self.repo.subscription_type_constraint_delete(constraint_name=constraint_name)

        return SuccessResult(item=constraint_id)