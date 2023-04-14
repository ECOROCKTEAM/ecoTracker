from dataclasses import dataclass

from src.core.entity.user import User
from src.core.exception.base import PermissionError
from src.core.dto.contact import ContactTypeCreateDTO, ContactTypeDTO
from src.core.interfaces.base import IRepositoryCore


@dataclass
class Result:
    item: ContactTypeDTO



class ContactTypeCreateUC:

    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def realization(self, *,
                          user: User,
                          new_contact_type: ContactTypeCreateDTO) -> Result:
        
        if not user.application_role.ADMIN:
            raise PermissionError(user.username)
        
        contact_type = await self.repo.contact_type_create(new_type=new_contact_type)

        return Result(item=contact_type)

