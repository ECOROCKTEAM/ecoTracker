from abc import ABC, abstractmethod
from typing import List, Union

from src.core.dto.subscription import (
    SubscriptionCreateDTO,
    SubscriptionDTO,
    SubscriptionPeriodCreateDTO,
    SubscriptionPeriodDTO,
    SubscriptionPeriodUnitCreateDTO,
    SubscriptionPeriodUnitDTO,
    SubscriptionTypeCreateDTO,
    SubscriptionTypeDTO,
)

from src.core.entity.task import Task
from src.core.entity.user import UserSubscription, User, UserTask
from src.core.entity.subscription import Constraint
from src.core.entity.contact import UserContact

from src.core.dto.user.role import UserRoleCreateDTO, UserRoleDTO, UserUserRoleDTO, UserUserRoleUpdateDTO
from src.core.dto.plugs import ObjectPlug
from src.core.dto.occupancy import (
    OccupancyTypeCreateDTO,
    OccupancyTypeDTO,
    OccupancyStatusCreateDTO,
    OccupancyStatusDTO,
)
from src.core.dto.score import ScoreUserDTO
from src.core.entity.task import TaskCreateDTO, TaskDTO, TaskGetDTO, TaskUpdateDTO
from src.core.dto.misc import SubscriptionTypeConstraintCreateDTO
from src.core.dto.user.contact import (
    ContactDTO,
    ContactDeleteDTO,
    ContactTypeCreateDTO,
    ContactTypeDTO,
    ContactCreateDTO,
    ContactUserUpdateDTO,
)
from src.core.dto.user import UserCreateDTO


class IRepositoryCore(ABC):
    @abstractmethod
    async def user_task_done(self, *, obj: UserTask) -> bool:
        """User task complite

        Args:
            obj (UserTask): UserTask complited object

        Returns:
            bool: boolean
        """
        pass

    @abstractmethod
    async def user_role_application_update(self, *, obj: UserUserRoleUpdateDTO) -> UserUserRoleDTO:
        """User application role update

        Args:
            obj (UserUserRoleUpdateDTO): DTO which contains user identify for update him and updating role

        Returns:
            UserUserRoleDTO: DTO of user identify and application role
        """
        pass

    @abstractmethod
    async def user_role_application_create(self, *, obj: UserRoleCreateDTO) -> UserRoleDTO:
        """Creating application role

        Args:
            obj (str): DTO representation of new application role object

        Returns:
            UserRoleApplication: DTO of new application role
        """
        pass

    @abstractmethod
    async def user_task_delete(self, *, user_id: str, task_id: int) -> int:
        """Deleting task to user task list

        Args:
            user_id (str): user identify
            task_id (int): task identify

        Returns:
            int: deleted task id from user task list
        """
        pass

    @abstractmethod
    async def user_task_get(self, *, user_id: str, task_id: id) -> UserTask:
        """get task which belong to user

        Args:
            user_id (str): user identify
            task_id (int): task identify

        Returns:
            Task: UserTask entity
        """
        pass

    @abstractmethod
    async def user_task_add(self, *, user_id: str, task_id: int) -> UserTask:
        """Adding task to user task list

        Args:
            user_id (str): user identify
            task_id (int): task identify

        Returns:
            UserTask: User entity and Task entity relation
        """
        pass

    @abstractmethod
    async def task_list(
        self, *, sorting_obj: ObjectPlug, paggination_obj: ObjectPlug, filter_obj: ObjectPlug
    ) -> List[TaskDTO]:
        """List of tasks

        Args:
            sorting_obj (str): sorting object
            paggination_obj (str): paggination object
            filter_obj (str): filter object

        Returns:
            List[TaskDTO]: List of DTO task object
        """
        pass

    @abstractmethod
    async def occupancy_status_create(self, *, obj: OccupancyStatusCreateDTO) -> OccupancyStatusDTO:
        """Create occupancy status

        Args:
            obj (OccupancyStatusCreateDTO): DTO for creating occupancy status

        Returns:
            OccupancyStatusDTO: DTO of occupancy status
        """
        pass

    @abstractmethod
    async def occupancy_type_create(self, *, obj: OccupancyTypeCreateDTO) -> OccupancyTypeDTO:
        """Create occupancy type

        Args:
            obj (OccupancyTypeCreateDTO): DTO of creating occupancy type

        Returns:
            OccupancyTypeDTO: DTO occupancy type
        """
        pass

    @abstractmethod
    async def task_get(self, *, obj: TaskGetDTO) -> Task:
        """Get task

        Args:
            obj (TaskGetDTO): DTO for task get method

        Returns:
            Task: Task entity
        """
        pass

    @abstractmethod
    async def task_update(self, *, obj: TaskUpdateDTO) -> Task:
        """Task update

        Args:
            obj (TaskUpdateDTO): DTO for update task method

        Returns:
            Task: Updated task entity
        """
        pass

    @abstractmethod
    async def task_delete(self, *, obj: Task) -> int:
        """delete task

        Args:
            obj (Task): Task entity

        Returns:
            int: id of deleted task
        """
        pass

    @abstractmethod
    async def task_create(self, *, obj: TaskCreateDTO) -> TaskDTO:
        """create task

        Args:
            obj (TaskCreateDTO): DTO for creating task

        Returns:
            TaskDTO: task DTO
        """
        pass

    @abstractmethod  # Проверить логику вывода
    async def score_user_list(
        self, *, username: str = None, sorting_obj: str = None
    ) -> Union[List[ScoreUserDTO], List[List[ScoreUserDTO], int]]:
        """Get user score list.

        Args:
            username (str, optional): if username -> we'll get rating user in this list. Defaults to None.
            sorting_obj (str, optional): object for list sorting. Defaults to None.

        Returns:
            List[ScoreUserDTO]: If username: return user rating and list of DTO user score
                                else: return list of DTO user score
        """
        pass

    @abstractmethod
    async def score_user_get(self, *, username: str) -> ScoreUserDTO:
        """Get score for user

        Args:
            username (str): user identify

        Returns:
            ScoreUserDTO: DTO for user score
        """

    @abstractmethod
    async def contact_type_create(self, *, obj: ContactTypeCreateDTO) -> ContactTypeDTO:
        """Creating contact type. This can only be done by application administrator

        Args:
            create_obj (ContactTypeCreateDTO): DTO contact type for creating

        Returns:
            ContactTypeDTO: New contact type
        """
        pass

    @abstractmethod
    async def contact_create(self, *, user_id: str, obj: ContactCreateDTO) -> UserContact:
        """contact creating by user for himself

        Args:
            user_id (str): user identify
            create_obj (ContactCreateDTO): DTO for new user contact

        Returns:
            UserContact: Relation between user and his new contact
        """
        pass

    @abstractmethod
    async def contact_update(self, *, obj: ContactUserUpdateDTO) -> UserContact:
        """updating user contact

        Args:
            obj (ContactUserUpdateDTO): DTO with user_id, updating contact identify and new data for update

        Returns:
            UserContact: UserContact entity
        """
        pass

    @abstractmethod
    async def contact_delete(self, *, user_id: str, obj: ContactDeleteDTO) -> int:
        """delete contact from user contact list

        Args:
            user_id (str): user identify
            obj (ContactDeleteDTO): DTO for deleting user contact

        Returns:
            int: id of deleted contact
        """


    @abstractmethod
    async def contact_list(
        self, *, user_id: str, filter_obj: ObjectPlug, sorting_obj: ObjectPlug, order_obj: ObjectPlug
    ) -> list[ContactDTO]:
        """contact list

        Args:
            user_id (str): user identify
            filter_obj (ObjectPlug): Some filter item
            sorting_obj (ObjectPlug): Some sorting obj
            order_obj (ObjectPlug): Some order obj

        Returns:
            list[ContactDTO]: list of DTO contact
        """
        pass

    @abstractmethod
    async def contact_get(self, *, user_id: str, contact_id: str) -> UserContact:
        """get one contact

        Args:
            user_id (str): user identify
            contact_id (str): contact identify

        Returns:
            UserContact: UserContact entity
        """
        pass

    @abstractmethod
    async def subscription_type_constraint_create(self, *, obj: SubscriptionTypeConstraintCreateDTO) -> Constraint:
        """Create constraint for Subscription

        Args:
            obj (SubscriptionTypeConstraintCreate): DTO for create  new constrains

        Returns:
            Constraint: Constraint entity
        """

    @abstractmethod
    async def subscription_type_constraint_delete(self, *, constraint_id: int) -> int:
        """Delete constraint for Subscription

        Args:
            constraint_name (str): Name of delete constraint

        Returns:
            int: id of deleted constraint
        """
        pass

    @abstractmethod
    async def subscription_period_unit_create(
        self, *, obj: SubscriptionPeriodUnitCreateDTO
    ) -> SubscriptionPeriodUnitDTO:
        """creating subscription period

        Args:
            obj (SubscriptionPeriodCreateDTO): DTO for creating subscription period

        Returns:
            SubscriptionPeriodDTO: New subscription period
        """

    @abstractmethod
    async def subscription_period_create(self, *, obj: SubscriptionPeriodCreateDTO) -> SubscriptionPeriodDTO:
        """Creating new period for subscriptios

        Args:
            obj (SubscriptionPeriodCreateDTO): DTO object for create period for subscriptions

        Returns:
            SubscriptionPeriodDTO: New period
        """
        pass

    @abstractmethod
    async def subscription_create(self, *, obj: SubscriptionCreateDTO) -> SubscriptionDTO:
        """create new subscription

        Args:
            obj (SubscriptionCreateDTO): DTO for creating subscription

        Returns:
            SubscriptionDTO: New subscription
        """
        pass

    @abstractmethod
    async def subscription_type_translate_create(self, *, obj: SubscriptionTypeCreateDTO) -> SubscriptionTypeDTO:
        """We'll create subscription_type if for it will be all translate.

        Args:
            obj (SubscriptionTypeCreateDTO): DTO for creating a new subscription type

        Returns:
            SubscriptionTypeDTO: subscription type
        """
        pass

    @abstractmethod
    async def user_subscription_update(self, *, user_id: str, subscription_id: int) -> UserSubscription:
        """Adds a subscription to user.

        Args:
            user_id (str): User identify
            subscription_id (int): Subscription identify

        Returns:
            UserSubscription: Relation between user and subscription.
        """
        pass
