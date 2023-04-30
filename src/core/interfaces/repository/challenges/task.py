from abc import abstractmethod, ABC

from src.core.entity.task import Task, TaskCreateDTO
from src.core.dto.mock import MockObj
from src.core.entity.task import TaskUpdateDTO


class ITaskRepository(ABC):
    @abstractmethod
    async def list(self, *, sorting_obj: MockObj, paggination_obj: MockObj, filter_obj: MockObj) -> list[Task]:
        """List of tasks

        Args:
            sorting_obj (str): sorting object
            paggination_obj (str): paggination object
            filter_obj (str): filter object

        Returns:
            list[Task]: list of Task entities
        """

    @abstractmethod
    async def get(self, *, id: int) -> Task:
        """Get task

        Args:
            id (int): task identify

        Returns:
            Task: Task entity
        """
        pass

    @abstractmethod
    async def update(self, *, obj: TaskUpdateDTO) -> Task:
        """Task update

        Args:
            obj (TaskUpdateDTO): DTO for update task method

        Returns:
            Task: Task entity
        """

    @abstractmethod
    async def delete(self, *, id: int) -> int:
        """delete task

        Args:
            id (int): task identify

        Returns:
            int: id of deleted task
        """

    @abstractmethod
    async def create(self, *, obj: TaskCreateDTO) -> Task:
        """Create task

        Args:
            obj (TaskCreateDTO): DTO for creating task

        Returns:
            Task: Task entity
        """
        pass
