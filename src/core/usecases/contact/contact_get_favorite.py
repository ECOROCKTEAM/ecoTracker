from dataclasses import dataclass

from src.core.dto.m2m.user.contact import ContactUserDTO
from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: ContactUserDTO


class ContactUserGetFavoriteUsecase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, user: User) -> Result:
        if not user.active:
            raise UserIsNotActivateError(msg="")

        async with self.uow as uow:
            contact_user = await uow.user_contact.get_favorite(user_id=user.id)

        return Result(item=contact_user)
