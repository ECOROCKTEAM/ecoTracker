from dataclasses import dataclass

from src.core.dto.m2m.user.contact import ContactUserDTO, ContactUserUpdateDTO
from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError
from src.core.interfaces.repository.user.contact import IUserContactRepository


@dataclass
class Result:
    item: ContactUserDTO


class ContactUserUpdateUsecase:
    def __init__(self, repo: IUserContactRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, update_obj: ContactUserUpdateDTO) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)

        _ = await self.repo.get(id=update_obj.contact_id)

        obj = await self.repo.update(obj=update_obj)
        return Result(item=obj)
