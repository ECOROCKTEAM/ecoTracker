from dataclasses import dataclass

from src.core.entity.user import User
from src.core.exception.contact import ContactIsFavoriteError
from src.core.exception.user import UserIsNotActivateError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    id: int


class ContactUserDeleteUsecase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, id: int) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)

        async with self.uow as uow:
            contact_user = await uow.user_contact.get(id=id)

            if contact_user.is_favorite:
                raise ContactIsFavoriteError(msg=f"{id=}")

            contact_user_delete = await uow.user_contact.delete(id=id)
            await uow.commit()

        return Result(id=contact_user_delete)
