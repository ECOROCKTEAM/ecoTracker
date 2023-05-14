from abc import abstractmethod, ABC
from dataclasses import dataclass

from src.core.dto.mock import MockObj
from src.core.enum.language import LanguageEnum
from src.core.entity.task import Task, TaskUser, TaskUserPlan
from src.core.dto.challenges.task import TaskUserCreateDTO, TaskUserPlanCreateDTO, TaskUserUpdateDTO


@dataclass
class TaskFilter:
    category_id: int | None = None


@dataclass
class TaskUserFilter:
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
            return_language (LanguageEnum): Необходимый язык

        Returns:
            Task: Task entity
        """

    @abstractmethod
    async def lst(
        self, *, sorting_obj: MockObj, pagination_obj: MockObj, filter_obj: TaskFilter, return_language: LanguageEnum
    ) -> list[Task]:
        """List of tasks

        Args:
            sorting_obj (str): sorting object
            paggination_obj (str): paggination object
            filter_obj (str): filter object
            return_language (LanguageEnum): Необходимый язык

        Returns:
            list[Task]: list of Task entities
        """

    @abstractmethod
    async def deactivate(self, *, id: int) -> int:
        """Отключить таск

        Args:
            id (int): ID базового задания

        Returns:
            int: ID базового задания
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
    async def user_task_create(self, *, obj: TaskUserCreateDTO) -> TaskUser:
        """Создать задание для пользователя

        Args:
            obj (TaskUserCreateDTO): Объект создания

        Returns:
            TaskUser: Сущность задачи пользователя
        """

    @abstractmethod
    async def user_task_update(self, *, obj: TaskUserUpdateDTO) -> TaskUser:
        """Обновить задание для пользователя

        Args:
            obj (TaskUserCreateDTO): Объект обновления

        Returns:
            TaskUser: Сущность задачи пользователя
        """

    @abstractmethod
    async def user_task_delete(self, *, user_id: int, task_id: int) -> int:
        """Delete user task

        Args:
            user_id (int): ID of user object
            task_id (int): ID of task object

        Returns:
            int: ID of deleted user task object
        """

    @abstractmethod
    async def user_task_lst(
        self,
        *,
        filter_obj: TaskUserFilter | None = None,
        order_obj: MockObj | None = None,
        pagination_obj: MockObj | None = None,
    ) -> list[TaskUser]:
        """Получить список заданий пользователя

        Args:
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
        filter_obj: TaskUserFilter | None = None,
        order_obj: MockObj | None = None,
        pagination_obj: MockObj | None = None,
    ) -> list[TaskUserPlan]:
        """Получить список плана задач

        Args:
            filter_obj (MockObj): Объект фильтрации
            order_obj (MockObj): Объект порядка
            pagination_obj (MockObj): Объект пагинации

        Returns:
            List[TaskUserPlan]: Список плана задач
        """
