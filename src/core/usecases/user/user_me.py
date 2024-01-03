from dataclasses import dataclass

from src.core.entity.user import User
from src.core.exception.base import EntityNotFound
from src.core.exception.user import UserIsNotActivateError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: User


class UserMeUsecase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user_id: str) -> Result:
        async with self.uow as uow:
            user = await uow.user.get(user_id=user_id)
            if not user:
                raise EntityNotFound(msg=user_id)

            if not user.active:
                raise UserIsNotActivateError(user_id=user_id)

            return Result(item=user)
