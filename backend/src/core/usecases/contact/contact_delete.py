from dataclasses import dataclass

from src.core.dto.contact import ContactDeleteDTO
from src.core.interfaces.base import IRepositoryCore
from src.core.entity.user import User
from src.core.exception.base import DomainError



@dataclass
class Result:
    id: int


class ContactDeleteUseCase:

    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, obj: ContactDeleteDTO) -> Result:
        
        if not user.active:
            raise DomainError(username=user.username)
        
        contact = await self.repo.contact_create(user_id=user.username, obj=obj)

        return Result(item=contact)