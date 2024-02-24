from dataclasses import dataclass

from src.core.dto.m2m.user.contact import ContactUserCreateDTO, ContactUserDTO
from src.core.entity.user import User
from src.core.exception.user import UserNotActive
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: ContactUserDTO


class ContactUserCreateUsecase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, obj: ContactUserCreateDTO) -> Result:
        if not user.active:
            raise UserNotActive(id=user.id)

        async with self.uow as uow:
            contact_user = await uow.user_contact.create(user_id=user.id, obj=obj)

            await uow.commit()
        return Result(item=contact_user)
