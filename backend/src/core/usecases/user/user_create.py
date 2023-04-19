from dataclasses import dataclass

from src.core.interfaces.base import IRepositoryCore
from src.core.entity.user import User
from src.core.dto.user import UserContactCreateDTO
from src.core.enum.subscription import SubscriptionTypeEnum


@dataclass
class Result:
    item: User


class UserCreateUseCase:
    
    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, new_user: UserContactCreateDTO) -> Result:
        
        user = await self.repo.user_create(user=new_user, subscription=SubscriptionTypeEnum.USUAL)

        return Result(item=user)