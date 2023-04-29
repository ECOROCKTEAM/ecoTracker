from dataclasses import dataclass

from src.core.dto.m2m.user.contact import ContactUserDTO
from src.core.interfaces.repository.user.contact import IUserContactRepository
from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError


@dataclass
class Result:
    item: ContactUserDTO


class ContactUserGetUseCase:
    def __init__(self, repo: IUserContactRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, contact_id: str) -> Result:
        if not user.active:
            raise UserIsNotActivateError(username=user.username)

        contact = await self.repo.get(id=contact_id)
        return Result(item=contact)
