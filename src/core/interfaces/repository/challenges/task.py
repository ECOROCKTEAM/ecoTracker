from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.core.dto.challenges.task import (
    TaskUserCreateDTO,
    TaskUserPlanCreateDTO,
    TaskUserUpdateDTO,
)
from src.core.dto.mock import MockObj
from src.core.entity.task import Task, TaskUser, TaskUserPlan
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.language import LanguageEnum


@dataclass
class TaskFilter:
    active: bool | None = None
    category_id: int | None = None


@dataclass
class TaskUserFilter:
    task_id: int | None = None
    status: OccupancyStatusEnum | None = None
    """"""


@dataclass
class TaskUserPlanFilter:
    """"""


class IRepositoryTask(ABC):
    @abstractmethod
    async def get(self, *, id: int, lang: LanguageEnum) -> Task:
        """Get task

        Args:
            id (int): task identify
            lang (LanguageEnum): Необходимый язык

        Returns:
            Task: Task entity
        """

    @abstractmethod
    async def lst(
        self, *, filter_obj: TaskFilter, sorting_obj: MockObj, pagination_obj: MockObj, lang: LanguageEnum
    ) -> list[Task]:
        """List of tasks

        Args:
            sorting_obj (str): sorting object
            paggination_obj (str): paggination object
            filter_obj (str): filter object
            lang (LanguageEnum): Необходимый язык

        Returns:
            list[Task]: list of Task entities
        """

    @abstractmethod
    async def user_task_get(self, *, user_id: int, task_id: int) -> TaskUser:
        """Получить задание для пользователя

        Args:
            user_id (int): ID of user object
            task_id (int): ID of task object

        Returns:
            TaskUser: Сущность задачи пользователя
        """

    @abstractmethod
    async def user_task_create(self, *, user_id: int, obj: TaskUserCreateDTO) -> TaskUser:
        """Создать задание для пользователя

        Args:
            user_id (int): ID of user
            obj (TaskUserCreateDTO): Объект создания

        Returns:
            TaskUser: Сущность задачи пользователя
        """

    @abstractmethod
    async def user_task_update(self, *, user_id: int, task_id: int, obj: TaskUserUpdateDTO) -> TaskUser:
        """Обновить задание для пользователя

        Args:
            user_id (int): ID of user
            task_id (int): ID of task
            obj (TaskUserCreateDTO): Объект обновления

        Returns:
            TaskUser: Сущность задачи пользователя
        """

    @abstractmethod
    async def user_task_lst(
        self,
        *,
        user_id: int,
        filter_obj: TaskUserFilter | None = None,
        order_obj: MockObj | None = None,
        pagination_obj: MockObj | None = None,
    ) -> list[TaskUser]:
        """Получить список заданий пользователя

        Args:
            user_id (int): ID of user
            filter_obj (TaskUserFilter): Объект фильтрации
            order_obj (MockObj): Объект порядка
            pagination_obj (MockObj): Объект пагинации

        Returns:
            List[TaskUser]: Список сущностей заданий пользователя
        """

    @abstractmethod
    async def plan_create(self, *, obj: TaskUserPlanCreateDTO) -> TaskUserPlan:
        """Создать план задач

        Args:
            obj (TaskUserPlanCreateDTO): Объект создания

        Returns:
            TaskUserPlan: Сущность плана задач
        """

    @abstractmethod
    async def plan_delete(self, *, id: int) -> int:
        """Удалить план задач

        Args:
            id (int): ID плана

        Returns:
            int: ID плана
        """

    @abstractmethod
    async def plan_lst(
        self,
        *,
        user_id: int,
        # filter_obj: TaskUserFilter | None = None,
        order_obj: MockObj | None = None,
        pagination_obj: MockObj | None = None,
    ) -> list[TaskUserPlan]:
        """Получить список плана задач

        Args:
            user_id (int): ID of user
            filter_obj (MockObj): Объект фильтрации
            order_obj (MockObj): Объект порядка
            pagination_obj (MockObj): Объект пагинации

        Returns:
            List[TaskUserPlan]: Список плана задач
        """
