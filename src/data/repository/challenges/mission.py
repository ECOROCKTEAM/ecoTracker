import typing
from dataclasses import asdict

from asyncpg.exceptions import ForeignKeyViolationError
from sqlalchemy import and_, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.const.translate import DEFAULT_LANGUANGE
from src.core.dto.challenges.mission import (
    MissionGroupCreateDTO,
    MissionGroupUpdateDTO,
    MissionUserCreateDTO,
    MissionUserUpdateDTO,
)
from src.core.dto.mock import MockObj
from src.core.entity.mission import Mission, MissionGroup, MissionUser
from src.core.enum.language import LanguageEnum
from src.core.exception.base import EntityNotCreated, EntityNotFound, TranslateNotFound
from src.core.interfaces.repository.challenges.mission import (
    IRepositoryMission,
    MissionFilter,
    MissionGroupFilter,
    MissionUserFilter,
)
from src.data.models.challenges.mission import (
    GroupMissionModel,
    MissionModel,
    MissionTranslateModel,
    UserMissionModel,
)


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
        id=model.id,
        user_id=model.user_id,
        mission_id=model.mission_id,
        date_start=model.date_start,
        date_close=model.date_close,
        status=model.status,
    )


def mission_group_to_entity(model: GroupMissionModel) -> MissionGroup:
    return MissionGroup(
        id=model.id,
        group_id=model.group_id,
        mission_id=model.mission_id,
        status=model.status,
        date_start=model.date_start,
        date_close=model.date_close,
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
        if filter_obj.active is not None:
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

    async def user_mission_get(self, *, id: int, user_id: int) -> MissionUser:
        stmt = select(UserMissionModel).where(
            and_(
                UserMissionModel.id == id,
                UserMissionModel.user_id == user_id,
            )
        )
        model = await self.db_context.scalar(stmt)
        if not model:
            raise EntityNotFound(msg="")
        return mission_user_to_entity(model)

    async def user_mission_create(self, *, user_id: int, obj: MissionUserCreateDTO) -> MissionUser:
        stmt = insert(UserMissionModel).values(user_id=user_id, **asdict(obj)).returning(UserMissionModel)
        try:
            res = await self.db_context.scalar(stmt)
        except IntegrityError as error:
            error.orig = typing.cast(BaseException, error.orig)  # just for types
            if isinstance(error.orig.__cause__, ForeignKeyViolationError):
                raise EntityNotCreated(msg="Not found fk") from error
            raise EntityNotCreated(msg="") from error
        res = typing.cast(UserMissionModel, res)  # just for types
        await self.db_context.refresh(res)
        return mission_user_to_entity(res)

    async def user_mission_update(self, *, id: int, user_id: int, obj: MissionUserUpdateDTO) -> MissionUser:
        stmt = (
            update(UserMissionModel)
            .where(
                and_(
                    UserMissionModel.id == id,
                    UserMissionModel.user_id == user_id,
                )
            )
            .values(**obj.to_dict())
            .returning(UserMissionModel)
        )
        res = await self.db_context.scalar(stmt)
        if not res:
            raise EntityNotFound(msg="")
        await self.db_context.refresh(res)
        return mission_user_to_entity(res)

    async def user_mission_lst(
        self, *, user_id: int, filter_obj: MissionUserFilter, order_obj: MockObj, pagination_obj: MockObj
    ) -> list[MissionUser]:
        stmt = select(UserMissionModel)
        where_clause = []
        where_clause.append(UserMissionModel.user_id == user_id)
        if filter_obj.mission_id is not None:
            where_clause.append(UserMissionModel.mission_id == filter_obj.mission_id)
        if filter_obj.status is not None:
            where_clause.append(UserMissionModel.status == filter_obj.status)
        stmt = stmt.where(*where_clause)
        res = await self.db_context.scalars(stmt)
        return [mission_user_to_entity(model) for model in res]

    async def group_mission_create(self, *, group_id: int, obj: MissionGroupCreateDTO) -> MissionGroup:
        stmt = insert(GroupMissionModel).values(group_id=group_id, **asdict(obj)).returning(GroupMissionModel)
        try:
            res = await self.db_context.scalar(stmt)
        except IntegrityError as error:
            error.orig = typing.cast(BaseException, error.orig)  # just for types
            if isinstance(error.orig.__cause__, ForeignKeyViolationError):
                raise EntityNotCreated(msg="Not found fk") from error
            raise EntityNotCreated(msg="") from error
        if res is None:
            raise EntityNotCreated(msg="")
        await self.db_context.refresh(res)
        return mission_group_to_entity(res)

    async def group_mission_get(self, *, id: int, group_id: int) -> MissionGroup:
        stmt = select(GroupMissionModel).where(and_(GroupMissionModel.id == id, GroupMissionModel.group_id == group_id))
        model = await self.db_context.scalar(stmt)
        if not model:
            raise EntityNotFound(msg="")
        return mission_group_to_entity(model)

    async def group_mission_update(self, *, id: int, group_id: int, obj: MissionGroupUpdateDTO) -> MissionGroup:
        stmt = (
            update(GroupMissionModel)
            .where(
                and_(
                    GroupMissionModel.id == id,
                    GroupMissionModel.group_id == group_id,
                )
            )
            .values(**obj.to_dict())
            .returning(GroupMissionModel)
        )
        res = await self.db_context.scalar(stmt)
        if not res:
            raise EntityNotFound(msg="")
        await self.db_context.refresh(res)
        return mission_group_to_entity(res)

    async def group_mission_lst(
        self, *, filter_obj: MissionGroupFilter, order_obj: MockObj, pagination_obj: MockObj
    ) -> list[MissionGroup]:
        where_clause = []
        stmt = select(GroupMissionModel)
        if filter_obj.group_id_list is not None:
            where_clause.append(GroupMissionModel.group_id.in_(filter_obj.group_id_list))
        if filter_obj.group_id is not None:
            where_clause.append(GroupMissionModel.group_id == filter_obj.group_id)
        if filter_obj.mission_id is not None:
            where_clause.append(GroupMissionModel.mission_id == filter_obj.mission_id)
        if filter_obj.status is not None:
            where_clause.append(GroupMissionModel.status == filter_obj.status)
        stmt = stmt.where(*where_clause)
        res = await self.db_context.scalars(stmt)
        return [mission_group_to_entity(model) for model in res]
