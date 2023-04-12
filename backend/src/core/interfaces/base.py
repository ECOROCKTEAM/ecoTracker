from typing import List

from abc import ABC, abstractmethod

# Tasks imports
from src.core.dto.tasks import CreateTaskDTO, UpdateTaskDTO
from src.core.entity.task import Task

# Mission imports
from src.core.dto.mission import CreateMissionBaseDTO, CreateMissionCommunityDTO, UpdateMissionCommunityDTO
from src.core.entity.mission import MissionBase, MissionCommunity

# Community imports
from src.core.dto.community import CreateCommunityDTO
from src.core.entity.community import Community

# User imports
from src.core.dto.user import CreateUserDTO
from src.core.entity.user import User

#score imports
from src.core.dto.score import ScoreUserGetDTO

# contact imports
from src.core.entity.contact import ContactType


class BaseAbstractRepo(ABC):

    # ContactUser chapter

    @abstractmethod
    def contact_type_create(self, *, name: str) -> ContactType:
        pass

    # ScoreUser chapter

    @abstractmethod
    def score_user_get(self, *, username: str) -> ScoreUserGetDTO:
        pass


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
    def task_update(self, *, updated_task: UpdateTaskDTO) -> Task: #find how to update fields
        pass

    @abstractmethod
    def task_delete(self, *, name: str) -> bool:  
        pass

    # Base Mission chapter

    @abstractmethod
    def mission_base_create(self, *, new_mission: CreateMissionBaseDTO) -> MissionBase: 
        pass

    @abstractmethod
    def mission_base_get(self, *, mission_name: str) -> MissionBase: 
        pass

    @abstractmethod
    def missions_base_list(self, *,
                           sorting_obj: str = None, 
                           paggination_obj: str = None, 
                           filter_obj: str = None,
                ) -> List[MissionBase]: # +
        pass

    @abstractmethod
    def mission_base_update(self, *, find_some_info: str) -> MissionBase: # finish: fix mission usecase
        pass

    @abstractmethod
    def mission_base_delete(self, *, mission_name: str) -> bool: 
        pass

    # Mission Community chapter
    @abstractmethod
    def mission_comminuty_create(self, *, new_mission=CreateMissionCommunityDTO) -> MissionCommunity:
        pass

    @abstractmethod
    def mission_community_get(self, *, name: str) -> MissionCommunity:
        pass

    @abstractmethod
    def mission_community_delete(self, *, name: str) -> MissionCommunity:
        pass

    @abstractmethod
    def mission_community_list(self, *, 
                               sorting_obj: str = None, 
                               paggination_obj: str = None, 
                               filter_obj: str = None,
                            ) -> List[MissionCommunity]:
        pass

    @abstractmethod
    def mission_community_update(self, *
                                 new_mission_obj: UpdateMissionCommunityDTO
                        ) -> MissionCommunity: # finish: fix mission usecase
        pass

    # Mission User Chapter

    """ Realize after description Use Cases """

    # Community chapter
    @abstractmethod
    def community_create(self, *, new_community: CreateCommunityDTO) -> Community: 
        pass

    @abstractmethod
    def community_update(self, *, find_some_info: str) -> Community: # finish: fix mission usecase
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
    def user_create(self, *, new_user: CreateUserDTO) -> User:
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
                ) -> List[User]: 
        pass

