from abc import ABC, abstractmethod

from src.core.dto.m2m.user.subscription import UserSubscriptionDTO, UserSubscriptionUpdateDTO
from src.core.dto.m2m.user.task import UserTaskCreateDTO, UserTaskDTO, UserTaskDeleteDTO, UserTaskGetDTO, UserTaskUpdateDTO
from src.core.entity.user import User, UserCreateDTO, UserUpdateDTO
from src.core.dto.mock import MockObj


class IUserRepository(ABC):

    @abstractmethod
    async def create(self, *, obj: UserCreateDTO) -> User:
        """Create user \ Registration

        Args:
            obj (UserCreateDTO): DTO for creating user object

        Returns:
            User: User entity

        Raises:
            RepoError: Repository error
            UserDidNotCreated: User didn't created

        """

    @abstractmethod 
    async def update(self, *, obj: UserUpdateDTO) -> User:
        """User update

        Args:
            obj (UserUpdateDTO): DTO for update user

        Returns:
            User: User entity
        """

    @abstractmethod 
    async def user_task_update(self, *, obj: UserTaskUpdateDTO) -> UserTaskDTO: 
        """User task update. 

        Args:
            obj (UserTaskUpdateDTO): DTO for update user task object.

        Returns:
            UserTaskDTO: DTO of user task object
        """

    @abstractmethod
    async def user_task_delete(self, *, id: int) -> int:
        """ Deleting task from user task list

        Args:
            task_id (int): int of user task object
        
        Returns:
            int: id of deleted task from user task list
        """

    @abstractmethod
    async def user_task_get(self, *, id: int) -> UserTaskDTO:
        """get task which belongs to user

        Args:
            id (int): int of user task object

        Returns:
            UserTaskDTO: DTO of user task object 
        """

    @abstractmethod 
    async def user_task_list(
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
    async def user_task_create(self, *, obj: UserTaskCreateDTO) -> UserTaskDTO:
        """ Adding task to user task list

        Args:
            obj (UserTaskCreateDTO): DTO for creating relation between user and task

        Returns:
            UserTaskDTO: DTO of user task object
        """


    @abstractmethod
    async def user_subscription_update(self, *, user_id: str, obj: UserSubscriptionUpdateDTO) -> UserSubscriptionDTO:
        """Update user subscription

        Args:
            user_id (str): user identify
            obj (UserSubscriptionUpdateDTO): DTO for update user subsctiprion

        Returns:
            UserSubscriptionDTO: DTO of user subscription object
        """

