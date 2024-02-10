from dataclasses import dataclass

from src.core.dto.m2m.user.contact import ContactUserDTO
from src.core.entity.user import User
from src.core.exception.contact import ContactIsFavoriteError, ContactIsNotActiveError
from src.core.exception.user import UserIsNotActivateError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: ContactUserDTO


class ContactUserSetFaforiteUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, id: int) -> Result:
        if not user.active:
            raise UserIsNotActivateError(msg=f"User={user.id} is not active")

        async with self.uow as uow:
            current_favorite_user_contact = await uow.user_contact.get_favorite(user_id=user.id)

            if current_favorite_user_contact.id == id:
                raise ContactIsFavoriteError(msg=f"{id=}")

            user_contact = await uow.user_contact.get(id=id)

            if not user_contact.active:
                raise ContactIsNotActiveError(msg=f"{id=}")

            _ = await uow.user_contact.set_favorite(id=current_favorite_user_contact.id, is_favorite=False)

            await uow.commit()

            new_favorite_user_contact = await uow.user_contact.set_favorite(id=id, is_favorite=True)

            await uow.commit()

        return Result(item=new_favorite_user_contact)
