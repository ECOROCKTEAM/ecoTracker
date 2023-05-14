from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.const.translate import DEFAULT_LANGUANGE
from src.core.dto.challenges.task import TaskUserCreateDTO, TaskUserPlanCreateDTO, TaskUserUpdateDTO
from src.core.dto.mock import MockObj
from src.core.enum.language import LanguageEnum
from src.core.exception.base import EntityNotFound
from src.core.interfaces.repository.challenges.task import IRepositoryTask, TaskFilter, TaskUserFilter
from src.core.entity.task import Task, TaskUser, TaskUserPlan
from src.data.models.challenges.task import TaskModel, TaskTranslateModel


def task_model_to_entity(model: TaskModel, translated_model: TaskTranslateModel) -> Task:
    return Task(
        id=model.id,
        score=model.score,
        category_id=model.category_id,
        name=translated_model.name,
        description=translated_model.description,
        language=translated_model.language,
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
        self, *, sorting_obj: MockObj, pagination_obj: MockObj, filter_obj: TaskFilter, return_language: LanguageEnum
    ) -> list[Task]:
        where_clause = []
        if filter_obj.category_id:
            where_clause.append(TaskModel.category_id == filter_obj.category_id)
        stmt = (
            select(TaskModel, TaskTranslateModel)
            .join(
                TaskTranslateModel,
                and_(TaskModel.id == TaskTranslateModel.task_id, TaskTranslateModel.language == return_language),
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

        # entity_list: list[Task] = []
        # for models in holder.values():
        #     task = models["task"]
        #     task_translate = models["translate"]
        #     entity_list.append(task_model_to_entity(model=task, translated_model=task_translate))

        return [
            task_model_to_entity(model=models["task"], translated_model=models["translate"])
            for models in holder.values()
        ]

    async def deactivate(self, *, id: int) -> int:
        return await super().deactivate(id=id)

    async def user_task_create(self, *, obj: TaskUserCreateDTO, return_language: LanguageEnum) -> TaskUser:
        return await super().user_task_create(obj=obj, return_language=return_language)

    async def user_task_delete(self, *, id: int, return_language: LanguageEnum) -> int:
        return await super().user_task_delete(id=id, return_language=return_language)

    async def user_task_get(self, *, id: int, return_language: LanguageEnum) -> TaskUser:
        return await super().user_task_get(id=id, return_language=return_language)

    async def user_task_lst(
        self,
        *,
        filter_obj: TaskUserFilter | None = None,
        order_obj: MockObj | None = None,
        pagination_obj: MockObj | None = None,
        return_language: LanguageEnum,
    ) -> list[TaskUser]:
        return await super().user_task_lst(
            filter_obj=filter_obj, order_obj=order_obj, pagination_obj=pagination_obj, return_language=return_language
        )

    async def user_task_update(self, *, obj: TaskUserUpdateDTO, return_language: LanguageEnum) -> TaskUser:
        return await super().user_task_update(obj=obj, return_language=return_language)

    async def plan_create(self, *, obj: TaskUserPlanCreateDTO) -> TaskUserPlan:
        return await super().plan_create(obj=obj)

    async def plan_delete(self, *, id: int) -> int:
        return await super().plan_delete(id=id)

    async def plan_lst(
        self,
        *,
        filter_obj: TaskUserFilter | None = None,
        order_obj: MockObj | None = None,
        pagination_obj: MockObj | None = None,
    ) -> list[TaskUserPlan]:
        return await super().plan_lst(filter_obj=filter_obj, order_obj=order_obj, pagination_obj=pagination_obj)
