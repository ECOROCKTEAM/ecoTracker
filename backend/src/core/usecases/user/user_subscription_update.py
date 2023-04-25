from dataclasses import dataclass

from src.core.dto.m2m.user.subscription import UserSubscriptionDTO, UserSubscriptionUpdateDTO
from src.core.interfaces.user.subscription import IUserSubscriptionRepository
from src.core.entity.user import User


@dataclass
class Result:
    item: UserSubscriptionDTO


class UserSubscriptionUpdateUseCase:
    def __init__(self, repo: IUserSubscriptionRepository) -> None:
        self.repo = repo

    async def __call__(self, user: User, obj: UserSubscriptionUpdateDTO) -> Result:

        sub = await self.repo.update(obj=obj)
        return Result(item=sub)
