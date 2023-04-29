from dataclasses import dataclass

from src.core.interfaces.repository.user.user import IUserRepository
from src.core.entity.user import User, UserUpdateDTO


@dataclass
class Result:
    item: User


class UserUpdateUseCase:
    def __init__(self, repo: IUserRepository) -> None:
        self.repo = repo

    async def __call__(self, *, obj: UserUpdateDTO) -> Result:
        user = await self.repo.update(obj=obj)
        return Result(item=user)
