from dataclasses import dataclass

from src.core.dto.m2m.user.contact import ContactUserDTO, ContactUserUpdateDTO
from src.core.entity.user import User
from src.core.exception.user import UserNotActive
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: ContactUserDTO


class ContactUserUpdateUsecase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, obj: ContactUserUpdateDTO) -> Result:
        if not user.active:
            raise UserNotActive(id=user.id)

        async with self.uow as uow:
            contact_user_update = await uow.user_contact.update(obj=obj, user_id=user.id)
            await uow.commit()

        return Result(item=contact_user_update)
