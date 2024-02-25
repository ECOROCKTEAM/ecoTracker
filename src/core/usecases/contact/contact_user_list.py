from dataclasses import dataclass, field

from src.core.dto.m2m.user.contact import ContactUserDTO
from src.core.dto.utils import SortObj
from src.core.entity.user import User
from src.core.exception.user import UserNotActive
from src.core.interfaces.repository.user.contact import UserContactFilter
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
        sorting_obj: SortObj,
    ) -> Result:
        if not user.active:
            raise UserNotActive(id=user.id)

        async with self.uow as uow:
            user_contacts = await uow.user_contact.lst(user_id=user.id, filter_obj=filter_obj, sorting_obj=sorting_obj)

        return Result(items=user_contacts)
