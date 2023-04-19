from dataclasses import dataclass

from src.core.entity.user import User
from src.core.exception.user import UserPermissionError
from src.core.dto.contact import ContactTypeCreateDTO, ContactTypeDTO
from src.core.interfaces.base import IRepositoryCore


@dataclass
class Result:
    item: ContactTypeDTO


class ContactTypeCreateUseCase:

    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *,
                       user: User,
                       obj: ContactTypeCreateDTO) -> Result:

        if not user.application_role.ADMIN:
            raise UserPermissionError(user.username)

        contact_type = await self.repo.contact_type_create(obj=obj)

        return Result(item=contact_type)
