from dataclasses import dataclass, field
from typing import Optional

from src.core.dto.user.contact import ContactDTO
from src.core.interfaces.base import IRepositoryCore
from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError



@dataclass
class Result:
    item: list[ContactDTO] = field(default_factory=list)


class ContactListUseCase:

    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, user: User) -> Optional[Result]:
        
        if not user.active:
            raise UserIsNotActivateError(username=user.username)
        
        contact = await self.repo.contact_list(user_id=user.username)

        return Result(item=contact)