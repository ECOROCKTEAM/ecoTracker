from abc import ABC, abstractmethod

from src.core.dto.m2m.user.filters import UserTaskFilter
from src.core.dto.m2m.user.task import UserTaskCreateDTO, UserTaskUpdateDTO
from src.core.entity.task import TaskUser


class IUserTaskRepository(ABC):
    @abstractmethod
    async def update(self, *, obj: UserTaskUpdateDTO) -> TaskUser:
        """User task update.

        Args:
            obj (UserTaskUpdateDTO): DTO for update user task object.

        Returns:
            TaskUser: DTO of user task object
        """

    @abstractmethod
    async def delete(self, *, id: int) -> int:
        """Deleting task from user task list

        Args:
            task_id (int): int of user task object

        Returns:
            int: id of deleted task from user task list
        """

    @abstractmethod
    async def get(self, *, id: int) -> TaskUser:
        """get task which belongs to user

        Args:
            id (int): int of user task object

        Returns:
            TaskUser: DTO of user task object
        """

    @abstractmethod
    async def list(self, *, user_id: int, filter_obj: UserTaskFilter | None = None) -> list[TaskUser]:
        """List of user tasks

        Args:
            user_id (int): user identify

        Returns:
            list[TaskUser]: List of DTO user task objects
        """

    @abstractmethod
    async def create(self, *, obj: UserTaskCreateDTO) -> TaskUser:
        """Adding task to user task list

        Args:
            obj (UserTaskCreateDTO): DTO for creating relation between user and task

        Returns:
            TaskUser: DTO of user task object
        """
