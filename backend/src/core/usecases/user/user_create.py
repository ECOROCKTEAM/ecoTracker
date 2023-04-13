from dataclasses import dataclass

from src.core.interfaces.base import IRepositoryCore
from src.core.entity.user import User
from src.core.dto.user import CreateUserDTO
from src.core.exception.user import CreateUserError
from src.core.enum.subscription import SubscriptionTypeEnum


@dataclass
class SuccessResult:
    item: User


class UserCreateUseCase:
    
    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, new_user: CreateUserDTO) -> SuccessResult:

        if not all([new_user.username, new_user.password]):
            raise CreateUserError(username=new_user.username, password=new_user.password)
        
        user = await self.repo.user_create(new_user=new_user)
        user_with_sub = await self.repo.user_subscription_assignment(user=user, subscription_type=SubscriptionTypeEnum.USUAL)

        return SuccessResult(item=user_with_sub)