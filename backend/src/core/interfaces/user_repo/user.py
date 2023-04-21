from abc import ABC, abstractmethod

from src.core.entity.user import User, UserCreateDTO, UserUpdateDTO
from src.core.dto.mock import MockObj


class IUserRepository(ABC):

    @abstractmethod
    async def user_create(self, *, obj: UserCreateDTO) -> User:
        """Create user \ Registration

        Args:
            user (CreateUserDTO): DTO for creating user

        Returns:
            User: User entity

        Raises:
            RepoError: Repository error
            UserDidNotCreated: User didn't created

        """

    @abstractmethod # Возможно тут можно через этот метод сделать и деактивацию юзера, если в через usecase передавать id и статус юзера для деактивации
    async def user_update(self, *, obj: UserUpdateDTO) -> User:
        """User update

        Args:
            obj (UserUpdateDTO): DTO for update user

        Returns:
            User: Updated user entity
        """

    @abstractmethod
    async def user_task_update(self, *, user_task: UserTaskDTO, obj: UserTaskUpdateDTO) -> UserTaskDTO: 
        """User task complite

        Args:
            user_task (UserTaskDTO): DTO user task object which will be update
            obj (UserTaskUpdateDTO): DTO for update user task object. Хз почему я при update методах писал на выходах bool.

        Returns:
            UserTaskDTO: DTO of user task object
        """

    @abstractmethod
    async def user_task_delete(self, *, obj: UserTaskDeleteDTO) -> int:
        """ Deleting task to user task list

        Args:
            obj (UserTaskDeleteDTO): DTO for delete user task object
        
        Returns:
            int: id of deleted task from user task list
        """

    @abstractmethod
    async def user_task_get(self, *, UserTaskGetDTO) -> UserTaskDTO:
        """get task which belongs to user

        Args:
            obj (UserTaskGetDTO): DTO to get relation object between user and task

        Returns:
            UserTaskDTO: DTO of user task object 
        """

    @abstractmethod # по идее нам не нужен тут ещё и task_id, тк тут у нас лист. Фильтровать эти записи по статусу будем уже в запросе? (status_id)
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

    @abstractmethod # было user_task_add. Посчитал, что мы хоть и добавляем таксу в список тасков пользователя, но именно создаём связь, поэтому create
    async def user_task_create(self, *, obj: UserTaskCreateDTO) -> UserTaskDTO:
        """ Adding task to user task list

        Args:
            obj (UserTaskCreateDTO): DTO for creating relation between user and task

        Returns:
            UserTaskDTO: DTO of user task object
        """

    @abstractmethod # думаю, что в следующих методах будет достаточно идента юзера
    async def user_role_application_update(self, *, user_id: str, obj: UserApplicationRoleUpdateDTO) -> UserApplicationRoleDTO:
        """User application role update

        Args:
            user_id (str): user identify
            obj (UserApplicationRoleUpdateDTO): DTO for update user application role

        Returns:
            UserApplicationRoleDTO: DTO of user application role object
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

