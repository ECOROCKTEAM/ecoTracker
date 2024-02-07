from dataclasses import dataclass, field

from src.core.dto.m2m.user.contact import ContactUserDTO
from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError
from src.core.interfaces.repository.user.contact import (
    UserContactFilter,
    UserContactOrder,
    UserContactSorting,
)
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    items: list[ContactUserDTO] = field(default_factory=list)


class ContactUserListUsecase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(
        self,
        *,
        user: User,
        filter_obj: UserContactFilter,
        sorting_obj: UserContactSorting,
        order_obj: UserContactOrder,
    ) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)

        async with self.uow as uow:
            user_contacts = await uow.user_contact.list(
                user_id=user.id, filter_obj=filter_obj, sorting_obj=sorting_obj, order_obj=order_obj
            )

        return Result(items=user_contacts)
