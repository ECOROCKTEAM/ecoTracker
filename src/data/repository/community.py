import typing
from dataclasses import asdict

from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.community.community import CommunityCreateDTO, CommunityUpdateDTO
from src.core.dto.community.invite import CommunityInviteDTO, CommunityInviteUpdateDTO
from src.core.dto.m2m.user.community import (
    UserCommunityCreateDTO,
    UserCommunityDTO,
    UserCommunityUpdateDTO,
)
from src.core.dto.mock import MockObj
from src.core.entity.community import Community
from src.core.enum.community.role import CommunityRoleEnum
from src.core.exception.base import EntityNotChange, EntityNotCreated, EntityNotFound
from src.core.interfaces.repository.community.community import (
    CommunityFilter,
    CommunityUserFilter,
    IRepositoryCommunity,
)
from src.data.models.community.community import CommunityModel
from src.data.models.user.user import UserCommunityModel
from src.utils import as_dict_skip_none


def model_to_dto(model: CommunityModel) -> Community:
    return Community(
        id=model.id, name=model.name, privacy=model.privacy, active=model.active, description=model.description
    )


def user_community_model_to_dto(model: UserCommunityModel) -> UserCommunityDTO:
    return UserCommunityDTO(user_id=model.user_id, community_id=model.community_id, role=model.role)


def model_to_invite_dto(model: CommunityModel) -> CommunityInviteDTO:
    return CommunityInviteDTO(community_id=model.id, code=model.code, expire_time=model.code_expire_time)


class RepositoryCommunity(IRepositoryCommunity):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def get(self, *, id: int) -> Community:
        stmt = select(CommunityModel).where(CommunityModel.id == id)
        res = await self.db_context.scalar(stmt)
        if not res:
            raise EntityNotFound(msg="")
        return model_to_dto(res)

    async def create(self, *, obj: CommunityCreateDTO) -> Community:
        stmt = insert(CommunityModel).values(**asdict(obj)).returning(CommunityModel)
        try:
            res = await self.db_context.scalar(stmt)
        except IntegrityError as error:
            error.orig = typing.cast(BaseException, error.orig)  # just for types
            if isinstance(error.orig.__cause__, UniqueViolationError):
                raise EntityNotCreated(msg="Uniq failed") from error
            raise EntityNotCreated(msg="") from error
        if not res:
            raise EntityNotFound(msg="")
        return model_to_dto(res)

    async def update(self, *, id: int, obj: CommunityUpdateDTO) -> Community:
        stmt = (
            update(CommunityModel)
            .where(CommunityModel.id == id)
            .values(**as_dict_skip_none(obj))
            .returning(CommunityModel)
        )
        try:
            res = await self.db_context.scalar(stmt)
        except IntegrityError as error:
            error.orig = typing.cast(BaseException, error.orig)  # just for types
            if isinstance(error.orig.__cause__, UniqueViolationError):
                raise EntityNotChange(msg="Uniq failed") from error
            raise EntityNotChange(msg="") from error
        if not res:
            raise EntityNotFound(msg="")
        return model_to_dto(res)

    async def lst(self, *, filter_obj: CommunityFilter, order_obj: MockObj, pagination_obj: MockObj) -> list[Community]:
        stmt = select(CommunityModel)
        where_clause = []
        if filter_obj.user_id is not None:
            stmt = stmt.join(UserCommunityModel)
            where_clause.append(UserCommunityModel.user_id == filter_obj.user_id)
            where_clause.append(UserCommunityModel.role != CommunityRoleEnum.BLOCKED)
        if filter_obj.active is not None:
            where_clause.append(CommunityModel.active == filter_obj.active)
        stmt = stmt.where(*where_clause)  # todo .order_by().limit().offset()
        res = await self.db_context.scalars(stmt)
        return [model_to_dto(model) for model in res]

    async def deactivate(self, *, id: int) -> int:
        stmt = update(CommunityModel).where(CommunityModel.id == id).values(active=False).returning(CommunityModel.id)
        res = await self.db_context.scalar(stmt)
        if not res:
            raise EntityNotFound(msg="")
        return res

    async def user_add(self, *, obj: UserCommunityCreateDTO) -> UserCommunityDTO:
        stmt = insert(UserCommunityModel).values(asdict(obj)).returning(UserCommunityModel)
        try:
            res = await self.db_context.scalar(stmt)
        except IntegrityError as error:
            error.orig = typing.cast(BaseException, error.orig)  # just for types
            if isinstance(error.orig.__cause__, ForeignKeyViolationError):
                raise EntityNotCreated(msg="Not found fk") from error
            if isinstance(error.orig.__cause__, UniqueViolationError):
                raise EntityNotCreated(msg="Uniq fail") from error
            raise EntityNotCreated(msg="") from error
        if not res:
            raise EntityNotFound(msg="")
        return user_community_model_to_dto(res)

    async def user_get(
        self,
        *,
        community_id: int,
        user_id: int,
    ) -> UserCommunityDTO:
        stmt = select(UserCommunityModel).where(
            UserCommunityModel.user_id == user_id, UserCommunityModel.community_id == community_id
        )
        res = await self.db_context.scalar(stmt)
        if not res:
            raise EntityNotFound(msg="")
        return user_community_model_to_dto(res)

    async def user_list(self, *, id: int, filter_obj: CommunityUserFilter) -> list[UserCommunityDTO]:
        stmt = select(UserCommunityModel).join(CommunityModel)
        where_clause = [CommunityModel.id == id]
        if filter_obj.role_list:
            where_clause.append(UserCommunityModel.role.in_(filter_obj.role_list))
        stmt = stmt.where(*where_clause)
        res = await self.db_context.scalars(stmt)
        return [user_community_model_to_dto(model) for model in res]

    async def user_role_update(
        self, *, community_id: int, user_id: int, obj: UserCommunityUpdateDTO
    ) -> UserCommunityDTO:
        stmt = (
            update(UserCommunityModel)
            .where(UserCommunityModel.community_id == community_id, UserCommunityModel.user_id == user_id)
            .values(as_dict_skip_none(obj))
            .returning(UserCommunityModel)
        )
        res = await self.db_context.scalar(stmt)
        if not res:
            raise EntityNotFound(msg="")
        return user_community_model_to_dto(res)

    async def user_remove(self, *, community_id: int, user_id: int) -> bool:
        stmt = (
            delete(UserCommunityModel)
            .where(UserCommunityModel.community_id == community_id, UserCommunityModel.user_id == user_id)
            .returning(UserCommunityModel.community_id)
        )
        res = await self.db_context.scalar(stmt)
        return bool(res)

    async def code_set(self, *, id: int, obj: CommunityInviteUpdateDTO) -> CommunityInviteDTO:
        stmt = (
            update(CommunityModel)
            .where(CommunityModel.id == id)
            .values(code=obj.code, code_expire_time=obj.expire_time)
            .returning(CommunityModel)
        )
        res = await self.db_context.scalar(stmt)
        if not res:
            raise EntityNotFound(msg="")
        await self.db_context.refresh(res)
        return model_to_invite_dto(res)

    async def code_get(self, *, id: int) -> CommunityInviteDTO:
        stmt = select(CommunityModel).where(CommunityModel.id == id)
        res = await self.db_context.scalar(stmt)
        if not res:
            raise EntityNotFound(msg="")
        return model_to_invite_dto(res)

    async def get_by_code(self, code: str) -> Community:
        stmt = select(CommunityModel).where(CommunityModel.code == code, CommunityModel.code_expire_time > func.now())
        res = await self.db_context.scalar(stmt)
        if not res:
            raise EntityNotFound(msg="")
        return model_to_dto(res)
