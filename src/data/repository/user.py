from dataclasses import asdict
from typing import cast

from asyncpg import UniqueViolationError
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.entity.subscription import Subscription
from src.core.entity.user import User, UserCreateDTO, UserUpdateDTO
from src.core.exception.base import EntityNotChange, EntityNotCreated, EntityNotFound
from src.core.interfaces.repository.user.user import IUserRepository
from src.data.models.user.user import UserModel


def model_to_dto(model: UserModel) -> User:
    return User(
        id=model.id,
        username=model.username,
        password=model.password,
        subscription=Subscription(),
        active=model.active,
        language=model.language,
    )


class UserRepository(IUserRepository):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def get(self, *, user_id: str) -> User:
        stmt = select(UserModel).where(UserModel.id == user_id)
        res = await self.db_context.scalar(stmt)
        if not res:
            raise EntityNotFound(msg="")
        return model_to_dto(model=res)

    async def create(self, *, user_obj: UserCreateDTO, sub_obj: Subscription) -> User:
        stmt = insert(UserModel).values(**asdict(user_obj)).returning(UserModel)
        try:
            res = await self.db_context.scalar(stmt)
        except IntegrityError as error:
            error.orig = cast(BaseException, error.orig)
            if isinstance(error.orig.__cause__, UniqueViolationError):
                raise EntityNotChange(msg="Uniq failed") from error
            raise EntityNotCreated(msg="") from error
        if not res:
            raise EntityNotFound(msg="")

        return model_to_dto(model=res)

    async def update(self, *, obj: UserUpdateDTO) -> User:
        return await super().update(obj=obj)

    async def update_subscription(self, *, user_id: str, sub_id: int) -> User:
        return await super().update_subscription(user_id=user_id, sub_id=sub_id)
