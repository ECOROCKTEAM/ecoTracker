from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.dto.challenges.mission import (
    MissionCommunityCreateDTO,
    MissionCommunityUpdateDTO,
    MissionUserCreateDTO,
    MissionUserUpdateDTO,
)
from src.core.dto.mock import MockObj
from src.core.entity.mission import Mission, MissionCommunity, MissionUser
from src.core.enum.language import LanguageEnum
from src.core.exception.base import EntityNotFound
from src.core.interfaces.repository.challenges.mission import (
    IRepositoryMission,
    MissionCommunityFilter,
    MissionFilter,
    MissionUserFilter,
)
from src.data.models.challenges.mission import MissionModel
from src.data.repository.challenges.mapper import category_model_to_dto, select_translation


def model_to_dto(model: MissionModel, lang: LanguageEnum) -> Mission:
    translation = select_translation(translations=model.translations, lang=lang)
    return Mission(
        id=model.id,
        name=translation.name,
        active=model.active,
        score=model.score,
        description=translation.description,
        instruction=translation.instruction,
        category=category_model_to_dto(model=model.category, lang=lang),
        language=translation.language,
    )


class RepositoryMission(IRepositoryMission):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def get(self, *, id: int, lang: LanguageEnum) -> Mission:
        model = await self.db_context.get(entity=MissionModel, ident={"id": id})
        if not model:
            raise EntityNotFound(msg="")
        return model_to_dto(model=model, lang=lang)

    async def lst(
        self, *, filter_obj: MissionFilter, order_obj: MockObj, pagination_obj: MockObj, lang: LanguageEnum
    ) -> list[Mission]:
        where_clause = []
        if filter_obj.active:
            where_clause.append(MissionModel.active == filter_obj.active)
        stmt = select(MissionModel).where(*where_clause)  # todo .order_by().limit().offset()
        res = await self.db_context.scalars(stmt)
        return [model_to_dto(model, lang) for model in res]

    async def user_mission_get(self, *, id: int, lang: LanguageEnum) -> MissionUser:
        return await super().user_mission_get(id=id, lang=lang)

    async def user_mission_create(self, *, obj: MissionUserCreateDTO, lang: LanguageEnum) -> MissionUser:
        return await super().user_mission_create(obj=obj, lang=lang)

    async def user_mission_update(self, *, obj: MissionUserUpdateDTO, lang: LanguageEnum) -> MissionUser:
        return await super().user_mission_update(obj=obj, lang=lang)

    async def user_mission_lst(
        self, *, filter_obj: MissionUserFilter, order_obj: MockObj, pagination_obj: MockObj, lang: LanguageEnum
    ) -> list[MissionUser]:
        return await super().user_mission_lst(
            filter_obj=filter_obj, order_obj=order_obj, pagination_obj=pagination_obj, lang=lang
        )

    async def community_mission_create(self, *, obj: MissionCommunityCreateDTO, lang: LanguageEnum) -> MissionCommunity:
        return await super().community_mission_create(obj=obj, lang=lang)

    async def community_mission_get(self, *, id: int, lang: LanguageEnum) -> MissionCommunity:
        return await super().community_mission_get(id=id, lang=lang)

    async def community_mission_update(self, *, obj: MissionCommunityUpdateDTO, lang: LanguageEnum) -> MissionCommunity:
        return await super().community_mission_update(obj=obj, lang=lang)

    async def community_mission_lst(
        self, *, filter_obj: MissionCommunityFilter, order_obj: MockObj, pagination_obj: MockObj, lang: LanguageEnum
    ) -> list[MissionCommunity]:
        return await super().community_mission_lst(
            filter_obj=filter_obj, order_obj=order_obj, pagination_obj=pagination_obj, lang=lang
        )
