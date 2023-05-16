from dataclasses import asdict
from sqlalchemy import and_, select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.const.translate import DEFAULT_LANGUANGE
from src.core.dto.challenges.task import TaskUserCreateDTO, TaskUserPlanCreateDTO, TaskUserUpdateDTO
from src.core.dto.mock import MockObj
from src.core.enum.language import LanguageEnum
from src.core.exception.base import EntityNotCreated, EntityNotFound
from src.core.exception.task import TaskAlreadyDeactivatedError
from src.core.interfaces.repository.challenges.task import IRepositoryTask, TaskFilter, TaskUserFilter
from src.core.entity.task import Task, TaskUser, TaskUserPlan
from src.data.models.challenges.task import TaskModel, TaskTranslateModel, UserTaskModel


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
            raise EntityNotFound()
        task, task_translate = result
        if task_translate is None:
            task_default_lang = select(TaskTranslateModel).where(
                and_(TaskTranslateModel.task_id == id, TaskTranslateModel.language == DEFAULT_LANGUANGE)
            )
            task_translate = await self.db_context.scalar(task_default_lang)
            if task_translate is None:
                raise EntityNotFound()
        return task_model_to_entity(model=task, translated_model=task_translate)

    async def lst(
        self, *, sorting_obj: MockObj, pagination_obj: MockObj, filter_obj: TaskFilter, lang: LanguageEnum
    ) -> list[Task]:
        where_clause = []
        if filter_obj.category_id:
            where_clause.append(TaskModel.category_id == filter_obj.category_id)
        if filter_obj.active:
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
                    raise EntityNotFound()
                holder[task.id]["translate"] = result
            else:
                holder[task.id]["translate"] = task_translate

        return [
            task_model_to_entity(model=models["task"], translated_model=models["translate"])
            for models in holder.values()
        ]

    async def deactivate(self, *, obj_id: int) -> int:
        task = select(TaskModel).where(TaskModel.id == obj_id)
        task = await self.db_context.scalar(task)
        if not task:
            raise EntityNotFound()
        if not task.active:
            raise TaskAlreadyDeactivatedError(task_id=task.id)
        # Нужны ли тут эти проверки? Или сразу обновлять таску и всё?
        stmt = update(TaskModel).where(TaskModel.id == obj_id).values(active=False).returning(TaskModel.id)
        result = await self.db_context.scalar(stmt)
        if not result:
            raise EntityNotFound()
        return result

    # доделать с юзером
    async def user_task_create(self, *, user_id: int, obj: TaskUserCreateDTO) -> TaskUser:
        stmt = insert(UserTaskModel).values(user_id=user_id, **asdict(obj)).returning(UserTaskModel)
        result = await self.db_context.scalar(stmt)
        if result is None:
            raise EntityNotCreated()
        return user_task_to_entity(model=result)

    async def user_task_get(self, *, user_id: int, task_id: int) -> TaskUser:
        return await super().user_task_get(user_id=user_id, task_id=task_id)

    async def user_task_lst(
        self,
        *,
        user_id: int,
        filter_obj: TaskUserFilter | None = None,
        order_obj: MockObj | None = None,
        pagination_obj: MockObj | None = None,
    ) -> list[TaskUser]:
        return await super().user_task_lst(
            user_id=user_id,
            filter_obj=filter_obj,
            order_obj=order_obj,
            pagination_obj=pagination_obj,
        )

    async def user_task_update(self, *, user_id: int, task_id: int, obj: TaskUserUpdateDTO) -> TaskUser:
        return await super().user_task_update(user_id=user_id, task_id=task_id, obj=obj)

    async def plan_create(self, *, obj: TaskUserPlanCreateDTO) -> TaskUserPlan:
        return await super().plan_create(obj=obj)

    async def plan_delete(self, *, id: int) -> int:
        return await super().plan_delete(id=id)

    async def plan_lst(
        self, *, user_id: int, order_obj: MockObj | None = None, pagination_obj: MockObj | None = None
    ) -> list[TaskUserPlan]:
        return await super().plan_lst(user_id=user_id, order_obj=order_obj, pagination_obj=pagination_obj)
