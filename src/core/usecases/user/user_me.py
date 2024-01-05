from dataclasses import dataclass
from typing import Any

from src.core.entity.subscription import Subscription
from src.core.entity.user import User
from src.core.enum.language import LanguageEnum
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


class UserMeUsecaseDevelop:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user_id: Any) -> Result:
        return Result(
            item=User(
                id="id_1337_fake",
                username="Shrek Shrekovi4 (dev)",
                password="was removed",
                active=True,
                subscription=Subscription(),
                language=LanguageEnum.EN,
            )
        )
