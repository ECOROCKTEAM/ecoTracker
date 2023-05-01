from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import asdict

from src.core.dto.community.filters import CommunityIncludeUserFilter, CommunityListFilter
from src.core.dto.community.invite import CommunityInviteUpdateDTO, CommunityInviteDTO, CommunityInviteCreateDTO
from src.core.dto.m2m.user.community import UserCommunityUpdateDTO, UserCommunityDTO, UserCommunityCreateDTO
from src.core.dto.mock import MockObj
from src.core.entity.community import Community, CommunityUpdateDTO, CommunityCreateDTO
from src.core.interfaces.repository.community.community import IRepositoryCommunity
from src.data.models.community.community import CommunityModel


def model_to_dto(model: CommunityModel) -> Community:
    return Community(name=model.name, privacy=model.privacy, active=model.active, description=model.description)


def dto_to_model(dto: Community) -> CommunityModel:
    pass


class RepositoryCommunity(IRepositoryCommunity):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def get(self, *, id: str) -> Community:
        stmt = select(CommunityModel).where(CommunityModel.name == id)
        result = await self.db_context.scalar(stmt)
        if result:
            return model_to_dto(result)

    async def create(self, *, obj: CommunityCreateDTO) -> Community:
        stmt = insert(CommunityModel).values(**asdict(obj)).returning(CommunityModel)
        res = await self.db_context.scalar(stmt)
        return model_to_dto(res)

    async def update(self, *, id: str, obj: CommunityUpdateDTO) -> Community:
        pass

    async def list_(
        self, *, filter_obj: CommunityListFilter, order_obj: MockObj, pagination_obj: MockObj
    ) -> list[Community]:
        pass

    async def deactivate(self, *, id: str) -> str:
        pass

    async def user_add(self, *, obj: UserCommunityCreateDTO) -> UserCommunityDTO:
        pass

    async def user_get(self, *, id: int) -> UserCommunityDTO:
        pass

    async def user_list(self, *, id: str, filter: CommunityIncludeUserFilter) -> list[UserCommunityDTO]:
        pass

    async def user_role_update(self, *, obj: UserCommunityUpdateDTO) -> UserCommunityDTO:
        pass

    async def invite_link_create(self, *, obj: CommunityInviteCreateDTO) -> CommunityInviteDTO:
        pass

    async def invite_link_get(self, *, id: str) -> CommunityInviteDTO:
        pass

    async def invite_link_update(self, *, obj: CommunityInviteUpdateDTO) -> CommunityInviteDTO:
        pass


# async def _update(self, *, obj: UserTaskUpdateDTO) -> UserTaskDTO:
#     values = asdict(obj)
#     id_ = values.pop("id")
#     stmt = update(TaskModel).where(id=id_).values(**values).returning(TaskModel)
#     result: TaskModel = await self.db_contex.scalar(stmt)
#     return model_to_dto(result)
#
# async def _delete(self, *, id: int) -> int:
#     stmt = delete(TaskModel).where(TaskModel.id == id).returning(TaskModel.id)
#     result = await self.db_contex.scalar(stmt)
#     return result
#
