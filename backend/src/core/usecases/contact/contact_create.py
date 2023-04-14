from dataclasses import dataclass

from src.core.dto.contact import ContactCreateDTO
from src.core.interfaces.base import IRepositoryCore
from src.core.entity.contact import UserContact
from src.core.entity.user import User
from src.core.exception.base import DomainError



@dataclass
class Result:
    item: UserContact


class ContactCreateUseCase:

    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, create_obj: ContactCreateDTO) -> Result:
        
        if not user.active:
            raise DomainError(username=user.username)
        
        contact = await self.repo.contact_create(user_id=user.username, create_obj=create_obj)

        return Result(item=contact)