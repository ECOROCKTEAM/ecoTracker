from dataclasses import dataclass, field

from src.core.dto.m2m.user.contact import ContactUserDTO
from src.core.dto.mock import MockObj
from src.core.interfaces.repository.user.contact import IUserContactRepository
from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError


@dataclass
class Result:
    items: list[ContactUserDTO] = field(default_factory=list)


class ContactUserListUseCase:
    def __init__(self, repo: IUserContactRepository) -> None:
        self.repo = repo

    async def __call__(
        self,
        *,
        user: User,
        filter_obj: MockObj | None = None,
        sorting_obj: MockObj | None = None,
        order_obj: MockObj | None = None,
    ) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)

        contact = await self.repo.list(
            user_id=user.id, filter_obj=filter_obj, sorting_obj=sorting_obj, order_obj=order_obj
        )
        return Result(items=contact)
