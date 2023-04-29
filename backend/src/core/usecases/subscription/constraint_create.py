from dataclasses import dataclass

from src.core.entity.user import User
from src.core.dto.subscription.constraint import SubscriptionConstraintDTO, SubscriptionConstraintCreateDTO
from src.core.interfaces.repository.subscription.subscription import ISubscriptionRepository
from src.core.exception.user import UserPermissionError


@dataclass
class Result:
    item: SubscriptionConstraintDTO


class SubscriptionСonstraintCreateUserCase:
    def __init__(self, repo: ISubscriptionRepository) -> None:
        self.repo = repo


    async def __call__(
            self, *,
            user: User,
            obj: SubscriptionConstraintCreateDTO,
            ) -> Result:
        
        if not user.role.enum.ADMIN:
            raise UserPermissionError(username=user.username)

        constraint = await self.repo.constraint_create(obj=obj)

        return Result(item=constraint)