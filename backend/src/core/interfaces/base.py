from typing import List

from abc import ABC, abstractmethod

# Tasks imports
from src.core.dto.tasks import CreateTaskDTO, UpdateTaskDTO
from src.core.entity.task import Task

# Mission imports
from src.core.dto.mission import CreateMissionDTO
from src.core.entity.mission import MissionBase

# Community imports
from src.core.dto.community import CreateCommunityDTO
from src.core.entity.community import Community

# User imports
from src.core.dto.user import CreateUserDTO
from src.core.entity.user import User


class BaseAbstractRepo(ABC):

    # Tasks chapter
    @abstractmethod
    def task_create(self, *, new_task: CreateTaskDTO) -> Task: 
        pass

    @abstractmethod
    def task_get(self, *, name: str) -> Task:
        pass

    @abstractmethod
    def tasks_list(self, *,
                   sorting_obj: str = None, 
                   paggination_obj: str = None, 
                   filter_obj: str = None,
                ) -> List[Task]: 
        pass

    @abstractmethod
    def task_update(self, *, some_update_obj: str) -> Task: #finish
        pass

    @abstractmethod
    def task_update(self, *, updated_task: UpdateTaskDTO) -> Task: #find how to update fields
        pass

    @abstractmethod
    def task_delete(self, *, name: str) -> bool:  
        pass

    # Mission chapter

    @abstractmethod
    def mission_create(self, *, new_mission: CreateMissionDTO, username: str) -> MissionBase: 
        pass

    @abstractmethod
    def mission_get(self, *, mission_name: str) -> MissionBase:  
        pass

    @abstractmethod
    def missions_list(self, *,
                   sorting_obj: str = None, 
                   paggination_obj: str = None, 
                   filter_obj: str = None,
                ) -> List[MissionBase]: # add sorting
        pass

    @abstractmethod
    def mission_update(self, *, find_some_info: str) -> MissionBase: # finish: fix mission usecase
        pass

    # Community chapter
    @abstractmethod
    def community_create(self, *, new_community: CreateCommunityDTO) -> Community: 
        pass

    @abstractmethod
    def community_update(self, *, find_some_info: str) -> Community: # Finish
        pass

    @abstractmethod
    def community_get(self, *, community_name: str) -> Community:  
        pass

    @abstractmethod
    def communities_list(self, *,
                   sorting_obj: str = None, 
                   paggination_obj: str = None, 
                   filter_obj: str = None,
                ) -> List[Community]: 
        pass

    # User chapter

    @abstractmethod
    def user_create(self, *, new_user: CreateUserDTO) -> User: # add some update fields in arguments
        pass

    @abstractmethod
    def user_delete(self, *, username: str) -> bool: 
        pass

    @abstractmethod
    def user_get(self, *, username: str) -> User: 
        pass

    @abstractmethod
    def users_list(self, *,
                   sorting_obj: str = None, 
                   paggination_obj: str = None, 
                   filter_obj: str = None,
                ) -> List[User]: #finish: implement sorting
        pass

