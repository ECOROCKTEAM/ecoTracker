from dataclasses import dataclass

from src.core.interfaces.user.user import IUserRepository
from src.core.entity.user import User, UserCreateDTO


@dataclass
class Result:
    item: User


class UserCreateUseCase:
    def __init__(self, repo: IUserRepository) -> None:
        self.repo = repo

    async def __call__(self, *, obj: UserCreateDTO) -> Result:

        user = await self.repo.create(obj=obj)
        return Result(item=user)
