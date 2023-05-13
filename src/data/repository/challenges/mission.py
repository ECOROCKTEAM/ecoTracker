from dataclasses import asdict

from sqlalchemy import and_, insert, select, update
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
from src.core.exception.base import EntityNotCreated, EntityNotFound, TranslateNotFound
from src.core.interfaces.repository.challenges.mission import (
    IRepositoryMission,
    MissionCommunityFilter,
    MissionFilter,
    MissionUserFilter,
)
from src.data.models.challenges.mission import MissionModel, MissionTranslateModel
from src.data.models.community.community import CommunityMissionModel
from src.data.models.user.user import UserMissionModel


def mission_to_entity(model: MissionModel, model_translate: MissionTranslateModel) -> Mission:
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


def mission_user_to_entity(model: UserMissionModel) -> MissionUser:
    return MissionUser(
        user_id=model.user_id,
        mission_id=model.mission_id,
        status=model.status,
    )


def mission_community_to_entity(model: CommunityMissionModel) -> MissionCommunity:
    return MissionCommunity(
        community_id=model.community_id,
        mission_id=model.mission_id,
        status=model.status,
        author=model.author,
        place=model.place,
        meeting_date=model.meeting_date,
        people_required=model.people_required,
        people_max=model.people_max,
        comment=model.comment,
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
        return mission_to_entity(model=model, model_translate=model_translate)

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
            entity_list.append(mission_to_entity(model=mission, model_translate=mission_translate))
        return entity_list

    async def user_mission_get(self, *, user_id: int, mission_id: int) -> MissionUser:
        model = await self.db_context.get(entity=UserMissionModel, ident={"user_id": user_id, "mission_id": mission_id})
        if not model:
            raise EntityNotFound(msg="")
        return mission_user_to_entity(model)

    async def user_mission_create(self, *, obj: MissionUserCreateDTO) -> MissionUser:
        stmt = insert(UserMissionModel).values(asdict(obj)).returning(UserMissionModel)
        res = await self.db_context.scalar(stmt)
        if res is None:
            raise EntityNotCreated(msg="")
        return mission_user_to_entity(res)

    async def user_mission_update(self, *, user_id: int, mission_id: int, obj: MissionUserUpdateDTO) -> MissionUser:
        stmt = (
            update(UserMissionModel)
            .where(and_(UserMissionModel.user_id == user_id, UserMissionModel.mission_id == mission_id))
            .values(**obj.to_dict())
            .returning(UserMissionModel)
        )
        res = await self.db_context.scalar(stmt)
        if not res:
            raise EntityNotFound(msg="")
        return mission_user_to_entity(res)

    async def user_mission_lst(
        self, *, filter_obj: MissionUserFilter, order_obj: MockObj, pagination_obj: MockObj
    ) -> list[MissionUser]:
        where_clause = []
        if filter_obj.user_id:
            where_clause.append(UserMissionModel.user_id == filter_obj.user_id)
        if filter_obj.mission_id:
            where_clause.append(UserMissionModel.mission_id == filter_obj.mission_id)
        if filter_obj.status:
            where_clause.append(UserMissionModel.status == filter_obj.status)
        stmt = select(UserMissionModel).where(*where_clause)
        res = await self.db_context.scalars(stmt)
        return [mission_user_to_entity(model) for model in res]

    async def community_mission_create(self, *, obj: MissionCommunityCreateDTO) -> MissionCommunity:
        stmt = insert(CommunityMissionModel).values(asdict(obj)).returning(CommunityMissionModel)
        res = await self.db_context.scalar(stmt)
        if res is None:
            raise EntityNotCreated(msg="")
        return mission_community_to_entity(res)

    async def community_mission_get(self, *, community_id: int, mission_id: int) -> MissionCommunity:
        model = await self.db_context.get(
            entity=CommunityMissionModel, ident={"community_id": community_id, "mission_id": mission_id}
        )
        if not model:
            raise EntityNotFound(msg="")
        return mission_community_to_entity(model)

    async def community_mission_update(
        self, *, community_id: int, mission_id: int, obj: MissionCommunityUpdateDTO
    ) -> MissionCommunity:
        stmt = (
            update(CommunityMissionModel)
            .where(
                and_(CommunityMissionModel.community_id == community_id, CommunityMissionModel.mission_id == mission_id)
            )
            .values(**obj.to_dict())
            .returning(CommunityMissionModel)
        )
        res = await self.db_context.scalar(stmt)
        if not res:
            raise EntityNotFound(msg="")
        return mission_community_to_entity(res)

    async def community_mission_lst(
        self, *, filter_obj: MissionCommunityFilter, order_obj: MockObj, pagination_obj: MockObj
    ) -> list[MissionCommunity]:
        where_clause = []
        if filter_obj.community_id:
            where_clause.append(CommunityMissionModel.community_id == filter_obj.community_id)
        if filter_obj.mission_id:
            where_clause.append(CommunityMissionModel.mission_id == filter_obj.mission_id)
        if filter_obj.status:
            where_clause.append(CommunityMissionModel.status == filter_obj.status)
        stmt = select(CommunityMissionModel).where(*where_clause)
        res = await self.db_context.scalars(stmt)
        return [mission_community_to_entity(model) for model in res]
