from dataclasses import dataclass

from src.core.dto.m2m.user.contact import ContactUserDTO
from src.core.entity.user import User
from src.core.exception.base import EntityNotFound, LogicError
from src.core.exception.contact import ContactNotActive
from src.core.exception.user import UserNotActive
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: ContactUserDTO


class ContactUserSetFavoriteUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, id: int) -> Result:
        if not user.active:
            raise UserNotActive(id=user.id)

        async with self.uow as uow:
            try:
                current_favorite_user_contact = await uow.user_contact.get_favorite(user_id=user.id)

                user_contact = await uow.user_contact.get(id=id, user_id=user.id)
                if not user_contact.active:
                    raise ContactNotActive(id=user_contact.id)

                if current_favorite_user_contact.id == id:
                    raise LogicError(msg=f"Current contact={id} is already favorite")

                _ = await uow.user_contact.set_favorite(id=current_favorite_user_contact.id, is_favorite=False)
            except EntityNotFound:
                pass

            new_favorite_user_contact = await uow.user_contact.set_favorite(id=id, is_favorite=True)
            await uow.commit()

        return Result(item=new_favorite_user_contact)
