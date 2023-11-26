from dataclasses import dataclass

from src.core.entity.user import User, UserUpdateDTO
from src.core.interfaces.repository.user.user import IUserRepository


@dataclass
class Result:
    item: User


class UserUpdateUsecase:
    def __init__(self, repo: IUserRepository) -> None:
        self.repo = repo

    async def __call__(self, *, obj: UserUpdateDTO) -> Result:
        user = await self.repo.update(obj=obj)
        return Result(item=user)
