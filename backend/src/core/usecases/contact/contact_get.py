from dataclasses import dataclass

from src.core.interfaces.base import IRepositoryCore
from src.core.entity.contact import UserContact
from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError


@dataclass
class Result:
    item: UserContact


class ContactGetUseCase:
    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, obj_id: str) -> Result:
        if not user.active:
            raise UserIsNotActivateError(username=user.username)

        contact = await self.repo.contact_get(user_id=user.username, obj_id=obj_id)

        return Result(item=contact)
