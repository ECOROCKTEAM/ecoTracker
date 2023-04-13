from dataclasses import dataclass

from src.core.exception.base import PermissionError
from src.core.entity.user import User
from src.core.dto.misc import SubscriptionTypeConstraintCreateDTO
from src.core.interfaces.base import IRepositoryCore
from src.core.entity.subscription import Constraint

@dataclass
class SuccessResult:
    item: Constraint


class SubscriptionConstraintCreateUseCase:

    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, user: User, new_constraint: SubscriptionTypeConstraintCreateDTO) -> SuccessResult:

        if not user.application_role.ADMIN:
            raise PermissionError(username=user.username)

        constraint = await self.repo.subscription_type_constraint_create(new_obj=new_constraint)

        return SuccessResult(item=constraint)