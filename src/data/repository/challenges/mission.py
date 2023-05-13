from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.const.translate import DEFAULT_LANGUANGE
from src.core.dto.challenges.mission import (
    MissionCommunityCreateDTO,
    MissionCommunityUpdateDTO,
    MissionUserCreateDTO,
    MissionUserUpdateDTO,
)
from src.core.dto.mock import MockObj
from src.core.entity.mission import Mission, MissionCommunity, MissionUser
from src.core.enum.language import LanguageEnum
from src.core.exception.base import EntityNotFound, TranslateNotFound
from src.core.interfaces.repository.challenges.mission import (
    IRepositoryMission,
    MissionCommunityFilter,
    MissionFilter,
    MissionUserFilter,
)
from src.data.models.challenges.mission import MissionModel, MissionTranslateModel


def model_to_dto(model: MissionModel, model_translate: MissionTranslateModel) -> Mission:
    return Mission(
        id=model.id,
        name=model_translate.name,
        active=model.active,
        score=model.score,
        description=model_translate.description,
        instruction=model_translate.instruction,
        category_id=model.category_id,
        language=model_translate.language,
    )


class RepositoryMission(IRepositoryMission):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def get(self, *, id: int, lang: LanguageEnum) -> Mission:
        stmt = (
            select(
                MissionModel,
                MissionTranslateModel,
            )
            .join(
                MissionTranslateModel,
                and_(MissionModel.id == MissionTranslateModel.mission_id, MissionTranslateModel.language == lang),
                isouter=True,
            )
            .where(MissionModel.id == id)
        )
        coro = await self.db_context.execute(stmt)
        res = coro.one_or_none()
        if res is None:
            raise EntityNotFound(msg="")
        model, model_translate = res
        if model_translate is None:
            stmt_mission_negative = select(
                MissionTranslateModel,
            ).where(
                and_(
                    MissionTranslateModel.mission_id == id,
                    MissionTranslateModel.language == DEFAULT_LANGUANGE,
                )
            )
            model_translate = await self.db_context.scalar(stmt_mission_negative)
            if model_translate is None:
                raise TranslateNotFound(msg="")
        return model_to_dto(model=model, model_translate=model_translate)

    async def lst(
        self, *, filter_obj: MissionFilter, order_obj: MockObj, pagination_obj: MockObj, lang: LanguageEnum
    ) -> list[Mission]:
        where_clause = []
        if filter_obj.active:
            where_clause.append(MissionModel.active == filter_obj.active)
        stmt = (
            select(
                MissionModel,
                MissionTranslateModel,
            )
            .join(
                MissionTranslateModel,
                and_(MissionModel.id == MissionTranslateModel.mission_id, MissionTranslateModel.language == lang),
                isouter=True,
            )
            .where(*where_clause)
        )  # todo .order_by().limit().offset()

        coro = await self.db_context.execute(stmt)
        res = coro.all()
        holder = {}
        mission_default_lang_ids = []
        for mission, mission_translate in res:
            if mission_translate is None:
                mission_default_lang_ids.append(mission.id)
            holder[mission.id] = {}
            holder[mission.id]["model"] = mission
            holder[mission.id]["translate"] = mission_translate
        if len(mission_default_lang_ids) > 0:
            stmt_mission_negative = select(
                MissionTranslateModel,
            ).where(
                and_(
                    MissionTranslateModel.mission_id.in_(mission_default_lang_ids),
                    MissionTranslateModel.language == DEFAULT_LANGUANGE,
                )
            )
            coro = await self.db_context.scalars(stmt_mission_negative)
            result = coro.all()
            for model in result:
                holder[model.mission_id]["translate"] = model

        entity_list: list[Mission] = []
        for models in holder.values():
            mission = models["model"]
            mission_translate = models["translate"]
            entity_list.append(model_to_dto(model=mission, model_translate=mission_translate))
        return entity_list

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
