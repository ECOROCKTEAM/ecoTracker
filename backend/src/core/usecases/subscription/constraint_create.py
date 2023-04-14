from dataclasses import dataclass

from src.core.exception.base import PermissionError
from src.core.entity.user import User
from src.core.dto.misc import SubscriptionTypeConstraintCreateDTO
from src.core.interfaces.base import IRepositoryCore
from src.core.entity.subscription import Constraint

@dataclass
class Result:
    item: Constraint


class SubscriptionConstraintCreateUseCase:

    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, user: User, create_obj: SubscriptionTypeConstraintCreateDTO) -> Result:

        if not user.application_role.ADMIN:
            raise PermissionError(username=user.username)

        constraint = await self.repo.subscription_type_constraint_create(obj=create_obj)

        return Result(item=constraint)