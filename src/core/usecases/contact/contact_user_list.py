from dataclasses import dataclass, field

from src.core.dto.m2m.user.contact import ContactUserDTO
from src.core.interfaces.repository.user.contact import IUserContactRepository
from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError


@dataclass
class Result:
    items: list[ContactUserDTO] = field(default_factory=list)


class ContactUserListUseCase:
    def __init__(self, repo: IUserContactRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User) -> Result:
        if not user.active:
            raise UserIsNotActivateError(username=user.username)

        contact = await self.repo.list(user_id=user.username)
        return Result(items=contact)
