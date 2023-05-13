from dataclasses import dataclass

from src.core.dto.mock import MockObj
from src.core.entity.user import User, UserCreateDTO
from src.core.interfaces.repository.subscription.subscription import ISubscriptionRepository
from src.core.interfaces.repository.user.user import IUserRepository


@dataclass
class Result:
    item: User


class UserCreateUseCase:
    def __init__(self, user_repo: IUserRepository, subscription_repo: ISubscriptionRepository) -> None:
        self.user_repo = user_repo
        self.sub_repo = subscription_repo

    async def __call__(self, *, obj: UserCreateDTO) -> Result:
        subscription = await self.sub_repo.list(filter_obj=MockObj)  # type: ignore
        user = await self.user_repo.create(user_obj=obj, sub_obj=subscription)  # type: ignore
        return Result(item=user)
