from dataclasses import dataclass

from src.core.dto.m2m.user.contact import ContactUserDTO
from src.core.entity.user import User
from src.core.exception.contact import ContactIsFavoriteError, ContactIsNotActiveError
from src.core.exception.user import UserIsNotActivateError
from src.core.interfaces.repository.user.contact import UserContactFilter
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: ContactUserDTO


class ContactSetFaforiteUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, contact_id: int) -> Result:
        if not user.active:
            raise UserIsNotActivateError(msg=f"User={user.id} is not active")

        async with self.uow as uow:
            filter_obj = UserContactFilter(is_favorite=True)

            current_favorite_user_contact = await uow.user_contact.list(user_id=user.id, filter_obj=filter_obj)

            if current_favorite_user_contact[0].id == contact_id:
                raise ContactIsFavoriteError(msg=f"{contact_id=}")

            user_contact = await uow.user_contact.get(contact_id=contact_id, user_id=user.id)

            if not user_contact.active:
                raise ContactIsNotActiveError(msg=f"{contact_id=}")

            _ = await uow.user_contact.set_favorite(
                user_id=user.id, contact_id=current_favorite_user_contact[0].id, is_favorite=False
            )

            await uow.commit()

            new_favorite_contact = await uow.user_contact.set_favorite(
                user_id=user.id, contact_id=contact_id, is_favorite=True
            )

            await uow.commit()

        return Result(item=new_favorite_contact)
