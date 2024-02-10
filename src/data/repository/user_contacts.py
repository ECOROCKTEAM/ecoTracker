from dataclasses import asdict
from typing import cast

from asyncpg import UniqueViolationError
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.m2m.user.contact import (
    ContactUserCreateDTO,
    ContactUserDTO,
    ContactUserUpdateDTO,
)
from src.core.exception.base import EntityNotChange, EntityNotCreated, EntityNotFound
from src.core.interfaces.repository.user.contact import (
    IUserContactRepository,
    UserContactFilter,
    UserContactOrder,
    UserContactSorting,
)
from src.data.models.user.user import UserContactModel
from src.utils import as_dict_skip_none


def model_to_dto(model: UserContactModel) -> ContactUserDTO:
    return ContactUserDTO(
        id=model.id,
        user_id=model.user_id,
        value=model.value,
        type=model.type,
        active=model.active,
        is_favorite=model.is_favorite,
    )


class UserContactRepository(IUserContactRepository):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def get(self, *, id: int) -> ContactUserDTO:
        stmt = select(UserContactModel).where(UserContactModel.id == id)
        res = await self.db_context.scalar(stmt)
        if not res:
            raise EntityNotFound(msg=f"User contact {id=} not found")
        return model_to_dto(model=res)

    async def get_favorite(self, *, user_id: str) -> ContactUserDTO:
        stmt = select(UserContactModel).where(UserContactModel.user_id == user_id, UserContactModel.is_favorite)
        res = await self.db_context.scalar(stmt)
        if not res:
            raise EntityNotFound(msg="")
        return model_to_dto(model=res)

    async def delete(self, *, id: int) -> int:
        stmt = delete(UserContactModel).where(UserContactModel.id == id).returning(UserContactModel.id)
        res = await self.db_context.scalar(stmt)
        if not res:
            raise EntityNotFound(msg=f"User contact {id=} not found")
        return res

    async def set_favorite(self, *, id: int, is_favorite: bool) -> ContactUserDTO:
        stmt = (
            update(UserContactModel)
            .where(UserContactModel.id == id)
            .values(is_favorite=is_favorite)
            .returning(UserContactModel)
        )
        res = await self.db_context.scalar(stmt)
        if not res:
            raise EntityNotFound(msg="")
        return model_to_dto(model=res)

    async def create(self, *, user_id: str, obj: ContactUserCreateDTO) -> ContactUserDTO:
        stmt = insert(UserContactModel).values(user_id=user_id, **asdict(obj)).returning(UserContactModel)
        try:
            res = await self.db_context.scalar(stmt)
        except IntegrityError as error:
            error.orig = cast(BaseException, error.orig)  # just for types
            if isinstance(error.orig.__cause__, UniqueViolationError):
                raise EntityNotCreated(msg="Uniq failed") from error
            raise EntityNotCreated(msg="") from error
        if not res:
            raise EntityNotFound(msg="")
        return model_to_dto(model=res)

    async def update(self, *, obj: ContactUserUpdateDTO) -> ContactUserDTO:
        stmt = (
            update(UserContactModel)
            .where(UserContactModel.id == obj.id)
            .values(**as_dict_skip_none(obj))
            .returning(UserContactModel)
        )
        try:
            res = await self.db_context.scalar(stmt)
        except IntegrityError as error:
            error.orig = cast(BaseException, error.orig)  # just for types
            if isinstance(error.orig.__cause__, UniqueViolationError):
                raise EntityNotChange(msg="Uniq failed") from error
            raise EntityNotChange(msg="") from error
        if not res:
            raise EntityNotFound(msg="")
        return model_to_dto(model=res)

    async def list(
        self,
        *,
        user_id: str,
        filter_obj: UserContactFilter,
        sorting_obj: UserContactSorting,
        order_obj: UserContactOrder,
    ) -> list[ContactUserDTO]:
        where_clause = [UserContactModel.user_id == user_id]
        stmt = select(UserContactModel)
        if filter_obj.active is not None:
            where_clause.append(UserContactModel.active == filter_obj.active)
        if filter_obj.is_favorite is not None:
            where_clause.append(UserContactModel.is_favorite == filter_obj.is_favorite)
        if filter_obj.type is not None:
            where_clause.append(UserContactModel.type == filter_obj.type)
        stmt = stmt.where(*where_clause)
        res = await self.db_context.scalars(stmt)
        if not res:
            raise EntityNotFound(msg="")
        return [model_to_dto(item) for item in res]
