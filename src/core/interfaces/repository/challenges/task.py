from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.core.dto.challenges.task import (
    TaskUserCreateDTO,
    TaskUserPlanCreateDTO,
    TaskUserUpdateDTO,
)
from src.core.dto.utils import IterableObj, Pagination, SortObj
from src.core.entity.task import Task, TaskUser, TaskUserPlan
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.language import LanguageEnum


@dataclass
class SortUserTaskObj(SortObj):
    field: str = "task_id"


@dataclass
class TaskFilter:
    active: bool | None = None
    category_id: int | None = None


@dataclass
class TaskUserFilter:
    task_id: int | None = None
    task_active: bool | None = None
    status: OccupancyStatusEnum | None = None


@dataclass
class TaskUserPlanFilter:
    task_active: bool | None = None
    category_id: int | None = None


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
        self, *, filter_obj: TaskFilter, sorting_obj: SortObj, iterable_obj: IterableObj, lang: LanguageEnum
    ) -> Pagination[list[Task]]:
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
    async def user_task_get(self, *, user_id: str, id: int) -> TaskUser:
        """Получить задание для пользователя

        Args:
            id (int): User task object identify

        Returns:
            TaskUser: Сущность задачи пользователя
        """

    @abstractmethod
    async def user_task_add(self, *, user_id: str, obj: TaskUserCreateDTO) -> TaskUser:
        """Создать задание для пользователя

        Args:
            user_id (str): ID of user
            obj (TaskUserCreateDTO): Объект создания

        Returns:
            TaskUser: Сущность задачи пользователя
        """

    @abstractmethod
    async def user_task_update(self, *, user_id: str, id: int, obj: TaskUserUpdateDTO) -> TaskUser:
        """Обновить задание для пользователя

        Args:
            id (int): User task object identify
            obj (TaskUserCreateDTO): Объект обновления

        Returns:
            TaskUser: Сущность задачи пользователя
        """

    @abstractmethod
    async def user_task_lst(
        self, *, user_id: str, filter_obj: TaskUserFilter, sorting_obj: SortUserTaskObj, iterable_obj: IterableObj
    ) -> Pagination[list[TaskUser]]:
        """Получить список заданий пользователя

        Args:
            user_id (str): ID of user
            filter_obj (TaskUserFilter): Объект фильтрации
            sorting_obj (SortUserTaskObj): Объект порядка
            iterable_obj (IterableObj): Объект пагинации

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
    async def plan_delete(self, *, user_id: str, task_id: int) -> TaskUserPlan:
        """Удалить план задач

        Args:
            user_id (str): ID of user
            task_id (int): ID of task

        Returns:
            TaskUserPlan: Task user entity object
        """

    @abstractmethod
    async def plan_lst(
        self, *, user_id: str, filter_obj: TaskUserPlanFilter, sorting_obj: SortUserTaskObj, iterable_obj: IterableObj
    ) -> Pagination[list[TaskUserPlan]]:
        """Получить список плана задач

        Args:
            user_id (str): ID of user
            filter_obj (TaskUserPlanFilter): Объект фильтрации
            sorting_obj (SortUserTaskObj): Объект порядка
            iterable_obj (IterableObj): Объект пагинации

        Returns:
            List[TaskUserPlan]: Список плана задач
        """
