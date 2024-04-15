from dataclasses import asdict
from typing import cast

from asyncpg import UniqueViolationError
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.entity.subscription import Subscription
from src.core.entity.user import User, UserCreateDTO, UserUpdateDTO
from src.core.exception.base import EntityNotCreated, EntityNotFound
from src.core.interfaces.repository.user.user import IUserRepository
from src.data.models.user.user import UserModel


def model_to_dto(model: UserModel, premium: bool = True) -> User:
    return User(
        id=model.id,
        username=model.username,
        subscription=Subscription(),
        active=model.active,
        language=model.language,
        premium=premium,
    )


class UserRepository(IUserRepository):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def get(self, *, id: str) -> User:
        stmt = select(UserModel).where(UserModel.id == id)
        res = await self.db_context.scalar(stmt)
        if not res:
            raise EntityNotFound(msg="")
        return model_to_dto(model=res)

    async def create(self, *, obj: UserCreateDTO) -> User:
        stmt = insert(UserModel).values(**asdict(obj)).returning(UserModel)
        try:
            res = await self.db_context.scalar(stmt)
        except IntegrityError as error:
            error.orig = cast(BaseException, error.orig)
            if isinstance(error.orig.__cause__, UniqueViolationError):
                raise EntityNotCreated(msg="Uniq failed") from error
            raise EntityNotCreated(msg="") from error
        if not res:
            raise EntityNotFound(msg="")

        return model_to_dto(model=res)

    async def update(self, *, obj: UserUpdateDTO) -> User:
        return await super().update(obj=obj)

    async def update_subscription(self, *, user_id: str, sub_id: int) -> User:
        return await super().update_subscription(user_id=user_id, sub_id=sub_id)
