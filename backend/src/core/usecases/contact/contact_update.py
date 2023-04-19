from dataclasses import dataclass

from src.core.entity.contact import UserContact
from src.core.dto.user.contact import ContactUpdateDTO, ContactUserUpdateDTO
from src.core.interfaces.base import IRepositoryCore
from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError



@dataclass
class Result:
    item: UserContact


class ContactUpdateUseCase:

    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, updating_contact_id: str, update_obj: ContactUpdateDTO) -> Result:
        
        if not user.active:
            raise UserIsNotActivateError(username=user.username)
        
        user_contact = ContactUserUpdateDTO(
            username=user.username,
            updating_contact_id=updating_contact_id,
            contact=update_obj.value,
            type=update_obj.type
        )
        
        contact = await self.repo.contact_update(obj=user_contact)

        return Result(item=contact)