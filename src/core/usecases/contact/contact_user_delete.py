from dataclasses import dataclass

from src.core.entity.user import User
from src.core.exception.base import LogicError
from src.core.exception.user import UserNotActive
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    id: int


class ContactUserDeleteUsecase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, id: int) -> Result:
        if not user.active:
            raise UserNotActive(id=user.id)

        async with self.uow as uow:
            contact_user = await uow.user_contact.get(id=id, user_id=user.id)

            if contact_user.is_favorite:
                raise LogicError(msg="Current contact is favorite, change favorite before delete!")

            contact_user_delete = await uow.user_contact.delete(id=id, user_id=user.id)
            await uow.commit()

        return Result(id=contact_user_delete)
