from dataclasses import dataclass
from typing import Any

from src.core.entity.subscription import Subscription
from src.core.entity.user import User, UserCreateDTO
from src.core.enum.language import LanguageEnum
from src.core.exception.base import AuthError, EntityNotFound
from src.core.exception.user import UserIsNotActivateError
from src.core.interfaces.repository.auth import IAuthProviderRepository
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: User


class UserMeUsecase:
    def __init__(self, uow: IUnitOfWork, auth_provider: IAuthProviderRepository) -> None:
        self.uow = uow
        self.auth_provider = auth_provider

    async def __call__(self, *, token: str) -> Result:
        async with self.uow as uow:
            try:
                user_identity = await self.auth_provider.get_user_by_token(token=token)
            except Exception as e:
                raise AuthError(msg=f"Error in getting by token: {e}") from e

            try:
                user = await uow.user.get(user_id=user_identity.id)
            except EntityNotFound:
                user = await uow.user.create(
                    user_obj=UserCreateDTO(
                        id=user_identity.id,
                        username=user_identity.name,
                        password="",
                        active=True,
                        language=LanguageEnum.EN,
                    ),
                    sub_obj=Subscription(),
                )
                await uow.commit()

            if all([user, not user.active]):
                raise UserIsNotActivateError(user_id=user_identity.id)

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
