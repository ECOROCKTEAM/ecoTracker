from dataclasses import dataclass

from src.core.entity.user import User
from src.core.exception.user import UserPermissionError
from src.core.dto.user.contact import ContactTypeCreateDTO, ContactTypeDTO
from src.core.interfaces.user.contact import iUserContactRepository


@dataclass
class Result:
    item: ContactTypeDTO


class ContactTypeCreateUseCase:
    def __init__(self, repo: iUserContactRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, obj: ContactTypeCreateDTO) -> Result:
        if not user.role.enum.ADMIN:
            raise UserPermissionError(user.username)

        contact_type = await self.repo.contact_type_create(obj)

        return Result(item=contact_type)
