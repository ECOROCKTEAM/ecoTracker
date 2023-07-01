import typing
from dataclasses import asdict

from asyncpg.exceptions import ForeignKeyViolationError
from sqlalchemy import and_, delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.const.translate import DEFAULT_LANGUANGE
from src.core.dto.challenges.task import (
    TaskUserCreateDTO,
    TaskUserPlanCreateDTO,
    TaskUserUpdateDTO,
)
from src.core.dto.mock import MockObj
from src.core.entity.task import Task, TaskUser, TaskUserPlan
from src.core.enum.language import LanguageEnum
from src.core.exception.base import EntityNotCreated, EntityNotFound, TranslateNotFound
from src.core.interfaces.repository.challenges.task import (
    IRepositoryTask,
    TaskFilter,
    TaskUserFilter,
    TaskUserPlanFilter,
)
from src.data.models.challenges.task import (
    TaskModel,
    TaskTranslateModel,
    UserTaskModel,
    UserTaskPlanModel,
)
from src.utils import as_dict_skip_none


def plan_model_to_entity(model: UserTaskPlanModel) -> TaskUserPlan:
    return TaskUserPlan(
        user_id=model.user_id,
        task_id=model.task_id,
    )


def task_model_to_entity(model: TaskModel, translated_model: TaskTranslateModel) -> Task:
    return Task(
        id=model.id,
        score=model.score,
        category_id=model.category_id,
        name=translated_model.name,
        active=model.active,
        description=translated_model.description,
        language=translated_model.language,
    )


def user_task_to_entity(model: UserTaskModel) -> TaskUser:
    return TaskUser(
        id=model.id,
        date_start=model.date_start,
        date_close=model.date_close,
        status=model.status,
        user_id=model.user_id,
        task_id=model.task_id,
    )


class RepositoryTask(IRepositoryTask):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def get(self, *, id: int, lang: LanguageEnum) -> Task:
        stmt = (
            select(TaskModel, TaskTranslateModel)
            .join(
                TaskTranslateModel,
                and_(TaskModel.id == TaskTranslateModel.task_id, TaskTranslateModel.language == lang),
                isouter=True,
            )
            .where(TaskModel.id == id)
        )
        record = await self.db_context.execute(stmt)
        result = record.one_or_none()
        if result is None:
            raise EntityNotFound(msg=f"Task.id={id} not found")
        task, task_translate = result
        if task_translate is None:
            task_default_lang = select(TaskTranslateModel).where(
                and_(TaskTranslateModel.task_id == id, TaskTranslateModel.language == DEFAULT_LANGUANGE)
            )
            task_translate = await self.db_context.scalar(task_default_lang)
            if task_translate is None:
                raise TranslateNotFound(msg=f"Task={task} with task_translate={task_translate} not found")
        return task_model_to_entity(model=task, translated_model=task_translate)

    async def lst(
        self, *, filter_obj: TaskFilter, order_obj: MockObj, pagination_obj: MockObj, lang: LanguageEnum
    ) -> list[Task]:
        where_clause = []
        if filter_obj.category_id is not None:
            where_clause.append(TaskModel.category_id == filter_obj.category_id)
        if filter_obj.active is not None:
            where_clause.append(TaskModel.active == filter_obj.active)
        stmt = (
            select(TaskModel, TaskTranslateModel)
            .join(
                TaskTranslateModel,
                and_(TaskModel.id == TaskTranslateModel.task_id, TaskTranslateModel.language == lang),
                isouter=True,
            )
            .where(*where_clause)
        )
        coro = await self.db_context.execute(stmt)
        result = coro.all()
        holder = {}
        for task, task_translate in result:
            holder[task.id] = {}
            holder[task.id]["task"] = task
            if task_translate is None:
                task_default_lang = select(TaskTranslateModel).where(
                    and_(TaskTranslateModel.task_id == task.id, TaskTranslateModel.language == DEFAULT_LANGUANGE)
                )
                result = await self.db_context.scalar(task_default_lang)
                if not result:
                    raise EntityNotFound(msg=f"{task=}, {task_translate=}")
                holder[task.id]["translate"] = result
            else:
                holder[task.id]["translate"] = task_translate

        return [
            task_model_to_entity(model=models["task"], translated_model=models["translate"])
            for models in holder.values()
        ]

    async def user_task_add(self, *, user_id: int, obj: TaskUserCreateDTO) -> TaskUser:
        stmt = insert(UserTaskModel).values(user_id=user_id, **asdict(obj)).returning(UserTaskModel)
        try:
            result = await self.db_context.scalar(stmt)
        except IntegrityError as error:
            error.orig = typing.cast(BaseException, error.orig)  # just for types
            if isinstance(error.orig.__cause__, ForeignKeyViolationError):
                raise EntityNotCreated(msg="Not found fk") from error
            raise EntityNotCreated(msg="") from error
        if result is None:
            raise EntityNotCreated(msg=f"UserTask object with task_id={obj.task_id}, user_id={user_id} not created")
        await self.db_context.refresh(result)
        return user_task_to_entity(model=result)

    async def user_task_get(self, *, id: int) -> TaskUser:
        stmt = select(UserTaskModel).where(UserTaskModel.id == id)
        result = await self.db_context.scalar(stmt)
        if result is None:
            raise EntityNotFound(msg=f"UserTask object with id={id} not found")
        return user_task_to_entity(model=result)

    async def user_task_lst(
        self,
        *,
        user_id: int,
        filter_obj: TaskUserFilter,
        order_obj: MockObj,
        pagination_obj: MockObj,
    ) -> list[TaskUser]:
        stmt = select(UserTaskModel)
        where_clause = []
        where_clause.append(UserTaskModel.user_id == user_id)
        if filter_obj.task_id is not None:
            where_clause.append(UserTaskModel.task_id == filter_obj.task_id)
        if filter_obj.status is not None:
            where_clause.append(UserTaskModel.status == filter_obj.status)
        if filter_obj.task_active is not None:
            stmt = stmt.join(TaskModel, UserTaskModel.task_id == TaskModel.id)
            where_clause.append(TaskModel.active == filter_obj.task_active)
        stmt = stmt.where(*where_clause)
        result = await self.db_context.scalars(stmt)
        return [user_task_to_entity(model=model) for model in result]

    async def user_task_update(self, *, id: int, obj: TaskUserUpdateDTO) -> TaskUser:
        stmt = (
            update(UserTaskModel)
            .values(as_dict_skip_none(obj))
            .where(
                UserTaskModel.id == id,
            )
            .returning(UserTaskModel)
        )
        result = await self.db_context.scalar(stmt)
        if result is None:
            raise EntityNotFound(msg=f"UserTask object={id} not found and was not updated")
        await self.db_context.refresh(result)
        return user_task_to_entity(model=result)

    async def plan_create(self, *, obj: TaskUserPlanCreateDTO) -> TaskUserPlan:
        stmt = insert(UserTaskPlanModel).values(**asdict(obj)).returning(UserTaskPlanModel)
        try:
            result = await self.db_context.scalar(stmt)
        except IntegrityError as error:
            error.orig = typing.cast(BaseException, error.orig)  # just for types
            if isinstance(error.orig.__cause__, ForeignKeyViolationError):
                raise EntityNotCreated(msg="Not found fk") from error
            raise EntityNotCreated(msg="") from error
        if result is None:
            raise EntityNotCreated(msg=f"UserTaskPlan with task_id={obj.task_id}, user_id={obj.user_id} not created")
        return plan_model_to_entity(model=result)

    async def plan_delete(self, *, user_id: int, task_id: int) -> TaskUserPlan:
        stmt = (
            delete(UserTaskPlanModel)
            .where(UserTaskPlanModel.user_id == user_id, UserTaskPlanModel.task_id == task_id)
            .returning(UserTaskPlanModel)
        )
        result = await self.db_context.scalar(stmt)
        if result is None:
            raise EntityNotFound(msg=f"UserTaskPlan with task_id={task_id}, user_id={user_id} not deleted")
        return plan_model_to_entity(model=result)

    async def plan_lst(
        self, *, user_id: int, filter_obj: TaskUserPlanFilter, order_obj: MockObj, pagination_obj: MockObj
    ) -> list[TaskUserPlan]:
        stmt = select(UserTaskPlanModel)
        where_clause = []
        where_clause.append(UserTaskPlanModel.user_id == user_id)
        if filter_obj.task_active is not None:
            stmt = stmt.join(TaskModel, UserTaskPlanModel.task_id == TaskModel.id)
            where_clause.append(TaskModel.active == filter_obj.task_active)
        stmt = stmt.where(*where_clause)
        result = await self.db_context.scalars(stmt)
        return [plan_model_to_entity(model=model) for model in result]
