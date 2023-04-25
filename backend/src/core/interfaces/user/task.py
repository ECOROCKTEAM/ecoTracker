from abc import ABC, abstractmethod

from src.core.dto.m2m.user.task import UserTaskCreateDTO, UserTaskDTO, UserTaskUpdateDTO
from src.core.dto.mock import MockObj


class IUserTaskRepository(ABC):
    
    @abstractmethod 
    async def update(self, *, obj: UserTaskUpdateDTO) -> UserTaskDTO: 
        """User task update. 

        Args:
            obj (UserTaskUpdateDTO): DTO for update user task object.

        Returns:
            UserTaskDTO: DTO of user task object
        """

    @abstractmethod
    async def delete(self, *, id: int) -> int:
        """ Deleting task from user task list

        Args:
            task_id (int): int of user task object
        
        Returns:
            int: id of deleted task from user task list
        """

    @abstractmethod
    async def get(self, *, id: int) -> UserTaskDTO:
        """get task which belongs to user

        Args:
            id (int): int of user task object

        Returns:
            UserTaskDTO: DTO of user task object 
        """

    @abstractmethod 
    async def list(
        self, *, 
        user_id: str,
        filter_obj: MockObj = None,
        sorting_obj: MockObj = None,
        order_obj: MockObj = None
                             ) -> list[UserTaskDTO]:
        """List of user tasks

        Args:
            user_id (str): user identify
            filter_obj (MockObj, optional): filter object. Defaults to None.
            sorting_obj (MockObj, optional): sort object. Defaults to None.
            order_obj (MockObj, optional): order object. Defaults to None.

        Returns:
            list[UserTaskDTO]: List of DTO user task objects
        """

    @abstractmethod 
    async def create(self, *, obj: UserTaskCreateDTO) -> UserTaskDTO:
        """ Adding task to user task list

        Args:
            obj (UserTaskCreateDTO): DTO for creating relation between user and task

        Returns:
            UserTaskDTO: DTO of user task object
        """
