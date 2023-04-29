from dataclasses import dataclass

from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError
from src.core.dto.user.contact import ContactTypeDTO
from src.core.interfaces.repository.user.contact import IUserContactRepository


@dataclass
class Result:
    items: list[ContactTypeDTO]


class ContactTypeListUseCase:
    def __init__(self, repo: IUserContactRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User) -> Result:
        if not user.active:
            raise UserIsNotActivateError

        contact_list = await self.repo.contact_type_list()
        return Result(items=contact_list)
