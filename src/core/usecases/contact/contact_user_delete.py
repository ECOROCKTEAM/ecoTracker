from dataclasses import dataclass

from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError
from src.core.interfaces.repository.user.contact import IUserContactRepository


@dataclass
class Result:
    id: int


class ContactUserDeleteUseCase:
    def __init__(self, repo: IUserContactRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, contact_id: int) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)

        contact = await self.repo.delete(contact_id=contact_id)
        return Result(id=contact)
