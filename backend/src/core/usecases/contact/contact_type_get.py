from dataclasses import dataclass

from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError
from src.core.dto.user.contact import ContactTypeDTO
from src.core.interfaces.user.contact import IUserContactRepository


@dataclass
class Result:
    item: ContactTypeDTO


class ContactTypeGetUseCase:
    def __init__(self, repo: IUserContactRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, id: int) -> Result:
        if not user.active:
            raise UserIsNotActivateError(username=user.username)
        
        contact = await self.repo.contact_type_get(id=id)
        return Result(item=contact)