from dataclasses import dataclass

from src.core.dto.auth.firebase import UserIdentity
from src.core.dto.m2m.user.contact import ContactUserCreateDTO
from src.core.entity.user import User, UserCreateDTO
from src.core.enum.language import LanguageEnum
from src.core.enum.user.contact import ContactTypeEnum
from src.core.exception.base import AuthError, EntityNotFound
from src.core.exception.user import UserNotActive
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
                raise AuthError(msg=f"User not found by token: {e}") from e
            try:
                user = await uow.user.get(id=user_identity.id)
            except EntityNotFound:
                user = await uow.user.create(
                    obj=UserCreateDTO(
                        id=user_identity.id,
                        username=user_identity.name,
                        active=True,
                        language=LanguageEnum.EN,
                    ),
                )
                await self.create_default_user_profile(uow=uow, user=user_identity)
                await uow.commit()

        if not user.active:
            raise UserNotActive(id=user_identity.id)

        return Result(item=user)

    async def create_default_user_profile(self, *, uow: IUnitOfWork, user: UserIdentity) -> None:
        await self.create_user_contact(uow=uow, user=user)
        # await self.create_user_subscription(uow=uow, user=user)
        # await self.create_user_tasks(uow=uow, user=user)

    async def create_user_contact(self, *, uow: IUnitOfWork, user: UserIdentity) -> None:
        await uow.user_contact.create(
            user_id=user.id,
            obj=ContactUserCreateDTO(
                value=user.email,
                type=ContactTypeEnum.MAIL,
                active=True,
                is_favorite=True,
            ),
        )

    # async def create_user_subscription(self, *, uow: IUnitOfWork, user: UserIdentity) -> None:
    #     ...

    # async def create_user_tasks(self, *, uow: IUnitOfWork, user: UserIdentity) -> None:
    #     ...
