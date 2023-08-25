import typing
from dataclasses import asdict

from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.group.group import GroupCreateDTO, GroupUpdateDTO
from src.core.dto.group.invite import GroupInviteDTO, GroupInviteUpdateDTO
from src.core.dto.m2m.user.group import (
    UserGroupCreateDTO,
    UserGroupDTO,
    UserGroupUpdateDTO,
)
from src.core.dto.mock import MockObj
from src.core.entity.group import Group
from src.core.enum.group.role import GroupRoleEnum
from src.core.exception.base import EntityNotChange, EntityNotCreated, EntityNotFound
from src.core.interfaces.repository.group.group import (
    GroupFilter,
    GroupUserFilter,
    IRepositoryGroup,
)
from src.data.models.group.group import GroupModel
from src.data.models.user.user import UserGroupModel
from src.utils import as_dict_skip_none


def model_to_dto(model: GroupModel) -> Group:
    return Group(
        id=model.id, name=model.name, privacy=model.privacy, active=model.active, description=model.description
    )


def user_group_model_to_dto(model: UserGroupModel) -> UserGroupDTO:
    return UserGroupDTO(user_id=model.user_id, group_id=model.group_id, role=model.role)


def model_to_invite_dto(model: GroupModel) -> GroupInviteDTO:
    return GroupInviteDTO(group_id=model.id, code=model.code, expire_time=model.code_expire_time)


class RepositoryGroup(IRepositoryGroup):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def get(self, *, id: int) -> Group:
        stmt = select(GroupModel).where(GroupModel.id == id)
        res = await self.db_context.scalar(stmt)
        if not res:
            raise EntityNotFound(msg="")
        return model_to_dto(res)

    async def create(self, *, obj: GroupCreateDTO) -> Group:
        stmt = insert(GroupModel).values(**asdict(obj)).returning(GroupModel)
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

    async def update(self, *, id: int, obj: GroupUpdateDTO) -> Group:
        stmt = update(GroupModel).where(GroupModel.id == id).values(**as_dict_skip_none(obj)).returning(GroupModel)
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

    async def lst(self, *, filter_obj: GroupFilter, order_obj: MockObj, pagination_obj: MockObj) -> list[Group]:
        stmt = select(GroupModel)
        where_clause = []
        if filter_obj.user_id is not None:
            stmt = stmt.join(UserGroupModel)
            where_clause.append(UserGroupModel.user_id == filter_obj.user_id)
            where_clause.append(UserGroupModel.role != GroupRoleEnum.BLOCKED)
        if filter_obj.active is not None:
            where_clause.append(GroupModel.active == filter_obj.active)
        stmt = stmt.where(*where_clause)  # todo .order_by().limit().offset()
        res = await self.db_context.scalars(stmt)
        return [model_to_dto(model) for model in res]

    async def deactivate(self, *, id: int) -> int:
        stmt = update(GroupModel).where(GroupModel.id == id).values(active=False).returning(GroupModel.id)
        res = await self.db_context.scalar(stmt)
        if not res:
            raise EntityNotFound(msg="")
        return res

    async def user_add(self, *, obj: UserGroupCreateDTO) -> UserGroupDTO:
        stmt = insert(UserGroupModel).values(asdict(obj)).returning(UserGroupModel)
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
        return user_group_model_to_dto(res)

    async def user_get(
        self,
        *,
        group_id: int,
        user_id: int,
    ) -> UserGroupDTO:
        stmt = select(UserGroupModel).where(UserGroupModel.user_id == user_id, UserGroupModel.group_id == group_id)
        res = await self.db_context.scalar(stmt)
        if not res:
            raise EntityNotFound(msg="")
        return user_group_model_to_dto(res)

    async def user_list(self, *, id: int, filter_obj: GroupUserFilter) -> list[UserGroupDTO]:
        stmt = select(UserGroupModel).join(GroupModel)
        where_clause = [GroupModel.id == id]
        if filter_obj.role_list:
            where_clause.append(UserGroupModel.role.in_(filter_obj.role_list))
        if filter_obj.user_id__in is not None:
            where_clause.append(UserGroupModel.user_id.in_(filter_obj.user_id__in))
        stmt = stmt.where(*where_clause)
        res = await self.db_context.scalars(stmt)
        return [user_group_model_to_dto(model) for model in res]

    async def user_role_update(self, *, group_id: int, user_id: int, obj: UserGroupUpdateDTO) -> UserGroupDTO:
        stmt = (
            update(UserGroupModel)
            .where(UserGroupModel.group_id == group_id, UserGroupModel.user_id == user_id)
            .values(as_dict_skip_none(obj))
            .returning(UserGroupModel)
        )
        res = await self.db_context.scalar(stmt)
        if not res:
            raise EntityNotFound(msg="")
        return user_group_model_to_dto(res)

    async def user_remove(self, *, group_id: int, user_id: int) -> bool:
        stmt = (
            delete(UserGroupModel)
            .where(UserGroupModel.group_id == group_id, UserGroupModel.user_id == user_id)
            .returning(UserGroupModel.group_id)
        )
        res = await self.db_context.scalar(stmt)
        return bool(res)

    async def code_set(self, *, id: int, obj: GroupInviteUpdateDTO) -> GroupInviteDTO:
        stmt = (
            update(GroupModel)
            .where(GroupModel.id == id)
            .values(code=obj.code, code_expire_time=obj.expire_time)
            .returning(GroupModel)
        )
        res = await self.db_context.scalar(stmt)
        if not res:
            raise EntityNotFound(msg="")
        await self.db_context.refresh(res)
        return model_to_invite_dto(res)

    async def code_get(self, *, id: int) -> GroupInviteDTO:
        stmt = select(GroupModel).where(GroupModel.id == id)
        res = await self.db_context.scalar(stmt)
        if not res:
            raise EntityNotFound(msg="")
        return model_to_invite_dto(res)

    async def get_by_code(self, code: str) -> Group:
        stmt = select(GroupModel).where(GroupModel.code == code, GroupModel.code_expire_time > func.now())
        res = await self.db_context.scalar(stmt)
        if not res:
            raise EntityNotFound(msg="")
        return model_to_dto(res)
